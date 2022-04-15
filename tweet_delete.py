from bottle import delete, response
import g
import os
import pymysql

##############################
@delete("/tweet/<id>")
@delete("/<language>/tweet/<id>")
def _(language="en", id=""):
    if f"{language}_server_error" not in g.ERRORS : language = "en"
    try:
        if not id:
            errors = {
                "en_error": "tweet_id is missing",
                "da_error": "tweet_id mangler."
            }
            return g._SEND(400, errors[f"{langauge}_error"])
    except Exception as ex:
        print(ex)
        return g._SEND(500, g.ERRORS[f"{language}_server_error"])

    try:
        db_connect = pymysql.connect(**g.DB_CONFIG)
        db = db_connect.cursor()
        db.execute("SELECT tweets.tweet_image FROM tweets WHERE tweet_id = %s", (id,))
        tweet_image = db.fetchone()
        print("#"*30)
        print(tweet_image)
        db.execute("DELETE FROM tweets WHERE tweet_id = %s", (id,))
        counter = db.rowcount
        db_connect.commit()
        if not counter: return g._SEND(204, "")
        if tweet_image['tweet_image'] != "": os.remove(f"./images/{tweet_image['tweet_image']}")
        response.status = 200
        return {"info":"Tweet deleted"}
    except Exception as ex:
        print(ex)
        return g._SEND(500, g.ERRORS[f"{language}_server_error"])
    finally: 
        db.close()