from bottle import get, request, view
import g

##############################
@get("/home")
@get("/<language>/home")
@view("home")
def _(language = "en"):
    is_fetch = True if request.headers.get('From-Fetch') else False
    return dict(tabs=g.TABS, title="Home", is_fetch=is_fetch)