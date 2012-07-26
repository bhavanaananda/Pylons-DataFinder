# -*- coding: utf-8 -*-
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

import logging

from datafinder.lib.base import BaseController, render
from pylons import request, response, url
from pylons.controllers.util import redirect
from pylons import tmpl_context as c
log = logging.getLogger(__name__)
import urllib2
import base64
import urllib
from datafinder.lib.multipartform import MultiPartForm
from pylons import app_globals as ag

#silo
#title
#description
#notes
#administrators
#managers
#users
#disk_allocation
class AdminController(BaseController):
    def index(self):
        c.silo_name = ''
        c.ident = ''
        c.id =""
        c.path =""
        c.user_logged_in_name=""
        c.q=""
        c.typ=""
        srcurl = ag.root +'/admin'
        silo = request.params.get('silo', None)
        title = request.params.get('title', None)
        description = request.params.get('description', None)
        notes = request.params.get('notes', None)
        administrators = request.params.get('administrators', None)
        managers = request.params.get('managers', None)
        users = request.params.get('users', None)
        disk_allocation = request.params.get('disk_allocation', None)
        
        req = urllib2.Request(srcurl)
        USER = "admin"
        PASS = "test"
        auth = 'Basic ' + base64.urlsafe_b64encode("%s:%s" % (USER, PASS))
        req.add_header('Authorization', auth)
        req.add_header('Accept', 'application/JSON')
        req.add_data(urllib.urlencode({'silo': silo, 
                                       'title':title,
                                       'description':description, 
                                       'notes':notes, 
                                       'administrators':administrators,
                                       'managers':managers,
                                       'users':users,
                                       'disk_allocation':disk_allocation}))
        print req.get_data()
        ans = urllib2.urlopen(req)
        print
        print 'SERVER RESPONSE:'
        print ans.read()

#        print "silo%s"%(silo)
#        print "title%s"%(title)
#        print "description%s"%(description)
#        print "notes%s"%(notes)
#        print "administrators%s"%(administrators)
#        print "managers%s"%(managers)
#        print "users%s"%(users)
#        print "disk_allocation%s"%(disk_allocation)
#        return render('/list_sources.html')
        return redirect(url(controller='list_sources', action='index')) 