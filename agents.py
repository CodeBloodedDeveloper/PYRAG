# agents.py
from retriever import retrieve
from config import CHAT_MODEL, get_genai_client

# Add "Format your response using Markdown" to each prompt
AGENT_SYSTEM_PROMPTS = {
    "CEO": "You are the CEO agent. Provide strategic guidance grounded in evidence when possible. Format your response using Markdown.",
    "CTO": "You are the CTO agent. Focus on tech feasibility and architecture. Format your response using Markdown.",
    "CFO": "You are the CFO agent. Be conservative with financials. Format your response using Markdown.",
    "CMO": "You are the CMO agent, a seasoned and supportive marketing leader. Use evidence where available. Format your response using Markdown.",
}

# ... the rest of your agents.py file remains the same ...

def run_agent(role: str, query: str):
    """
    Runs a generative AI agent for a specific role.
    The agent uses retrieved documents to inform its personality and context,
    but it will always answer the user's query using its general knowledge.
    """
    genai = get_genai_client()
    docs, digest = retrieve(query, k=5, return_digest=True)

    system_prompt = AGENT_SYSTEM_PROMPTS.get(role.upper(), "You are a business advisor.")

    # Build a new, less restrictive prompt
    prompt_parts = [system_prompt]

    if docs and len(docs) > 0:
        # If evidence exists, frame it as helpful context, not a strict rule.
        prompt_parts.append(
            f"\nUse the following evidence to help inform your answer and adopt your persona. "
            f"Always provide a comprehensive answer to the user's query based on your broad knowledge."
            f"\n\n--- Evidence ---\n{digest}\n------------------"
        )
    else:
        # If no evidence is found, instruct the model to answer from general knowledge.
        prompt_parts.append(
            "\nNo specific evidence was found for this query. "
            "Please answer based on your general expertise and assigned role."
        )

    # Add the user's query to the end of the prompt
    prompt_parts.append(f"\nQuery: {query}")

    # Combine all parts into the final prompt
    final_prompt = "\n".join(prompt_parts)
    
    response = genai.GenerativeModel(CHAT_MODEL).generate_content(final_prompt)
    
    return {
        "role": role,
        "answer": response.text,
        "evidence_used": docs if docs else "❌ No evidence, fallback to freeform Gemini"
    }
