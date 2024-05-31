import streamlit as st
import pandas as pd
from ydata_profiling import ProfileReport
import base64

# Function to generate the profile report
def generate_profile_report(df):
    profile = ProfileReport(df, title="FJ InsightPro Analytics", explorative=True)
    return profile

# Function to load data from CSV
def load_data(file_path):
    try:
        df = pd.read_csv(file_path)
        return df
    except Exception as e:
        st.error(f"An error occurred while loading the file: {e}")
        return None

# Function to download HTML report
def download_html(html_text):
    b64 = base64.b64encode(html_text.encode()).decode()
    href = f'<a href="data:text/html;base64,{b64}" download="report.html">Download HTML Report</a>'
    return href

# Main function
def main():
    # Page layout
    st.set_page_config(
        page_title="FJ InsightPro Analytics",
        page_icon=":bar_chart:",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    # Center-align the title and description
    st.markdown(
        """
        <div style="text-align: center;">
            <h1>FJ InsightPro Analytics</h1>
            <p><strong>Welcome to the FJ InsightPro Analytics!</strong></p>
            <p>This web application enables you to upload a CSV file and generate an enhanced report.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # File upload
    uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

    # If file uploaded
    if uploaded_file is not None:
        st.info("File uploaded successfully.")

        # Load data
        df = load_data(uploaded_file)

        if df is not None:
            # Generate profile report
            with st.spinner("Generating profile report..."):
                profile = generate_profile_report(df)

            # Display report
            st.subheader("Preview of the Dataset")
            st.dataframe(df.head())

            # Download HTML report
            html_report = profile.to_html()
            st.markdown(download_html(html_report), unsafe_allow_html=True)
            
            # Provide link to raw data
            st.markdown(get_table_download_link(df), unsafe_allow_html=True)
        else:
            st.warning("Please upload a valid CSV file.")
    else:
        st.info("Please upload a CSV file.")

# Function to download CSV
def get_table_download_link(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="raw_data.csv">Download Raw Data</a>'
    return href

if __name__ == "__main__":
    main()
