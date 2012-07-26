
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
import urllib2
import base64
import urllib
from datafinder.lib.multipartform import MultiPartForm

class ListSourcesController(BaseController):
    def index(self):
        c.silo_name = ''
        c.ident = ''
        c.id =""
        c.q=""
        c.typ=""
        c.path =""
        ##c.source_infos=[["AA","TITLE AA","DATE INFO"],["BB","TITLE BB","DATE INFO"],["BB","TITLE BB","DATE INFO"]]
        c.user_logged_in_name=""
        c.src = ag.root
        
        srcurl = ag.root +'/silos'
        req = urllib2.Request(srcurl)
        USER = "admin"
        PASS = "test"
        auth = 'Basic ' + base64.urlsafe_b64encode("%s:%s" % (USER, PASS))
        req.add_header('Authorization', auth)
        req.add_header('Accept', 'application/JSON')
#        req.add_data(urllib.urlencode({'silo': silo, 
#                                       'title':title,
#                                       'description':description, 
#                                       'notes':notes, 
#                                       'administrators':administrators,
#                                       'managers':managers,
#                                       'users':users,
#                                       'disk_allocation':disk_allocation}))
#        print req.get_data()
        ans = urllib2.urlopen(req)
#        print
#        print 'SERVER RESPONSE:'
        c.sources =  json.loads(ans.read())
        print c.sources
        
        c.source_infos = {}
        for source in c.sources:
         
            srcurl = ag.root + '/' + source + '/states'
            req = urllib2.Request(srcurl)
            req.add_header('Authorization', auth)
            req.add_header('Accept', 'application/JSON')
#        req.add_data(urllib.urlencode({'silo': silo, 
#                                       'title':title,
#                                       'description':description, 
#                             show group_permission          'notes':notes, 
#                                       'administrators':administrators,
#                                       'managers':managers,
#                                       'users':users,
#                                       'disk_allocation':disk_allocation}))
            ans = urllib2.urlopen(req)
            state_info =  json.loads(ans.read())
#            print state_info
#            state_info = ag.granary.describe_silo(silo)
#            if 'title' in state_info and state_info['title']:
#                c.source_infos[source].append(state_info['title'])
#            else:
#                c.source_infos[source].append(len(state_info['datasets']))
            c.source_infos[source] = [source, len(state_info['datasets']), '']
#            c.source_infos[source].append('') #getSiloModifiedDate(silo)
        print "sourceinfos:"
        print c.source_infos
        return render('/list_of_sources.html')
