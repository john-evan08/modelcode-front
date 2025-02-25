import streamlit as st
import httpx

# Base API URL
API_URL = "http://localhost:8000"

# API Endpoints
SET_PROJECT_URL = f"{API_URL}/set_project"
ANSWER_URL = f"{API_URL}/project/answer"

# Streamlit App Title
st.title("Code Repo Q&A")

# Set Project Section
st.subheader("Set Project")
project_name = st.text_input("Enter Project Root Path")

if st.button("Set Project"):
    if project_name:
        try:
            response = httpx.post(
                SET_PROJECT_URL, json={"root_path": project_name}, timeout=30
            )
            if response.status_code == 200:
                st.success("Project set successfully!")
            else:
                st.error(f"Failed to set project: {response.text}")
        except httpx.RequestError as e:
            st.error(f"Request failed: {e}")
    else:
        st.warning("Please enter a project root path.")

# Ask Question Section
st.subheader("Ask a Question")
question = st.text_area("Enter your question about the project")

if st.button("Get Answer"):
    if project_name and question:
        try:
            response = httpx.post(ANSWER_URL, json={"q": question}, timeout=30)

            if response.status_code == 200:
                answer = response.json().get("answer", "No answer received.")
                st.markdown(answer)  # Display answer as Markdown
            else:
                st.error(f"Failed to get answer: {response.text}")
        except httpx.RequestError as e:
            st.error(f"Request failed: {e}")
    else:
        st.warning("Please set a project and enter a question.")
