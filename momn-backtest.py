import streamlit as st
import os

st.title("Mobile se File Upload Karo, PC se Download Karo")
# File Upload

uploaded_file = st.file_uploader("Yahan File Upload Karo", type=["png", "jpg", "pdf", "txt", "csv", "xlsx"])

if uploaded_file is not None:

    file_name = uploaded_file.name

    file_path = os.path.join("shared_files", file_name)

    # Ensure directory exists

    os.makedirs("shared_files", exist_ok=True)

    # Save file locally

    with open(file_path, "wb") as f:

        f.write(uploaded_file.getbuffer())

    # Create a public download link

    download_link = f"https://your-streamlit-app-url/shared_files/{file_name}"

    st.success("File Uploaded Successfully!")

    st.markdown(f"**Download from PC using this link:** [Download {file_name}]({download_link})")
