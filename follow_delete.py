from bottle import delete, response
import g
import pymysql

##############################
@delete("/follow/<follow_user_id>/<follows_user_id>")
@delete("<language>/follow/<follow_user_id>/<follows_user_id>")
def _(language="en", follow_user_id=None, follows_user_id=None):
    try:
        if f"{language}_server_error" not in g.ERRORS : language = "en"
        follow_user_id, error = g._IS_DIGIT(follow_user_id, language)
        if error: return g._SEND(400, error)
        follows_user_id, error = g._IS_DIGIT(follows_user_id, language)
        if error: return g._SEND(400, error)
    except Exception as ex:
        print(ex)
        return g._SEND(500, g.ERRORS[f"{language}_server_error"])

    try:
        db_connect = pymysql.connect(**g.DB_CONFIG)
        db = db_connect.cursor()

        db.execute("DELETE FROM follows WHERE follow_user_id = %s AND follows_user_id = %s", (follow_user_id, follows_user_id))
        counter = db.rowcount
        if not counter: return g._SEND(204, "")

        db.execute("UPDATE users SET user_total_follows = user_total_follows - 1 WHERE user_id = %s", (follow_user_id,))
        counter = db.rowcount
        if not counter: return g._SEND(204, "")

        db.execute("UPDATE users SET user_total_followers = user_total_followers - 1 WHERE user_id = %s", (follows_user_id,))
        counter = db.rowcount
        if not counter: return g._SEND(204, "")

        db_connect.commit()
        response.status = 200
        return {"info": f"{follow_user_id} has unfollowed {follows_user_id}"}
    except Exception as ex:
        print(ex)
        return g._SEND(500, g.ERRORS[f"{language}_server_error"])
    finally:
        db.close()