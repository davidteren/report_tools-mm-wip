import unittest
import pandas as pd
import numpy as np
from io import StringIO
from report_analyzer import (
    load_data,
    filter_data,
    consolidate_item_data,
    format_boolean_columns
)

class TestReportAnalyzer(unittest.TestCase):
    def setUp(self):
        # Create a sample CSV data for testing
        csv_data = """Region,Store Code,Store Name,Store Brand,Item Code,Description,Unit Size,Price,Start Date,End Date,Language,SPM Code,Reused SPM,PB Available,Store Halal,Product Non-Halal
Region1,S1001,Store A,Brand X,I101,Item Description 1,500g,9.99,2025-01-01,2025-01-15,EN,SPM001,Yes,Yes,No,No
Region1,S1002,Store B,Brand X,I101,Item Description 1,500g,9.99,2025-01-01,2025-01-15,EN,SPM002,No,Yes,Yes,No
Region1,S1002,Store B,Brand X,I102,Item Description 2,300g,5.99,2025-01-01,2025-01-15,FR,SPM003,No,No,Yes,No
Region2,S2001,Store C,Brand Y,I101,Item Description 1,500g,10.99,2025-01-01,2025-01-15,EN,SPM004,No,Yes,No,Yes
Region2,S2001,Store C,Brand Y,I103,Item Description 3,1kg,15.99,2025-01-01,2025-01-15,ES,,No,No,No,Yes
"""
        self.test_df = pd.read_csv(StringIO(csv_data))
        
    def test_load_data(self):
        # Test with the StringIO instead of file to avoid file dependency
        df = load_data(StringIO(self.test_df.to_csv(index=False)))
        self.assertEqual(len(df), 5)
        self.assertIn('Region', df.columns)
        self.assertIn('Store Halal', df.columns)
        self.assertIn('Product Non-Halal', df.columns)
        
    def test_filter_data(self):
        # Test filtering by region
        filtered_df = filter_data(self.test_df, region='Region1')
        self.assertEqual(len(filtered_df), 3)
        self.assertTrue(all(filtered_df['Region'] == 'Region1'))
        
        # Test filtering by store code
        filtered_df = filter_data(self.test_df, store_code='S1002')
        self.assertEqual(len(filtered_df), 2)
        self.assertTrue(all(filtered_df['Store Code'] == 'S1002'))
        
        # Test filtering by halal store
        filtered_df = filter_data(self.test_df, store_halal=True)
        self.assertEqual(len(filtered_df), 3)
        self.assertTrue(all(filtered_df['Store Halal'] == 'Yes'))
        
        # Test filtering by PB availability
        filtered_df = filter_data(self.test_df, pb_available=True)
        self.assertEqual(len(filtered_df), 3)
        self.assertTrue(all(filtered_df['PB Available'] == 'Yes'))
        
        # Test combined filters
        filtered_df = filter_data(self.test_df, region='Region1', store_halal=True)
        self.assertEqual(len(filtered_df), 2)
        self.assertTrue(all(filtered_df['Region'] == 'Region1'))
        self.assertTrue(all(filtered_df['Store Halal'] == 'Yes'))
        
    def test_consolidate_item_data(self):
        # Test consolidation of item data
        consolidated_df = consolidate_item_data(self.test_df)
        
        # After consolidation, we should have unique items (identified by Item Code)
        # with lists of stores and other repeated data
        self.assertEqual(len(consolidated_df), 3)  # 3 unique item codes
        
        # Check that I101 has 3 stores
        item1_row = consolidated_df[consolidated_df['Item Code'] == 'I101'].iloc[0]
        self.assertEqual(len(item1_row['Stores']), 3)
        
        # Check that the description is consistent
        self.assertEqual(item1_row['Description'], 'Item Description 1')
        
    def test_format_boolean_columns(self):
        # Test that boolean columns are formatted correctly
        formatted_df = format_boolean_columns(self.test_df)
        
        # Check that Yes/No values are properly converted
        self.assertTrue(all(formatted_df['Store Halal'].isin([True, False])))
        self.assertTrue(all(formatted_df['Product Non-Halal'].isin([True, False])))
        self.assertTrue(all(formatted_df['PB Available'].isin([True, False])))
        self.assertTrue(all(formatted_df['Reused SPM'].isin([True, False])))

if __name__ == '__main__':
    unittest.main()
