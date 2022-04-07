from bottle import default_app, get, view, run, static_file

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
import home_get             # GET
import login_get            # GET

import signup_post          # POST
import login_post           # POST

##############################
try:
    # Production
    import production
    application = default_app()
except:
    # Development
    run(host="127.0.0.1", port=3333, debug=True, reloader=True, server="paste")