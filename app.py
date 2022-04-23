from bottle import default_app, error, get, view, run, static_file

##############################
@get("/app.css")
def _():
    return static_file("app.css", root=".")

##############################
@get("/scripts/<script>")
def _(script):
    return static_file(script, root="./scripts")

##############################
@get("/images/<image>")
def _(image):
    return static_file(image, root="./images", mimetype="image/*")

##############################
import index_get                # GET
import login_get                # GET
import home_get                 # GET
import logout_get               # GET
import explore_get              # GET
import profile_get              # GET
import tweet_get                # GET
import tweets_by_user_id_get    # GET

import signup_post              # POST
import login_post               # POST
import logout_post              # POST
import tweet_post               # POST
import follow_post              # POST
import like_post                # POST

import tweet_put                # PUT
import user_put                 # PUT

import tweet_delete             # DELETE
import follow_delete            # DELETE
import like_delete              # DELETE

##############################
@error(404)
@view("404")
def _(error):
  return

##############################
try:
    # Production
    import production
    application = default_app()
except:
    # Development
    run(host="127.0.0.1", port=3333, debug=True, reloader=True, server="paste")