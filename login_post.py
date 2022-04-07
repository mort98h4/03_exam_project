from bottle import post, redirect, request, response
import g
import time
import jwt
import pymysql
import json

##############################
@post("/login")
@post("/<language>/login")
def _(language = "en"):
    try:
        if f"{language}_server_error" not in g.ERRORS: language = "en"

        user_email, error = g._IS_EMAIL(request.forms.get("user_email"), language)
        if error: return g._SEND(400, error)
        user_password, error = g._IS_PASSWORD(request.forms.get("user_password"), language)
        if error: return g._SEND(400, error)

    except Exception as ex:
        print(ex)
        return g._SEND(500, g.ERRORS[f"{language}_server_error"])

    try:
        db_connect = pymysql.connect(**g.DB_CONFIG)
        db = db_connect.cursor()
        db.execute("SELECT * FROM users WHERE user_email = %s", (user_email,))
        user = db.fetchone()

        if not user: 
            errors = {
                "en": "Email does not match a user.",
                "da": "Email er ikke tilknyttet en bruger."
            }
            return g._SEND(400, errors[language])

        if not user_password == user['user_password']:
            errors = {
                "en": "Password was incorrect.",
                "da": "Kodeordet var ikke korrekt."
            }
            return g._SEND(400, errors[language]) 

        user_session = {
            "fk_user_id": user["user_id"],
            "iat": int(time.time())
        }

        query = """
                INSERT INTO sessions
                (fk_user_id,
                iat)
                VALUES(%s, %s)"""

        db.execute(query, (user_session["fk_user_id"], user_session["iat"]))
        db_connect.commit()

        session_id = db.lastrowid
        user_session["session_id"] = int(session_id)

        encoded_jwt = jwt.encode(user_session, g.JWT_SECRET, algorithm="HS256")
        response.set_cookie("jwt", encoded_jwt, path="/")

        return g._SEND(200, "Succesfull log in.")
    except Exception as ex:
        print(ex)
        return g._SEND(500, g.ERRORS[f"{language}_server_error"])
    finally:
        db.close()