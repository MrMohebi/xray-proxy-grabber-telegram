from client import app

@app.on_message
def from_proxy_channels(client, message):
    print(message.text)



