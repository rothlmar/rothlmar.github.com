---
layout: page
title: Index Page
---

<ul>
  {% for post in site.posts %}
    <li>
      <a href="{{ post.url }}">{{ post.title }}</a><br />
      {{ post.author }}
    </li>
  {% endfor %}
</ul>