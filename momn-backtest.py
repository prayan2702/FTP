import streamlit as st
import os

st.title("Upload from Mobile & Download on PC")

# Cloud Storage Alternative
UPLOAD_FOLDER = "shared_files"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Upload Section
uploaded_file = st.file_uploader("Upload a file", type=["png", "jpg", "pdf", "txt", "csv", "xlsx"])

if uploaded_file is not None:
    file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)

    # Save file
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.session_state["last_uploaded_file"] = uploaded_file.name  # Save filename in session

    st.success(f"File `{uploaded_file.name}` uploaded successfully!")
    st.write("You can now download this file from another device.")

# Download Section (Accessible from Any Device)
if "last_uploaded_file" in st.session_state:
    latest_file = os.path.join(UPLOAD_FOLDER, st.session_state["last_uploaded_file"])

    with open(latest_file, "rb") as f:
        file_bytes = f.read()

    st.download_button(
        label="Download Last Uploaded File",
        data=file_bytes,
        file_name=st.session_state["last_uploaded_file"],
        mime="application/octet-stream"
    )
