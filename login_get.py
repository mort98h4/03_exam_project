from bottle import delete, get, view, redirect, response, request
import g
import jwt
import time
import pymysql

##############################
@get("/login")
@get("/<language>/login")
@view("login")
def _(language = "en"):
    if f"{language}_server_error" not in g.ERRORS: language = "en"

    if request.get_cookie("jwt"):
        cookie = request.get_cookie("jwt")
        decoded_jwt = jwt.decode(cookie, g.JWT_SECRET, algorithms=["HS256"])
        now = int(time.time())
        seconds_since_session_created = int(now - decoded_jwt["iat"])
        try:
            db_connect = pymysql.connect(**g.DB_CONFIG)
            db = db_connect.cursor()
            if seconds_since_session_created > 86000: 
                print("Session expired")
                response.set_cookie("jwt", cookie, expires=0)
                db.execute("DELETE FROM sessions WHERE session_id = %s", (decoded_jwt["session_id"],))
                counter = db.rowcount
                db_connect.commit()
                if not counter: print("Ups!")
                print(f"Rows deleted: {counter}")
                return
            if seconds_since_session_created < 86000:
                print("Session not expired")
                db.execute(""" 
                       UPDATE sessions
                       SET iat = %s
                       WHERE sessions.session_id = %s """, (now, decoded_jwt["session_id"]))
                counter = db.rowcount
                db_connect.commit()
                if not counter: print("Ups!")
                print(f"Rows updated: {counter}")
        except Exception as ex:
            print(ex)
            return g._SEND(500, g.ERRORS[f"{language}_server_error"])       

        finally:
            db.close()

        return redirect("/explore")
        
    return