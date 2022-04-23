from bottle import get, request, response, view
import g
import jwt
import time
import datetime
import pymysql

##############################
@get("/profile/<user_handle>")
@get("/<language>/profile/<user_handle>")
@view("profile")
def _(language="en", user_handle=""):
    is_fetch = True if request.headers.get('From-Fetch') else False
    if f"{language}_server_error" not in g.ERRORS: language = "en"

    print("#"*30)
    print(user_handle)

    tabs = [
        {"icon": "fas fa-hashtag fa-fw", "title": "Explore", "id": "explore"},
        {"icon": "fa-solid fa-gear fa-fw", "title": "Settings", "id": "settings"}
    ]
    user = {}
    follows = []
    likes = []

    if request.get_cookie("jwt"):
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

                user = g._GET_USER_BY_ID(decoded_jwt['fk_user_id'])
                follows = g._GET_FOLLOWS_USER_IDS(user['user_id'], language)
                likes = g._GET_LIKES_BY_USER_ID(user['user_id'], language)
                tabs = g._GET_TABS(user['user_handle'])

        except Exception as ex:
            print(ex)
            return g._SEND(500, g.ERRORS[f"{language}_server_error"])

    try: 
        db_connect = pymysql.connect(**g.DB_CONFIG)
        db = db_connect.cursor()
        db.execute("SELECT * FROM users WHERE user_handle = %s", (user_handle,))
        display_user = db.fetchone()
        display_user['user_created_at_date'] = datetime.datetime.fromtimestamp(int(display_user['user_created_at'])).strftime('%B %Y')
        print("#"*30)
        print(display_user)
        db.execute("""
                SELECT tweets.tweet_id, 
                tweets.tweet_text, 
                tweets.tweet_image, 
                tweets.tweet_created_at, 
                tweets.tweet_created_at_date, 
                tweets.tweet_updated_at, 
                tweets.tweet_updated_at_date, 
                tweets.tweet_user_id, 
                tweets.tweet_total_likes,
                users.user_first_name, 
                users.user_last_name, 
                users.user_handle, 
                users.user_image_src 
                FROM tweets
                JOIN users
                WHERE tweets.tweet_user_id = %s AND users.user_id = %s
                ORDER BY tweet_created_at DESC
        """, (display_user['user_id'], display_user['user_id']))
        tweets = db.fetchall()
        for tweet in tweets:
            tweet['tweet_created_at_date'] = g._DATE_STRING(int(tweet['tweet_created_at']))

        return dict(tabs=tabs, title=user_handle, is_fetch=is_fetch, user=user, follows=follows, likes=likes, display_user=display_user, tweets=tweets)
    except Exception as ex:
        print(ex)
        return g._SEND(500, g.ERRORS[f"{language}_server_error"])
    finally:
        db.close()