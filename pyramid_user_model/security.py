import os

from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.security import Allow, Authenticated
from pyramid_user_model.models import MyModel

from passlib.apps import custom_app_context as pwd_context


class NewRoot(object):

    def __init__(self, request):
        self.request = request

    __acl__ = [
        (Allow, Authenticated, 'valid_user'),
    ]


def check_credentials(request, username, password):
    """Return True if correct username and password, else False."""
    if username and password:
        query = request.dbsession.query(MyModel)
        user_profile = query.filter(MyModel.username == username).first()
        return pwd_context.verify(password, user_profile['password'])
    return False


def includeme(config):
    """Security-related configuration."""
    auth_secret = os.environ.get('AUTH_SECRET', 'itsaseekrit')
    authn_policy = AuthTktAuthenticationPolicy(
        secret=auth_secret,
        hashalg='sha512'
    )
    config.set_authentication_policy(authn_policy)
    authz_policy = ACLAuthorizationPolicy()
    config.set_authorization_policy(authz_policy)
    config.set_root_factory(NewRoot)
