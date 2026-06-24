import hashlib


def generate_hashes(filepath):

    md5_hash = hashlib.md5()
    sha256_hash = hashlib.sha256()

    with open(filepath, "rb") as f:

        while chunk := f.read(4096):
            md5_hash.update(chunk)
            sha256_hash.update(chunk)

    return {
        "md5": md5_hash.hexdigest(),
        "sha256": sha256_hash.hexdigest()
    }