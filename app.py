from flask import Flask, render_template, send_file
import os

from routes import home_bp, upload_bp

from modules.database import (
    init_db,
    get_total_cases,
    get_recent_cases,
    get_recent_activity
)

app = Flask(__name__)

# Register Blueprints
app.register_blueprint(home_bp)
app.register_blueprint(upload_bp)

# Initialize Database
init_db()

# Upload Folder
UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route("/dashboard")
def dashboard():

    total_cases = get_total_cases()

    recent_cases = get_recent_cases()

    recent_activity = get_recent_activity()

    return render_template(

        "dashboard.html",

        total_cases=total_cases,

        recent_cases=recent_cases,

        recent_activity=recent_activity

    )


@app.route("/download/<int:case_id>")
def download_report(case_id):

    pdf_file = f"FX-{case_id}_Report.pdf"

    return send_file(

        pdf_file,

        as_attachment=True

    )


if __name__ == "__main__":

    app.run(

        host="0.0.0.0",

        port=5000,

        debug=True

    )