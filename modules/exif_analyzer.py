from PIL import Image
from PIL.ExifTags import TAGS


def extract_exif(filepath):

    exif_data = {}

    try:

        image = Image.open(filepath)

        exif = image._getexif()

        if exif:

            for tag_id, value in exif.items():

                tag = TAGS.get(tag_id, tag_id)

                exif_data[tag] = value

    except Exception as e:

        exif_data["Error"] = str(e)

    return exif_data