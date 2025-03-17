import streamlit as st
import pandas as pd
import os
import plotly.express as px
from report_analyzer import load_data, get_regions, get_item_codes_by_region, get_item_details

# Set page configuration
st.set_page_config(
    page_title="Job Report Analyzer",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Add custom CSS
st.markdown("""
<style>
    .main .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
    }
    h1, h2, h3 {
        margin-top: 0;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #f0f2f6;
        border-radius: 4px 4px 0 0;
        gap: 1px;
        padding-top: 10px;
        padding-bottom: 10px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #ffffff;
        border-bottom: 2px solid #4e8cff;
    }
    .store-list {
        border: 1px solid #f0f2f6;
        border-radius: 5px;
        padding: 10px;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

# App title
st.title("Job Report Analyzer")

# Load data
file_path = "job_report_20250314144738-sample-200.csv"

@st.cache_data
def get_cached_data(file_path):
    return load_data(file_path)

try:
    df = get_cached_data(file_path)
    # Show data loading success message
    st.success(f"Data loaded successfully: {len(df)} records")
    
    # Create sidebar for filtering
    st.sidebar.header("Filters")
    
    # Get unique regions
    regions = get_regions(df)
    selected_region = st.sidebar.selectbox("Select Region", ["All Regions"] + regions)
    
    # Filter data based on selected region
    if selected_region != "All Regions":
        filtered_df = df[df['Region'] == selected_region]
        region_item_codes = get_item_codes_by_region(df, selected_region)
    else:
        filtered_df = df
        region_item_codes = get_item_codes_by_region(df)
    
    # Display regions and item codes in the main area
    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.subheader("Regions and Item Codes")
        
        # Create tabs for each region
        if selected_region != "All Regions":
            regions_to_display = [selected_region]
        else:
            regions_to_display = regions
        
        # Create expander for each region
        for region in regions_to_display:
            with st.expander(region, expanded=(len(regions_to_display) == 1)):
                # Get item codes for the region
                item_codes = region_item_codes.get(region, [])
                
                # Create buttons for each item code
                for item_code in item_codes:
                    # Find one example of this item
                    item_example = df[(df['Region'] == region) & (df['Item Code'] == item_code)].iloc[0]
                    description = item_example['Description']
                    
                    # Create a button with item code and description
                    if st.button(f"{item_code} - {description}", key=f"{region}_{item_code}"):
                        st.session_state['selected_item'] = {'region': region, 'item_code': item_code}
    
    with col2:
        st.subheader("Item Details")
        
        # Display item details if an item is selected
        if 'selected_item' in st.session_state:
            selected_region = st.session_state['selected_item']['region']
            selected_item_code = st.session_state['selected_item']['item_code']
            
            # Get detailed information for the selected item
            item_details = get_item_details(df, selected_item_code, selected_region)
            
            if item_details:
                # Create tabs for different regions if the item exists in multiple regions
                if len(item_details['Regions']) > 0:
                    tabs = st.tabs([region_info['Region'] for region_info in item_details['Regions']])
                    
                    for i, tab in enumerate(tabs):
                        region_info = item_details['Regions'][i]
                        
                        with tab:
                            # Display item information
                            st.markdown(f"### Item Information")
                            col1, col2 = st.columns(2)
                            with col1:
                                st.markdown(f"**Region:** {region_info['Region']}")
                                st.markdown(f"**Store Brand:** {region_info['Store Brand']}")
                                st.markdown(f"**Language:** {region_info['Language']}")
                                st.markdown(f"**Item Code:** {item_details['Item Code']}")
                                st.markdown(f"**Description:** {item_details['Description']}")
                            with col2:
                                st.markdown(f"**Unit Size:** {item_details['Unit Size']}")
                                st.markdown(f"**Price:** {item_details['Price']}")
                                st.markdown(f"**Start Date:** {item_details['Start Date']}")
                                st.markdown(f"**End Date:** {item_details['End Date']}")
                                st.markdown(f"**SPM Code:** {item_details['SPM Code']}")
                            
                            # Display stores
                            st.markdown(f"### Stores")                        
                            stores = region_info['Stores']
                            
                            # Display as a simple table
                            store_data = []
                            for store in stores:
                                store_data.append({
                                    "Store Code": store['Store Code'],
                                    "Store Name": store['Store Name']
                                })
                            
                            if store_data:
                                st.dataframe(pd.DataFrame(store_data), use_container_width=True)
                else:
                    st.info("No details available for this item.")
        else:
            st.info("Select an item code from the left panel to view details.")
    
    # Additional analysis section
    st.header("Summary Analytics")
    
    # Show distribution of items by region
    region_counts = df['Region'].value_counts().reset_index()
    region_counts.columns = ['Region', 'Count']
    
    fig = px.bar(
        region_counts,
        x='Region',
        y='Count',
        title='Distribution of Items by Region',
        color='Region'
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Show top items by count
    col1, col2 = st.columns(2)
    
    with col1:
        top_items = df['Item Code'].value_counts().reset_index().head(10)
        top_items.columns = ['Item Code', 'Count']
        
        # Merge with descriptions
        item_descriptions = df[['Item Code', 'Description']].drop_duplicates('Item Code')
        top_items = top_items.merge(item_descriptions, on='Item Code')
        
        fig = px.bar(
            top_items,
            x='Item Code',
            y='Count',
            title='Top 10 Items by Frequency',
            color='Item Code',
            hover_data=['Description']
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Show distribution by store brand
        brand_counts = df['Store Brand'].value_counts().reset_index()
        brand_counts.columns = ['Store Brand', 'Count']
        
        fig = px.pie(
            brand_counts,
            values='Count',
            names='Store Brand',
            title='Distribution by Store Brand'
        )
        st.plotly_chart(fig, use_container_width=True)

except Exception as e:
    st.error(f"Error loading data: {str(e)}")

# Add footer
st.markdown("---")
st.markdown("Job Report Analyzer v1.0", unsafe_allow_html=True)

