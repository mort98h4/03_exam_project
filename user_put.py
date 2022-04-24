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
        user_id, error = g._IS_DIGIT(user_id, language)
        if error: return g._SEND(400, error)
        
        allowed_keys = ["user_id", "user_image_src", "user_description", "user_image_name", "user_cover_image", "user_cover_image_name"]
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
        user_image_src_file = user['user_image_src']
        user_cover_image_file = user['user_cover_image']

        user_description, error = g._IS_USER_DESCRIPTION(request.forms.get('user_description'), language)
        if error: return g._SEND(400, error)
        if request.files.get('user_image_src'):
            user_image_src, error = g._IS_IMAGE(request.files.get('user_image_src'), language)
            if error: return g._SEND(400, error)
        else:
            user_image_src = request.forms.get("user_image_name")
        if request.files.get('user_cover_image'):
            user_cover_image, error = g._IS_IMAGE(request.files.get('user_cover_image'), language)
            if error: return g._SEND(400, error)
        else:
            user_cover_image = request.forms.get("user_cover_image_name")

        user['user_image_src'] = user_image_src
        user['user_cover_image'] = user_cover_image
        user['user_description'] = user_description

        db.execute("""
                    UPDATE users
                    SET user_image_src = %s,
                    user_cover_image = %s,
                    user_description = %s
                    WHERE user_id = %s
                    """, (user['user_image_src'], user['user_cover_image'], user['user_description'], user_id))
        counter = db.rowcount
        db_connect.commit()
        if not counter: return g._SEND(204, "")
        print("#"*30)
        print(f"Rows updated: {counter}")
        if user_image_src_file != "default_profile.png" and user_image_src_file != user_image_src: os.remove(f"./images/{user_image_src_file}")
        if user_cover_image_file != "" and user_cover_image_file != user_cover_image: os.remove(f"./images/{user_cover_image_file}")
        response.status = 200
        return json.dumps(user)
    except Exception as ex:
        print(ex)
        return g._SEND(500, g.ERRORS[f"{language}_server_error"])
    finally: 
        db.close()