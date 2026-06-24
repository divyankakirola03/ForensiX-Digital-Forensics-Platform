from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)
from reportlab.lib.styles import getSampleStyleSheet


def generate_report(case_id, metadata, hashes, exif):

    pdf_name = f"FX-{case_id}_Report.pdf"

    doc = SimpleDocTemplate(pdf_name)

    styles = getSampleStyleSheet()

    elements = []

    elements.append(
        Paragraph(
            "ForensiX Investigation Report",
            styles['Title']
        )
    )

    elements.append(Spacer(1, 20))

    elements.append(
        Paragraph(
            f"Case ID: FX-{case_id}",
            styles['Heading2']
        )
    )

    elements.append(
        Paragraph(
            f"Filename: {metadata['filename']}",
            styles['BodyText']
        )
    )

    elements.append(
        Paragraph(
            f"Size: {metadata['size']} KB",
            styles['BodyText']
        )
    )

    elements.append(
        Paragraph(
            f"Created: {metadata['created']}",
            styles['BodyText']
        )
    )

    elements.append(
        Paragraph(
            f"MD5: {hashes['md5']}",
            styles['BodyText']
        )
    )

    elements.append(
        Paragraph(
            f"SHA256: {hashes['sha256']}",
            styles['BodyText']
        )
    )

    elements.append(
        Paragraph(
            f"Camera Model: {exif.get('Model', 'N/A')}",
            styles['BodyText']
        )
    )

    elements.append(
        Paragraph(
            f"Date Taken: {exif.get('DateTime', 'N/A')}",
            styles['BodyText']
        )
    )

    doc.build(elements)

    return pdf_name