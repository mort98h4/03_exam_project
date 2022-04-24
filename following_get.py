from bottle import get, request, response
import g
import pymysql
import json

##############################
@get("/<user_id>/following")
@get("/<language>/<user_id>/following")
def _(user_id="", language="en"):
    try:
        if f"{language}_server_error" not in g.ERRORS: language = "en"
        user_id, error = g._IS_ID(user_id, language)
        if error: return g._SEND(400, error)
    except Exception as ex:
        print(ex)
        return g._SEND(500, g.ERRORS[f"{language}_server_error"])
    
    try:
        db_connect = pymysql.connect(**g.DB_CONFIG)
        db = db_connect.cursor()
        db.execute("""
            SELECT follows.follow_user_id,
            users.user_id,
            users.user_first_name,
            users.user_last_name,
            users.user_handle,
            users.user_image_src,
            users.user_description
            FROM follows
            JOIN users
            WHERE follows.follow_user_id = %s
            AND follows.follows_user_id = users.user_id
        """, (user_id,))
        following = db.fetchall()
        counter = db.rowcount
        if not counter: return g._SEND(204, "")
        response.status = 200
        return json.dumps(following)
    except Exception as ex:
        print(ex)
        return g._SEND(500, g.ERRORS[f"{language}_server_error"])
    finally:
        db.close()