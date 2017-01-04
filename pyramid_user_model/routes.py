def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('user', '/users/{id:\d+}')
    # config.add_route('newuser', '/users/register')
    config.add_route('login', '/login')
    config.add_route('logout', '/logout')