---
layout: default
title: Alexandre Loeblein Heinen
---

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="Alexandre Loeblein Heinen - Personal Website">
    <title>Alexandre Loeblein Heinen</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        :root {
            --primary-color: #0f172a;
            --secondary-color: #334155;
            --accent-color: #3b82f6;
            --text-color: #1e293b;
            --light-gray: #f1f5f9;
            --border-color: #e2e8f0;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', sans-serif;
            line-height: 1.6;
            color: var(--text-color);
            background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
            min-height: 100vh;
        }

        .container {
            max-width: 900px;
            margin: 0 auto;
            padding: 2rem;
        }

        header {
            text-align: center;
            padding: 4rem 0 3rem;
            animation: fadeInDown 0.8s ease;
        }

        h1 {
            font-size: 3rem;
            font-weight: 700;
            color: var(--primary-color);
            margin-bottom: 0.5rem;
            letter-spacing: -0.02em;
        }

        .subtitle {
            font-size: 1.25rem;
            color: var(--secondary-color);
            font-weight: 300;
        }

        .profile-section {
            background: white;
            border-radius: 16px;
            padding: 3rem;
            margin: 2rem 0;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05), 0 10px 15px rgba(0, 0, 0, 0.03);
            animation: fadeInUp 0.8s ease;
        }

        .section-title {
            font-size: 1.5rem;
            font-weight: 600;
            color: var(--primary-color);
            margin-bottom: 1.5rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }

        .section-title::before {
            content: '';
            width: 4px;
            height: 24px;
            background: var(--accent-color);
            border-radius: 2px;
        }

        .about-text {
            color: var(--secondary-color);
            font-size: 1.1rem;
            line-height: 1.8;
            margin-bottom: 2rem;
        }

        .social-links {
            display: flex;
            gap: 1rem;
            justify-content: center;
            flex-wrap: wrap;
        }

        .social-link {
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            padding: 0.75rem 1.5rem;
            background: var(--light-gray);
            color: var(--text-color);
            text-decoration: none;
            border-radius: 8px;
            font-weight: 500;
            transition: all 0.3s ease;
            border: 2px solid transparent;
        }

        .social-link:hover {
            background: var(--accent-color);
            color: white;
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
        }

        .social-link svg {
            width: 20px;
            height: 20px;
            fill: currentColor;
        }

        .articles-section {
            background: white;
            border-radius: 16px;
            padding: 3rem;
            margin: 2rem 0;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05), 0 10px 15px rgba(0, 0, 0, 0.03);
            animation: fadeInUp 0.8s ease 0.2s both;
        }

        .article-list {
            list-style: none;
        }

        .article-item {
            padding: 1.25rem;
            margin-bottom: 1rem;
            background: var(--light-gray);
            border-radius: 8px;
            border-left: 4px solid var(--accent-color);
            transition: all 0.3s ease;
        }

        .article-item:hover {
            transform: translateX(8px);
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
        }

        .article-item a {
            color: var(--primary-color);
            text-decoration: none;
            font-weight: 500;
            font-size: 1.1rem;
        }

        .article-item a:hover {
            color: var(--accent-color);
        }

        footer {
            text-align: center;
            padding: 3rem 0;
            color: var(--secondary-color);
            font-size: 0.9rem;
        }

        @keyframes fadeInDown {
            from {
                opacity: 0;
                transform: translateY(-20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        @media (max-width: 768px) {
            h1 {
                font-size: 2rem;
            }

            .profile-section,
            .articles-section {
                padding: 2rem;
            }

            .social-links {
                flex-direction: column;
            }

            .social-link {
                width: 100%;
                justify-content: center;
            }
        }

        /* Smooth scroll */
        html {
            scroll-behavior: smooth;
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>Alexandre Loeblein Heinen</h1>
            <p class="subtitle">Software Engineer & Technical Writer</p>
        </header>

        <section class="profile-section">
            <h2 class="section-title">About Me</h2>
            <p class="about-text">
                Welcome to my personal space on the web. I'm passionate about software engineering, 
                algorithms, and sharing technical knowledge through writing. 
                This is where I document my explorations and insights.
            </p>
            
            <div class="social-links">
                <a href="https://linkedin.com/in/alexandrelheinen" class="social-link" target="_blank" rel="noopener">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
                        <path d="M19 0h-14c-2.761 0-5 2.239-5 5v14c0 2.761 2.239 5 5 5h14c2.762 0 5-2.239 5-5v-14c0-2.761-2.238-5-5-5zm-11 19h-3v-11h3v11zm-1.5-12.268c-.966 0-1.75-.79-1.75-1.764s.784-1.764 1.75-1.764 1.75.79 1.75 1.764-.783 1.764-1.75 1.764zm13.5 12.268h-3v-5.604c0-3.368-4-3.113-4 0v5.604h-3v-11h3v1.765c1.396-2.586 7-2.777 7 2.476v6.759z"/>
                    </svg>
                    LinkedIn
                </a>
                <a href="https://github.com/alexandrelheinen" class="social-link" target="_blank" rel="noopener">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
                        <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/>
                    </svg>
                    GitHub
                </a>
            </div>
        </section>

        <section class="articles-section">
            <h2 class="section-title">Technical Articles</h2>
            <ul class="article-list">
                <li class="article-item">
                    <a href="./dubins-paths.md">3D Dubins Paths: Beyond the Plane</a>
                </li>
            </ul>
        </section>

        <footer>
            <p>&copy; 2026 Alexandre Loeblein Heinen. All rights reserved.</p>
        </footer>
    </div>
</body>
</html>