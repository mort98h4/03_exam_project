from bottle import response
import re
import sqlite3
import pymysql

DB_CONFIG = {
            "host":"localhost",
            "port":8889,
            "user":"root",
            "password":"root",
            "database":"twatter",
            "cursorclass": pymysql.cursors.DictCursor
        }

ERRORS = {
    "en_server_error": "Server error",
    "da_server_error": "Server fejl"
}

JWT_SECRET = "4w50m3 k3Y"

REGEX_EMAIL = '^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$'

##############################
def _SEND(status = 400, error_message = "Unknown error"):
    response.status = status
    return {"info": error_message}

##############################
def _IS_NAME(name=None, language="en"):
    min, max = 2, 25
    errors_name_missing = {
        "en": f"Name is missing.",
        "da": "Navn mangler."
    }
    errors_min = {
        "en": f"Name must be at least {min}",
        "da": f"Navn skal minimum indholde {min} tegn."
    }
    errors_max = {
        "en": f"Name is not allowed to exceed {max} characters.",
        "da": f"Navn må ikke være mere end {max} tegn."
    }

    if not name: return None, errors_name_missing[language]
    name = re.sub("[\n\t]*", "", name)
    name = re.sub(" +", " ", name)
    name = name.strip()
    if len(name) < min: return None, errors_min[language]
    if len(name) > max: return None, errors_max[language]
    name = name.capitalize()
    return name, None

##############################
def _IS_EMAIL(email=None, language="en"):
    errors_missing = {
        "en":"Email is missing.",
        "da":"Email mangler."
    }
    errors_invalid = {
        "en":"Email is invalid",
        "da":"Ugyldig email."
    }

    if not email: return None, errors_missing[language]
    email = email.strip()
    if not re.match(REGEX_EMAIL, email): return None, errors_invalid[language]
    return email, None

##############################
def _IS_HANDLE(handle=None, language="en"):
    min, max = 2, 30
    errors_missing = {
        "en":"Username is missing",
        "da":"Brugernavn mangler."
    }
    errors_min = {
        "en":f"Username must be at least {min} characters.",
        "da":f"Brugernavn skal minimum være {min} tegn."
    }
    errors_max = {
        "en":f"Username is not allowed to exceed {max} characters.",
        "da":f"Brugernavn må ikke være mere end {max} tegn."
    }
    errors_invalid_characters = {
        "en":"Username can only contain alphanumeric characters, '.', '-' or '_'.",
        "da":"Brugernavn må kun indeholde tal, bogstaver, '.', '-' eller '_'."
    }
    errors_invalid_character_succesion = {
        "en":"Username must not begin or end with '.', '-' or '_' and they must not succeed each other either.",
        "da":"Brugernavn må ikke begynde eller ende med '.', '-' eller '_', og de må ikke efterfølge hinanden."

    }
    if not handle: return None, errors_missing[language]
    if len(handle) < min: return None, errors_min[language]
    if len(handle) > max: return None, errors_max[language]
    if not re.match("^[a-zA-Z0-9\\._-]*$", handle): return None, errors_invalid_characters[language]
    if not re.match("^(?!.*[_.-]{2})[^_.-].*[^_.-]$", handle): return None, errors_invalid_character_succesion[language]
    return handle, None

##############################
def _IS_PASSWORD(password=None, language="en"):
    errors_missing = {
        "en":"Password is missing.",
        "da":"Kodeord mangler."
    }
    errors_invalid = {
        "en":"Password must be at least 8 characters containing at least 1 uppercase letter, 1 lowercase letter and 1 number.",
        "da":"Kodeord skal minimum være 8 tegn langt, og indeholde minimum 1 stort bogstav, 1 lille bogstav og 1 tal."
    }
    if not password: return None, errors_missing[language]
    if not re.match("^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$", password): return None, errors_invalid[language]
    return password, None

##############################
def _DELETE_SESSION(session=None, language = "en"):
    try:
        db_connect = pymysql.connect(**DB_CONFIG)
        db = db_connect.cursor() 
        db.execute("DELETE FROM sessions WHERE session_id = %s", (session["session_id"],))
        counter = db.rowcount
        db_connect.commit()
        if not counter: print("Ups!")
        print(f"Rows deleted: {counter}")
    except Exception as ex:
        print(ex)
        return _SEND(500, ERRORS[f"{language}_server_error"])
    finally:
        db.close()

##############################
def _UPDATE_SESSION(session=None, now=None, language = "en"):
    try: 
        db_connect = pymysql.connect(**DB_CONFIG)
        db = db_connect.cursor()
        db.execute(""" 
                       UPDATE sessions
                       SET iat = %s
                       WHERE sessions.session_id = %s """, (now, session["session_id"]))
        counter = db.rowcount
        db_connect.commit()
        if not counter: print("Ups!")
        print(f"Rows updated: {counter}")
    except Exception as ex:
        print(ex)
        return _SEND(500, ERRORS[f"{language}_server_error"])
    finally:
        db.close()

##############################
def _DB_CONNECT(db_name):
    db = sqlite3.connect(db_name)
    db.row_factory = _CREATE_JSON_FROM_SQLITE_RESULT
    return db

##############################
def _CREATE_JSON_FROM_SQLITE_RESULT(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d