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
from pylons import tmpl_context as c
log = logging.getLogger(__name__)
from pylons import app_globals as ag
from datafinder.model import meta, SourceInfo
from sqlalchemy.exc import IntegrityError
import smtplib
from email.mime.text import MIMEText


class ContributeController(BaseController):
    def index(self):
        c.silo_name = ''
        c.ident = ''
        c.id =""
        c.path =""
        c.user_logged_in_name=""
        c.q=""
        c.typ=""
        c.src = ag.root
        c.host = ag.host
        c.silo=""
        c.source = ""
        c.kw={}       
        c.activate = None
        c.message=None
        c.header = "create"
        c.kw={}
        return render('/contribute.html')
    
    def approve(self,source):
        c.silo_name = ''
        c.ident = ''
        c.id =""
        c.path =""
        c.user_logged_in_name=""
        c.q=""
        c.typ=""
        c.src = ag.root
        c.host = ag.host
        c.silo=""
        c.source = source
        c.message =None
        state_info = None       
        print "source requested: "
        print c.source 
        c.activate=""
        c.header = "approve"
        c.kw={}
        text = "Approval needed for the registered source: '" + source +"'"
        msg = MIMEText(text)
        msg['Subject'] = msg
        msg['From'] = "bhavana.ananda@bodleian.ox.ac.uk"
        msg['To'] = "bhavana.ananda@bodleian.ox.ac.uk"

        try:
            s_q= meta.Session.query(SourceInfo).filter(SourceInfo.silo == c.source).filter(SourceInfo.activate == False)  
            for src in s_q:
                c.kw = {'silo':src.silo, 
                        'title':src.title,                       
                        'description':src.description,
                        'notes':src.notes,
                        'administrators': src.administrators,
                        'managers':src.managers,
                        'users':src.users,
                        'disk_allocation':src.disk_allocation,
                        'activate':src.activate
                       }       
        except IntegrityError:
            meta.Session.rollback()
            return False     
        return render("/contribute.html")     