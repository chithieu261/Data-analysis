from hw8 import *
import hw8, inspect
import unittest, json, numpy as np, pandas as pd, io
from compare_pandas import *
from contextlib import redirect_stdout

''' 
Auxiliary files needed:
    compare_pandas.py
    sm.pkl
The following files are needed by both hw8 and the test and
so are also necessary:
    trump_240129_519pm.json, trump_240130_1139am.json
    biden_240129_519pm.json, biden_240130_1139am.json
'''

class TestFns(unittest.TestCase):
    def test_get_sentiment(self):
        params = [
            [0.02888736263736263, 0.2792765678477078],
            [0.06876249872461995, 0.20514299052865126],
            [0.10101743233511665, 0.22910261384398592],
            [-0.006501710095460084, 0.21899473981970394],
            ]
        self.assertTrue(compare_lists(params[0], get_sentiment('trump_240129_519pm.json')))
        self.assertTrue(compare_lists(params[1], get_sentiment('trump_240130_1139am.json')))
        self.assertTrue(compare_lists(params[2], get_sentiment('biden_240129_519pm.json')))
        self.assertTrue(compare_lists(params[3], get_sentiment('biden_240130_1139am.json')))
   
    def test_get_ct_sentiment_frame(self):
        correct = pd.read_pickle('sm.pkl')
        self.assertTrue(compare_frames(correct, get_ct_sentiment_frame(), 0.005))
        text = inspect.getsource(get_ct_sentiment_frame)
        self.assertTrue('pkl' not in text)
   
def main():
    test = unittest.defaultTestLoader.loadTestsFromTestCase(TestFns)
    results = unittest.TextTestRunner().run(test)
    print('Correctness score = ', str((results.testsRun - len(results.errors) - len(results.failures)) / results.testsRun * 60) + ' / 60')
    hw8.main()
    
if __name__ == "__main__":
    main()