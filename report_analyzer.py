import pandas as pd
import numpy as np
import os
from typing import Dict, List, Optional, Union, Any

def load_data(file_path: Union[str, Any]) -> pd.DataFrame:
    """
    Load CSV data from the given file path or file object
    
    Args:
        file_path: Path to the CSV file or file object
        
    Returns:
        pandas DataFrame with the report data
    """
    try:
        # Check if file_path is a string (path) or file-like object
        if isinstance(file_path, str):
            # It's a file path
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"File not found: {file_path}")
            df = pd.read_csv(file_path)
        else:
            # It's a file-like object (e.g., from file_uploader)
            # Reset file pointer to beginning to ensure we read from the start
            try:
                file_path.seek(0)
            except:
                pass  # Not all file-like objects support seek
            df = pd.read_csv(file_path)
        
        # Validate that required columns exist
        required_columns = [
            "Region", "Store Code", "Store Name", "Store Brand", 
            "Item Code", "Description", "Unit Size", "Price", 
            "Start Date", "End Date", "Language", "SPM Code"
        ]
        
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            raise ValueError(f"Missing required columns: {', '.join(missing_columns)}")
            
        return df
    except pd.errors.EmptyDataError:
        raise ValueError("The file is empty.")
    except pd.errors.ParserError:
        raise ValueError("Error parsing CSV file. Please check the file format.")
    except Exception as e:
        print(f"Error loading data: {str(e)}")
        raise

def get_regions(df: pd.DataFrame) -> List[str]:
    """
    Get unique regions from the data
    
    Args:
        df: DataFrame with report data
        
    Returns:
        List of unique regions
    """
    return sorted(df['Region'].unique().tolist())

def get_item_codes_by_region(df: pd.DataFrame, region: Optional[str] = None) -> Dict[str, List[str]]:
    """
    Get item codes grouped by region
    
    Args:
        df: DataFrame with report data
        region: Optional region to filter by
        
    Returns:
        Dictionary with regions as keys and lists of item codes as values
    """
    if region:
        filtered_df = df[df['Region'] == region]
    else:
        filtered_df = df
        
    result = {}
    for region in filtered_df['Region'].unique():
        region_df = filtered_df[filtered_df['Region'] == region]
        result[region] = sorted(region_df['Item Code'].unique().tolist())
    
    return result

def get_item_details(df: pd.DataFrame, item_code: str, region: Optional[str] = None) -> Dict[str, Any]:
    """
    Get detailed information for a specific item code
    
    Args:
        df: DataFrame with report data
        item_code: Item code to get details for
        region: Optional region to filter by
        
    Returns:
        Dictionary with item details
    """
    if region:
        filtered_df = df[(df['Item Code'] == item_code) & (df['Region'] == region)]
    else:
        filtered_df = df[df['Item Code'] == item_code]
    
    if filtered_df.empty:
        return {}
    
    # Get the first row for consistent item information
    first_row = filtered_df.iloc[0]
    
    # Group stores by region and store brand
    stores_by_region_brand = {}
    for region_name in filtered_df['Region'].unique():
        region_df = filtered_df[filtered_df['Region'] == region_name]
        
        for brand in region_df['Store Brand'].unique():
            brand_df = region_df[region_df['Store Brand'] == brand]
            
            if (region_name, brand) not in stores_by_region_brand:
                stores_by_region_brand[(region_name, brand)] = []
            
            for _, row in brand_df.iterrows():
                store_info = {
                    'Store Code': row['Store Code'],
                    'Store Name': row['Store Name'],
                    'SPM Code': row['SPM Code'] if pd.notna(row['SPM Code']) else "",
                    'Language': row['Language'] if pd.notna(row['Language']) else ""
                }
                stores_by_region_brand[(region_name, brand)].append(store_info)
    
    # Create final result
    result = {
        'Item Code': item_code,
        'Description': first_row['Description'],
        'Unit Size': first_row['Unit Size'],
        'Price': first_row['Price'],
        'Start Date': first_row['Start Date'],
        'End Date': first_row['End Date'],
        'SPM Code': first_row['SPM Code'] if pd.notna(first_row['SPM Code']) else "",
        'Regions': []
    }
    
    # Add region and store brand information
    for (region_name, brand), stores in stores_by_region_brand.items():
        region_info = {
            'Region': region_name,
            'Store Brand': brand,
            'Language': stores[0]['Language'],  # Taking the language from the first store
            'Stores': stores
        }
        result['Regions'].append(region_info)
    
    return result

