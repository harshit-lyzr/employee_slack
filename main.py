import os
from openai import OpenAI
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_sdk import WebClient
from slack_bolt import App
from lyzr_agent_api.client import AgentAPI
from lyzr_agent_api.models.chat import ChatRequest
from dotenv import load_dotenv

load_dotenv()
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_APP_TOKEN = os.getenv("SLACK_APP_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
LYZR_API_KEY = os.getenv("LYZR_API_KEY")


lyzr_client = AgentAPI(x_api_key=LYZR_API_KEY)

# Event API & Web API
app = App(token=SLACK_BOT_TOKEN)
client = WebClient(SLACK_BOT_TOKEN)
client1 = OpenAI(api_key=OPENAI_API_KEY)


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


# This gets activated when the bot is tagged in a channel
@app.event("app_mention")
def handle_message_events(body, logger):

    # Log message
    print(str(body["event"]["text"]).split(">")[1])

    # Create prompt for ChatGPT
    prompt = str(body["event"]["text"]).split(">")[1]

    # Let thre user know that we are busy with the request 
    # response = client.chat_postMessage(channel=body["event"]["channel"],
    #                                    thread_ts=body["event"]["event_ts"],
    #                                    text=f"Hello from your Employee Suport Agent! 😄 \nKeep an eye out—I’ll be back soon!")


    if 'thread_ts' in body['event']:
        session_id = body['event']['thread_ts']
        print("thread: ", session_id)
        print("TS: ", body['event']['ts'])
        message = call_lyzragent(prompt, session_id)
        response = client.chat_postMessage(channel=body["event"]["channel"],
                                           thread_ts=body["event"]["event_ts"],
                                           text=f"\n{message}")
    else:
        client.chat_postMessage(channel=body["event"]["channel"],
                                thread_ts=body["event"]["event_ts"],
                                text=f"Hello and welcome to Employee Support! 😊 \nJust a moment while I gather the info you need—thank you for your patience!")
        print("TS: ", body['event']['ts'])
        session_id = body['event']['ts']
        message = call_lyzragent(prompt, session_id)
        response = client.chat_postMessage(channel=body["event"]["channel"],
                                           thread_ts=body["event"]["event_ts"],
                                           text=f"\n{message}")
    # Check ChatGPT
    # openai.api_key = OPENAI_API_KEY
    # message = call_chatagent(prompt)

    # print(body["event"]["event_ts"])
    #
    # # Reply to thread
    # response = client.chat_postMessage(channel=body["event"]["channel"],
    #                                    thread_ts=body["event"]["event_ts"],
    #                                    text=f"\n{message}")


if __name__ == "__main__":
    SocketModeHandler(app, SLACK_APP_TOKEN).start()