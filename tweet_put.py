from bottle import put, request, response
import g
import time
from datetime import datetime
import os
import json
import pymysql

##############################
@put("/tweet/<tweet_id>")
@put("/<language>/tweet/<tweet_id>")
def _(language="en", tweet_id=""):
    try:
        if f"{language}_server_error" not in g.ERRORS : language = "en"

        if not tweet_id:
            errors = {
                "en_error": "tweet_id is missing",
                "da_error": "tweet_id mangler."
            }
            return g._SEND(400, errors[f"{langauge}_error"])
        
        allowed_keys = ["tweet_id", "tweet_text", "tweet_image", "tweet_image_name"]
        for key in request.forms.keys():
            if not key in allowed_keys:
                print(key)
                return g._SEND(400, f"Forbidden {key}.")

    except Exception as ex:
        print(ex)
        return g._SEND(500, g.ERRORS[f"{language}_server_error"])
    
    try:
        db_connect = pymysql.connect(**g.DB_CONFIG)
        db = db_connect.cursor()
        db.execute("SELECT * FROM tweets WHERE tweet_id = %s", (tweet_id,))
        tweet = db.fetchone()
        if not tweet: return g._SEND(204, "")
        image_file_name = tweet['tweet_image']
        print("#"*40)
        print(image_file_name)

        tweet_text, error = g._IS_TWEET_TEXT(request.forms.get('tweet_text'), language)
        if error: return g._SEND(400, error)
        if request.files.get("tweet_image"):
            tweet_image, error = g._IS_IMAGE(request.files.get("tweet_image"), language)
            if error: return g._SEND(400, error)
        else:
            tweet_image = request.forms.get('tweet_image_name')

        tweet['tweet_text'] = tweet_text
        tweet['tweet_image'] = tweet_image
        tweet['tweet_updated_at'] = str(int(time.time()))
        tweet['tweet_updated_at_date'] = datetime.now().strftime("%Y-%B-%d-%A %H:%M:%S")

        db.execute("""
                    UPDATE tweets
                    SET tweet_text = %s,
                    tweet_image = %s,
                    tweet_updated_at = %s,
                    tweet_updated_at_date = %s
                    WHERE tweet_id = %s
                    """, (tweet['tweet_text'], tweet['tweet_image'], tweet['tweet_updated_at'], tweet['tweet_updated_at_date'], tweet_id))
        counter = db.rowcount
        db_connect.commit()
        if not counter: return g._SEND(204, "")
        print("#"*30)
        print(f"Rows updated: {counter}")
        if image_file_name != "" and image_file_name != tweet_image: os.remove(f"./images/{image_file_name}")
        response.status = 200
        return json.dumps(tweet)
    except Exception as ex:
        print(ex)
        return g._SEND(500, g.ERRORS[f"{language}_server_error"])
    finally:
        db.close()
