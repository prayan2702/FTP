import streamlit as st
st.title("Mobile se File Upload karo aur PC pe Download karo")

# File Upload
uploaded_file = st.file_uploader("Yahan File Upload Karo", type=["png", "jpg", "pdf", "txt", "csv", "xlsx"])

if uploaded_file is not None:

    file_name = uploaded_file.name

    file_bytes = uploaded_file.read()

    # Download Button

    st.download_button(

        label="Download File",

        data=file_bytes,

        file_name=file_name,

        mime="application/octet-stream"

    )
