from hw6 import *
import hw6, unittest, inspect
from compare_pandas import *

''' 
Auxiliary files needed:
    compare_pandas.py
    data_79_23.csv, data_2024.csv 
    hw5_frame.pkl (copied and renamed data_79_X.pkl from hw5), ice_20Y.pkl, fig1_frame.pkl, fig2_frame.pkl
'''

class TestFns(unittest.TestCase):
    def test_get_2024(self):
        self.assertTrue(compare_series(pd.read_pickle('ice_2024.pkl'), get_2024(), 0.005))
        text = inspect.getsource(get_2024)
        self.assertTrue('pkl' not in text)
   
    def test_extract_fig_1_frame(self):
        hw5_frame = pd.read_pickle('hw5_frame.pkl')
        f1f = extract_fig_1_frame(hw5_frame) 
        self.assertTrue(compare_frames(pd.read_pickle('fig1_frame.pkl'), f1f, 0.005))
        text = inspect.getsource(extract_fig_1_frame)
        self.assertTrue('pkl' not in text)
  
    def test_extract_fig_2_frame(self):
        hw5_frame = pd.read_pickle('hw5_frame.pkl')
        f2f = extract_fig_2_frame(hw5_frame) 
        self.assertTrue(compare_frames(pd.read_pickle('fig2_frame.pkl'), f2f, 0.005))
        text = inspect.getsource(extract_fig_2_frame)
        self.assertTrue('pkl' not in text)
   
def main():
    test = unittest.defaultTestLoader.loadTestsFromTestCase(TestFns)
    results = unittest.TextTestRunner().run(test)
    print('Correctness score = ', str((results.testsRun - len(results.errors) - len(results.failures)) / results.testsRun * 60) + ' / 60')
    hw6.main()
    
if __name__ == "__main__":
    main()