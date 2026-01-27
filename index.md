---
layout: default
title: Alexandre Loeblein Heinen
description: Engineer, Math & Innovation Enthusiast, Conversationalist
---

<div class="container">
    <header>
        <h1>Alexandre Loeblein Heinen</h1>
        <p class="subtitle">Building robots | Solving problems | Writing stories</p>
    </header>

    <section class="profile-section">
        <h2 class="section-title">About me</h2>
        <img src="https://github.com/alexandrelheinen.png" alt="Alexandre Loeblein Heinen" class="profile-image">
        <p class="about-text">
            Welcome to my personal space! This is a landing page for researchers, recruiters, partners, and anyone 
            curious about the intersection of robotics, mathematics, and real-world engineering. More than 
            just a portfolio, this is my experiment in documenting professional experiences, sharing technical 
            insights, and exploring ideas outside the constraints of traditional formats.
        </p>
        <p class="about-text">
            For over eight years, I have navigated the world of autonomous systems as a founding engineer in 
            deep-tech startups and as a leader in technical teams, political structures, and unions. During 
            this time, I have had the opportunity to work across diverse application fields: medical robotics, 
            precision agriculture, leisure products, cinematography, industrial inspection, ISR, and most 
            recently, the defense industry.
        </p>
        <p class="about-text">
            Here, I write about what matters to me: robotics, embedded systems, GNC algorithms, drones, 
            software architecture, mathematics, innovation, and whatever else sparks curiosity along the way. 
            This space is free from the rigid structures of CVs and corporate profiles. It is a place for 
            exploration, technical depth, and honest reflection.
        </p>
        <p class="about-text">
            Looking for something more formal? The links below provide access to my structured CVs (English and French), 
            LinkedIn profile, and GitHub repositories. Enjoy the journey!
        </p>
        
        {% include navigation.html %}
    </section>

    <section class="articles-section">
        <h2 class="section-title">Articles: My "Technical Drafts"</h2>
        <ul class="article-list">
            {% assign articles = site.pages | where_exp: "page", "page.path contains 'articles/'" | where_exp: "page", "page.title" | sort: "date" | reverse %}
            {% for article in articles %}
            <li class="article-item">
                <a href="{{ article.url | relative_url }}">{{ article.title }}</a>
            </li>
            {% endfor %}
        </ul>
    </section>

    <footer>
        <p>&copy; 2026 Alexandre Loeblein Heinen. All rights reserved.</p>
    </footer>
</div>
