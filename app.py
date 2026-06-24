import streamlit as st
import pandas as pd
import plotly.express as px
import io

# Page Configuration
st.set_page_config(page_title="Ultimate Relational BI & Python Engine", layout="wide", page_icon="🚀")

st.title("🚀 The Ultimate Relational Analytics & Code Engine")
st.subheader("Upload single or multiple raw CSVs to auto-clean, build relational models, generate 7 master charts, and extract executive insights.")

# 1. MULTI-FILE UPLOADER & AUTO-CLEANING
uploaded_files = st.file_uploader("Upload your dataset(s) (CSV format allowed)", type="csv", accept_multiple_files=True)

if uploaded_files:
    datasets = {}
    
    st.header("🧹 1. Raw Data Processing & Quality Scrubbing")
    st.write("The engine has executed automatic string trimming, dropped blank lines, and aligned date structures.")
    
    # Process and Clean each uploaded file
    for uploaded_file in uploaded_files:
        df = pd.read_csv(uploaded_file)
        file_name = uploaded_file.name.split('.')[0]
        
        # --- AUTOMATED CLEANING & PREPROCESSING ---
        df.dropna(how='all', inplace=True)  # Drop entirely blank rows
        
        for col in df.columns:
            # Clean whitespaces from text data
            if df[col].dtype == 'object':
                df[col] = df[col].astype(str).str.strip()
                # Auto-parse dates safely
                try:
                    df[col] = pd.to_datetime(df[col], errors='ignore')
                except:
                    pass
        
        datasets[file_name] = df
        
        # Display individual table profiles
        with st.expander(f"📋 Processed Table Profile: {file_name}"):
            c1, c2, c3 = st.columns(3)
            c1.metric("Rows", f"{df.shape[0]:,}")
            c2.metric("Columns", df.shape[1])
            c3.metric("Missing Fields Handled", df.isna().sum().sum())
            st.dataframe(df.head(5), use_container_width=True)

    # 2. RELATIONSHIP ENGINE & CONNECTOR
    st.markdown("---")
    st.header("🔀 2. Data Modeling & Relationship Key Mapper")
    
    active_df = None
    active_name = ""
    left_table, right_table, left_key, right_key, how_method = "", "", "", "", "left"
    
    if len(datasets) > 1:
        st.write("Multiple tables detected. Select the matching keys below to create a Power BI style schema relationship (JOIN).")
        
        col_link1, col_link2, col_link3 = st.columns(3)
        with col_link1:
            left_table = st.selectbox("Primary Fact Table (e.g., Transactions)", list(datasets.keys()), key="left_t")
        with col_link2:
            right_table = st.selectbox("Dimension Lookup Table (e.g., Customers)", [k for k in datasets.keys() if k != left_table], key="right_t")
        with col_link3:
            left_key = st.selectbox(f"Join Key from {left_table}", datasets[left_table].columns, key="left_k")
            right_key = st.selectbox(f"Join Key from {right_table}", datasets[right_table].columns, key="right_k")
            
        join_type = st.radio("Join Direction Type", ["Left Join (Keep all records from Fact table)", "Inner Join (Only matching keys)"], horizontal=True)
        how_method = "left" if "Left" in join_type else "inner"
        
        try:
            # Execute Relational Compilation
            active_df = pd.merge(datasets[left_table], datasets[right_table], left_on=left_key, right_on=right_key, how=how_method, suffixes=('', '_dim'))
            active_name = f"{left_table}_linked_{right_table}"
            st.success(f"✔️ Successfully linked model relationship! Combined matrix contains **{active_df.shape[0]:,} rows** and **{active_df.shape[1]} columns**.")
        except Exception as e:
            st.error(f"Failed to join tables. Verify that data keys hold similar structures. Error: {e}")
            active_name = list(datasets.keys())[0]
            active_df = datasets[active_name]
    else:
        active_name = list(datasets.keys())[0]
        active_df = datasets[active_name]
        st.info("Single table loaded. Displaying independent visual profiles.")

    # Extract column attributes from the active working dataframe
    numeric_cols = active_df.select_dtypes(include=['number']).columns.tolist()
    categorical_cols = active_df.select_dtypes(include=['object', 'category']).columns.tolist()
    date_cols = active_df.select_dtypes(include=['datetime', 'datetime64']).columns.tolist()
    all_potential_time_cols = date_cols + [c for c in categorical_cols if 'year' in c.lower() or 'date' in c.lower() or 'month' in c.lower()]

    # 3. FULL PYTHON ENVIRONMENT PIPELINE (GLOBAL)
    st.markdown("---")
    st.header("🐍 3. Full Python Jupyter Notebook Pipeline")
    st.write("Copy this block to run a professional, end-to-end Exploratory Data Analysis (EDA) locally inside a notebook.")
    
    python_pipeline_code = f"""```python
import pandas as pd
import numpy as np
import plotly.express as px

# 1. Load data assets
df_active = pd.read_csv('{active_name if len(datasets) == 1 else uploaded_files[0].name}')

print("--- DATASET SUMMARY ---")
print(df_active.info())

print("\\n--- DESCRIPTIVE STATISTICS ---")
print(df_active.describe(include='all').T)

# 2. Automated Missing Value Analysis
missing_data = df_active.isnull().sum()
print("\\n--- MISSING VALUES PER COLUMN ---")
print(missing_
