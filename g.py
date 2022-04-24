from bottle import response
import re
import os
import uuid
import imghdr
import sqlite3
import pymysql
import time
import datetime
import math

try:
    import production
    DB_CONFIG = {
        "host": "mort98h4.mysql.eu.pythonanywhere-services.com",
        "user": "mort98h4",
        "password": "iBs2O9boZqZy",
        "database": "mort98h4$twatter",
        "cursorclass": pymysql.cursors.DictCursor
    }
except:
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

TABS = [
  {"icon": "fas fa-home fa-fw", "title": "Home", "id":"home"},
  {"icon": "fas fa-hashtag fa-fw", "title": "Explore", "id": "explore"},
  {"icon": "far fa-bell fa-fw", "title": "Notifications", "id": "notifications"},
  {"icon": "far fa-envelope fa-fw", "title": "Messages", "id": "messages"},
  {"icon": "far fa-bookmark fa-fw", "title": "Bookmarks", "id": "bookmarks"},
  {"icon": "fas fa-clipboard-list fa-fw", "title": "Lists", "id": "lists"},
  {"icon": "far fa-user fa-fw", "title": "Profile", "id": "profile"},
  {"icon": "fas fa-ellipsis-h fa-fw", "title": "More", "id": "more"}
]

def _GET_TABS(user_handle=""):
    tabs = TABS
    for tab in tabs: 
        if tab['id'] == "profile": tab['id'] = f"profile{'/' + user_handle}"
    return tabs

##############################
def _SEND(status = 400, error_message = "Unknown error"):
    response.status = status
    return {"info": error_message}

##############################
def _IS_ID(id="", language="en"):
    errors_id_missing = {
        "en": f"Id is missing.",
        "da": f"Id mangler."
    }
    errors_id_invalid = {
        "en": f"Id is invalid.",
        "da": f"Id er ikke valid."
    }

    if not id: return None, errors_id_missing[language]
    is_digit = id.isdigit()
    if not is_digit: return None, errors_id_invalid[language]
    return id, None

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
def _IS_TWEET_TEXT(text=None, language="en"):
    min, max = 1, 255
    errors_text_missing = {
        "en": "Tweet_text is missing.",
        "da": "Tweet_text mangler."
    }
    errors_min = {
        "en": f"Tweet_text must be at least {min} character.",
        "da": f"Tweet_text skal minimum indeholde {min} tegn."
    }
    errors_max = {
        "en": f"Tweet_text must be less than {max} characters.",
        "da": f"Tweet_text må maksimum indeholde {max} tegn."
    }

    if not text: return None, errors_text_missing[language]
    text = re.sub("[\n\t]*", "", text)
    text = re.sub(" +", " ", text)
    text = text.strip()
    if len(text) < min: return None, errors_min[language]
    if len(text) > max: return None, errors_max[language]
    return text, None

##############################
def _IS_IMAGE(image=None, language="en"):
    errors_file_not_allowed = {
        "en": "Filetype is not allowed",
        "da": "Filtypen er ikke tilladt."
    }
    errors_suspicious_file = {
        "en": "Suspicious image file.",
        "da": "Mistænkelig billedfil."
    }

    file_name, file_extension = os.path.splitext(image.filename)
    if file_extension not in (".png", ".jpeg", ".jpg"): return None, errors_file_not_allowed[language]
    if file_extension == ".jpg": file_extension = ".jpeg"
    image_name = f"{str(uuid.uuid4())}{file_extension}"
    image.save(f"./images/{image_name}")
    imghdr_extension = imghdr.what(f"./images/{image_name}")
    if not file_extension == f".{imghdr_extension}":
        os.remove(f"./images/{image_name}")
        return None, errors_suspicious_file[language]
    return image_name, None

def _IS_USER_DESCRIPTION(text=None, language="en"):
    min, max = 1, 160
    errors_text_missing = {
        "en": "user_description is missing.",
        "da": "user_description mangler."
    }
    errors_min = {
        "en": f"user_description must be at least {min} character.",
        "da": f"user_description skal minimum indeholde {min} tegn."
    }
    errors_max = {
        "en": f"user_description must be less than {max} characters.",
        "da": f"Tuser_description må maksimum indeholde {max} tegn."
    }

    if not text: return None, errors_text_missing[language]
    text = re.sub("[\n\t]*", "", text)
    text = re.sub(" +", " ", text)
    text = text.strip()
    if len(text) < min: return None, errors_min[language]
    if len(text) > max: return None, errors_max[language]
    return text, None

##############################
def _DATE_STRING(epoch):
    now = int(time.time())
    time_passed = now - epoch
    if time_passed < 60: return f"{time_passed}s"
    if time_passed < 3600: return f"{math.floor(time_passed/60)}m"
    if time_passed < 86000: return f"{math.floor(time_passed/3600)}h"
    if time_passed > 85999: 
        month = datetime.datetime.fromtimestamp(epoch).strftime('%B')
        date_year = datetime.datetime.fromtimestamp(epoch).strftime('%d %Y')
        return f"{month[:3]} {date_year}"

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
def _GET_USER_BY_ID(id=None, language="en"):
    try:
        db_connect = pymysql.connect(**DB_CONFIG)
        db = db_connect.cursor()
        db.execute("SELECT * FROM users WHERE user_id = %s", (id,))
        user = db.fetchone()
        return user
    except Exception as ex:
        print(ex)
        return _SEND(500, ERRORS[f"{language}_server_error"])
    finally:
        db.close()

##############################
def _GET_FOLLOWS_USER_IDS(user_id=None, language="en"):
    try:
        db_connect = pymysql.connect(**DB_CONFIG)
        db = db_connect.cursor()
        db.execute("SELECT * FROM follows WHERE follow_user_id = %s", (user_id,))
        follows = db.fetchall()
        follow_ids = []
        for follow in follows:
            follow_ids.append(follow['follows_user_id'])
        return follow_ids
    except Exception as ex:
        print(ex)
        return _SEND(500, ERRORS[f"{language}_server_error"])
    finally:
        db.close()

##############################
def _GET_LIKES_BY_USER_ID(user_id=None, language="en"):
    try:
        db_connect = pymysql.connect(**DB_CONFIG)
        db = db_connect.cursor()
        db.execute("SELECT * FROM likes WHERE like_user_id = %s", (user_id,))
        likes = db.fetchall()
        tweet_ids = []
        for like in likes:
            tweet_ids.append(like['like_tweet_id'])
        return tweet_ids
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