from hw5 import *
import hw5
import unittest, json, pandas as pd, os, numpy as np, inspect
from compare_pandas import *
from compare_files import compare_files

''' 
Auxiliary files needed:
compare_pandas.py, compare_files.py
N_seaice_extent_daily_v3.0.csv
raw_data.pkl, clean_data.pkl, data_79_22.pkl, data_2023.pkl
columns.json
'''

class TestFns(unittest.TestCase):
    def test_get_data(self):
        ts_correct = pd.read_pickle('raw_data.pkl')
        self.assertTrue(compare_series(ts_correct, get_data(), 0.001, dtype=True))
        text = inspect.getsource(get_data)
        self.assertTrue('pkl' not in text)

    def test_clean_data(self):
        ts_correct = pd.read_pickle('clean_data.pkl')
        raw = pd.read_pickle('raw_data.pkl')
        better_be_none = clean_data(raw)
        self.assertTrue(compare_series(ts_correct, raw, 0.001, dtype=True))
        self.assertIsNone(better_be_none)
        text = inspect.getsource(clean_data)
        self.assertTrue('pkl' not in text)
   
    def test_get_column_labels(self):
        with open('columns.json') as fp:
            correct = json.load(fp) 
        self.assertEqual(correct, get_column_labels())
        
    def test_extract_df(self):
        ts_correct = pd.read_pickle('clean_data.pkl')
        df_correct = pd.read_pickle('data_79_23.pkl')
        self.assertTrue(compare_frames(df_correct, extract_df(ts_correct), 0.001))
        text = inspect.getsource(extract_df)
        self.assertTrue('pkl' not in text)
        
    def test_extract_2024(self):
        ts_clean_correct = pd.read_pickle('clean_data.pkl')
        ts_correct = pd.read_pickle('data_2024.pkl')
        ts = extract_2024(ts_clean_correct)
        self.assertTrue(compare_series(ts_correct, ts, 0.001, dtype=True))
        text = inspect.getsource(extract_2024)
        self.assertTrue('pkl' not in text)
        
    def test_main(self):
        if os.path.exists('data_79_23.csv'):
            os.remove('data_79_23.csv')
        if os.path.exists('data_2024.csv'):
            os.remove('data_2024.csv')
        hw5.main()
        # get rid of the apply F18 - the pkl is now float
        df_correct = pd.read_pickle('data_79_23.pkl')
        df = pd.read_csv('data_79_23.csv', index_col=0)
        self.assertTrue(compare_frames(df_correct, df, 0.001, dtype=True))
        ts_correct = pd.read_pickle('data_2024.pkl')
        # this actually creates a weird Series with index.name == 0.
        # could assign to None if I cared.
        df2 = pd.read_csv('data_2024.csv', header=None, parse_dates=True) 
        ts = pd.Series(df2.iloc[:, 1].values, df2.iloc[:, 0].values)
        self.assertTrue(compare_series(ts_correct, ts, 0.001, dtype=True))
        text = inspect.getsource(hw5.main)
        self.assertTrue('pkl' not in text)
       
def main():
    test = unittest.defaultTestLoader.loadTestsFromTestCase(TestFns)
    results = unittest.TextTestRunner().run(test)
    print('Correctness score = ', str((results.testsRun - len(results.errors) - len(results.failures)) / results.testsRun * 100) + ' / 100')
    
if __name__ == "__main__":
    main()