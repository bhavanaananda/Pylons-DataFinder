from datafinder.tests import *

class TestRegisterSourceController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='register_source', action='index'))
        # Test response...
