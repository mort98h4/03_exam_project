from bottle import post, request, response, redirect
import g
import time
from datetime import datetime
import pymysql
import json

##############################
@post("/signup")
@post("/<language>/signup")
def _(language = "en"):
    try:
        if f"{language}_server_error" not in g.ERRORS: language = "en"

        # VALIDATION
        user_first_name, error = g._IS_NAME(request.forms.get("user_first_name"), language)
        if error: return g._SEND(400, error)
        user_last_name, error = g._IS_NAME(request.forms.get("user_last_name"), language)
        if error: return g._SEND(400, error)
        user_email, error = g._IS_EMAIL(request.forms.get("user_email"), language)
        if error: return g._SEND(400, error)
        user_handle, error = g._IS_HANDLE(request.forms.get("user_handle"), language)
        if error: return g._SEND(400, error)
        user_password, error = g._IS_PASSWORD(request.forms.get("user_password"), language)
        if error: return g._SEND(400, error)
        if not request.forms.get("user_confirm_password"):
            errors = {
                "en":"Confirm password is missing.",
                "da":"Bekræft kodord mangler."
            }
            return g._SEND(400, errors[language])
        user_confirm_password = request.forms.get("user_confirm_password")
        if not user_confirm_password == user_password:
            errors = {
                "en":"Confirm password is not identical to password.",
                "da":"Bekræft kodeord er ikke identisk med kodeord."
            }
            return g._SEND(400, errors[language])

        user = (
            user_first_name,
            user_last_name,
            user_email,
            user_handle,
            user_password,
            "default_profile.png",
            "",
            "",
            str(int(time.time())),
            datetime.now().strftime("%Y-%B-%d-%A %H:%M:%S"),
            int(0),
            int(0),
            int(0),
            int(0)
        )

    except Exception as ex:
        print(ex)
        return g._SEND(500, g.ERRORS[f"{language}_server_error"])

    try: 
        db_connect = pymysql.connect(**g.DB_CONFIG)
        db = db_connect.cursor()
        query = """
                INSERT INTO users
                (user_first_name,
                user_last_name,
                user_email,
                user_handle,
                user_password,
                user_image_src,
                user_cover_image,
                user_description,
                user_created_at,
                user_created_at_date,
                user_total_follows,
                user_total_followers,
                user_total_tweets,
                user_is_admin)
                VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
         """
        db.execute(query, user)
        db_connect.commit()

        response.status = 201
        return json.dumps(user)
    except Exception as ex:
        print(ex)
        if "user_handle" in str(ex): 
            print("user_handle already exists.")
            error = {
                "en_user_handle_error": "Username already exists.",
                "da_user_handle_error": "Brugernavn findes allerede."
            }
            return g._SEND(400, error[f"{language}_user_handle_error"])
        if "user_email" in str(ex): 
            print("user_email already exists.")
            error = {
                "en_user_email_error": "Email already exists.",
                "da_user_email_error": "Email findes allerede."
            }
            return g._SEND(400, error[f"{language}_user_email_error"])

        return g._SEND(500, g.ERRORS[f"{language}_server_error"])
    finally:
        db.close()