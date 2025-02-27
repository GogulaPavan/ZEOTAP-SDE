import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def set_page_style():
    st.markdown(
        """
        <style>
        .stDataFrame { border-radius: 10px; overflow: hidden; }
        .stSidebar { background-color: #f0f2f6; padding: 10px; border-radius: 10px; }
        .stButton>button { background-color: #007bff; color: white; border-radius: 5px; }
        .stButton>button:hover { background-color: #0056b3; }
        .stSelectbox, .stTextInput { border-radius: 5px; }
        </style>
        """,
        unsafe_allow_html=True,
    )

def main():
    set_page_style()
    st.title("Google Sheets Clone")
    
    # Initialize session state for spreadsheet
    if 'data' not in st.session_state:
        # Initialize DataFrame with object dtype to allow mixed data types
        st.session_state.data = pd.DataFrame(index=range(10), columns=[chr(65+i) for i in range(5)], dtype=object)
    
    df = st.session_state.data
    
    # Display editable spreadsheet
    edited_df = st.data_editor(df, num_rows="dynamic", key="spreadsheet")
    
    st.session_state.data = edited_df
    
    # Sidebar for functions
    st.sidebar.header("Mathematical Functions")
    function = st.sidebar.selectbox("Select Function", ["SUM", "AVERAGE", "MAX", "MIN", "COUNT", "MEDIAN", "MODE", "PRODUCT"])
    
    col = st.sidebar.selectbox("Select Column", df.columns)
    
    if st.sidebar.button("Apply Function"):
        numeric_values = pd.to_numeric(df[col], errors='coerce')
        if function == "SUM":
            result = numeric_values.sum()
        elif function == "AVERAGE":
            result = numeric_values.mean()
        elif function == "MAX":
            result = numeric_values.max()
        elif function == "MIN":
            result = numeric_values.min()
        elif function == "COUNT":
            result = numeric_values.count()
        elif function == "MEDIAN":
            result = numeric_values.median()
        elif function == "MODE":
            result = numeric_values.mode()[0] if not numeric_values.mode().empty else "N/A"
        elif function == "PRODUCT":
            result = numeric_values.prod()
        st.sidebar.write(f"Result: {result}")
    
    # Data Quality Functions
    st.sidebar.header("Data Quality Functions")
    dq_function = st.sidebar.selectbox("Select Function", ["TRIM", "UPPER", "LOWER", "REMOVE_DUPLICATES", "FIND_AND_REPLACE"])
    
    if dq_function in ["TRIM", "UPPER", "LOWER"]:
        if st.sidebar.button("Apply"):
            if dq_function == "TRIM":
                df[col] = df[col].astype(str).str.strip()
            elif dq_function == "UPPER":
                df[col] = df[col].astype(str).str.upper()
            elif dq_function == "LOWER":
                df[col] = df[col].astype(str).str.lower()
            st.session_state.data = df
            st.sidebar.success("Function Applied!")
    
    elif dq_function == "REMOVE_DUPLICATES":
        if st.sidebar.button("Remove Duplicates"):
            df.drop_duplicates(inplace=True)
            st.session_state.data = df
            st.sidebar.success("Duplicates Removed!")
    
    elif dq_function == "FIND_AND_REPLACE":
        find_text = st.sidebar.text_input("Find")
        replace_text = st.sidebar.text_input("Replace With")
        if st.sidebar.button("Replace"):
            df.replace(find_text, replace_text, inplace=True)
            st.session_state.data = df
            st.sidebar.success("Text Replaced!")
    
    # Save & Load
    st.sidebar.header("Save & Load")
    if st.sidebar.button("Download CSV"):
        csv = df.to_csv(index=False).encode('utf-8')
        st.sidebar.download_button(label="Download Spreadsheet", data=csv, file_name="spreadsheet.csv", mime="text/csv")
    
    uploaded_file = st.sidebar.file_uploader("Upload CSV", type=["csv"])
    if uploaded_file is not None:
        st.session_state.data = pd.read_csv(uploaded_file)
        st.sidebar.success("Spreadsheet Loaded!")
    
    # Data Visualization
    st.sidebar.header("Data Visualization")
    chart_type = st.sidebar.selectbox("Select Chart Type", ["Bar Chart", "Line Chart", "Pie Chart"])
    chart_col = st.sidebar.selectbox("Select Column for Chart", df.columns)
    
    if st.sidebar.button("Generate Chart"):
        fig, ax = plt.subplots()
        data = pd.to_numeric(df[chart_col], errors='coerce').dropna()
        
        if chart_type == "Bar Chart":
            ax.bar(data.index, data.values)
        elif chart_type == "Line Chart":
            ax.plot(data.index, data.values)
        elif chart_type == "Pie Chart":
            ax.pie(data, labels=data.index, autopct='%1.1f%%')
        
        st.pyplot(fig)
    
if __name__ == "__main__":
    main()