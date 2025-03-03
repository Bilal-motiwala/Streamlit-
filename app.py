import streamlit as st  # type: ignore
import pandas as pd  # type: ignore
import os
from io import BytesIO

st.set_page_config(page_title="Data Sweeper", layout='wide')
st.title("📀 Data Sweeper")
st.write("Transform your files between CSV and Excel formats with built-in cleaning and visualization!")

uploaded_files = st.file_uploader(
    "Upload your files (CSV or Excel):",
    type=["csv", "xlsx"],
    accept_multiple_files=True
)

if uploaded_files:
    st.write(f"Uploaded {len(uploaded_files)} files.")

    for uploaded_file in uploaded_files:
        st.write(f"**File Name:** {uploaded_file.name}")
        st.write(f"**File Size:** {uploaded_file.size / 1024:.2f} KB")

        # Load file into a DataFrame
        file_ext = os.path.splitext(uploaded_file.name)[1]  # Get the file extension
        if file_ext == ".csv":
            df = pd.read_csv(uploaded_file)
        else:  # Assume it's an Excel file
            df = pd.read_excel(uploaded_file)

        # Show 5 rows of the dataframe
        st.write("Preview of the DataFrame:")
        st.dataframe(df.head())

        # Data Cleaning Options
        st.subheader("Data Cleaning Options")
        if st.checkbox(f"Clean Data for {uploaded_file.name}"):
            col1, col2 = st.columns(2)

            with col1:
                if st.button(f"Remove Duplicates from {uploaded_file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.write("✅ Duplicates Removed!")
                    st.dataframe(df.head())

            with col2:
                if st.button(f"Fill Missing Values for {uploaded_file.name}"):
                    numeric_cols = df.select_dtypes(include=['number']).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.write("✅ Missing Values Filled!")
                    st.dataframe(df.head())

            # Choose Specific Columns to Keep
            st.subheader("Select Columns to Keep")
            columns = st.multiselect(f"Choose Columns for {uploaded_file.name}", df.columns, default=df.columns)
            df = df[columns]

            # Data Visualization
            st.subheader("📊 Data Visualization")
            if st.checkbox(f"Show Visualization for {uploaded_file.name}"):
                st.bar_chart(df.select_dtypes(include='number').iloc[:, :2])

            # File Conversion
            st.subheader("🔄 Conversion Options")
            conversion_type = st.radio(f"Convert {uploaded_file.name} to:", ["CSV", "Excel"], key=uploaded_file.name)

            if st.button(f"Convert {uploaded_file.name}"):
                buffer = BytesIO()

                if conversion_type == "CSV":
                    df.to_csv(buffer, index=False)
                    buffer.seek(0)
                    new_filename = uploaded_file.name.replace(file_ext, ".csv")
                    mime_type = "text/csv"

                elif conversion_type == "Excel":
                    df.to_excel(buffer, index=False, engine='xlsxwriter')
                    buffer.seek(0)
                    new_filename = uploaded_file.name.replace(file_ext, ".xlsx")
                    mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

                # Provide a download link
                st.download_button(
                    label=f"Download {new_filename}",
                    data=buffer,
                    file_name=new_filename,
                    mime=mime_type
                )


st.success("🎉 All files processed!")