from bottle import post, redirect, request, response
import g
import jwt

##############################
@post("/logout")
@post("/<language>/logout")
def _(language = "en"):
    if f"{language}_server_error" not in g.ERRORS: language = "en"

    try:
        cookie = request.get_cookie("jwt")
        decoded_jwt = jwt.decode(cookie, g.JWT_SECRET, algorithms=["HS256"])
        print("#"*30)
        print(decoded_jwt)
        g._DELETE_SESSION(decoded_jwt, language)
        response.set_cookie("jwt", cookie, path="/", expires=0)
    
    except Exception as ex:
        print(ex)
        return g._SEND(500, g.ERRORS[f"{language}_server_error"])
    
    finally:
        return redirect("/")