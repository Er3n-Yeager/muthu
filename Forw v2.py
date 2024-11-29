from pyrogram import Client, filters
from pyrogram.types import Message
from apscheduler.schedulers.background import BackgroundScheduler
import requests

scheduler= BackgroundScheduler()

api_id = "12862156"
api_hash = "d913a2ef10183c683144ff851481d9fd"
bot_token = "7785098411:AAHWRxYtmE1LVQ3C6HYn14Aph46Tkp7oF_w"
private_channel_id = "-1002379931772"   # Use the channel ID or username (e.g., "@your_channel")

app = Client("my_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

# Dictionary to store caption words and PDF files for users
user_data = {}

@app.on_message(filters.command("caption"))
def set_caption(client, message: Message):
    # Store the caption words
    caption = message.text.split(maxsplit=1)
    if len(caption) > 1:
        user_data[message.from_user.id] = {"caption": caption[1], "pdfs": []}
        message.reply_text(f"Caption set to: {caption[1]}")
    else:
        message.reply_text("Please provide caption words after /caption.")

@app.on_message(filters.document)
def store_pdf(client, message: Message):
    user_id = message.from_user.id
    if user_id in user_data:
        # Append the PDF file to the user's list
        user_data[user_id]["pdfs"].append(message.document.file_id)
        message.reply_text("PDF added to your list.")

@app.on_message(filters.command("done"))
def forward_pdfs(client, message: Message):
    user_id = message.from_user.id
    if user_id not in user_data or not user_data[user_id]["pdfs"]:
        message.reply_text("You need to set a caption and send at least one PDF first using /caption.")
        return

    # Retrieve the caption and PDF files for the user
    caption = user_data[user_id]["caption"]
    pdfs = user_data[user_id]["pdfs"]

    # Forward all PDFs to the private channel with the provided caption
    for pdf_file_id in pdfs:
        app.send_document(chat_id=private_channel_id, document=pdf_file_id, caption=caption)

    # Clear user data after processing
    del user_data[user_id]
    message.reply_text("PDFs forwarded successfully!")

def ping_server():
    # This function can make a simple request to a lightweight endpoint
    try:
        requests.get("https://eren-v2.onrender.com")  # Ping a test endpoint
        print("Ping successful")
    except requests.RequestException as e:
        print(f"Ping failed: {e}")

if __name__ == "__main__":
    scheduler.add_job(ping_server, 'interval', minutes=14)  # Schedule the ping_server function every 14 minutes
    scheduler.start()  # Start the scheduler
    app.run()
