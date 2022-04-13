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
    if f"{language}_server_error" not in g.ERRORS : language = "en"

    try:
        # Validation
        if not request.forms.get("user_id"):
            errors = {
                "en_error":"user_id is missing.",
                "da_error":"user_id mangler."
            }
            return g._SEND(400, errors[f"{language}_error"])

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
        user_id = request.forms.get("user_id")

        tweet = (
            tweet_text,
            tweet_image,
            tweet_created_at,
            tweet_created_at_date,
            tweet_updated_at,
            tweet_updated_at_date,
            user_id
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
                    user_id
                )
                VALUES(%s, %s, %s, %s, %s, %s, %s) 
        """
        db.execute(query, tweet)
        db_connect.commit()
        
        response.status = 201
        tweet_id = db.lastrowid
        db.execute("""
                    SELECT tweets.tweet_id, 
                    tweets.tweet_text, 
                    tweets.tweet_image, 
                    tweets.tweet_created_at, 
                    tweets.tweet_created_at_date, 
                    tweets.tweet_updated_at, 
                    tweets.tweet_updated_at_date, 
                    tweets.user_id, 
                    users.user_handle, 
                    users.user_first_name, 
                    users.user_last_name, 
                    users.user_image_src
                    FROM tweets
                    JOIN users
                    WHERE tweets.tweet_id = %s
                    AND users.user_id = %s
                    """, (tweet_id, user_id))
        tweet = db.fetchone()

        return json.dumps(tweet)

    except Exception as ex:
        print(ex)
        return g._SEND(500, g.ERRORS[f"{language}_server_error"])

    finally:
        db.close()