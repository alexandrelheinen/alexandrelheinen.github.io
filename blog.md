---
layout: default
title: Blog
permalink: /blog/
---

<div class="blog-page">
  <h1>Technical Articles</h1>
  <p>
    Welcome to my technical blog where I explore topics in robotics, mathematics, embedded systems, 
    and innovation. This space serves as a platform to share knowledge, document projects, and 
    discuss emerging technologies.
  </p>

  {% if site.posts.size > 0 %}
  <ul class="post-list">
    {% for post in site.posts %}
    <li>
      <span class="post-meta"><time datetime="{{ post.date | date_to_xmlschema }}">{{ post.date | date: "%B %d, %Y" }}</time></span>
      <h3>
        <a class="post-link" href="{{ post.url | relative_url }}">{{ post.title }}</a>
      </h3>
      <p>{{ post.excerpt | strip_html | truncate: 200 }}</p>
    </li>
    {% endfor %}
  </ul>
  {% else %}
  <p class="placeholder-text">
    Articles coming soon! I'm working on content covering robotics algorithms, control systems, 
    mathematical foundations, and embedded system design patterns.
  </p>
  {% endif %}
</div>
