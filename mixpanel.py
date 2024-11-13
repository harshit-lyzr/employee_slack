import requests


def send_mixpanel_event(query, user_id,email, username, processing_time, is_thread, event="User Query"):
    url = "https://api.mixpanel.com/track?ip=1"

    payload = [
        {
            "properties": {
                "token": "678f1abb780477a49cf430386970d9cd",
                "distinct_id": user_id,
                "query": query,
                "email": email,
                'slack_username': username,
                'time_taken': processing_time,
                'new_thread': is_thread
            },
            "event": event
        }
    ]

    headers = {
        "accept": "text/plain",
        "content-type": "application/json"
    }

    # Send the POST request
    response = requests.post(url, json=payload, headers=headers)

    return response.json()
