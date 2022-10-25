import unittest
from race_statistics import stat

class TestComputedDescriptives(unittest.TestCase):
    def test_output(self):
        self.assertEqual(stat("01|15|59, 1|47|16, 01|17|20, 1|32|34, 2|17|17"),"Range: 01|01|18 Average: 01|38|05 Median: 01|32|34")

# tutorial: https://www.youtube.com/watch?v=Oz0Z2tNuvDw 
#
# 1. Test from within the file (uncomment):
# if __name__ == '__main__':
#     unittest.main()
#
# 2. Test from the terminal:
#  2.1 First launch python from the directory/ cd to the directory 'ex_race_statistics'
#   2.2 Enter: python -m unittest test_race_statistics.py

#arrange/act/assert
#F.I.R.S.T
#Fast
#Independent [of other unit tests]
#Repeatable [same result across repititions -> test-retest reliability]
#Self-validation [should be self-validating, tell me if a test has been passed without having to check each one]
#Timely [Written at the right time and right place during development]