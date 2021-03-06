from bottle import get, request, response
import g
import pymysql
import json

##############################
@get("/tweets/<user_id>/following/<offset>")
@get("<language>/tweets/<user_id>/following/<offset>/")
def _(user_id="", offset=None, language="en"):
    try:
        if f"{language}_server_error" not in g.ERRORS : language = "en"
        user_id, error = g._IS_DIGIT(user_id, language)
        if error: return g._SEND(400, error)
        offset, error = g._IS_DIGIT(offset, language)
        if error: return g._SEND(400, error)
    except Exception as ex:
        print(ex)
        return g._SEND(500, g.ERRORS[f"{language}_server_error"])

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
                JOIN follows ON tweets.tweet_user_id = follows.follows_user_id
                WHERE follows.follow_user_id = %s
                UNION 
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
                JOIN users 
                WHERE user_id = %s AND tweet_user_id = %s
                ORDER BY tweet_created_at DESC
                LIMIT %s,10
            """, (user_id, user_id, user_id, int(offset)))
        tweets = db.fetchall()
        counter = db.rowcount
        if not counter: return g._SEND(204, "")
        for tweet in tweets:
            tweet['tweet_created_at_date'] = g._DATE_STRING(int(tweet['tweet_created_at']))

        response_to_client = {"tweets":tweets, "liked_tweets":[], "follows":[], "user_id":user_id}
        db.execute("SELECT * FROM likes WHERE like_user_id = %s", (user_id,))
        liked_tweets = db.fetchall()
        for liked_tweet in liked_tweets:
            response_to_client['liked_tweets'].append(liked_tweet['like_tweet_id'])
        response_to_client['follows'] = g._GET_FOLLOWS_USER_IDS(user_id, language)

        response.status = 200
        return json.dumps(response_to_client)
    except Exception as ex:
        print(ex)
        return g._SEND(500, g.ERRORS[f"{language}_server_error"])
    finally:
        db.close()