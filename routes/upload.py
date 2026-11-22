from flask import Blueprint
from flask import render_template
from flask import request
from flask import current_app
from datetime import datetime
import os

from modules.hashing import generate_hashes
from modules.metadata import get_metadata
from modules.exif_analyzer import extract_exif
from modules.report_generator import generate_report
from modules.risk_engine import calculate_risk

from modules.database import (
    save_evidence,
    find_duplicate,
    add_custody_log
)

upload_bp = Blueprint(
    "upload",
    __name__
)


@upload_bp.route("/upload", methods=["POST"])
def upload_file():

    file = request.files["evidence"]

    if file.filename == "":

        return "No File Selected"

    filepath = os.path.join(
        current_app.config["UPLOAD_FOLDER"],
        file.filename
    )

    file.save(filepath)

    hashes = generate_hashes(filepath)

    metadata = get_metadata(filepath)

    exif = extract_exif(filepath)

    duplicate = find_duplicate(
        hashes["sha256"]
    )

    duplicate_found = duplicate is not None

    risk = calculate_risk(
        metadata,
        exif,
        duplicate_found
    )

    if duplicate:

        return render_template(
            "duplicate.html",
            existing_case=duplicate[0],
            metadata=metadata,
            hashes=hashes,
            risk=risk
        )

    case_id = save_evidence(
        metadata["filename"],
        hashes["md5"],
        hashes["sha256"],
        metadata["size"],
        metadata["created"]
    )

    add_custody_log(case_id, "Evidence Uploaded")
    add_custody_log(case_id, "MD5 Hash Generated")
    add_custody_log(case_id, "SHA256 Hash Generated")
    add_custody_log(case_id, "Metadata Extracted")
    add_custody_log(case_id, "EXIF Analysis Completed")

    generate_report(
        case_id,
        metadata,
        hashes,
        exif
    )

    add_custody_log(case_id, "PDF Report Generated")

    return render_template(
    "report.html",
    metadata=metadata,
    hashes=hashes,
    exif=exif,
    case_id=case_id,
    risk=risk,
    generated_on=datetime.now().strftime("%d %B %Y %H:%M:%S")
)