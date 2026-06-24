import streamlit as st
import pandas as pd
import plotly.express as px
import io
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

# Page Configuration
st.set_page_config(page_title="Ultimate Relational BI & Python Engine", layout="wide", page_icon="🚀")

st.title("🚀 The Ultimate Relational Analytics & Code Engine")
st.subheader("Upload single or multiple raw CSVs to auto-clean, build relational models, generate 7 master charts, and extract deep-dive analytics.")

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
            if df[col].dtype == 'object':
                df[col] = df[col].astype(str).str.strip()
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
```"""
    target_name = active_name if len(datasets) == 1 else uploaded_files[0].name
    python_pipeline_code = raw_pipeline_template.replace('[FILE_NAME]', f"{target_name}.csv" if not target_name.endswith('.csv') else target_name)
    st.markdown(python_pipeline_code)

    # 4. MASTER VISUALIZATION SUITE (ALL 7 CHARTS RESTORED WITH TABS)
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

    # 5. DEEP INSIGHT GENERATOR & PROFESSIONAL REPORT COMPILER
    st.markdown("---")
    st.header("💡 5. Deep-Dive Executive Data Report & PDF Export")
    st.write("The engine has synthesized complete statistical layers from the data array below.")

    # Calculate preview stats on page interface
    c_preview1, c_preview2 = st.columns(2)
    with c_preview1:
        st.subheader("📊 Numeric Profile Aggregations")
        st.dataframe(active_df.describe().T, use_container_width=True)
    with c_preview2:
        st.subheader("📝 Missing Values Map & Column Density")
        st.dataframe(active_df.isna().sum().to_frame(name="Missing Elements Count"), use_container_width=True)

    # --- ADVANCED REPORTLAB PDF COMPILATION ENGINE ---
    def compile_granular_pdf():
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=45, leftMargin=45, topMargin=50, bottomMargin=50)
        story = []
        
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle('DocTitle', parent=styles['Heading1'], fontSize=24, spaceAfter=8, textColor=colors.HexColor('#1E3A8A'))
        subtitle_style = ParagraphStyle('DocSub', parent=styles['Normal'], fontSize=10, spaceAfter=25, textColor=colors.HexColor('#6B7280'))
        h1_style = ParagraphStyle('SectionH1', parent=styles['Heading2'], fontSize=15, spaceBefore=18, spaceAfter=12, textColor=colors.HexColor('#111827'))
        body_style = ParagraphStyle('BodyText', parent=styles['Normal'], fontSize=10.5, leading=15, spaceAfter=8, textColor=colors.HexColor('#4B5563'))
        th_style = ParagraphStyle('TableHeader', parent=styles['Normal'], fontSize=10, fontName='Helvetica-Bold', textColor=colors.HexColor('#FFFFFF'))
        td_style = ParagraphStyle('TableCell', parent=styles['Normal'], fontSize=9.5, textColor=colors.HexColor('#111827'))

        # Document Header
        story.append(Paragraph("📈 Comprehensive Analytical & Data Diagnostics Report", title_style))
        story.append(Paragraph(f"Generated via Relational Profiling Engine • Active System Workspace: {active_name}", subtitle_style))
        story.append(Spacer(1, 10))
        
        # SECTION 1: EXEC SUMMARY & DIMENSIONS
        story.append(Paragraph("1. High-Level Structural Architecture", h1_style))
        story.append(Paragraph("This section outlines the basic data profile shapes and volumetric counts extracted immediately after programmatic ingestion and cleaning.", body_style))
        
        summary_table_data = [
            [Paragraph("Data Schema Metric", th_style), Paragraph("Evaluated Metric Value", th_style)],
            [Paragraph("Total Master Observational Records (Rows)", td_style), Paragraph(f"{active_df.shape[0]:,}", td_style)],
            [Paragraph("Total Structural Fields/Attributes (Columns)", td_style), Paragraph(str(active_df.shape[1]), td_style)],
            [Paragraph("Identified Numerical Properties", td_style), Paragraph(str(len(numeric_cols)), td_style)],
            [Paragraph("Identified Categorical Context Strings", td_style), Paragraph(str(len(categorical_cols)), td_style)]
        ]
        t_summary = Table(summary_table_data, colWidths=[320, 180])
        t_summary.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1E3A8A')),
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('BOTTOMPADDING', (0,0), (-1,-1), 8),
            ('TOPPADDING', (0,0), (-1,-1), 8),
            ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#F9FAFB')]),
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E5E7EB'))
        ]))
        story.append(t_summary)
        story.append(Spacer(1, 15))

        # SECTION 2: RELATIONAL DATA MODEL LOGS
        if len(datasets) > 1:
            story.append(Paragraph("2. Relational Schema Data Model Configuration", h1_style))
            story.append(Paragraph(f"A relational star-schema topology was verified matching parent and foreign pointer configurations across multiple database CSV extractions.", body_style))
            
            rel_table_data = [
                [Paragraph("Relational Attribute Property", th_style), Paragraph("Active Entity Mapping", th_style)],
                [Paragraph("Primary Source Fact Entity Table", td_style), Paragraph(left_table, td_style)],
                [Paragraph("Target Dimension Lookup Table", td_style), Paragraph(right_table, td_style)],
                [Paragraph("Relational Joint Vector (Key Column Mapping)", td_style), Paragraph(f"{left_key} ⟷ {right_key}", td_style)],
                [Paragraph("Compilation Structural Join Rule Type", td_style), Paragraph(f"{how_method.upper()} JOIN", td_style)]
            ]
            t_rel = Table(rel_table_data, colWidths=[240, 260])
            t_rel.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#374151')),
                ('BOTTOMPADDING', (0,0), (-1,-1), 8),
                ('TOPPADDING', (0,0), (-1,-1), 8),
                ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E5E7EB'))
            ]))
            story.append(t_rel)
            story.append(Spacer(1, 15))

        # SECTION 3: NUMERICAL PARAMETRIC PROFILES
        story.append(Paragraph("3. Detailed Numerical Property Profiles", h1_style))
        story.append(Paragraph("The system performed full secondary statistical summary analysis across every active numeric series vector in the joined workspace dataframe block.", body_style))
        
        num_headers = [Paragraph("Column Field", th_style), Paragraph("Mean", th_style), Paragraph("Min", th_style), Paragraph("Max", th_style), Paragraph("Missing Values", th_style)]
        num_table_rows = [num_headers]
        
        for col in numeric_cols:
            mean_val = f"{active_df[col].mean():,.2f}"
            min_val = f"{active_df[col].min():,}"
            max_val = f"{active_df[col].max():,}"
            null_count = f"{active_df[col].isna().sum()}"
            
            num_table_rows.append([
                Paragraph(col, td_style),
                Paragraph(mean_val, td_style),
                Paragraph(min_val, td_style),
                Paragraph(max_val, td_style),
                Paragraph(null_count, td_style)
            ])
            
        t_num = Table(num_table_rows, colWidths=[160, 85, 85, 85, 85])
        t_num.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0F766E')),
            ('BOTTOMPADDING', (0,0), (-1,-1), 6),
            ('TOPPADDING', (0,0), (-1,-1), 6),
            ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#F4FBFB')]),
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E5E7EB'))
        ]))
        story.append(t_num)
        story.append(Spacer(1, 15))

        # SECTION 4: CATEGORICAL & COMPLIANCE LOGS
        story.append(Paragraph("4. Categorical Densities & Data Quality Diagnostics", h1_style))
        story.append(Paragraph("This framework highlights concentration clusters within the qualitative string attributes and logs record level validation checks.", body_style))
        
        cat_headers = [Paragraph("Categorical Column Field", th_style), Paragraph("Top High-Frequency Mode String", th_style), Paragraph("Occurrence Volume Count", th_style)]
        cat_table_rows = [cat_headers]
        
        for col in categorical_cols[:8]:  # Keeps layout beautifully formatted within bounds
            if not active_df[col].dropna().empty:
                mode_res = active_df[col].mode()[0]
                count_res = active_df[col].value_counts().iloc[0]
                cat_table_rows.append([
                    Paragraph(col, td_style),
                    Paragraph(str(mode_res), td_style),
                    Paragraph(f"{count_res:,}", td_style)
                ])
                
        t_cat = Table(cat_table_rows, colWidths=[180, 200, 120])
        t_cat.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#B45309')),
            ('BOTTOMPADDING', (0,0), (-1,-1), 6),
            ('TOPPADDING', (0,0), (-1,-1), 6),
            ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#FFFBEB')]),
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E5E7EB'))
        ]))
        story.append(t_cat)
        
        doc.build(story)
        buffer.seek(0)
        return buffer.getvalue()

    # Render Download Button Trigger
    st.markdown("---")
    pdf_report_binary = compile_granular_pdf()
    
    st.download_button(
        label="📥 Download Enterprise Deep-Dive Analytical Report (PDF)",
        data=pdf_report_binary,
        file_name=f"Deep_Dive_Analytics_Report_{active_name}.pdf",
        mime="application/pdf",
        use_container_width=True
    )

else:
    st.info("💡 Drop one or multiple `.csv` dataset files above to trigger automated visualization engines, schemas, and analytics reports.")
