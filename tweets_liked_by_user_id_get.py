from bottle import get, request, response
import g
import pymysql
import json

##############################
@get("/liked/tweets/<user_id>/<min>/<max>")
@get("<language>/liked/tweets/<user_id>/<min>/<max>")
def _(user_id="", min=None, max=None, language="en"):
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
            JOIN users ON tweets.tweet_user_id = users.user_id
            JOIN likes ON tweets.tweet_id = likes.like_tweet_id
            WHERE likes.like_user_id = %s 
            ORDER BY tweet_created_at DESC
            LIMIT %s,%s;
        """, (user_id, int(min), int(max)))
        tweets = db.fetchall()
        counter = db.rowcount
        if not counter: return g._SEND(204, "")
        for tweet in tweets:
            tweet['tweet_created_at_date'] = g._DATE_STRING(int(tweet['tweet_created_at']))
        response.status = 200
        return json.dumps(tweets)
    except Exception as ex:
        print(ex)
        return g._SEND(500, g.ERRORS(f"{language}_server_error"))
    finally:
        db.close()