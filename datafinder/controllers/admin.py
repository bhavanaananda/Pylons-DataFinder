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

import logging, json
from datafinder.lib.base import BaseController, render
from pylons import request, response, url
from pylons.controllers.util import abort, redirect
from pylons import tmpl_context as c
log = logging.getLogger(__name__)
import urllib2
import base64
import urllib
from sqlalchemy.exc import IntegrityError
from datafinder.lib.multipartform import MultiPartForm
from pylons import app_globals as ag
from datafinder.lib.HTTP_request import HTTPRequest
from datafinder.lib import SparqlQueryTestCase
from datafinder.lib.auth_entry import add_user, update_user, list_usernames, list_user_groups
from datafinder.lib.conneg import MimeType as MT, parse as conneg_parse
from datafinder.model import meta, SourceInfo
from sqlalchemy.exc import IntegrityError
from sqlalchemy import orm

class AdminController(BaseController):
    def index(self):
        c.silo_name = ''
        c.ident = ''
        c.id =""
        c.path =""
        c.user_logged_in_name=""
        c.q=""
        c.typ=""
        c.host=ag.host
        print "endpointhost"
        print c.host
        srcurl = ag.root +'/admin'
        silo = request.params.get('silo', "")
        title = request.params.get('title', "")
        description = request.params.get('description', "")
        notes = request.params.get('notes', "")
        administrators = request.params.get('administrators', "")
        managers = request.params.get('managers', "")
        users = request.params.get('users', "")
        disk_allocation = request.params.get('disk_allocation', "")

        user_name = 'admin'
        password = 'test'
        datastore = HTTPRequest(endpointhost=c.host)
        
        datastore.setRequestUserPass(endpointuser=user_name, endpointpass=password)
        fields = \
            [ ("silo", silo),
              ("title", title),
              ("description", description),
              ("notes", notes),
              ("administrators", administrators),
              ("managers", managers),
              ("users", users),
              ("disk_allocation", disk_allocation)
            ]
        print fields
        files =[]
        (reqtype, reqdata) = SparqlQueryTestCase.encode_multipart_formdata(fields, files)
        
        (resp,respdata) = datastore.doHTTP_POST(reqdata, reqtype, resource="/admin", expect_type="application/JSON")
        print 'respdata', respdata
        print 'msg', resp.msg
        print 'reason', resp.reason
        print 'status',resp.status
        print resp.read()
##            print "response data for update metadata"
        if  resp.status== 204 or resp.status==201:
            c.message = "Source successfully created."
            
            #Modify the source entry in the sqllite database in the data finder. Change activate = True.
            try:
                s_q= meta.Session.query(SourceInfo).filter(SourceInfo.silo == silo)
                s_q.one()
                s_q.update({
                               'title':title,
                               'description':description,
                               'notes':notes,
                               'administrators':administrators,
                               'managers':managers,
                               'users':users,
                               'disk_allocation':disk_allocation,
                               'activate':True
                            })     
                meta.Session.commit()
            except orm.exc.NoResultFound:
                sourceinfo.activate =  True
                meta.Session.add(sourceinfo)
                meta.Session.commit()
                pass
            except IntegrityError:
                #log.error('Error adding user %s'%user_details['username'])
                #print traceback.format_exc()
                meta.Session.rollback()
                return False
            return redirect(url(controller='list_sources', action='index')) 
        else:
            c.message = "Source could not be successfully activated"
            c.message = c.message + " status: " + repr(resp.status) + " " + resp.reason
            c.kw = {    'silo':silo, 
                        'title':title,                       
                        'description':description,
                        'notes':notes,
                        'administrators': administrators,
                        'managers':managers,
                        'users':users,
                        'disk_allocation':disk_allocation
                       }
            c.header="approve"
            c.activate=None    
            return render("/create_new_source.html")    
#        req = urllib2.Request(srcurl)
#        USER = "admin"
#        PASS = "test"
#        auth = 'Basic ' + base64.urlsafe_b64encode("%s:%s" % (USER, PASS))
#        req.add_header('Authorization', auth)
#        req.add_header('Accept', 'application/JSON')
#        req.add_data(urllib.urlencode({'silo': silo, 
#                                       'title':title,
#                                       'description':description, 
#                                       'notes':notes, 
#                                       'administrators':administrators,
#                                       'managers':managers,
#                                       'users':users,
#                                       'disk_allocation':disk_allocation}))
#        print req.get_data()
#        ans = urllib2.urlopen(req)
#        print
#        print 'SERVER RESPONSE:'
#        print ans.read()

    
    def savesource(self):
        c.silo_name = ''
        c.ident = ''
        c.id =""
        c.path =""
        c.user_logged_in_name=""
        c.q=""
        c.typ=""
        c.host=ag.host
        sourceinfo= SourceInfo()
        c.message= None
        #srcurl = ag.root +'/admin'
        sourceinfo.silo = request.params.get('silo', "")
        sourceinfo.title = request.params.get('title', "")
        sourceinfo.description = request.params.get('description', "")
        sourceinfo.notes = request.params.get('notes', "")
        sourceinfo.administrators = request.params.get('administrators', "")
        sourceinfo.managers = request.params.get('managers', "")
        sourceinfo.users = request.params.get('users', "")
        sourceinfo.disk_allocation = request.params.get('disk_allocation', "")
        
        try:
            s_q= meta.Session.query(SourceInfo).filter(SourceInfo.silo == sourceinfo.silo)
            s_q.one()
            s_q.update({
                           'title':sourceinfo.title,
                           'description':sourceinfo.description,
                           'notes':sourceinfo.notes,
                           'administrators': sourceinfo.administrators,
                           'managers':sourceinfo.managers,
                           'users':sourceinfo.users,
                           'disk_allocation':sourceinfo.disk_allocation,
                           'activate':False
                        })     
            meta.Session.commit()
        except orm.exc.NoResultFound:
            sourceinfo.activate =  False
            meta.Session.add(sourceinfo)
            meta.Session.commit()
            pass
        except IntegrityError:
            #log.error('Error adding user %s'%user_details['username'])
            #print traceback.format_exc()
            meta.Session.rollback()
            return False


#        user_name = 'admin'
#        password = 'test'
#        datastore = HTTPRequest(endpointhost=c.host)
#        datastore.setRequestUserPass(endpointuser=user_name, endpointpass=password)

#        fields = \
#            [ ("silo", silo),
#              ("title", title),
#              ("description", description),
#              ("notes", notes),
#              ("administrators", administrators),
#              ("managers", managers),
#              ("uers", users),
#              ("disk_allocation", disk_allocation)
#            ]
#        files =[]
#        (reqtype, reqdata) = SparqlQueryTestCase.encode_multipart_formdata(fields, files)
#        (resp,respdata) = datastore.doHTTP_POST(
#            reqdata, reqtype, resource="/admin")
      

        return redirect(url(controller='list_sources', action='index')) 
  
    def registersource(self):
        c.silo_name = ''
        c.ident = ''
        c.id =""
        c.path =""
        c.user_logged_in_name=""
        c.q=""
        c.typ=""
        c.host=ag.host
        sourceinfo= SourceInfo()
        c.message=None
        #srcurl = ag.root +'/admin'
        sourceinfo.silo = request.params.get('silo', "")
        sourceinfo.title = request.params.get('title', "")
        sourceinfo.description = request.params.get('description', "")
        sourceinfo.notes = request.params.get('notes', "")
        sourceinfo.administrators = request.params.get('administrators', "")
        sourceinfo.managers = request.params.get('managers', "")
        sourceinfo.users = request.params.get('users', "")
        sourceinfo.disk_allocation = request.params.get('disk_allocation', "")
        
        try:
            s_q= meta.Session.query(SourceInfo).filter(SourceInfo.silo == sourceinfo.silo)
            s_q.one()
            c.message = "Source with the chosen name already exists. Choose another"
            c.kw = {'silo':sourceinfo.silo, 
                        'title':sourceinfo.title,                       
                        'description':sourceinfo.description,
                        'notes':sourceinfo.notes,
                        'users':sourceinfo.users,
                        'disk_allocation':sourceinfo.disk_allocation
                       }
            c.header="create"
            c.activate=None    
            return render("/create_new_source.html")    
        except orm.exc.NoResultFound:
            sourceinfo.activate =  False
            meta.Session.add(sourceinfo)
            meta.Session.commit()
            pass
        except IntegrityError:
            #log.error('Error adding user %s'%user_details['username'])
            #print traceback.format_exc()
            meta.Session.rollback()
            return False

        return redirect(url(controller='list_sources', action='index'))   
    
#    @rest.restrict('GET', 'POST', 'DELETE')
    def sourceinfo(self, source):
        c.silo_name = ''
        c.ident = ''
        c.id =""
        c.path =""
        c.user_logged_in_name=""
        c.q=""
        c.typ=""
        c.src = ag.root
#        if not request.environ.get('repoze.who.identity'):
#            abort(401, "Not Authorised")
#        if not ag.granary.issilo(silo):
#            abort(404)
#        ident = request.environ.get('repoze.who.identity')
#        c.ident = ident
#        c.silo = silo
#        silos = ag.authz(ident, permission=['administrator', 'manager'])
#        if not silo in silos:
#            abort(403, "Do not have administrator or manager credentials for silo %s"%silo)
#        user_groups = list_user_groups(ident['user'].user_name)
#        if ('*', 'administrator') in user_groups:
#            #User is super user
#            c.roles = ["admin", "manager", "user"]
#        elif (silo, 'administrator') in user_groups:
#            c.roles = ["admin", "manager", "user"]
#        elif (silo, 'manager') in user_groups:
#            c.roles = ["manager", "user"]
#        else:
#            abort(403, "Do not have administrator or manager credentials for silo %s"%silo)
        http_method = request.environ['REQUEST_METHOD']
        ## hardcoded for now
        c.roles = ["admin", "manager", "user"]
        ##c.kw = ag.granary.describe_silo(source)
        c.host = ag.host
        c.silo=""
        
        
        user_name = 'admin'
        password = 'test'
        datastore = HTTPRequest(endpointhost=c.host)
        datastore.setRequestUserPass(endpointuser=user_name, endpointpass=password)
        c.source = source
        c.message =""
        state_info = None     
        print "source requested: "
        print c.source 
        c.kw={}
#        try:
#            c.kw = {    'silo':src.silo, 
#                        'title':src.title,                       
#                        'description':src.description,
#                        'notes':src.notes,
#                        'users':src.users,
#                        'disk_allocation':src.disk_allocation,
#                        'activate':src.activate
#                    }    
#            s_q= meta.Session.query(SourceInfo).filter(SourceInfo.silo == c.source).filter(SourceInfo.activate == False)  
#            s_q.one()
#            return render("/admin_sourceview.html") 
#        except orm.exc.NoResultFound:
#            sourceinfo.activate =  False
#            meta.Session.add(sourceinfo)
#            meta.Session.commit()
#            pass      
#        except IntegrityError:
#            meta.Session.rollback()
#            return False     
            
            ## If the source is not activated only then get the source information from the registered information area
        (resp, respdata) = datastore.doHTTP_GET(resource='/' + c.source + '/states', expect_type="application/JSON")
        state_info =  json.loads(respdata)       
        ##print json.loads(respdata)
        c.kw=state_info
        
        print "http_method = "
        print http_method
        if http_method == "GET":
            return render("/admin_sourceinfo.html")
        elif http_method == "POST":
            ##silo = request.params.get('silo', None)
            title = request.params.get('title', '')
            description = request.params.get('description', '')
            notes = request.params.get('notes', '')
            administrators = request.params.get('administrators', '')
            managers = request.params.get('managers', '')
            users = request.params.get('users', '')
            disk_allocation = request.params.get('disk_allocation', '')
            fields = \
                [ ("silo", source),
                  ("title", title),
                  ("description", description),
                  ("notes", notes),
                  ("administrators", administrators),
                  ("managers", managers),
                  ("users", users),
                  ("disk_allocation", disk_allocation)
                ]
            print fields
            files =[]
            (reqtype, reqdata) = SparqlQueryTestCase.encode_multipart_formdata(fields, files)
            (resp,respdata) = datastore.doHTTP_POST(reqdata, reqtype, resource='/' + source + "/admin", expect_type="application/JSON")
            resource ='/' + source + "/admin"
            print 'respdata', respdata
            print 'msg', resp.msg
            print 'reason', resp.reason
            print 'status',resp.status
            print resp.read()
##            print "response data for update metadata"
            if  resp.status== 204:
                c.message = "Metadata updated"
                return render("/admin_sourceinfo.html")
            else:
                abort(resp.status, respdata )
                
        elif http_method == "DELETE":
            ##fields = [("silo", source)]
            ##print fields
            ##files =[]
            (reqtype, reqdata) = SparqlQueryTestCase.encode_multipart_formdata(fields, files)
            ##(resp,respdata) = datastore.doHTTP_DELETE(reqdata, reqtype, resource='/' + source + "/admin", expect_type="application/JSON")
          
            (resp,respdata) = datastore.doHTTP_DELETE(resource='/' + source + "/admin")
            resource ='/' + source + "/admin"
            print resp.read()
 
            print "Response Status = "
            print resp.status 

            if  resp.status== 200:
                #Modify the source entry in the sqllite database in the data finder. Change activate = False.
                try:
                    s_q= meta.Session.query(SourceInfo).filter(SourceInfo.silo == source)
                    s_q.one()
                    s_q.update({
                                   'title':title,
                                   'description':description,
                                   'notes':notes,
                                   'administrators':administrators,
                                   'managers':managers,
                                   'users':users,
                                   'disk_allocation':disk_allocation,
                                   'activate':False
                                })     
                    meta.Session.commit()
                except orm.exc.NoResultFound:
                    sourceinfo.activate =  False
                    meta.Session.add(sourceinfo)
                    meta.Session.commit()
                    pass
                except IntegrityError:
                    #log.error('Error adding user %s'%user_details['username'])
                    #print traceback.format_exc()
                    meta.Session.rollback()
                    return False
                c.message = "Metadata deleted"
                return True 
            else:
                print "Failure"
                abort(resp.status, respdata )
