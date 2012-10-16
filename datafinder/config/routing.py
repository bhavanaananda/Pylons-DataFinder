"""Routes configuration

The more specific and detailed routes should be defined first so they
may take precedent over the more generic routes. For more information
refer to the routes manual at http://routes.groovie.org/docs/
"""
from routes import Mapper

def make_map(config):
    """Create, configure and return the routes Mapper"""
    map = Mapper(directory=config['pylons.paths']['controllers'],
                 always_scan=config['debug'])
    map.minimization = False
    map.explicit = False

    # The ErrorController route (handles 404/500 error pages); it should
    # likely stay at the top, ensuring it can always be resolved
    map.connect('/error/{action}', controller='error')
    map.connect('/error/{action}/{id}', controller='error')

    # CUSTOM ROUTES HERE

    map.redirect('/*(url)/', '/{url}',
             _redirect_code='301 Moved Permanently')

    
    map.connect('/home', controller='home', action='index')
    map.connect("/login", controller='account', action='login')
    map.connect('/cookies', controller='cookies', action='index')
    map.connect('/about', controller='about', action='index')
    map.connect('/list_sources', controller='list_sources', action='index')
    map.connect('/contribute', controller='contribute', action='index')    
    map.connect('/create_source', controller='create_source', action='index')
    map.connect('/{source}/approve_source', controller='create_source', action='approve')
    map.connect('/admin/save_source', controller='admin', action='savesource')
    map.connect('/admin/register_source', controller='admin', action='registersource')
    map.connect('/admin', controller='admin', action='index')
    map.connect('/{source}/admin', controller='admin', action='sourceinfo')
    ##map.connect('/manage_source', controller='manage_source', action='index')
    map.connect('/manage_source/{source}', controller='manage_source', action='managesource')
##    map.connect('/search', controller='search', action='index')
##    map.redirect('/search/{action}', 'http://192.168.2.211/search/{action}')
    map.connect('/{controller}/{action}')
    map.connect('/{controller}/{action}/{id}')
    return map
