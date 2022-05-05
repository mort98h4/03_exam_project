from bottle import get, request, response
import g
import pymysql
import json

##############################
@get("/users/<user_handle>")
@get("/<language>/users/<user_handle>")
def _(user_handle="", language="en"):
    try:
        if f"{language}_server_error" not in g.ERRORS: language = "en"
        user_handle, error = g._IS_HANDLE(user_handle, language)
        if error: return g._SEND(400, error)
        
    except Exception as ex:
        print(ex)
        return g._SEND(500, g.ERRORS[f"{language}_server_error"])

    try:
        db_connect = pymysql.connect(**g.DB_CONFIG)
        db = db_connect.cursor()
        query = f'SELECT * FROM users WHERE user_handle LIKE "%{user_handle}%" ORDER BY user_total_followers DESC LIMIT 0,5'
        db.execute(query)
        users = db.fetchall()
        counter = db.rowcount
        if not counter: return g._SEND(204, "")
        response.status = 200
        return json.dumps(users)
    except Exception as ex:
        print(ex)
        return g._SEND(500, g.ERRORS[f"{language}_server_error"])
    finally:
        db.close()