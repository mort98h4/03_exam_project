from bottle import post, response, request
import g
import pymysql

##############################
@post("/follow/<follow_user_id>/<follows_user_id>")
@post("/<language>/follow/<follow_user_id>/<follows_user_id>")
def _(language="en", follow_user_id=None, follows_user_id=None):
    if f"{language}_server_error" not in g.ERRORS : language = "en"

    try:
        follow = (
            follow_user_id,
            follows_user_id
        )

        db_connect = pymysql.connect(**g.DB_CONFIG)
        db = db_connect.cursor()
        query = """
                INSERT INTO follows
                (
                    follow_user_id,
                    follows_user_id
                )
                VALUES(%s, %s)
        """
        db.execute(query, follow)
        db_connect.commit()
        response.status = 201

        return {"follow_user_id": follow_user_id, "follows_user_id": follows_user_id}
    except Exception as ex: 
        print(ex)
        return g._SEND(500, g.ERRORS[f"{language}_server_error"])

    finally:
        db.close()