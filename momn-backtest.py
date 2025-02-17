import streamlit as st
import os

st.title("📂 Mobile se Upload Karo, PC se Download Karo")

# Shared Folder for Uploaded Files
UPLOAD_FOLDER = "shared_files"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Upload Section (Mobile ya PC se)
uploaded_file = st.file_uploader("File Upload Karo", type=["png", "jpg", "pdf", "txt", "csv", "xlsx"])

if uploaded_file is not None:
    file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)

    # Save file in shared folder
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.success(f"✅ File `{uploaded_file.name}` successfully uploaded!")
    st.experimental_rerun()  # Refresh app so that PC session can see new files

# Show List of Available Files for Download
st.subheader("📥 Available Files for Download")

files = os.listdir(UPLOAD_FOLDER)
if files:
    for file in files:
        file_path = os.path.join(UPLOAD_FOLDER, file)
        with open(file_path, "rb") as f:
            file_bytes = f.read()

        st.download_button(
            label=f"⬇️ Download {file}",
            data=file_bytes,
            file_name=file,
            mime="application/octet-stream"
        )
else:
    st.info("📁 No files uploaded yet. Upload a file to see it here.")
