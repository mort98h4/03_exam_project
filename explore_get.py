from bottle import get, request, view
import g

##############################
@get("/explore")
@get("/<langauge>/explore")
@view("explore")
def _():
    is_fetch = True if request.headers.get('From-Fetch') else False
    return dict(tabs=g.TABS, title="Explore", is_fetch=is_fetch)