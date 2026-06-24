import os
from datetime import datetime


def get_metadata(filepath):

    stats = os.stat(filepath)

    metadata = {
        "filename": os.path.basename(filepath),
        "size": round(stats.st_size / 1024, 2),
        "created": datetime.fromtimestamp(
            stats.st_ctime
        ).strftime("%d-%m-%Y %H:%M:%S"),
        "modified": datetime.fromtimestamp(
            stats.st_mtime
        ).strftime("%d-%m-%Y %H:%M:%S"),
        "extension": os.path.splitext(filepath)[1]
    }

    return metadata