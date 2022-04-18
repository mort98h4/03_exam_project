from bottle import get, redirect, request, response, view
import g
import jwt
import time
import pymysql

##############################
@get("/home")
@get("/<language>/home")
@view("home")
def _(language = "en"):
    if f"{language}_server_error" not in g.ERRORS: language = "en"
    is_fetch = True if request.headers.get('From-Fetch') else False
    display_page = False

    if request.get_cookie("jwt"):
        cookie = request.get_cookie("jwt")
        decoded_jwt = jwt.decode(cookie, g.JWT_SECRET, algorithms=["HS256"])
        print("#"*30)
        print(decoded_jwt)
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

                display_page = True

        except Exception as ex:
            print(ex)
            return g._SEND(500, g.ERRORS[f"{language}_server_error"])

    if display_page: 
        try: 
            user = g._GET_USER_BY_ID(decoded_jwt['fk_user_id'], language)
            tabs = g._GET_TABS(user['user_handle'])
            tweets = g._GET_ALL_TWEETS(language)
            for tweet in tweets:
                tweet['tweet_created_at_date'] = g._DATE_STRING(int(tweet['tweet_created_at']))
            follows = g._GET_FOLLOWS_USER_IDS(user['user_id'], language)
            
            response.status = 200
            return dict(tabs=tabs, title="Home", is_fetch=is_fetch, user=user, tweets=tweets, follows=follows)
        except Exception as ex:
            print(ex)
            return g._SEND(500, g.ERRORS[f"{language}_server_error"])

    return redirect("/explore")