import requests
import json
from sseclient import SSEClient

def send_message(session, text, conversation_id, cookies):
    """Send a message to the AI and handle the response stream."""
    url = 'https://pi.ai/api/chat'
    payload = {
        "text": text,
        "conversation": conversation_id
    }
    payload_str = json.dumps(payload)  # Serialize the payload to a JSON string
    content_length = str(len(payload_str.encode('utf-8')))  # Calculate the content length

    headers = {
        'Accept': 'text/event-stream',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Accept-Language': 'en-US,en;q=0.9',
        'Content-Type': 'application/json',
        'Content-Length': content_length,
        'Cookie': cookies,  # Pass cookies as a parameter
        'Origin': 'https://pi.ai',
        'Referer': 'https://pi.ai/talk',
        'Sec-Ch-Ua': '"Chromium";v="124", "Microsoft Edge";v="124", "Not-A.Brand";v="99"',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Platform': "Windows",
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0',
        'X-Api-Version': '3'
    }

    response = session.post(url, headers=headers, data=payload_str, stream=True)
    return response

def handle_response(response):
    """Process the SSE stream and extract AI responses."""
    client = SSEClient(response)
    all_data = []
    for event in client.events():
        all_data.append(event.data)  # Collect all data first

    # Now process the collected data
    message_buffer = ""
    for data in all_data:
        parsed_data = json.loads(data)
        if 'text' in parsed_data:
            message_buffer += parsed_data['text']

    if message_buffer:
        print("Complete AI Response:", message_buffer)

def chat_with_ai(conversation_id, cookies):
    session = requests.Session()

    print("Chat with AI (type 'exit' to quit)")
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            break

        response = send_message(session, user_input, conversation_id, cookies)
        if response.ok:
            handle_response(response)
        else:
            print('Failed to send message:', response.status_code)

if __name__ == "__main__":
    conversation_id = input("Enter conversation ID: ")
    cookies = input("Enter cookies: ")
    chat_with_ai(conversation_id, cookies)
