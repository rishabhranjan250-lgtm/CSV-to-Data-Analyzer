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
    
    raw_pipeline_template = """```python
import pandas as pd
import numpy as np
import plotly.express as px

# 1. Load data assets
df_active = pd.read_csv('[FILE_NAME]')

print("--- DATASET SUMMARY ---")
print(df_active.info())

print("\\n--- DESCRIPTIVE STATISTICS ---")
print(df_active.describe(include='all').T)

# 2. Automated Missing Value Analysis
missing_data = df_active.isnull().sum()
print("\\n--- MISSING VALUES PER COLUMN ---")
print(missing_data[missing_data > 0])

# 3. Correlation Engine
numeric_df = df_active.select_dtypes(include=['number'])
if not numeric_df.empty:
    print("\\n--- CORRELATION MATRIX ---")
    print(numeric_df.corr())
    
# 4. Outlier Detection using IQR Method
print("\\n--- OUTLIER IDENTIFICATION ---")
for col in numeric_df.columns:
    q1 = df_active[col].quantile(0.25)
    q3 = df_active[col].quantile(0.75)
    iqr = q3 - q1
    lower_bound = q1 - (1.5 * iqr)
    upper_bound = q3 + (1.5 * iqr)
    outliers = df_active[(df_active[col] < lower_bound) | (df_active[col] > upper_bound)].shape[0]
    print(f"Column '{col}' has {outliers} potential extreme outliers.")
```"""

    target_name = active_name if len(datasets) == 1 else uploaded_files[0].name
    python_pipeline_code = raw_pipeline_template.replace('[FILE_NAME]', f"{target_name}.csv" if not target_name.endswith('.csv') else target_name)
    st.markdown(python_pipeline_code)

    # 4. MASTER VISUALIZATION SUITE (7 CHARTS WITH DUAL TABS)
    st.markdown("---")
    st.header("📊 4. Connected Master Visualization Suite")
    st.write("Switch tabs under each chart to instantly grab execution codes.")

    # VISUAL 1: BAR CHART
    if len(categorical_cols) > 0 and len(numeric_cols) > 0:
        st.markdown("### 📈 1. Clustered Column / Bar Chart")
        c_x = st.selectbox("Select Dimension (X-Axis)", categorical_cols, key="v1_x")
        c_y = st.selectbox("Select Value (Y-Axis)", numeric_cols, key="v1_y")
        
        fig1 = px.bar(active_df, x=c_x, y=c_y, title=f"Total {c_y} by {c_x}", color=c_x, template="plotly_white")
        st.plotly_chart(fig1, use_container_width=True)
        
        t1, t2 = st.tabs(["📊 Power BI Setup Blueprint", "🐍 Python Snippet"])
        with t1:
            st.markdown(f"**Visual Type:** Clustered Column Chart\n* **X-Axis:** `{c_x}`\n* **Y-Axis:** `{c_y}` (Sum/Average)\n\n**DAX Measure:**\n```dax\nTotal_{c_y.replace(' ', '_')} = SUM('{active_name}'[{c_y}])\n```")
        with t2:
            st.markdown(f"```python\nfig = px.bar(df, x='{c_x}', y='{c_y}', title='Total {c_y} by {c_x}', color='{c_x}')\nfig.show()\n```")

    # VISUAL 2: LINE CHART
    if len(all_potential_time_cols) > 0 and len(numeric_cols) > 0:
        st.markdown("---")
        st.markdown("### 📉 2. Line Chart (Trend Analysis)")
        t_x = st.selectbox("Select Time Axis (X-Axis)", all_potential_time_cols, key="v2_x")
        t_y = st.selectbox("Select Metric (Y-Axis)", numeric_cols, key="v2_y")
        
        df_sorted = active_df.sort_values(by=t_x)
        fig2 = px.line(df_sorted, x=t_x, y=t_y, title=f"Movement of {t_y} over {t_x}", template="plotly_white")
        st.plotly_chart(fig2, use_container_width=True)
        
        t1, t2 = st.tabs(["📊 Power BI Setup Blueprint", "🐍 Python Snippet"])
        with t1:
            st.markdown(f"**Visual Type:** Line Chart\n* **X-Axis:** `{t_x}`\n* **Y-Axis:** `{t_y}`\n\n**Power Query M-Code Type Cast:**\n```powerquery\n= Table.TransformColumnTypes(#\"Changed Type\",{{\"{t_x}\", type date}})\n```")
        with t2:
            st.markdown(f"```python\nfig = px.line(df.sort_values('{t_x}'), x='{t_x}', y='{t_y}', title='Trend Line')\nfig.show()\n```")

    # VISUAL 3: PIE CHART
    if len(categorical_cols) > 0 and len(numeric_cols) > 0:
        st.markdown("---")
        st.markdown("### 🍩 3. Donut / Pie Chart (Part-to-Whole Share)")
        p_slice = st.selectbox("Select Category Split (Legend)", categorical_cols, key="v3_slice")
        p_val = st.selectbox("Select Size Value", numeric_cols, key="v3_val")
        
        fig3 = px.pie(active_df, names=p_slice, values=p_val, hole=0.4, title=f"Share of {p_val} by {p_slice}")
        st.plotly_chart(fig3, use_container_width=True)
        
        t1, t2 = st.tabs(["📊 Power BI Setup Blueprint", "🐍 Python Snippet"])
        with t1:
            st.markdown(f"**Visual Type:** Donut Chart\n* **Legend:** `{p_slice}`\n* **Values:** `{p_val}`")
        with t2:
            st.markdown(f"```python\nfig = px.pie(df, names='{p_slice}', values='{p_val}', hole=0.4)\nfig.show()\n```")

    # VISUAL 4: SCATTER PLOT
    if len(numeric_cols) >= 2:
        st.markdown("---")
        st.markdown("### 🎯 4. Scatter Plot (Variable Correlations)")
        s_x = st.selectbox("Select X Variable", numeric_cols, index=0, key="v4_x")
        s_y = st.selectbox("Select Y Variable", numeric_cols, index=min(1, len(numeric_cols)-1), key="v4_y")
        s_color = st.selectbox("Group Points By:", [None] + categorical_cols, key="v4_c")
        
        fig4 = px.scatter(active_df, x=s_x, y=s_y, color=s_color, title=f"Correlation: {s_x} vs {s_y}", template="plotly_white")
        st.plotly_chart(fig4, use_container_width=True)
        
        t1, t2 = st.tabs(["📊 Power BI Setup Blueprint", "🐍 Python Snippet"])
        with t1:
            powerbi_blueprint = f"""**Visual Type:** Scatter Chart
* **X Axis:** `{s_x}` (Select **Don't Summarize**)
* **Y Axis:** `{s_y}` (Select **Don't Summarize**)
* **Legend:** `{s_color if s_color else 'Leave Empty'}`"""
            st.markdown(powerbi_blueprint)
        with t2:
            color_argument = f"color='{s_color}', " if s_color else ""
            python_scatter_code = f"""```python
fig = px.scatter(df, x='{s_x}', y='{s_y}', {color_argument}title='Scatter Plot Grid')
fig.show()
```"""
            st.markdown(python_scatter_code)

    # VISUAL 5: HISTOGRAM
    if len(numeric_cols) > 0:
        st.markdown("---")
        st.markdown("### 📊 5. Histogram (Data Density)")
        h_val = st.selectbox("Select Target for Sizing Tiers", numeric_cols, key="v5_h")
        
        fig5 = px.histogram(active_df, x=h_val, marginal="box", title=f"Frequency Concentration of {h_val}", template="plotly_white")
        st.plotly_chart(fig5, use_container_width=True)
        
        t1, t2 = st.tabs(["📊 Power BI Setup Blueprint", "🐍 Python Snippet"])
        with t1:
            st.markdown(f"**Visual Type:** Column Chart with Bins\n1. Right-click `{h_val}` -> **New group**.\n2. Set **Group type** to **Bins**.\n3. Drag the Binned column to the **X-Axis** and the original column (Set to **Count**) to the **Y-Axis**.")
        with t2:
            st.markdown(f"```python\nfig = px.histogram(df, x='{h_val}', marginal='box')\nfig.show()\n```")

    # VISUAL 6: TREEMAP
    if len(categorical_cols) >= 2 and len(numeric_cols) > 0:
        st.markdown("---")
        st.markdown("### 🧱 6. Treemap (Hierarchical Category Matrix)")
        t_parent = st.selectbox("Select Parent Category", categorical_cols, index=0, key="v6_p")
        t_child = st.selectbox("Select Child Category", categorical_cols, index=min(1, len(categorical_cols)-1), key="v6_c")
        t_size = st.selectbox("Weight Determined By", numeric_cols, key="v6_s")
        
        fig6 = px.treemap(active_df, path=[t_parent, t_child], values=t_size, title=f"Hierarchy Matrix: {t_parent} -> {t_child}")
        st.plotly_chart(fig6, use_container_width=True)
        
        t1, t2 = st.tabs(["📊 Power BI Setup Blueprint", "🐍 Python Snippet"])
        with t1:
            st.markdown(f"**Visual Type:** Treemap\n* **Category:** Drag `{t_parent}` first, then `{t_child}` right underneath it.\n* **Values:** `{t_size}`")
        with t2:
            st.markdown(f"```python\nfig = px.treemap(df, path=['{t_parent}', '{t_child}'], values='{t_size}')\nfig.show()\n```")

    # VISUAL 7: BOX PLOT
    if len(categorical_cols) > 0 and len(numeric_cols) > 0:
        st.markdown("---")
        st.markdown("### 📦 7. Box & Whisker Plot (Statistical Spread)")
        box_cat = st.selectbox("Group Spread Across Categories (X)", categorical_cols, key="v7_x")
        box_num = st.selectbox("Analyze Variance of (Y)", numeric_cols, key="v7_y")
        
        fig7 = px.box(active_df, x=box_cat, y=box_num, points="all", title=f"Quartile Spread of {box_num} by {box_cat}", template="plotly_white")
        st.plotly_chart(fig7, use_container_width=True)
        
        t1, t2 = st.tabs(["📊 Power BI Setup Blueprint", "🐍 Python Snippet"])
        with t1:
            st.markdown(f"**Visual Type:** Box and Whisker plot\n* **Category:** `{box_cat}`\n* **Y Axis:** `{box_num}`")
        with t2:
            st.markdown(f"```python\nfig = px.box(df, x='{box_cat}', y='{box_num}', points='all')\nfig.show()\n```")

    # 5. GLOBAL AUTOMATED INSIGHTS & OUTCOMES
    st.markdown("---")
    st.header("💡 5. Executive Summary: Main Insights & Key Outcomes")
    st.write("Algorithmic summaries executed across your active data matrix:")

    ins_col1, ins_col2 = st.columns(2)

    with ins_col1:
        st.subheader("📊 Key Operational Highlights")
        if len(numeric_cols) > 0:
            target_col = numeric_cols[0]
            q1 = active_df[target_col].quantile(0.25)
            q3 = active_df[target_col].quantile(0.75)
            iqr = q3 - iqr if 'iqr' in locals() else (q3 - q1)
            outliers_count = active_df[(active_df[target_col] < (q1 - 1.5 * iqr)) | (active_df[target_col] > (q3 + 1.5 * iqr))].shape[0]
            if outliers_count > 0:
                st.markdown(f"* 🚨 **Anomaly Alert**: Found **{outliers_count} extreme variance entries (outliers)** inside the `{target_col}` column. These represent critical spikes requiring validation.")
            else:
                st.markdown(f"* ✅ **Data Stability**: The metric `{target_col}` shows zero massive structural anomalies, suggesting consistent operational tracking.")
        
        if len(categorical_cols) > 0:
            top_cat = categorical_cols[0]
            mode_val = active_df[top_cat].mode()[0]
            mode_pct = (active_df[active_df[top_cat] == mode_val].shape[0] / active_df.shape[0]) * 100
            st.markdown(f"* 🎯 **Dominant Segments**: Category value **`{mode_val}`** heavily controls the `{top_cat}` metric, accounting for **{mode_pct:.1f}%** of all documented data points.")

    with ins_col2:
        st.subheader("📈 Statistical Relationships & Modeling Notes")
        if len(numeric_cols) >= 2:
            corr_matrix = active_df[numeric_cols].corr()
            pairs = corr_matrix.unstack().sort_values(ascending=False).drop_duplicates()
            valid_pairs = pairs[pairs < 1.0]
            
            if not valid_pairs.empty and valid_pairs.iloc[0] > 0.4:
                top_pair = valid_pairs.index[0]
                st.markdown(f"* 🤝 **Strong Relationship**: A correlation of **{valid_pairs.iloc[0]:.2f}** exists between **`{top_pair[0]}`** and **`{top_pair[1]}`**. Changes in one explicitly map to shifts in the other.")
            else:
                st.markdown("* 🔍 **Independent Metrics**: No strong linear correlations were detected across numerical vectors.")
        
        if len(datasets) > 1:
            st.markdown(f"* 🔗 **Model Integrity**: Active relationship uses a `{how_method}` join mapping `{left_table}`.`{left_key}` onto `{right_table}`.`{right_key}`. Ready for star-schema conversion.")

        total_nulls = active_df.isna().sum().sum()
        if total_nulls > 0:
            st.markdown(f"* ⚙️ **Data Quality Note**: There are **{total_nulls} blank/missing cells** remaining in the combined matrix. Filter these in Power Query or use dropna() in Python before visualization.")
        else:
            st.markdown("* 💎 **Data Integrity**: 100% complete dataset. Zero null cells across all columns.")

else:
    st.info("💡 Drop one or multiple `.csv` dataset files above to trigger automated visualization engines, schemas, and analytics reports.")
