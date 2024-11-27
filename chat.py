import os
import requests
from lyzr_agent_api.client import AgentAPI
from lyzr_agent_api.models.chat import ChatRequest
from dotenv import load_dotenv

load_dotenv()
LYZR_API_KEY = os.getenv("LYZR_API_KEY")

lyzr_client = AgentAPI(x_api_key=LYZR_API_KEY)
def retrieve_data(query):
    url = 'https://rag-agent-api.dev.app.lyzr.ai/rag/retrieve/127754123179824'
    params = {'query': query}
    headers = {'accept': 'application/json'}

    response = requests.get(url, params=params, headers=headers)

    if response.status_code == 200:
        texts = [result['text'] for result in response.json().get('results', [])]
        return texts
    else:
        print(f"Error: {response.status_code}")
        return None

def call_lyzragent(question, session):

    response = lyzr_client.chat_with_agent(
        json_body=ChatRequest(
            user_id="harshit@lyzr.ai",
            agent_id="672d071761f92e3cfeebacd2",  # Replace with the actual agent ID
            message=question,
            session_id=session,
        )
    )

    return response['response']
