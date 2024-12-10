from flask import request, current_app, render_template


def not_found(error):
    current_app.logger.error(error)
    if request.host == current_app.config['APPLY_HOST']:
        return render_template("apply/404.html", is_error=True), 404
    elif request.host == current_app.config['ASSESS_HOST']:
        return render_template("assess/404.html"), 404
    

def internal_server_error(error):
    current_app.logger.error(error)
    if request.host == current_app.config['APPLY_HOST']:
        return render_template("apply/500.html", is_error=True), 500
    elif request.host == current_app.config['ASSESS_HOST']:
        return render_template("assess/500.html", is_error=True), 500
