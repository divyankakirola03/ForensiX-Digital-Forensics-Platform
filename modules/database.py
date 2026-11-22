import sqlite3


def init_db():

    conn = sqlite3.connect('forensix.db')

    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS evidence (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            filename TEXT,

            md5 TEXT,

            sha256 TEXT,

            size REAL,

            created TEXT

        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS custody_log (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            case_id INTEGER,

            action TEXT,

            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP

        )
    ''')

    conn.commit()
    conn.close()


def add_custody_log(case_id, action):

    conn = sqlite3.connect('forensix.db')

    cursor = conn.cursor()

    cursor.execute(
        '''
        INSERT INTO custody_log
        (
            case_id,
            action
        )
        VALUES (?, ?)
        ''',
        (
            case_id,
            action
        )
    )

    conn.commit()
    conn.close()


def get_recent_activity():

    conn = sqlite3.connect('forensix.db')

    cursor = conn.cursor()

    cursor.execute(
        '''
        SELECT case_id,
               action,
               timestamp
        FROM custody_log
        ORDER BY id DESC
        LIMIT 10
        '''
    )

    data = cursor.fetchall()

    conn.close()

    return data


def find_duplicate(sha256):

    conn = sqlite3.connect('forensix.db')

    cursor = conn.cursor()

    cursor.execute(
        '''
        SELECT id
        FROM evidence
        WHERE sha256 = ?
        ''',
        (sha256,)
    )

    result = cursor.fetchone()

    conn.close()

    return result


def save_evidence(filename, md5, sha256, size, created):

    conn = sqlite3.connect('forensix.db')

    cursor = conn.cursor()

    cursor.execute(
        '''
        INSERT INTO evidence
        (
            filename,
            md5,
            sha256,
            size,
            created
        )
        VALUES (?, ?, ?, ?, ?)
        ''',
        (
            filename,
            md5,
            sha256,
            size,
            created
        )
    )

    conn.commit()

    evidence_id = cursor.lastrowid

    conn.close()

    return evidence_id


def get_total_cases():

    conn = sqlite3.connect('forensix.db')

    cursor = conn.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM evidence"
    )

    total = cursor.fetchone()[0]

    conn.close()

    return total


def get_recent_cases():

    conn = sqlite3.connect('forensix.db')

    cursor = conn.cursor()

    cursor.execute(
        '''
        SELECT id,
               filename
        FROM evidence
        ORDER BY id DESC
        LIMIT 5
        '''
    )

    cases = cursor.fetchall()

    conn.close()

    return cases
def get_file_statistics():

    conn = sqlite3.connect("forensix.db")

    cursor = conn.cursor()

    cursor.execute("""
        SELECT filename
        FROM evidence
    """)

    rows = cursor.fetchall()

    conn.close()

    images = 0
    pdfs = 0
    docs = 0
    others = 0

    for row in rows:

        file = row[0].lower()

        if file.endswith((".png",".jpg",".jpeg",".gif",".bmp",".tiff",".webp")):
            images += 1

        elif file.endswith(".pdf"):
            pdfs += 1

        elif file.endswith((".doc",".docx",".ppt",".pptx",".xls",".xlsx")):
            docs += 1

        else:
            others += 1

    return {

        "images":images,

        "pdfs":pdfs,

        "docs":docs,

        "others":others

    }


def get_total_storage():

    conn = sqlite3.connect("forensix.db")

    cursor = conn.cursor()

    cursor.execute("""

        SELECT SUM(size)

        FROM evidence

    """)

    total = cursor.fetchone()[0]

    conn.close()

    if total is None:

        total = 0

    return round(total/1024,2)