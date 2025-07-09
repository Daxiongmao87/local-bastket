from flask import current_app, render_template, url_for
from flask_mail import Mail, Message
from threading import Thread
from itsdangerous import URLSafeTimedSerializer
import os


class EmailService:
    """Service class for handling email operations."""
    
    def __init__(self, app=None):
        self.mail = Mail()
        if app:
            self.init_app(app)
    
    def init_app(self, app):
        """Initialize email service with Flask app."""
        self.mail.init_app(app)
    
    def send_async_email(self, app, msg):
        """Send email asynchronously."""
        with app.app_context():
            self.mail.send(msg)
    
    def send_email(self, to, subject, template, **kwargs):
        """Send email with given template and data."""
        app = current_app._get_current_object()
        msg = Message(
            subject=f"[Local Basket] {subject}",
            recipients=[to],
            html=render_template(f"emails/{template}.html", **kwargs),
            sender=app.config['MAIL_DEFAULT_SENDER']
        )
        
        if app.config.get('MAIL_SUPPRESS_SEND'):
            app.logger.info(f"Email suppressed: {subject} to {to}")
            return True
        
        thread = Thread(target=self.send_async_email, args=[app, msg])
        thread.start()
        return thread
    
    def generate_confirmation_token(self, email):
        """Generate email confirmation token."""
        serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        return serializer.dumps(email, salt='email-confirmation')
    
    def confirm_token(self, token, expiration=3600):
        """Confirm email token and return email if valid."""
        serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        try:
            email = serializer.loads(
                token,
                salt='email-confirmation',
                max_age=expiration
            )
        except Exception:
            return False
        return email
    
    def send_confirmation_email(self, user):
        """Send email confirmation to user."""
        token = self.generate_confirmation_token(user.email)
        confirm_url = url_for('confirm_email', token=token, _external=True)
        
        return self.send_email(
            user.email,
            'Please confirm your email',
            'confirmation',
            user=user,
            confirm_url=confirm_url
        )
    
    def send_password_reset_email(self, user):
        """Send password reset email to user."""
        token = self.generate_confirmation_token(user.email)
        reset_url = url_for('reset_password', token=token, _external=True)
        
        return self.send_email(
            user.email,
            'Reset your password',
            'reset_password',
            user=user,
            reset_url=reset_url
        )


# Global email service instance
email_service = EmailService()