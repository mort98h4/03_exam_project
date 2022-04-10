from bottle import get, request, view

##############################
@get("/")
@view("index")
def _():
    return 