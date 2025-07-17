from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import Comment

@receiver(post_save, sender=Comment)
def send_comment_notification(sender, instance, created, **kwargs):
    if created:
        print(f"DEBUG: Comment signal triggered for comment ID {instance.pk}")
        subject = f'New Comment on "{instance.post.title}"'
        message = f"""
A new comment has been posted on the blog post "{instance.post.title}".

Comment by: {instance.author.username}
Posted on: {instance.date_posted.strftime('%B %d, %Y at %I:%M %p')}

Comment:
{instance.content}

View the post: http://localhost:8000/post/{instance.post.pk}
        """
        
        recipient_list = ['Rao@rsaamerica.com', 'angel@rsaamerica.com']
        
        try:
            print(f"DEBUG: Attempting to send email to {recipient_list}")
            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                recipient_list,
                fail_silently=False,
            )
            print("DEBUG: Email sent successfully!")
        except Exception as e:
            print(f"Failed to send email notification: {e}")
