from flask import render_template

def register_error_handlers(app):
    @app.errorhandler(400)
    def bad_request_error(error):
        return render_template('error_400.html'), 400

    @app.errorhandler(401)
    def unauthorized_error(error):
        return render_template('error_401.html'), 401

    @app.errorhandler(403)
    def forbidden_error(error):
        return render_template('error_403.html'), 403

    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('error_404.html'), 404

    @app.errorhandler(405)
    def method_not_allowed_error(error):
        return render_template('error_405.html'), 405

    @app.errorhandler(500)
    def internal_error(error):
        return render_template('error_500.html'), 500

    @app.errorhandler(502)
    def bad_gateway_error(error):
        return render_template('error_502.html'), 502

    @app.errorhandler(503)
    def service_unavailable_error(error):
        return render_template('error_503.html'), 503