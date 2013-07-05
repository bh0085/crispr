import unittest
import transaction

from pyramid import testing

from .models import Session


class TestMyView(unittest.TestCase):
    def setUp(self):
        pass
#        self.config = testing.setUp()
#        from sqlalchemy import create_engine
#        engine = create_engine('sqlite://')
#        from .models import (
#            Base,
#            MyModel,
#            )
#        Session.configure(bind=engine)
#        Base.metadata.create_all(engine)
#        with transaction.manager:
#            model = MyModel(name='one', value=55)
#            DBSession.add(model)

    def tearDown(self):
        pass
#        DBSession.remove()
#        testing.tearDown()

    def test_it(self):
        pass
#        from .views import my_view
#        request = testing.DummyRequest()
#        info = my_view(request)
#        self.assertEqual(info['one'].name, 'one')
#        self.assertEqual(info['project'], 'cfront')
