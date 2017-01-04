import os
import sys
import transaction

from pyramid.paster import (
    get_appsettings,
    setup_logging,
)

from passlib.apps import custom_app_context as pwd_context

from pyramid.scripts.common import parse_vars

from ..models.meta import Base
from ..models import (
    get_engine,
    get_session_factory,
    get_tm_session,
)
from ..models import MyModel


def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri> [var=value]\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)


def main(argv=sys.argv):
    if len(argv) < 2:
        usage(argv)
    config_uri = argv[1]
    options = parse_vars(argv[2:])
    setup_logging(config_uri)
    settings = get_appsettings(config_uri, options=options)

    engine = get_engine(settings)
    Base.metadata.create_all(engine)

    session_factory = get_session_factory(engine)

    USERS = [
        {'username': 'The First Person',
         'password': pwd_context.hash('itsapassword'),
         'firstname': 'John',
         'lastname': 'Piglly',
         'email': 'jpigs@here.com',
         'food': 'tortillas'},
        {'username': 'The Second Person',
         'password': pwd_context.hash('verysecure'),
         'firstname': 'Barb',
         'lastname': 'Piglly',
         'email': 'bpigs@here.com',
         'food': 'tortellini'}
    ]

    with transaction.manager:
        dbsession = get_tm_session(session_factory, transaction.manager)

        for user in USERS:
            model = MyModel(username=user['username'],
                            password=user['password'],
                            firstname=user['firstname'],
                            lastname=user['lastname'],
                            email=user['email'],
                            food=user['food'])
            dbsession.add(model)
