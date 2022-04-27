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
            # tabs = g._GET_TABS(user['user_handle'])
            tabs = g.TABS
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
                JOIN users ON tweets.tweet_user_id = users.user_id 
                JOIN follows ON tweets.tweet_user_id = follows.follows_user_id
                WHERE follows.follow_user_id = %s
                UNION 
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
                WHERE user_id = %s AND tweet_user_id = %s
                ORDER BY tweet_created_at DESC
                LIMIT %s,%s
            """, (user['user_id'], user['user_id'], user['user_id'], int(0), int(10)))
            tweets = db.fetchall()
            for tweet in tweets:
                tweet['tweet_created_at_date'] = g._DATE_STRING(int(tweet['tweet_created_at']))
            follows = g._GET_FOLLOWS_USER_IDS(user['user_id'], language)
            likes = g._GET_LIKES_BY_USER_ID(user['user_id'], language)
            
            response.status = 200
            return dict(tabs=tabs, title="Home", is_fetch=is_fetch, user=user, tweets=tweets, follows=follows, likes=likes)
        except Exception as ex:
            print(ex)
            return g._SEND(500, g.ERRORS[f"{language}_server_error"])
        finally:
            db.close()

    return redirect("/explore")