from pyrogram import Client, filters
from pyrogram.types import Message

api_id = "12862156"
api_hash = "d913a2ef10183c683144ff851481d9fd"
bot_token = "7300417256:AAEpjRkzBMSstvSp18J9-A875HbLA18HL40"
private_channel_id = "-1002379931772"  # Use the channel ID or username (e.g., "@your_channel")

app = Client("my_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

# Dictionary to store caption words for users
user_captions = {}

@app.on_message(filters.command("caption"))
def set_caption(client, message: Message):
    # Store the caption words
    caption = message.text.split(maxsplit=1)
    if len(caption) > 1:
        user_captions[message.from_user.id] = caption[1]
        message.reply_text(f"Caption set to: {caption[1]}")
    else:
        message.reply_text("Please provide caption words after /caption.")

@app.on_message(filters.command("done"))
def forward_pdfs(client, message: Message):
    user_id = message.from_user.id
    if user_id not in user_captions:
        message.reply_text("You need to set a caption first using /caption.")
        return

    # Retrieve the caption for the user
    caption = user_captions[user_id]
    
    # Iterate over messages in the chat to find PDFs sent after /caption
    for msg in app(message.chat.id):
        if msg.document and msg.document.mime_type == "application/pdf":
            # Forward PDF to the private channel
            .send_document(chat_id=private_channel_id, document=msg.document.file_id, caption=caption)
    
    # Clear user caption after processing
    del user_captions[user_id]
    message.reply_text("PDFs forwarded successfully!")

@app.on_message(filters.document & filters.private)
def handle_docs(client, message: Message):
    user_id = message.from_user.id
    if user_id not in user_captions:
        message.reply_text("You need to set a caption first using /caption.")
        return

app.run()
