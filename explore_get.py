from bottle import get, view

##############################
@get("/explore")
@get("/<language>/explore")
@view("explore")
def _(language = "en"):
    return 