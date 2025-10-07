# New CODE/ui.py

import streamlit as st
import os
from agents import run_agent
from ingest import ingest_json_file
from config import VECTOR_DB_DIR

# --- Database Initialization on First Run ---
# This is a simple, robust check that runs each time the app starts.
# If the database directory doesn't exist, it gets created.
if not os.path.exists(VECTOR_DB_DIR):
    with st.spinner("First-time setup: Building the vector database from source data. This may take a moment..."):
        ingest_json_file()
    st.success("Database built successfully! You can now ask questions.")
    # A small trick to stop and rerun the app after the database is built,
    # ensuring all components load correctly.
    st.rerun()

# --- Main App ---

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
                st.write(result.get('answer', "No answer found."))

                st.markdown("---")
                st.subheader("Evidence Used")
                evidence = result.get("evidence_used", "No evidence data provided.")
                if evidence and isinstance(evidence, (list, dict)):
                    st.json(evidence)
                else:
                    st.write(evidence)

            except Exception as e:
                st.error(f"An unexpected error occurred: {e}")
    else:
        st.warning("Please enter a question before asking the agent.")
