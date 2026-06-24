import streamlit as st
import pandas as pd
import plotly.express as px
import io

# Page Configuration
st.set_page_config(page_title="Ultimate Power BI & Python Code Engine", layout="wide", page_icon="🚀")

st.title("🚀 The Ultimate Automated Analytics & Code Engine")
st.subheader("Upload any CSV to automatically generate every possible visualization, Power BI blueprint, Python script, and executive insights.")

uploaded_file = st.file_uploader("Upload your dataset (CSV format)", type="csv")

if uploaded_file is not None:
    # 1. READ & PREPROCESS DATA
    df = pd.read_csv(uploaded_file)
    file_name = uploaded_file.name.split('.')[0]
    
    # Try converting object columns to datetime if they look like dates
    for col in df.columns:
        if df[col].dtype == 'object':
            try:
                df[col] = pd.to_datetime(df[col], errors='ignore')
            except:
                pass

    # Separate Column Types
    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
    categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
    date_cols = df.select_dtypes(include=['datetime', 'datetime64']).columns.tolist()
    
    # Fallback if no dates detected natively
    all_potential_time_cols = date_cols + [c for c in categorical_cols if 'year' in c.lower() or 'date' in c.lower() or 'month' in c.lower()]

    # --- SECTION 1: DATA PROFILE METRICS ---
    st.header("📋 1. Dataset Profile & Dimensions")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total Rows / Records", f"{df.shape[0]:,}")
    m2.metric("Total Fields / Columns", df.shape[1])
    m3.metric("Numeric Fields", len(numeric_cols))
    m4.metric("Categorical/Text Fields", len(categorical_cols))
    
    with st.expander("📝 View Raw Data Preview (Top 10 Rows)"):
        st.dataframe(df.head(10), use_container_width=True)

    # --- SECTION 2: FULL PYTHON ENVIRONMENT SCRIPTS ---
    st.markdown("---")
    st.header("🐍 2. Full Python Jupyter Notebook Pipeline")
    st.write("If you want to move beyond basic charts and perform a professional, end-to-end Exploratory Data Analysis (EDA) in Python, copy the script block below.")
    
    python_pipeline_code = f"""```python
import pandas as pd
import numpy as np
import plotly.express as px

# 1. Load the uploaded dataset
df = pd.read_csv('{uploaded_file.name}')

print("--- DATASET SUMMARY ---")
print(df.info())

print("\\n--- DESCRIPTIVE STATISTICS ---")
print(df.describe(include='all').T)

# 2. Automated Missing Value Handling
missing_data = df.isnull().sum()
print("\\n--- MISSING VALUES PER COLUMN ---")
print(missing_data[missing_data > 0])

# 3. Correlation Matrix (For all numerical metrics)
numeric_df = df.select_dtypes(include=['number'])
if not numeric_df.empty:
    print("\\n--- CORRELATION MATRIX ---")
    print(numeric_df.corr())
    
# 4. Outlier Detection using IQR Method
print("\\n--- OUTLIER IDENTIFICATION ---")
for col in numeric_df.columns:
    q1 = df[col].quantile(0.25)
    q3 = df[col].quantile(0.75)
    iqr = q3 - q1
    lower_bound = q1 - (1.5 * iqr)
    upper_bound = q3 + (1.5 * iqr)
    outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)].shape[0]
    print(f"Column '{{col}}' has {{outliers}} potential extreme outliers.")
```"""
    st.markdown(python_pipeline_code)

    # --- SECTION 3: THE COMPREHENSIVE VISUALIZATION ENGINES ---
    st.markdown("---")
    st.header("📊 3. Master Visualization Suite & Code Blueprints")
    st.write("Browse through every layout option matching your dataset below. Switch tabs under each chart to pull execution code.")

    # ----------------------------------------------------
    # VISUAL 1: BAR CHART (Categorical Comparison)
    # ----------------------------------------------------
    if len(categorical_cols) > 0 and len(numeric_cols) > 0:
        st.markdown("### 📈 1. Clustered Column / Bar Chart (Group Comparisons)")
        c_x = st.selectbox("Select Dimension (X-Axis)", categorical_cols, key="v1_x")
        c_y = st.selectbox("Select Aggregation Value (Y-Axis)", numeric_cols, key="v1_y")
        
        fig1 = px.bar(df, x=c_x, y=c_y, title=f"Total {c_y} by {c_x}", color=c_x, template="plotly_white")
        st.plotly_chart(fig1, use_container_width=True)
        
        t1, t2 = st.tabs(["📊 Power BI Setup Blueprint", "🐍 Python Snippet"])
        with t1:
            st.markdown(f"**Visual Type:** Clustered Column Chart\n* **X-Axis:** `{c_x}`\n* **Y-Axis:** `{c_y}` (Set to **Sum** or **Average**)\n\n**DAX Measure:**\n```dax\nTotal_{c_y.replace(' ', '_')} = SUM('{file_name}'[{c_y}])\n```")
        with t2:
            st.markdown(f"```python\nimport pandas as pd\nimport plotly.express as px\n\ndf = pd.read_csv('{uploaded_file.name}')\nfig = px.bar(df, x='{c_x}', y='{c_y}', title='Total {c_y} by {c_x}', color='{c_x}')\nfig.show()\n```")

    # ----------------------------------------------------
    # VISUAL 2: LINE CHART (Temporal Trend Analysis)
    # ----------------------------------------------------
    if len(all_potential_time_cols) > 0 and len(numeric_cols) > 0:
        st.markdown("---")
        st.markdown("### 📉 2. Line Chart (Trend Analysis / Time-Series)")
        t_x = st.selectbox("Select Time/Sequence Axis (X-Axis)", all_potential_time_cols, key="v2_x")
        t_y = st.selectbox("Select Performance Metric (Y-Axis)", numeric_cols, key="v2_y")
        
        df_sorted = df.sort_values(by=t_x)
        fig2 = px.line(df_sorted, x=t_x, y=t_y, title=f"Movement of {t_y} over {t_x}", template="plotly_white")
        st.plotly_chart(fig2, use_container_width=True)
        
        t1, t2 = st.tabs(["📊 Power BI Setup Blueprint", "🐍 Python Snippet"])
        with t1:
            st.markdown(f"**Visual Type:** Line Chart\n* **X-Axis:** `{t_x}` (Power BI will automatically build a Date Hierarchy)\n* **Y-Axis:** `{t_y}`\n\n**Power Query Step:** Ensure Type is Date:\n```powerquery\n= Table.TransformColumnTypes(#\"Changed Type\",{{\"{t_x}\", type date}})\n```")
        with t2:
            st.markdown(f"```python\ndf = pd.read_csv('{uploaded_file.name}')\ndf['{t_x}'] = pd.to_datetime(df['{t_x}'], errors='coerce')\ndf = df.sort_values('{t_x}')\nfig = px.line(df, x='{t_x}', y='{t_y}', title='Trend over Time')\nfig.show()\n```")

    # ----------------------------------------------------
    # VISUAL 3: PIE / DONUT CHART (Composition Breakdown)
    # ----------------------------------------------------
    if len(categorical_cols) > 0 and len(numeric_cols) > 0:
        st.markdown("---")
        st.markdown("### 🍩 3. Donut / Pie Chart (Part-to-Whole Share)")
        p_slice = st.selectbox("Select Category Split (Legend)", categorical_cols, key="v3_slice")
        p_val = st.selectbox("Select Size Value", numeric_cols, key="v3_val")
        
        fig3 = px.pie(df, names=p_slice, values=p_val, hole=0.4, title=f"Composition Share of {p_val} by {p_slice}")
        st.plotly_chart(fig3, use_container_width=True)
        
        t1, t2 = st.tabs(["📊 Power BI Setup Blueprint", "🐍 Python Snippet"])
        with t1:
            st.markdown(f"**Visual Type:** Donut Chart\n* **Legend:** `{p_slice}`\n* **Values:** `{p_val}`")
        with t2:
            st.markdown(f"```python\nfig = px.pie(df, names='{p_slice}', values='{p_val}', hole=0.4, title='Composition share')\nfig.show()\n```")

    # ----------------------------------------------------
    # VISUAL 4: SCATTER PLOT (Correlation & Distribution)
    # ----------------------------------------------------
    if len(numeric_cols) >= 2:
        st.markdown("---")
        st.markdown("### 🎯 4. Scatter Plot (Variable Interaction & Correlations)")
        s_x = st.selectbox("Select X-Axis Variable", numeric_cols, index=0, key="v4_x")
        s_y = st.selectbox("Select Y-Axis Variable", numeric_cols, index=min(1, len(numeric_cols)-1), key="v4_y")
        s_color = st.selectbox("Group / Color Code points by:", [None] + categorical_cols, key="v4_c")
        
        fig4 = px.scatter(df, x=s_x, y=s_y, color=s_color, title=f"Correlation Vector: {s_x} vs {s_y}", template="plotly_white")
        st.plotly_chart(fig4, use_container_width=True)
        
        t1, t2 = st.tabs(["📊 Power BI Setup Blueprint", "🐍 Python Snippet"])
        with t1:
            st.markdown(f"**Visual Type:** Scatter Chart\n* **X Axis:** `{s_x}` (Click arrow -> Select **Don't Summarize**)\n
