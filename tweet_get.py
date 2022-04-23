from bottle import get, request, response, view
import g
import jwt
import time
import datetime
import pymysql

##############################
@get("/tweet/<tweet_id>")
@get("/<language>/tweet/<tweet_id>")
@view("tweet_by_id")
def _(language="en", tweet_id=""):
    is_fetch = True if request.headers.get('From-Fetch') else False
    if f"{language}_server_error" not in g.ERRORS: language = "en"
    tabs = [
        {"icon": "fas fa-hashtag fa-fw", "title": "Explore", "id": "explore"},
        {"icon": "fa-solid fa-gear fa-fw", "title": "Settings", "id": "settings"}
    ]
    user = {}
    follows = []
    tweet = {"tweet_id": tweet_id}

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
                tabs = g._GET_TABS(user['user_handle'])

        except Exception as ex:
            print(ex)
            return g._SEND(500, g.ERRORS[f"{language}_server_error"])

    try:
        db_connect = pymysql.connect(**g.DB_CONFIG)
        db = db_connect.cursor()
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
            WHERE tweets.tweet_id = %s 
            AND tweets.tweet_user_id = users.user_id
        """, (tweet_id,))
        tweet = db.fetchone()
        time_of_day = datetime.datetime.fromtimestamp(int(tweet['tweet_created_at'])).strftime('%H:%M')
        month = datetime.datetime.fromtimestamp(int(tweet['tweet_created_at'])).strftime('%B')
        date_year = datetime.datetime.fromtimestamp(int(tweet['tweet_created_at'])).strftime('%d, %Y')
        tweet['tweet_created_at_date'] = f"{time_of_day} {month[:3]} {date_year}"
        print("#"*30)
        print(tweet)
        return dict(tweet=tweet, tabs=tabs, title="Tweet", is_fetch=is_fetch, user=user, follows=follows)
    except Exception as ex:
        print(ex)
        return g._SEND(500, g.ERRORS[f"{language}_server_error"])
    finally:
        db.close()