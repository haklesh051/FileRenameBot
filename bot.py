import logging
import os
from flask import Flask, request
from pyrogram import Client

# Logging setup
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)
logging.getLogger("pyrogram").setLevel(logging.WARNING)

# Config import
if bool(os.environ.get("WEBHOOK", False)):
    from sample_config import Config
else:
    from config import Config

# Flask app
server = Flask(__name__)

# Pyrogram client
plugins = dict(root="plugins")
app = Client(
    "RenameBot",
    bot_token=Config.TG_BOT_TOKEN,
    api_id=Config.APP_ID,
    api_hash=Config.API_HASH,
    plugins=plugins
)

Config.AUTH_USERS.add(6132794263)

@app.on_message()
def handle_all(client, message):
    # Example handler (aapke plugins already kaam karenge)
    logger.info(f"Message from {message.from_user.id}: {message.text}")

# Flask route for Telegram webhook
@server.route(f"/{Config.TG_BOT_TOKEN}", methods=["POST"])
def webhook():
    update = request.get_json(force=True)
    app.process_update(update)
    return "ok"

if __name__ == "__main__":
    if not os.path.isdir(Config.DOWNLOAD_LOCATION):
        os.makedirs(Config.DOWNLOAD_LOCATION)

    # Flask ko Render ke port par run karna
    port = int(os.environ.get("PORT", 5000))
    server.run(host="0.0.0.0", port=port)
