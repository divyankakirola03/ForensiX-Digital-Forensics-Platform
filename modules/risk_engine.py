def calculate_risk(metadata, exif, duplicate=False):

    score = 0

    reasons = []

    recommendations = []

    extension = metadata["extension"].lower()

    size = metadata["size"]


    if extension == ".pdf":

        score += 5

        reasons.append("PDF document")

        recommendations.append(
            "Inspect embedded metadata and document properties."
        )


    if extension in [".doc", ".docx", ".ppt", ".pptx", ".xls", ".xlsx"]:

        score += 5

        reasons.append("Office document")

        recommendations.append(
            "Inspect for embedded macros and hidden metadata."
        )


    if extension in [".png", ".jpg", ".jpeg", ".bmp", ".gif", ".tiff", ".webp"]:

        score += 5

        reasons.append("Image file")

        recommendations.append(
            "Preserve original image before examination."
        )

        if exif.get("make", "Not Available") == "Not Available":

            score += 10

            reasons.append("Missing EXIF metadata")

            recommendations.append(
                "Verify whether EXIF removal was intentional."
            )


    if extension in [".zip", ".rar", ".7z"]:

        score += 35

        reasons.append("Compressed archive")

        recommendations.append(
            "Analyze archive contents in an isolated environment."
        )


    if extension in [".exe", ".dll", ".bat", ".msi", ".scr"]:

        score += 60

        reasons.append("Executable file")

        recommendations.append(
            "Perform malware and behavioral analysis before execution."
        )


    if extension in [".js", ".vbs", ".ps1", ".py"]:

        score += 45

        reasons.append("Script file")

        recommendations.append(
            "Review source code for suspicious functionality."
        )


    if duplicate:

        score += 25

        reasons.append("Duplicate evidence")

        recommendations.append(
            "Verify chain of custody and duplicate origin."
        )


    if size > 102400:

        score += 15

        reasons.append("Large evidence file")

        recommendations.append(
            "Validate storage integrity and acquisition process."
        )


    known = [
        ".pdf",
        ".png",
        ".jpg",
        ".jpeg",
        ".gif",
        ".bmp",
        ".tiff",
        ".webp",
        ".doc",
        ".docx",
        ".ppt",
        ".pptx",
        ".xls",
        ".xlsx",
        ".zip",
        ".rar",
        ".7z",
        ".txt",
        ".csv",
        ".exe",
        ".dll",
        ".bat",
        ".js",
        ".py"
    ]

    if extension not in known:

        score += 20

        reasons.append("Unknown file type")

        recommendations.append(
            "Perform manual inspection before processing."
        )


    if score > 100:

        score = 100


    if score <= 20:

        level = "LOW"

    elif score <= 50:

        level = "MEDIUM"

    else:

        level = "HIGH"


    return {

        "score": score,

        "level": level,

        "reasons": reasons,

        "recommendations": recommendations

    }