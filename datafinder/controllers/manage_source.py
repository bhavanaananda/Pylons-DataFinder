
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
from pylons.decorators import rest
from datafinder.lib.base import BaseController, render
from pylons import tmpl_context as c
log = logging.getLogger(__name__)


class ManageSourceController(BaseController):
    @rest.restrict('GET')
    def index(self):
        c.ident = ''
        c.id =""
        c.path =""
        c.q=""
        c.typ=""
        c.user_logged_in_name=""


    @rest.restrict('GET')
    def managesource(self, source):
        c.silo_name = source
        c.ident = ''
        c.id =""
        c.q=""
        c.typ=""
        c.path =""
        c.user_logged_in_name=""
        return render('/manage_source.html')
