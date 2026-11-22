import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")

DATABASE = os.path.join(BASE_DIR, "forensix.db")

REPORT_FOLDER = os.path.join(BASE_DIR, "reports")