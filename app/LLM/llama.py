from langchain_community.llms import Ollama
from langchain.agents import initialize_agent, AgentType
from app.helper.json_cleaner import safe_json_parse
import json
import sys

llm = Ollama(model="llama3.2:3b")
def call_llm_no_retrive(prompt: str):
    try:
        response = llm.invoke(prompt)

        # Ambil teks
        response_text = getattr(response, "content", str(response)).strip()

        # Bersihkan markdown
        if response_text.startswith("```"):
            response_text = response_text.split("\n", 1)[-1].rsplit("```", 1)[0].strip()

        # Parse aman
        return safe_json_parse(response_text)

    except Exception as e:
        print(f"[Ollama Error] {e}", file=sys.stderr)
        return None
    



def llm_tool_calling(tools, prompt):
    agent = initialize_agent(
        tools,
        llm,
        agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True
    )
    answer = agent.run(prompt)
    return answer
    
