import openai
import random
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

# Load the sentiment analyzer from NLTK
sia = SentimentIntensityAnalyzer()

# Your OpenAI API key (replace 'your-openai-api-key' with your actual key)
openai.api_key = 'your-openai-api-key'

# Define the bot's initial price range
MIN_PRICE = 100
MAX_PRICE = 500
BOT_INITIAL_PRICE = random.randint(MIN_PRICE, MAX_PRICE)

def get_sentiment(text):
    """Analyze the sentiment of the user's input."""
    sentiment_score = sia.polarity_scores(text)
    if sentiment_score['compound'] >= 0.05:
        return "positive"
    elif sentiment_score['compound'] <= -0.05:
        return "negative"
    else:
        return "neutral"

def generate_bot_response(user_offer, user_message):
    """Generate a response from the bot using GPT-3."""
    sentiment = get_sentiment(user_message)
    
    # Construct a prompt for the GPT-3 model
    prompt = f"""You are a supplier. A customer has offered {user_offer}. Respond politely by either accepting, rejecting, or counteroffering.
    Consider giving a discount if the customer is polite. Your initial price is {BOT_INITIAL_PRICE}."""
    
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",  # Use GPT-3
            prompt=prompt,
            max_tokens=150
        )
        bot_response = response.choices[0].text.strip()
    except Exception as e:
        bot_response = f"An error occurred during the negotiation: {str(e)}"

    return bot_response, sentiment

# Start a simple negotiation chat loop
print(f"Supplier's initial price: {BOT_INITIAL_PRICE}")

def chat():
    while True:
        try:
            # Take user input
            user_offer = int(input("Enter your offer: "))
            user_message = input("Enter your message to the supplier: ")
        
            # Generate bot response
            bot_response, sentiment = generate_bot_response(user_offer, user_message)
        
            print(f"\nSupplier's response: {bot_response}")
            print(f"Detected sentiment: {sentiment}\n")
        
            # Check if the user wants to continue
            continue_negotiating = input("Do you want to continue negotiating? (yes/no): ").strip().lower()
            if continue_negotiating != "yes":
                print("Thank you for negotiating!")
                break
        except ValueError:
            print("Please enter a valid number for your offer.")
