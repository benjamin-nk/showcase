import unittest
from linear_regression import *

class TestOLSRegress(unittest.TestCase):
    def test_output(self):
        self.assertEqual(regressionLine([25,30,35,40,45,50], [78,70,65,58,48,42]), (114.381, -1.4457))
        self.assertEqual(regressionLine([56,42,72,36,63,47,55,49,38,42,68,60], [147,125,160,118,149,128,150,145,115,140,152,155]), (80.7777, 1.138))
        # Yt Ex:
        self.assertAlmostEqual(sum(regressionLine([17,13,12,15,16,14,16,16,18,19], [94,73,59,80,93,85,66,79,77,91])), sum((30.123, 3.178)),1)

if __name__ == '__main__':
    unittest.main()