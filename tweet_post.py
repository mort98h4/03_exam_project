from bottle import post, response, request
import g
import time
from datetime import datetime
import pymysql
import json

##############################
@post("/tweet")
@post("/<language>/tweet")
def _(language="en"):
    try:
        if f"{language}_server_error" not in g.ERRORS : language = "en"
        # Validation
        tweet_user_id, error = g._IS_DIGIT(request.forms.get("user_id"), language)
        if error: return g._SEND(400, error)

        tweet_text, error = g._IS_TWEET_TEXT(request.forms.get("tweet_text"), language)
        if error: return g._SEND(400, error)

        tweet_image = ""
        if request.files.get("tweet_image"):
            tweet_image, error = g._IS_IMAGE(request.files.get("tweet_image"), language)
            if error: return g._SEND(400, error)
        
        tweet_created_at = str(int(time.time()))
        tweet_created_at_date = datetime.now().strftime("%Y-%B-%d-%A %H:%M:%S")
        tweet_updated_at = ""
        tweet_updated_at_date = ""
        tweet_total_likes = 0

        tweet = (
            tweet_text,
            tweet_image,
            tweet_created_at,
            tweet_created_at_date,
            tweet_updated_at,
            tweet_updated_at_date,
            tweet_user_id,
            tweet_total_likes
        )

    except Exception as ex:
        print(ex)
        return g._SEND(500, g.ERRORS[f"{language}_server_error"])

    try:
        db_connect = pymysql.connect(**g.DB_CONFIG)
        db = db_connect.cursor()

        query = """
                INSERT INTO tweets
                (
                    tweet_text,
                    tweet_image,
                    tweet_created_at,
                    tweet_created_at_date,
                    tweet_updated_at,
                    tweet_updated_at_date,
                    tweet_user_id,
                    tweet_total_likes
                )
                VALUES(%s, %s, %s, %s, %s, %s, %s, %s) 
        """
        db.execute(query, tweet)
        tweet_id = db.lastrowid
        counter = db.rowcount
        if not counter: g._SEND(204, "")
        
        db.execute("UPDATE users SET user_total_tweets = user_total_tweets + 1 WHERE user_id = %s", (tweet_user_id,))
        counter = db.rowcount
        if not counter: g._SEND(204, "")

        response.status = 201
        db_connect.commit()
        
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
                    users.user_handle, 
                    users.user_first_name, 
                    users.user_last_name, 
                    users.user_image_src
                    FROM tweets
                    JOIN users
                    WHERE tweets.tweet_id = %s
                    AND users.user_id = %s
                    """, (tweet_id, tweet_user_id))
        tweet = db.fetchone()
        return json.dumps(tweet)

    except Exception as ex:
        print(ex)
        return g._SEND(500, g.ERRORS[f"{language}_server_error"])

    finally:
        db.close()