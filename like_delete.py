from bottle import delete, response
import g
import pymysql

##############################
@delete("/like/<tweet_id>/<user_id>")
@delete("<language>/like/<tweet_id>/<user_id>")
def _(language="en", tweet_id=None, user_id=None):
    try:
        if f"{language}_server_error" not in g.ERRORS : language = "en"
        tweet_id, error = g._IS_DIGIT(tweet_id, language)
        if error: return g._SEND(400, error)
        user_id, error = g._IS_DIGIT(user_id, language)
        if error: return g._SEND(400, error)
    except Exception as ex:
        print(ex)
        return g._SEND(500, g.ERRORS[f"{language}_server_error"])

    try:
        db_connect = pymysql.connect(**g.DB_CONFIG)
        db = db_connect.cursor()

        db.execute("DELETE FROM likes WHERE like_tweet_id = %s AND like_user_id = %s", (tweet_id, user_id))
        counter = db.rowcount
        if not counter: return g._SEND(204, "")

        db.execute("UPDATE tweets SET tweet_total_likes = tweet_total_likes - 1 WHERE tweet_id = %s", (tweet_id,))
        counter = db.rowcount
        if not counter: return g._SEND(204, "")

        db_connect.commit()
        response.status = 200
        return {"info": f"{user_id} has unliked {tweet_id}"}
    except Exception as ex:
        print(ex)
        return g._SEND(500, g.ERRORS[f"{language}_server_error"])
    finally:
        db.close()