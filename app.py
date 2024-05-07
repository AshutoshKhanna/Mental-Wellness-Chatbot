from flask import Flask, request, jsonify, render_template, session, redirect, url_for
from flask_oauthlib.client import OAuth
import speech_recognition as sr
import google.generativeai as genai
from dotenv import load_dotenv
import tempfile
import json
import requests 
import os

app = Flask(__name__, static_url_path='/static')
app.secret_key = os.urandom(24) 

load_dotenv()  # Load environment variables
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

oauth = OAuth(app)
google = oauth.remote_app(
    'google',
    consumer_key= os.getenv('CONSUMER_KEY'),
    consumer_secret= os.getenv('CONSUMER_SECRET'),
    request_token_params={
        'scope': 'email',
    },
    base_url='https://www.googleapis.com/oauth2/v1/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',   
)

@app.after_request
def add_no_cache_headers(response):
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response

@app.route('/')
def index():
    if 'google_token' in session:
        return render_template('index.html')
    else:
        return redirect(url_for('login'))

@app.route('/login')
def login():
    return google.authorize(callback=url_for('authorized', _external=True))

@app.route('/logout')
def logout():
    session.clear()
    session.pop('google_token', None)  # Remove 'google_token' from session
    response = redirect("https://accounts.google.com/logout")
    return response

@app.route('/login/authorized')
def authorized():
    response = google.authorized_response()
    if response is None or response.get('access_token') is None:
        return 'Access denied: reason={} error={}'.format(
            request.args['error_reason'],
            request.args['error_description']
        )
    session['google_token'] = (response['access_token'], '')

    return redirect(url_for('index'))

@google.tokengetter
def get_google_oauth_token():
    return session.get('google_token')

def get_gemini_response(input_text, prompt):
    model = genai.GenerativeModel("gemini-pro")
    # The content should be structured as a list of parts, where each part has a 'text' key.
    content = {
        "parts": [
            {"text": input_text},
            {"text": prompt}
        ]
    }
    response = model.generate_content(content)
    # Remove asterisks and bold markers from the response
    plain_text_response = response.text.replace('*', '').replace('**', '')
    # Format the response into paragraphs
    structured_text_response = '\n\n'.join(filter(None, plain_text_response.split('\n')))
    return structured_text_response  # Return the structured text response

@app.route('/get_response', methods=['POST'])
def get_response():
    user_message = request.json['message']
    prompt = "Please do not answer querries which are not related to mental health and well-being."

    assistant_response = get_gemini_response(user_message, prompt)

    return jsonify({"response": assistant_response})



@app.route('/get_voice_input', methods=['POST'])
def get_voice_input():
    r = sr.Recognizer()

    audio_data = request.files['audio_data']
    with tempfile.NamedTemporaryFile(delete=False) as temp_audio:
        temp_audio.write(audio_data.read())
        temp_audio_path = temp_audio.name

    with sr.AudioFile(temp_audio_path) as source:
        audio_text = r.recognize_google(source)

    os.remove(temp_audio_path)

    return jsonify({"voice_input": audio_text})

if __name__ == '__main__':
    app.run(debug=True)
