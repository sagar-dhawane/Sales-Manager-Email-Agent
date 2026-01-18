import os
from dotenv import load_dotenv

# Load the .env file from the root directory
load_dotenv(override=True)

# Export keys for other modules to use
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
SENDER_EMAIL = "sagardhawane123@gmail.com" # Your sender email
TARGET_EMAIL = "sagardhawane1000@gmail.com" # Your testing target