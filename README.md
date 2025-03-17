# Job Report Analyzer

This tool provides an interactive Streamlit application for analyzing job report data, focusing on retail product listings across different regions, store brands, and items.

## Features

- **Region and Item Code Browsing:** View products grouped by region and item code
- **Detailed Product View:** Shows region, store brand, language, and all associated stores
- **Interactive Filtering:** Filter data by region
- **Visualization Dashboard:** Charts showing distribution of items by region, store brand, and popularity

## Installation

1. Make sure you have Python 3.8+ installed
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Running the Application

From the report_tools directory, run:

```bash
streamlit run app.py
```

This will start the Streamlit server and open the application in your default web browser.

## Usage Guide

1. The app will automatically load the sample data file (`job_report_20250314144738-sample-200.csv`)
2. **Browse by Region:** Use the left panel to navigate through regions and item codes
3. **View Item Details:** Click on an item code to see detailed information in the right panel
4. **Filter Data:** Use the sidebar to filter by region
5. **Analyze Trends:** Scroll down to see visualizations of the data

## Project Structure

- `app.py`: Main Streamlit application
- `report_analyzer.py`: Data processing functions
- `job_report_20250314144738-sample-200.csv`: Sample data file
- `requirements.txt`: Required Python packages

## Development

### Running Tests

To run the test suite:

```bash
python -m unittest test_report_analyzer.py
```

### Adding New Features

Follow the project's approach when adding new features:
1. Implement the feature in `report_analyzer.py`
2. Add UI components to `app.py`
3. Document changes in the README

## Planned Enhancements

- Export functionality for reports
- Additional filtering options (by price range, date, etc.)
- Search functionality for item descriptions
- Comparison views between different time periods
