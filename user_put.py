from bottle import put, request, response
import g
import time
from datetime import datetime
import os
import json
import pymysql

##############################
@put("/user/<user_id>")
@put("/<language>/user/<user_id>")
def _(language="en", user_id=""):
    try:
        if f"{language}_server_error" not in g.ERRORS : language = "en"
        if not user_id:
            errors = {
                "en_error": "user_id is missing",
                "da_error": "user_id mangler."
            }
            return g._SEND(400, errors[f"{langauge}_error"])
        
        allowed_keys = ["user_id", "user_image_src", "user_description", "user_image_name"]
        for key in request.forms.keys():
            if not key in allowed_keys:
                print(key)
                return g._SEND(400, f"Forbidden {key}.")

    except Exception as ex:
        print(ex)
        return g._SEND(500, g.ERRORS[f"{language}_server_error"])

    try:
        db_connect = pymysql.connect(**g.DB_CONFIG)
        db = db_connect.cursor()
        db.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
        user = db.fetchone()
        if not user: return g._SEND(204, "")
        image_file_name = user['user_image_src']

        user_description, error = g._IS_USER_DESCRIPTION(request.forms.get('user_description'), language)
        if error: return g._SEND(400, error)
        if request.files.get('user_image_src'):
            user_image_src, error = g._IS_IMAGE(request.files.get('user_image_src'), language)
            if error: return g._SEND(400, error)
        else:
            user_image_src = request.forms.get("user_image_name")

        user['user_image_src'] = user_image_src
        user['user_description'] = user_description

        db.execute("""
                    UPDATE users
                    SET user_image_src = %s,
                    user_description = %s
                    WHERE user_id = %s
                    """, (user['user_image_src'], user['user_description'], user_id))
        counter = db.rowcount
        db_connect.commit()
        if not counter: return g._SEND(204, "")
        print("#"*30)
        print(f"Rows updated: {counter}")
        if image_file_name != "default_profile.png" and image_file_name != user_image_src: os.remove(f"./images/{image_file_name}")
        response.status = 200
        return json.dumps(user)
    except Exception as ex:
        print(ex)
        return g._SEND(500, g.ERRORS[f"{language}_server_error"])
    finally: 
        db.close()