import unittest
from valid_braces import *

class TestValidBraceCW(unittest.TestCase):
    def assert_valid(self,string):
        self.assertEqual(valid_braces(string), True, 'Expected "{0}" to be valid'.format(string))

    def assert_invalid(self,string):
        self.assertEqual(valid_braces(string), False, 'Expected "{0}" to be invalid'.format(string))

    def testoutput(self):
        self.assert_valid( "(asdasd)" )
        self.assert_invalid( "(}" )
        self.assert_valid( "[]" )
        self.assert_invalid("[(])")
        self.assert_valid( "{}" )
        self.assert_valid( "{}()[]" )
        self.assert_valid( "([{}])" )
        self.assert_invalid( "([}{])" )
        self.assert_valid( "{}({adsd}asd)[]asd" )
        self.assert_valid( "((das{{[dsa[]ds]das}}))" )
        self.assert_invalid( "(((({{" )
        self.assert_invalid( ")(}{][" )
        self.assert_invalid( "())({}}{()][][" )

if __name__ == '__main__':
    unittest.main()