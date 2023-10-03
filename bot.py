from dotenv import dotenv_values
import openai
import logging
from telegram import Update, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes , MessageHandler, filters, InlineQueryHandler
config = dotenv_values(".env")


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

#Initialize OPENAI and config
openai.api_key = config["OPENAI_API_KEY"]
MODEL_ENGINE = "gpt-3.5-turbo"

#we define a function that should process a specific type of update:
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=
        """Hi there I'm HealthServeAI, ask me any questions about HealthServe. I'm here to ensure you have a proper onboarding!""")
    
async def getResponse(user_input: str):
    CONVERSATIONS = []
    CONVERSATIONS.append({'role':'user', 'content':user_input})
    # Use OpenAI's ChatCompletion API to get the chatbot's response
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # The name of the OpenAI chatbot model to use
            messages=CONVERSATIONS,   # The conversation history up to this point, as a list of dictionaries
            max_tokens=3800,        # The maximum number of tokens (words or subwords) in the generated response
            stop=None,              # The stopping sequence for the generated response, if any (not used here)
            temperature=0.7,        # The "creativity" of the generated response (higher temperature = more creative)
        )

    # Find the first response from the chatbot that has text in it (some responses may not have text)
        for choice in response.choices:
            if "text" in choice:
                return choice.text

        # If no response with text is found, return the first response's content (which may be empty)
        return response.choices[0].message.content
    except Exception as error_msg:
        return "Sorry I was unable to generate a response form openAI"

async def chat_handler(update: Update, context: ContextTypes.DEFAULT_TYPE): # Define the chat message handler
    messageFromUser = update.message.text.strip()
    responseFromOpenAi = await getResponse(messageFromUser)
    await update.message.reply_text(responseFromOpenAi) # Send the response to the user

async def caps(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text_caps = ' '.join(context.args).upper()
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)

async def inline_caps(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.inline_query.query
    if not query:
        return
    results = []
    results.append(
        InlineQueryResultArticle(
            id=query.upper(),
            title='Caps',
            input_message_content=InputTextMessageContent(query.upper())
        )
    )
    await context.bot.answer_inline_query(update.inline_query.id, results)

async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")


if __name__ == '__main__':
    application = ApplicationBuilder().token(config["TELEGRAM_API_KEY"]).build()

   
    caps_handler = CommandHandler('caps', caps)
    chat_handler = MessageHandler(filters.TEXT &  (~filters.COMMAND), chat_handler)
    inline_caps_handler = InlineQueryHandler(inline_caps)
    unknown_handler = MessageHandler(filters.COMMAND, unknown)
    
    start_handler = CommandHandler('start', start)
    

    application.add_handler(start_handler)
    application.add_handler(caps_handler)
    application.add_handler(inline_caps_handler)
    #This handler must be added last
    application.add_handler(chat_handler)
    application.add_handler(unknown_handler)

    application.run_polling()
