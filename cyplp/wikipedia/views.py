from pyramid.view import view_config
import requests

import datetime
import os
import urllib
import urllib2
import json

from smc.mw import MediaWiki

from mw_expression import MediaWikiExpression

@view_config(route_name='home', renderer='templates/mytemplate.pt')
def my_view(request):
    return {'project': 'cyplp.wikipedia'}

@view_config(route_name='search', renderer='templates/search.pt')
def search(request):
    query = request.GET.get('q')
    if query is None:
        return {}

    req = requests.get(request.registry.settings['couchdb.url']+'/_fti/_design/search/by_content?q='+query)

    tmp =  req.json()
    print tmp

    if req.status_code == 500:
        return {}

    return tmp

@view_config(route_name='article', renderer='templates/article.pt')
def article(request):

    url = unicode(request.registry.settings['couchdb.url']+'/'+urllib.quote(request.matchdict['article']))
    print url
    now = datetime.datetime.now()
    req = urllib2.urlopen(url)
    tmp = json.loads(req.read())
    print datetime.datetime.now() - now
    from chameleon import PageTemplateFile
    PageTemplateFile.expression_types['mw'] = MediaWikiExpression
    # print MediaWiki(tmp['content']).as_string()
    # tmp['request'] = request
    # print PageTemplateFile(os.path.join(os.path.dirname(__file__), 'templates/article.pt'))(**tmp)
    # print tmp['content'].upper()
    return {'_id': tmp['_id'], 'content': tmp['content']}
