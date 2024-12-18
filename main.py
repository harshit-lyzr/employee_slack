import os
from openai import OpenAI
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_sdk import WebClient
from slack_bolt import App
from dotenv import load_dotenv
from chat import retrieve_data, call_lyzragent


load_dotenv()
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_APP_TOKEN = os.getenv("SLACK_APP_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Event API & Web API
app = App(token=SLACK_BOT_TOKEN)
client = WebClient(SLACK_BOT_TOKEN)
client1 = OpenAI(api_key=OPENAI_API_KEY)


# This gets activated when the bot is tagged in a channel
@app.event("app_mention")
def handle_message_events(body):
    # Extract message prompt
    prompt = str(body["event"]["text"]).split(">")[1]

    # Determine if the message is part of a thread
    is_thread = 'thread_ts' in body['event']
    sessions_id = body['event'].get('thread_ts', body['event']['ts'])

    # Helper function for posting messages
    def post_message_with_attachments(channel, ts, session_id):
        message = call_lyzragent(prompt, session_id)
        data = retrieve_data(query=prompt)
        attachments = [
            {
                "color": "#f2c744",
                "blocks": [
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": item
                        }
                    }
                ]
            } for item in data[:3]
        ]
        client.chat_postMessage(
            channel=channel,
            thread_ts=ts,
            text=f"\n{message} \n\n*Sources:*",
            attachments=attachments
        )

    # Post message based on thread status
    if is_thread:
        post_message_with_attachments(body["event"]["channel"], body["event"]["event_ts"], sessions_id)
    else:
        # Initial response for non-threaded mentions
        client.chat_postMessage(
            channel=body["event"]["channel"],
            thread_ts=body["event"]["event_ts"],
            text="Hello and welcome to Employee Support! :blush: \n\nJust a moment while I gather the info you need—thank you for your patience!"
        )
        post_message_with_attachments(body["event"]["channel"], body["event"]["event_ts"], sessions_id)



if __name__ == "__main__":
    SocketModeHandler(app, SLACK_APP_TOKEN).start()