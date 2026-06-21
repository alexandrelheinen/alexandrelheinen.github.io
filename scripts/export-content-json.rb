#!/usr/bin/env ruby
# frozen_string_literal: true

require "fileutils"
require "json"
require "pathname"
require "date"
require "time"
require "shellwords"
require "yaml"

CONTENT_ROOT = Pathname.new(ARGV[0] || "content").expand_path
OUTPUT_ROOT = Pathname.new(ARGV[1] || "_content_json").expand_path

def split_front_matter(text)
  text = text.sub(/\A\xEF\xBB\xBF/, "")
  return [{}, text] unless text.start_with?("---\n")

  parts = text.split(/^---\s*$\n?/, 3)
  return [{}, text] unless parts.length == 3

  data = YAML.safe_load(parts[1], permitted_classes: [Date, Time], aliases: true) || {}
  [data, parts[2]]
end

def git_repo?
  system("git rev-parse --is-inside-work-tree > /dev/null 2>&1")
end

def git_date(repo_relative_path, mode)
  return nil unless git_repo?

  case mode
  when :creation
    cmd = "git log --follow --diff-filter=A --format='%ad' --date=short -- #{repo_relative_path.shellescape}"
    raw = `#{cmd}`.strip.split("\n").last
  when :updated
    cmd = "git log --follow -1 --format='%ad' --date=short -- #{repo_relative_path.shellescape}"
    raw = `#{cmd}`.strip
  else
    return nil
  end

  raw unless raw.nil? || raw.empty?
end

def apply_git_chronology!(front_matter, repo_relative_path, type)
  return unless %w[article post].include?(type)

  creation = git_date(repo_relative_path, :creation)
  updated = git_date(repo_relative_path, :updated)

  # Editorial front matter wins. Git is only used to backfill missing values.
  # Bulk content moves can make git log -1 look recent for every file; keeping
  # explicit dates avoids showing "updated today" on unchanged pieces.
  front_matter["date"] ||= creation
  if front_matter["last_updated"].nil? || front_matter["last_updated"].to_s.strip.empty?
    front_matter["last_updated"] = front_matter["date"] || updated
  end
end

def json_ready(value)
  case value
  when Hash
    value.transform_values { |v| json_ready(v) }
  when Array
    value.map { |v| json_ready(v) }
  when Date, Time
    value.iso8601
  else
    value
  end
end

def write_json(path, payload)
  FileUtils.mkdir_p(path.dirname)
  path.write(JSON.pretty_generate(json_ready(payload)) + "\n")
end

def export_markdown_tree(source_dir, output_dir, type)
  return [] unless source_dir.directory?

  files = []
  source_dir.glob("**/*.{md,markdown}").sort.each do |source|
    front_matter, body = split_front_matter(source.read)
    slug = source.basename(source.extname).to_s
    relative_source = source.relative_path_from(CONTENT_ROOT).to_s
    repo_relative_path = Pathname.new("content").join(relative_source).to_s
    apply_git_chronology!(front_matter, repo_relative_path, type)
    output_path = output_dir.join("#{slug}.json")

    write_json(
      output_path,
      {
        "type" => type,
        "slug" => slug,
        "source_path" => relative_source,
        "front_matter" => front_matter,
        "body_markdown" => body.strip
      }
    )
    files << output_path.relative_path_from(OUTPUT_ROOT).to_s
  end
  files
end

def export_data_tree(source_dir, output_dir)
  return [] unless source_dir.directory?

  files = []
  source_dir.glob("**/*.{yml,yaml}").sort.each do |source|
    relative = source.relative_path_from(source_dir).to_s.sub(/\.(ya?ml)\z/, ".json")
    data = YAML.safe_load(source.read, permitted_classes: [Date, Time], aliases: true) || {}
    output_path = output_dir.join(relative)
    write_json(output_path, data)
    files << output_path.relative_path_from(OUTPUT_ROOT).to_s
  end
  files
end

FileUtils.rm_rf(OUTPUT_ROOT)

files = {
  "articles" => export_markdown_tree(CONTENT_ROOT.join("articles"), OUTPUT_ROOT.join("articles"), "article"),
  "posts" => export_markdown_tree(CONTENT_ROOT.join("collections", "posts"), OUTPUT_ROOT.join("collections", "posts"), "post"),
  "products" => export_markdown_tree(CONTENT_ROOT.join("collections", "products"), OUTPUT_ROOT.join("collections", "products"), "product"),
  "projects" => export_markdown_tree(CONTENT_ROOT.join("collections", "projects"), OUTPUT_ROOT.join("collections", "projects"), "project"),
  "jobs" => export_markdown_tree(CONTENT_ROOT.join("collections", "jobs"), OUTPUT_ROOT.join("collections", "jobs"), "job"),
  "resources" => export_markdown_tree(CONTENT_ROOT.join("collections", "resources"), OUTPUT_ROOT.join("collections", "resources"), "resource"),
  "page_fragments" => export_markdown_tree(CONTENT_ROOT.join("pages"), OUTPUT_ROOT.join("pages"), "page_fragment"),
  "data" => export_data_tree(CONTENT_ROOT.join("collections", "data"), OUTPUT_ROOT.join("data"))
}
counts = files.transform_values(&:length)

write_json(OUTPUT_ROOT.join("manifest.json"), {
  "generated_at" => Time.now.utc.iso8601,
  "content_root" => CONTENT_ROOT.to_s,
  "counts" => counts,
  "files" => files
})

puts "Exported content JSON to #{OUTPUT_ROOT}"
counts.each { |name, count| puts "  #{name}: #{count}" }
