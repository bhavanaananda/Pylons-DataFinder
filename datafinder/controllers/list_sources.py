
"""
Copyright (c) 2012 University of Oxford

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, --INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

import logging, json
from datafinder.lib.base import BaseController, render
from pylons import tmpl_context as c
log = logging.getLogger(__name__)
from pylons import app_globals as ag
from datafinder.lib.HTTP_request import HTTPRequest
from datafinder.model import meta, SourceInfo
from sqlalchemy.exc import IntegrityError

class ListSourcesController(BaseController):
    def index(self):
        c.silo_name = ''
        c.ident = ''
        c.id =""
        c.q=""
        c.typ=""
        c.path =""
        c.user_logged_in_name=""
        c.src = ag.root
        c.host = ag.host
        user_name = 'admin'
        password = 'test'
        datastore = HTTPRequest(endpointhost=c.host)
        datastore.setRequestUserPass(endpointuser=user_name, endpointpass=password)

        (resp, respdata) = datastore.doHTTP_GET(resource="/silos", expect_type="application/JSON")
        c.sources =  json.loads(respdata)
        print c.sources
        
        c.source_infos = {}
        for source in c.sources:
            (resp, respdata) = datastore.doHTTP_GET(resource='/' + source + '/states', expect_type="application/JSON")
            state_info =  json.loads(respdata)
            c.source_infos[source] = [source, len(state_info['datasets'])]
        ##print "sourceinfos:"
        ##print c.source_infos
        
        c.unregistered_sources = []
        
        
        try:
            s_q= meta.Session.query(SourceInfo.silo)
            for source in s_q:
                c.unregistered_sources.append(source.silo)
            print "Unregistered sources"
            print c.unregistered_sources
        except IntegrityError:
            meta.Session.rollback()
            return False
        return render('/list_of_sources.html')
