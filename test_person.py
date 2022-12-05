import unittest
from person import Person

class TestPerson(unittest.TestCase):
    def setUp(self):
        self.p1 = Person('amir', 'big')
        self.p2 = Person('joan', 'doe')

    @classmethod
    def setUpClass(self):
        print('setUpClass')

    @classmethod
    def tearDownClass(self):
        print('tearDownClass')

    def tearDown(self):
        print('done tearDown..')
        
    def test_fullname(self):
        self.assertEqual(self.p1.fullname(),'amir big')
        self.assertEqual(self.p2.fullname(),'joan doe')

    def test_email(self):
        self.assertEqual(self.p1.email(), 'amirbig@email.com')
        self.assertEqual(self.p2.email(), 'joandoe@email.com')

if __name__ == '__main__':
    unittest.main()