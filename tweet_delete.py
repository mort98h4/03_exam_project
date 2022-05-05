from bottle import delete, response
import g
import os
import pymysql

##############################
@delete("/tweet/<tweet_id>")
@delete("/<language>/tweet/<tweet_id>")
def _(language="en", tweet_id=""):
    try:
        if f"{language}_server_error" not in g.ERRORS : language = "en"
        tweet_id, error = g._IS_DIGIT(tweet_id, language)
        if error: return g._SEND(400, error)
    except Exception as ex:
        print(ex)
        return g._SEND(500, g.ERRORS[f"{language}_server_error"])

    try:
        db_connect = pymysql.connect(**g.DB_CONFIG)
        db = db_connect.cursor()

        db.execute("SELECT * FROM tweets WHERE tweet_id = %s", (tweet_id,))
        tweet = db.fetchone()
        counter = db.rowcount
        if not counter: return g._SEND(204, "")

        db.execute("DELETE FROM tweets WHERE tweet_id = %s", (tweet_id,))
        counter = db.rowcount
        if not counter: return g._SEND(204, "")
        if tweet['tweet_image'] != "": os.remove(f"./images/{tweet['tweet_image']}")

        db.execute("UPDATE users SET user_total_tweets = user_total_tweets - 1 WHERE user_id = %s", (tweet['tweet_user_id'],))
        counter = db.rowcount
        if not counter: return g._SEND(204, "")

        db.execute("DELETE from likes WHERE like_tweet_id = %s", (tweet_id,))
        counter = db.rowcount
        if not counter: return g._SEND(204, "")

        response.status = 200
        db_connect.commit()
        return {"info":"Tweet deleted"}
    except Exception as ex:
        print(ex)
        return g._SEND(500, g.ERRORS[f"{language}_server_error"])
    finally: 
        db.close()