from flask import Flask, render_template, request, send_file

from modules.hashing import generate_hashes
from modules.metadata import get_metadata
from modules.exif_analyzer import extract_exif
from modules.report_generator import generate_report

from modules.database import (
    init_db,
    save_evidence,
    find_duplicate,
    get_total_cases,
    get_recent_cases,
    add_custody_log,
    get_recent_activity
)

import os

app = Flask(__name__)

init_db()

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/dashboard')
def dashboard():

    total_cases = get_total_cases()

    recent_cases = get_recent_cases()

    recent_activity = get_recent_activity()

    return render_template(
        'dashboard.html',
        total_cases=total_cases,
        recent_cases=recent_cases,
        recent_activity=recent_activity
    )


@app.route('/upload', methods=['POST'])
def upload_file():

    file = request.files['evidence']

    if file.filename != '':

        filepath = os.path.join(
            app.config['UPLOAD_FOLDER'],
            file.filename
        )

        file.save(filepath)

        hashes = generate_hashes(filepath)

        metadata = get_metadata(filepath)

        exif = extract_exif(filepath)

        duplicate = find_duplicate(
            hashes['sha256']
        )

        if duplicate:

            return render_template(
                'duplicate.html',
                existing_case=duplicate[0],
                metadata=metadata,
                hashes=hashes
            )

        case_id = save_evidence(
            metadata['filename'],
            hashes['md5'],
            hashes['sha256'],
            metadata['size'],
            metadata['created']
        )

        # Chain of Custody Logs

        add_custody_log(
            case_id,
            "Evidence Uploaded"
        )

        add_custody_log(
            case_id,
            "MD5 Hash Generated"
        )

        add_custody_log(
            case_id,
            "SHA256 Hash Generated"
        )

        add_custody_log(
            case_id,
            "Metadata Extracted"
        )

        add_custody_log(
            case_id,
            "EXIF Analysis Completed"
        )

        generate_report(
            case_id,
            metadata,
            hashes,
            exif
        )

        add_custody_log(
            case_id,
            "PDF Report Generated"
        )

        return render_template(
            'report.html',
            metadata=metadata,
            hashes=hashes,
            exif=exif,
            case_id=case_id
        )

    return "No File Selected"


@app.route('/download/<int:case_id>')
def download_report(case_id):

    pdf_file = f"FX-{case_id}_Report.pdf"

    return send_file(
        pdf_file,
        as_attachment=True
    )


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)