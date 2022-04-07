from bottle import get, view

##############################
@get("/login")
@view("login")
def _():
    return