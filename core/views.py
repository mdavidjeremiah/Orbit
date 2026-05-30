from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from .models import ContactMessage, NewsletterSubscriber
import logging

logger = logging.getLogger(__name__)


# ── Static page views ───────────────────────────────────────────────────────

def index(request):
    return render(request, 'index.html')

def portfolio_details(request):
    return render(request, 'portfolio-details.html')

def service_details(request):
    return render(request, 'service-details.html')

def privacy(request):
    return render(request, 'privacy.html')

def terms(request):
    return render(request, 'terms.html')

def page_404(request):
    return render(request, '404.html', status=404)

def handler404(request, exception):
    return render(request, '404.html', status=404)


# ── Form endpoints ───────────────────────────────────────────────────────────

@require_POST
def contact(request):
    name    = request.POST.get('name', '').strip()
    email   = request.POST.get('email', '').strip()
    subject = request.POST.get('subject', '').strip()
    message = request.POST.get('message', '').strip()

    errors = {}
    if not name:    errors['name']    = 'Name is required.'
    if not email:   errors['email']   = 'Email is required.'
    if not subject: errors['subject'] = 'Subject is required.'
    if not message: errors['message'] = 'Message is required.'

    if errors:
        return JsonResponse({'success': False, 'errors': errors}, status=400)

    msg = ContactMessage.objects.create(
        name=name, email=email, subject=subject, message=message
    )

    _send_contact_thankyou(msg)

    # The original template's JS looks for a redirect or JSON success response.
    # We redirect back to the index page — the php-email-form JS handles the
    # success/error divs via XHR, so returning 200 with plain text is enough.
    return JsonResponse({'success': True, 'message': 'Your message has been sent. Thank you!'})


@require_POST
def newsletter(request):
    email = request.POST.get('email', '').strip()

    if not email:
        return JsonResponse({'success': False, 'errors': {'email': 'Email is required.'}}, status=400)

    subscriber, created = NewsletterSubscriber.objects.get_or_create(email=email)

    if created:
        _send_newsletter_welcome(email)
        return JsonResponse({'success': True, 'message': 'Your subscription request has been sent. Thank you!'})
    else:
        return JsonResponse({'success': True, 'message': 'You are already subscribed!'})


# ── Email helpers ────────────────────────────────────────────────────────────

def _send(subject, to, html, txt):
    try:
        msg = EmailMultiAlternatives(
            subject=subject,
            body=txt,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[to],
        )
        msg.attach_alternative(html, 'text/html')
        msg.send()
        logger.info('Email "%s" sent to %s', subject, to)
    except Exception as exc:
        logger.error('Failed to send email to %s: %s', to, exc)


def _send_contact_thankyou(msg):
    ctx = {
        'name':    msg.name,
        'subject': msg.subject,
        'sent_at': msg.submitted_at.strftime('%d %B %Y at %H:%M'),
    }
    html = render_to_string('emails/contact_thankyou.html', ctx)
    txt  = render_to_string('emails/contact_thankyou.txt', ctx)
    _send(f"Thanks for reaching out, {msg.name}! – Orbit", msg.email, html, txt)


def _send_newsletter_welcome(email):
    ctx  = {'email': email}
    html = render_to_string('emails/newsletter_welcome.html', ctx)
    txt  = render_to_string('emails/newsletter_welcome.txt', ctx)
    _send("Welcome to the Orbit Newsletter 🚀", email, html, txt)
