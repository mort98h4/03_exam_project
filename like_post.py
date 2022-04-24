from bottle import post, response, request
import g
import pymysql

##############################
@post("/like/<tweet_id>/<user_id>")
@post("<language>/like/<tweet_id>/<user_id>")
def _(language="en", tweet_id="", user_id=""):
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
        like = (
            tweet_id,
            user_id
        )

        db_connect = pymysql.connect(**g.DB_CONFIG)
        db = db_connect.cursor()
        query = """
                INSERT INTO likes
                (
                    like_tweet_id,
                    like_user_id
                )
                VALUES(%s, %s)
        """
        db.execute(query, like)
        counter = db.rowcount
        if not counter: return g._SEND(204, "")

        db.execute("UPDATE tweets SET tweet_total_likes = tweet_total_likes + 1 WHERE tweet_id = %s", (tweet_id,))
        counter = db.rowcount
        if not counter: return g._SEND(204, "")

        db_connect.commit()
        response.status = 201
        return {"like_tweet_id": tweet_id, "like_user_id": user_id}
    except Exception as ex: 
        print(ex)
        return g._SEND(500, g.ERRORS[f"{language}_server_error"])

    finally:
        db.close()