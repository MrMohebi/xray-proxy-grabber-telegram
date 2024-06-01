from telethon import TelegramClient
from dotenv import load_dotenv
import os

load_dotenv()

api_id = int(os.getenv('API_ID'))
api_hash = os.getenv('API_HASH')

if not (api_id or api_hash):
    raise Exception('You have to pass both API_ID and API_HASH env variables')

proxy = {}
if len(os.getenv('PROXY_URL')) > 2:
    p = os.getenv('PROXY_URL')
    [schema, urlPort] = p.split("://", 1)
    [url, port] = urlPort.rsplit(":", 1)
    proxy = {
        "proxy_type": schema,
        "addr": url,
        "port": int(port),
    }
    print("using proxy for telegram connection: ")
    print(proxy)

app = TelegramClient("v2ray-proxy-grabber-telegram", api_id, api_hash, proxy=proxy, auto_reconnect=True, connection_retries=20, retry_delay=5)


PROXY_CHANNELS = os.getenv('PROXY_CHANNELS').lower().split("@")
IS_DEBUG = bool(int(os.getenv('DEBUG_MODE')))
