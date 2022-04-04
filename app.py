from bottle import get, view, run, static_file

##############################
@get("/app.css")
def _():
    return static_file("app.css", root=".")

##############################
@get("/images/<image>")
def _(image):
    return static_file(image, root="./images", mimetype="image/*")

##############################
@get("/")
@view("index")
def _():
    return

##############################
try:
    # Production
    import production
    application = default_app()
except:
    # Development
    run(host="127.0.0.1", port=3333, debug=True, reloader=True, server="paste")