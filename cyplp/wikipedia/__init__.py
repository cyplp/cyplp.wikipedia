from pyramid.config import Configurator

from pyramid.threadlocal import get_current_registry


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)

    config.include('pyramid_chameleon')
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('article', '/wiki/{article}')

    config.add_route('search', '/search')

    get_current_registry().settings = settings

    config.scan()
    return config.make_wsgi_app()
