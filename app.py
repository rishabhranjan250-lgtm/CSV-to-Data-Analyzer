import streamlit as st
import pandas as pd
import plotly.express as px
import io

# Set page config
st.set_page_config(page_title="CSV to Power BI Insights", layout="wide", page_icon="📊")

st.title("📊 CSV Automated Insights & Power BI Guide")
st.subheader("Upload your dataset to get instant insights and Power BI blueprints.")

# File Uploader
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    # Read Data
    df = pd.read_csv(uploaded_file)
    
    # Session state to keep track of columns
    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
    categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
    date_cols = df.select_dtypes(include=['datetime', 'object']).columns.tolist() # Basic guess
    
    # --- SECTION 1: DATA PREVIEW ---
    st.header("👀 1. Dataset Preview")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Rows", df.shape[0])
    col2.metric("Total Columns", df.shape[1])
    col3.metric("Missing Values", df.isna().sum().sum())
    
    st.dataframe(df.head(10), use_container_width=True)
    
    # --- SECTION 2: AUTOMATED INSIGHTS ---
    st.markdown("---")
    st.header("💡 2. Quick Automated Insights")
    
    with st.expander("View Column Summary & Types", expanded=True):
        buffer = io.StringIO()
        df.info(buf=buffer)
        st.text(buffer.getvalue())

    if len(numeric_cols) > 0:
        st.subheader("Key Numerical Statistics")
        st.dataframe(df.describe().T, use_container_width=True)
        
        # High-level insight generation
        st.markdown("**Top Data Discoveries:**")
        for col in numeric_cols[:3]: # Limit to top 3 for brevity
            max_val = df[col].max()
            min_val = df[col].min()
            mean_val = df[col].mean()
            st.write(f"* **{col}**: Ranges from `{min_val}` to `{max_val}` with an average of `{mean_val:,.2f}`.")
            
    if len(categorical_cols) > 0:
        st.markdown("**Top Categorical Breakdowns:**")
        for col in categorical_cols[:2]:
            top_val = df[col].mode()[0]
            count_top = df[col].value_counts().iloc[0]
            st.write(f"* **{col}**: The most frequent category is `{top_val}` appearing `{count_top}` times.")

    # --- SECTION 3: VISUALIZATIONS & POWER BI BLUEPRINTS ---
    st.markdown("---")
    st.header("📈 3. Generated Charts & Power BI Blueprints")
    st.write("Below are interactive previews of charts along with instructions/DAX codes to recreate them in Power BI.")

    # Chart 1: Bar Chart (Categorical vs Numeric)
    if len(categorical_cols) > 0 and len(numeric_cols) > 0:
        st.subheader("Chart Type: Bar Chart (Distribution / Comparison)")
        cat_choice = st.selectbox("Select Categorical Axis (X)", categorical_cols, key="bar_cat")
        num_choice = st.selectbox("Select Numeric Value (Y)", numeric_cols, key="bar_num")
        
        # Aggregate data for clean charting
        chart_data = df.groupby(cat_choice)[num_choice].sum().reset_index()
        
        # Plotly Preview
        fig_bar = px.bar(chart_data, x=cat_choice, y=num_choice, title=f"Total {num_choice} by {cat_choice}")
        st.plotly_chart(fig_bar, use_container_width=True)
        
        # Power BI Recipe
        with st.expander("👉 Click to get Power BI Setup Blueprint"):
            st.markdown(f"""
            ### **How to build this in Power BI Desktop:**
            1. Click on the **Stacked Bar Chart** or **Clustered Column Chart** icon in the Visualizations pane.
            2. **Y-Axis (or X-Axis if horizontal):** Drag and drop your `[{cat_choice}]` column.
            3. **X-Axis (or Y-Axis if horizontal):** Drag and drop your `[{num_choice}]` column.
            4. Set the aggregation to **Sum** (default) or **Average** in the fields drop-down.
            
            ### **DAX Measure Code (Optional - for advanced dynamic calculation):**
            If you want to use a formal measure instead of dropping the raw column, create this measure:
            ```dax
            Total_{num_choice.replace(' ', '_')} = SUM('{uploaded_file.name.split(".")[0]}'[{num_choice}])
            ```
            """)

    # Chart 2: Line Chart (Trend Analysis)
    if len(numeric_cols) > 0:
        st.subheader("Chart Type: Line Chart (Trends)")
        
        # If there's a suspected date column or just use index/another numeric
        x_trend = st.selectbox("Select X-Axis (Time/Sequence)", date_cols + numeric_cols, key="line_x")
        y_trend = st.selectbox("Select Y-Axis (Value)", numeric_cols, key="line_y")
        
        fig_line = px.line(df.sort_values(by=x_trend), x=x_trend, y=y_trend, title=f"Trend of {y_trend} over {x_trend}")
        st.plotly_chart(fig_line, use_container_width=True)
        
        with st.expander("👉 Click to get Power BI Setup Blueprint"):
            st.markdown(f"""
            ### **How to build this in Power BI Desktop:**
            1. Click on the **Line Chart** icon in the Visualizations pane.
            2. **X-Axis:** Drag and drop `[{x_trend}]`. *(If it's a date, Power BI will automatically create a Date Hierarchy).*
            3. **Y-Axis:** Drag and drop `[{y_trend}]`.
            
            ### **Power Query M-Code (To ensure correct Date/Time data type):**
            Go to Home > Transform Data, select your column, and change data type to **Date**. The M code generated looks like this:
            ```powerquery
            = Table.TransformColumnTypes(#"Changed Type", {{"{x_trend}", type date}})
            ```
            """)

    # Chart 3: Scatter Plot (Correlation)
    if len(numeric_cols) >= 2:
        st.subheader("Chart Type: Scatter Plot (Correlation Analysis)")
        scat_x = st.selectbox("Select X Variable", numeric_cols, index=0, key="scat_x")
        scat_y = st.selectbox("Select Y Variable", numeric_cols, index=min(1, len(numeric_cols)-1), key="scat_y")
        
        fig_scatter = px.scatter(df, x=scat_x, y=scat_y, title=f"Correlation between {scat_x} and {scat_y}")
        st.plotly_chart(fig_scatter, use_container_width=True)
        
        with st.expander("👉 Click to get Power BI Setup Blueprint"):
            st.markdown(f"""
            ### **How to build this in Power BI Desktop:**
            1. Click on the **Scatter Chart** icon in the Visualizations pane.
            2. **X Axis:** Drag `[{scat_x}]`. Click the down arrow next to it and select **Don't Summarize**.
            3. **Y Axis:** Drag `[{scat_y}]`. Click the down arrow next to it and select **Don't Summarize**.
            4. *(Optional)* Drag a categorical column into the **Values** or **Legend** bucket to separate the dots.
            """)
            
else:
    st.info("ℹ️ Please upload a CSV file using the sidebar or the box above to generate your dashboard.")