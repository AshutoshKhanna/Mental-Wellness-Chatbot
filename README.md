# Mental Wellness Chatbot

This is a Flask application that provides a mental health companion chatbot to help users with their mental wellness issues. The chatbot utilizes the Google Generative AI API to generate responses based on user input and a predefined prompt.
![Mental Wellness Chatbot](/saarthi2.png "Mental Wellness Chatbot")
## Features

- Google OAuth2 authentication for user login
- Voice input recognition using Google Speech Recognition API
- Text-based chat interface for users to interact with the mental health companion chatbot

## Installation

1. Clone the repository:git clone https://github.com/your-repo/mental-wellness-chatbot.git
2. Navigate to the project directory:cd mental-wellness-chatbot
3. Create a virtual environment and activate it:python3 -m venv venv
source venv/bin/activate  # On Windows, use venv\Scripts\activate
4. Install the required dependencies:pip install -r requirements.txt
5. Create a `.env` file in the project directory and add your Google API key:GOOGLE_API_KEY=your-google-api-key CONSUMER_KEY=your-google-consumer-key CONSUMER_SECRET=your-google-consumer-secret
6. Run the Flask application:python app.py
   The application will be running at `http://localhost:5000`.

## Usage

1. Open the application in your web browser at `http://localhost:5000`.
2. Click the "Login" button and follow the prompts to authenticate with your Google account.
3. Once authenticated, you can interact with the mental health companion chatbot by typing your messages in the chat interface.
4. The chatbot will respond with well-structured JSON responses, where each paragraph is represented as a separate object.
5. You can also provide voice input by clicking the microphone icon and speaking into your device's microphone.

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.


      
