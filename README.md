# Orbit – Django Backend

The original Orbit template served through Django with working form backends.

## What was changed in the frontend

Exactly three things per HTML file — nothing else:

1. `{% load static %}` added at the top of each template
2. `assets/...` paths replaced with `{% static 'assets/...' %}` so Django serves them
3. `href="*.html"` links replaced with `{% url '...' %}` Django URL tags
4. Contact form: `action="forms/contact.php"` → `action="{% url 'contact' %}"` + `{% csrf_token %}`
5. Newsletter form: `action="forms/newsletter.php"` → `action="{% url 'newsletter' %}"` + `{% csrf_token %}`

Every pixel of the design is untouched.

## Quick start

```bash
pip install django
python manage.py migrate
python manage.py runserver
```

Open http://127.0.0.1:8000

Admin panel: http://127.0.0.1:8000/admin/
- Username: admin  |  Password: admin123  (change before deploying!)

## Email configuration

By default emails print to the terminal (console backend). To send real emails,
edit `orbit_site/settings.py` and swap the EMAIL_BACKEND block:

```python
EMAIL_BACKEND     = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST        = 'smtp.gmail.com'
EMAIL_PORT        = 587
EMAIL_USE_TLS     = True
EMAIL_HOST_USER   = 'you@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'
```

## Project structure

```
orbit_site/
├── manage.py
├── db.sqlite3
├── orbit_site/          ← Django config
│   ├── settings.py
│   └── urls.py
└── core/                ← app
    ├── models.py        ← ContactMessage, NewsletterSubscriber
    ├── views.py         ← page + form views, email helpers
    ├── admin.py         ← admin for both models
    ├── urls.py
    ├── static/assets/   ← all original CSS/JS/images (untouched)
    └── templates/
        ├── index.html              ← original template, minimal edits
        ├── portfolio-details.html
        ├── service-details.html
        ├── privacy.html
        ├── terms.html
        ├── 404.html
        └── emails/
            ├── contact_thankyou.html / .txt
            └── newsletter_welcome.html / .txt
```
