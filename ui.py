# New CODE/ui.py

import streamlit as st
import os
from agents import run_agent
from ingest import ingest_json_file
from config import VECTOR_DB_DIR

# --- Database Initialization on First Run ---
# This function runs once and caches the result to avoid re-running.
@st.cache_resource
def initialize_database():
    """
    Checks if the vector database exists. If not, it builds it from the source data.
    """
    if not os.path.exists(VECTOR_DB_DIR):
        st.info("First-time setup: Building the vector database from source data. This may take a moment...")
        ingest_json_file()
        st.success("Database built successfully! You can now ask questions.")

# --- Main App ---

# Call the initialization function at the start of the app
initialize_database()

st.title("Multi-Agent AI System 🤖")
st.subheader("Query the executive team about the business.")

# --- User Inputs ---
role = st.selectbox(
    "Choose an agent to ask:",
    ("CEO", "CTO", "CFO", "CMO"),
    index=3 # Default to CMO
)
query = st.text_area("Enter your question:", "What are the key takeaways from the 'Chaos in Marketing' podcast?")

# --- Agent Interaction ---
if st.button(f"Ask the {role}"):
    if query:
        with st.spinner(f"Asking the {role}..."):
            try:
                # Direct call to the agent logic
                result = run_agent(role, query)

                st.info(f"**Answer from {result.get('role', 'Agent')}:**")
                st.write(result.get("answer", "No answer found."))

                st.markdown("---")
                st.subheader("Evidence Used")
                # Ensure evidence is not None before trying to display it
                evidence = result.get("evidence_used", "No evidence data provided.")
                if evidence:
                    st.json(evidence)
                else:
                    st.write(evidence)

            except Exception as e:
                st.error(f"An unexpected error occurred: {e}")
    else:
        st.warning("Please enter a question before asking the agent.")