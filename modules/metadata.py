import os
from datetime import datetime

from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS


def convert_gps_to_degrees(value):
    try:
        degrees = float(value[0])
        minutes = float(value[1])
        seconds = float(value[2])

        return degrees + (minutes / 60) + (seconds / 3600)

    except (TypeError, ValueError, IndexError):
        return None


def extract_exif_data(filepath):

    exif_metadata = {}

    try:
        image = Image.open(filepath)
        exif = image.getexif()

        if not exif:
            return {
                "exif_available": False,
                "make": "Not Available",
                "model": "Not Available",
                "camera_make": "Not Available",
                "camera_model": "Not Available",
                "date_taken": "Not Available",
                "gps_latitude": "Not Available",
                "gps_longitude": "Not Available",
                "image_dimensions": f"{image.width} x {image.height}",
                "exif_data": {}
            }

        for tag_id, value in exif.items():

            tag_name = TAGS.get(tag_id, str(tag_id))

            if isinstance(value, bytes):
                value = value.decode("utf-8", errors="ignore")

            exif_metadata[tag_name] = str(value)

        camera_make = exif_metadata.get("Make", "Not Available")
        camera_model = exif_metadata.get("Model", "Not Available")

        date_taken = (
            exif_metadata.get("DateTimeOriginal")
            or exif_metadata.get("DateTimeDigitized")
            or exif_metadata.get("DateTime")
            or "Not Available"
        )

        gps_latitude = "Not Available"
        gps_longitude = "Not Available"

        try:
            gps_info = exif.get_ifd(34853)

            decoded_gps = {}

            for key, value in gps_info.items():
                gps_tag = GPSTAGS.get(key, key)
                decoded_gps[gps_tag] = value

            latitude = decoded_gps.get("GPSLatitude")
            latitude_ref = decoded_gps.get("GPSLatitudeRef")

            longitude = decoded_gps.get("GPSLongitude")
            longitude_ref = decoded_gps.get("GPSLongitudeRef")

            if latitude and longitude:

                lat = convert_gps_to_degrees(latitude)
                lon = convert_gps_to_degrees(longitude)

                if lat is not None and lon is not None:

                    if latitude_ref == "S":
                        lat = -lat

                    if longitude_ref == "W":
                        lon = -lon

                    gps_latitude = round(lat, 6)
                    gps_longitude = round(lon, 6)

        except Exception:
            pass

        return {
            "exif_available": True,

            # Old keys required by risk_engine.py
            "make": camera_make,
            "model": camera_model,

            # New keys
            "camera_make": camera_make,
            "camera_model": camera_model,

            "date_taken": date_taken,

            "gps_latitude": gps_latitude,
            "gps_longitude": gps_longitude,

            "image_dimensions": f"{image.width} x {image.height}",

            "exif_data": exif_metadata
        }

    except Exception as error:

        return {
            "exif_available": False,
            "make": "Not Available",
            "model": "Not Available",
            "camera_make": "Not Available",
            "camera_model": "Not Available",
            "date_taken": "Not Available",
            "gps_latitude": "Not Available",
            "gps_longitude": "Not Available",
            "image_dimensions": "Not Available",
            "exif_data": {},
            "exif_error": str(error)
        }


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

    exif_metadata = extract_exif_data(filepath)

    metadata.update(exif_metadata)

    return metadata