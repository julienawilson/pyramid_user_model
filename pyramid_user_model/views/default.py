from pyramid.response import Response
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError

from ..models import MyModel
import datetime
from pyramid.httpexceptions import HTTPFound

from learning_journal.security import check_credentials

from pyramid.security import remember, forget
from pyramid.session import check_csrf_token


@view_config(route_name='home', renderer='../templates/home.jinja2')
def home_view(request):
    """Render the home page."""
    return {}


@view_config(route_name='user',
             renderer='../templates/user_template.jinja2',
             permission='valid_user'
             )
def profile_view(request):
    """Render the User profile."""
    try:
        query = request.dbsession.query(MyModel)
        user = query.filter(MyModel.id == request.matchdict["id"]).first()
    except DBAPIError:
        return Response(db_err_msg, content_type='text/plain', status=500)
    return {'user': user}


@view_config(route_name='login',
             renderer='../templates/login.jinja2',
             )
def login_view(request):
    """Render the User profile."""
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        if check_credentials(request, username, password):
            auth_head = remember(request, username)
            return HTTPFound(
                request.route_url("home"),
                headers=auth_head)

    return {}


@view_config(route_name='logout')
def logout(request):
    """View to logout user."""
    auth_head = forget(request)
    return HTTPFound(request.route_url('home'), headers=auth_head)


db_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to run the "initialize_pyramid_user_model_db" script
    to initialize your database tables.  Check your virtual
    environment's "bin" directory for this script and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""
