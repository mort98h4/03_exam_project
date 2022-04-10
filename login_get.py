from bottle import get, view, redirect, response, request
import g
import jwt
import time

##############################
@get("/login")
@get("/<language>/login")
@view("login")
def _(language = "en"):
    if f"{language}_server_error" not in g.ERRORS: language = "en"

    if request.get_cookie("jwt"):
        display_page = True

        cookie = request.get_cookie("jwt")
        decoded_jwt = jwt.decode(cookie, g.JWT_SECRET, algorithms=["HS256"])
        now = int(time.time())
        seconds_since_session_created = int(now - decoded_jwt["iat"])
        try:
            if seconds_since_session_created > 86000: 
                print("Session expired")
                g._DELETE_SESSION(decoded_jwt, language)
                response.set_cookie("jwt", cookie, expires=0)
            if seconds_since_session_created < 86000:
                print("Session not expired")
                g._UPDATE_SESSION(decoded_jwt, now, language)

                decoded_jwt["iat"] = now
                encoded_jwt = jwt.encode(decoded_jwt, g.JWT_SECRET, algorithm="HS256")
                response.set_cookie("jwt", encoded_jwt, path="/")

                display_page = False
                
        except Exception as ex:
            print(ex)
            return g._SEND(500, g.ERRORS[f"{language}_server_error"])       

        if not display_page: return redirect("/home")
        
    return