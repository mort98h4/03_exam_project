from bottle import get, request, response
import g
import pymysql
import json
import jwt

##############################
@get("/tweets/<user_id>/<offset>")
@get("<language>/tweets/<user_id>/<offset>")
def _(user_id="", offset=None, language="en"):
    try:
        if f"{language}_server_error" not in g.ERRORS : language = "en"
        user_id, error = g._IS_DIGIT(user_id, language)
        if error: return g._SEND(400, error)
        offset, error = g._IS_DIGIT(offset, language)
        if error: return g._SEND(400, error)

        decoded_jwt = {}
        if request.get_cookie("jwt"):
            cookie = request.get_cookie("jwt")
            decoded_jwt = jwt.decode(cookie, g.JWT_SECRET, algorithms=["HS256"])

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
            WHERE tweets.tweet_user_id = %s AND users.user_id = %s
            ORDER BY tweet_created_at DESC
            LIMIT %s,10
        """, (user_id, user_id, int(offset),))
        tweets = db.fetchall()
        counter = db.rowcount
        if not counter: return g._SEND(204, "")
        for tweet in tweets:
            tweet['tweet_created_at_date'] = g._DATE_STRING(int(tweet['tweet_created_at']))

        response_to_client = {"tweets": tweets, "liked_tweets":[], "follows":[], "user_id":""}

        if decoded_jwt:
            db.execute("SELECT * FROM likes WHERE like_user_id = %s", (decoded_jwt['fk_user_id'],))
            liked_tweets = db.fetchall()
            for liked_tweet in liked_tweets:
                response_to_client['liked_tweets'].append(liked_tweet['like_tweet_id'])
            response_to_client['follows'] = g._GET_FOLLOWS_USER_IDS(decoded_jwt['fk_user_id'], language)
            response_to_client['user_id'] = decoded_jwt['fk_user_id']
        
        response.status = 200
        return json.dumps(response_to_client)
    except Exception as ex:
        print(ex)
        return g._SEND(500, g.ERRORS[f"{language}_server_error"])
    finally:
        db.close()