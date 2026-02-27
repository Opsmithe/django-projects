"""
Email Utility Module for Tennis Club Application

This module handles all email-related functionality including:
- Welcome emails for new members
- Email notifications
- Email templates
- Email sending with error handling

Author: Tennis Club Development Team
Date: 2026
"""

from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
import logging

# Set up logging for email operations
logger = logging.getLogger(__name__)


def send_welcome_email(member):
    """
    Send a welcome email to a newly registered member.
    
    This function sends a personalized welcome email to new members
    with their registration details and next steps.
    
    Args:
        member (Names): The member object containing user information
        
    Returns:
        bool: True if email was sent successfully, False otherwise
        
    Example:
        >>> from club.models import Names
        >>> member = Names.objects.get(id=1)
        >>> send_welcome_email(member)
        True
    """
    print(f"\n{'='*60}")
    print(f"SENDING WELCOME EMAIL")
    print(f"{'='*60}")
    print(f"Recipient: {member.firstname} {member.lastname}")
    print(f"Email: {member.email}")
    
    try:
        # Email subject
        subject = f'Welcome to Tennis Club, {member.firstname}!'
        print(f"Subject: {subject}")
        
        # Recipient email
        recipient_email = member.email
        
        # Context data for email template
        context = {
            'member': member,
            'club_name': 'Tennis Club',
            'support_email': settings.DEFAULT_FROM_EMAIL,
        }
        
        print("Rendering email template...")
        # Render HTML email template
        html_message = render_to_string('emails/welcome_email.html', context)
        
        # Create plain text version (fallback for email clients that don't support HTML)
        plain_message = strip_tags(html_message)
        
        print("Creating email message...")
        # Create email message with both HTML and plain text versions
        email = EmailMultiAlternatives(
            subject=subject,
            body=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[recipient_email]
        )
        
        # Attach HTML version
        email.attach_alternative(html_message, "text/html")
        
        print("Sending email...")
        # Send email
        email.send(fail_silently=False)
        
        print("✅ Email sent successfully!")
        print(f"{'='*60}\n")
        
        # Log success
        logger.info(f'Welcome email sent successfully to {recipient_email}')
        return True
        
    except Exception as e:
        # Log error
        print(f"❌ ERROR: {str(e)}")
        print(f"{'='*60}\n")
        logger.error(f'Failed to send welcome email to {recipient_email}: {str(e)}')
        import traceback
        traceback.print_exc()
        return False


def send_simple_welcome_email(member):
    """
    Send a simple text-based welcome email (alternative method).
    
    This is a simpler version that sends plain text emails without HTML.
    Useful for basic email functionality or as a fallback.
    
    Args:
        member (Names): The member object containing user information
        
    Returns:
        bool: True if email was sent successfully, False otherwise
    """
    try:
        subject = f'Welcome to Tennis Club, {member.firstname}!'
        
        message = f"""
        Dear {member.firstname} {member.lastname},
        
        Welcome to Tennis Club! We're excited to have you as a member.
        
        Your Registration Details:
        - Name: {member.firstname} {member.lastname}
        - Email: {member.email}
        - Phone: {member.phoneNumber}
        - City: {member.city}
        - Location: {member.location}
        - Member Since: {member.date_joined}
        
        What's Next?
        1. Explore our facilities and courts
        2. Check out upcoming tournaments
        3. Connect with other members
        4. Book your first court session
        
        If you have any questions, feel free to reach out to us.
        
        Best regards,
        Tennis Club Team
        """
        
        # Send simple text email
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[member.email],
            fail_silently=False,
        )
        
        logger.info(f'Simple welcome email sent to {member.email}')
        return True
        
    except Exception as e:
        logger.error(f'Failed to send simple welcome email: {str(e)}')
        return False


def send_member_update_notification(member, updated_by=None):
    """
    Send notification email when member information is updated.
    
    Args:
        member (Names): The member whose information was updated
        updated_by (str, optional): Name of person who made the update
        
    Returns:
        bool: True if email sent successfully, False otherwise
    """
    try:
        subject = 'Your Tennis Club Profile Has Been Updated'
        
        message = f"""
        Dear {member.firstname},
        
        Your Tennis Club profile has been updated.
        
        Current Information:
        - Name: {member.firstname} {member.lastname}
        - Email: {member.email}
        - Phone: {member.phoneNumber}
        - City: {member.city}
        - Location: {member.location}
        
        If you did not make these changes or have any concerns, 
        please contact us immediately.
        
        Best regards,
        Tennis Club Team
        """
        
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[member.email],
            fail_silently=False,
        )
        
        logger.info(f'Update notification sent to {member.email}')
        return True
        
    except Exception as e:
        logger.error(f'Failed to send update notification: {str(e)}')
        return False


def send_deletion_confirmation(member_email, member_name):
    """
    Send confirmation email when a member account is deleted.
    
    Args:
        member_email (str): Email address of deleted member
        member_name (str): Full name of deleted member
        
    Returns:
        bool: True if email sent successfully, False otherwise
    """
    try:
        subject = 'Tennis Club Account Deletion Confirmation'
        
        message = f"""
        Dear {member_name},
        
        This email confirms that your Tennis Club membership has been cancelled.
        
        We're sorry to see you go! If you change your mind, you're always 
        welcome to rejoin our community.
        
        Thank you for being part of Tennis Club.
        
        Best regards,
        Tennis Club Team
        """
        
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[member_email],
            fail_silently=False,
        )
        
        logger.info(f'Deletion confirmation sent to {member_email}')
        return True
        
    except Exception as e:
        logger.error(f'Failed to send deletion confirmation: {str(e)}')
        return False


def send_bulk_email(subject, message, recipient_list):
    """
    Send bulk emails to multiple recipients.
    
    Useful for announcements, newsletters, or notifications to all members.
    
    Args:
        subject (str): Email subject
        message (str): Email message body
        recipient_list (list): List of email addresses
        
    Returns:
        int: Number of emails sent successfully
    """
    try:
        sent_count = send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=recipient_list,
            fail_silently=False,
        )
        
        logger.info(f'Bulk email sent to {sent_count} recipients')
        return sent_count
        
    except Exception as e:
        logger.error(f'Failed to send bulk email: {str(e)}')
        return 0


# Email template helper functions

def get_email_context(member, **kwargs):
    """
    Generate common context data for email templates.
    
    Args:
        member (Names): Member object
        **kwargs: Additional context variables
        
    Returns:
        dict: Context dictionary for email templates
    """
    context = {
        'member': member,
        'club_name': 'Tennis Club',
        'support_email': settings.DEFAULT_FROM_EMAIL,
        'website_url': 'http://localhost:8000',  # Update for production
    }
    context.update(kwargs)
    return context


# ===================================
# USER AUTHENTICATION EMAILS
# ===================================

def send_welcome_email_to_user(user):
    """
    Send a welcome email to a newly registered user (authentication system).
    
    This is different from send_welcome_email() which is for member registration.
    This function is for users who create accounts through the authentication system.
    
    Args:
        user: Django User object
        
    Returns:
        bool: True if email sent successfully, False otherwise
    """
    print(f"\n{'='*60}")
    print(f"SENDING USER REGISTRATION WELCOME EMAIL")
    print(f"{'='*60}")
    print(f"Username: {user.username}")
    print(f"Email: {user.email}")
    
    try:
        subject = f'Welcome to Tennis Club, {user.username}!'
        print(f"Subject: {subject}")
        
        # Create HTML email content
        html_message = f"""
        <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                    <h2 style="color: #2c5282;">Welcome to Tennis Club, {user.username}!</h2>
                    
                    <p>Thank you for creating an account with us.</p>
                    
                    <div style="background-color: #f7fafc; padding: 15px; border-radius: 5px; margin: 20px 0;">
                        <h3 style="margin-top: 0;">Your Account Details:</h3>
                        <p><strong>Username:</strong> {user.username}</p>
                        <p><strong>Email:</strong> {user.email}</p>
                        {f'<p><strong>Name:</strong> {user.get_full_name()}</p>' if user.get_full_name() else ''}
                    </div>
                    
                    <p>You can now:</p>
                    <ul>
                        <li>View member information</li>
                        <li>Access your profile</li>
                        <li>Receive updates and notifications</li>
                    </ul>
                    
                    <p>If you have any questions, feel free to contact us.</p>
                    
                    <p style="margin-top: 30px;">
                        Best regards,<br>
                        <strong>Tennis Club Team</strong>
                    </p>
                </div>
            </body>
        </html>
        """
        
        # Plain text version
        plain_message = strip_tags(html_message)
        
        print("Sending email...")
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            html_message=html_message,
            fail_silently=False,
        )
        
        print("✅ Email sent successfully!")
        print(f"{'='*60}\n")
        logger.info(f'Welcome email sent to user {user.username} at {user.email}')
        return True
        
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        print(f"{'='*60}\n")
        logger.error(f'Failed to send welcome email to user {user.username}: {str(e)}')
        return False
