import os
from flask import Flask, render_template, redirect, url_for, session
from config import Config
from models import db
from models.user import User

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize SQLAlchemy database
    db.init_app(app)

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db.session.remove()

    # Context processor to make current user details available globally in templates
    @app.context_processor
    def inject_user_context():
        from datetime import date
        user = None
        student = None
        warden = None
        unread_notifications_count = 0
        
        try:
            if 'user_id' in session:
                user = User.query.get(session['user_id'])
                if user:
                    from models.notification import Notification
                    unread_notifications_count = Notification.query.filter_by(user_id=user.id, is_read=False).count()
                    if user.role == 'student':
                        student = user.student_profile
                    elif user.role == 'warden':
                        warden = user.warden_profile
        except Exception as e:
            db.session.rollback()
                    
        return dict(
            current_user=user,
            current_student=student,
            current_warden=warden,
            unread_notifications_count=unread_notifications_count,
            date=date
        )

    # Register blueprints
    from routes.auth import auth_bp
    from routes.student import student_bp
    from routes.warden import warden_bp
    from routes.api import api_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(student_bp)
    app.register_blueprint(warden_bp)
    app.register_blueprint(api_bp)

    # Landing page route
    @app.route('/')
    def index():
        if 'user_id' in session:
            role = session.get('role')
            if role == 'student':
                return redirect(url_for('student.dashboard'))
            elif role == 'warden':
                return redirect(url_for('warden.dashboard'))
        try:
            from models.notification import Announcement
            announcements = Announcement.query.order_by(Announcement.created_at.desc()).limit(3).all()
        except Exception:
            db.session.rollback()
            announcements = []
        return render_template('index.html', announcements=announcements)

    # Register custom error page handlers
    @app.errorhandler(400)
    def bad_request(error):
        return render_template('errors/400.html'), 400

    @app.errorhandler(401)
    def unauthorized(error):
        return render_template('errors/401.html'), 401

    @app.errorhandler(403)
    def forbidden(error):
        return render_template('errors/403.html'), 403

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_server_error(error):
        import traceback
        err_detail = traceback.format_exc()
        app.logger.error("Internal Server Error: %s", err_detail)
        # Detailed error message for debugging serverless deployment
        if os.getenv("VERCEL") or os.getenv("VERCEL_ENV") or app.debug:
            return f"""<!DOCTYPE html>
<html>
<head><title>500 Application Error</title></head>
<body style="font-family: monospace; padding: 2rem; background: #1e1e2e; color: #f38ba8;">
    <h2 style="color: #f38ba8;">500 Internal Server Error</h2>
    <p style="color: #cdd6f4;"><strong>Exception:</strong> {error}</p>
    <pre style="background: #11111b; color: #a6e3a1; padding: 1.5rem; border-radius: 8px; overflow-x: auto; white-space: pre-wrap;">{err_detail}</pre>
    <a href="/" style="color: #89b4fa;">Reload Home</a>
</body>
</html>""", 500
        return render_template('errors/500.html'), 500

    # Custom template filters
    @app.template_filter('time_format')
    def time_format(value):
        if value is None:
            return ""
        return value.strftime("%I:%M %p")

    @app.template_filter('date_format')
    def date_format(value):
        if value is None:
            return ""
        return value.strftime("%b %d, %Y")

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
