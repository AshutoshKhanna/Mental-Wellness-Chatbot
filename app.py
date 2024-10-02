from flask import Flask, request, jsonify, render_template, session, redirect, url_for
from authlib.integrations.flask_client import OAuth
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
google = oauth.register(
    name='google',
    client_id=os.getenv('CONSUMER_KEY'),
    client_secret=os.getenv('CONSUMER_SECRET'),
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    client_kwargs={'scope': 'email'},
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
    redirect_uri = url_for('authorized', _external=True)
    return google.authorize_redirect(redirect_uri)

@app.route('/logout')
def logout():
    session.clear()
    return redirect("https://accounts.google.com/logout")

@app.route('/login/authorized')
def authorized():
    token = google.authorize_access_token()
    if token is None:
        return 'Access denied: reason={} error={}'.format(
            request.args['error_reason'],
            request.args['error_description']
        )
    session['google_token'] = token
    return redirect(url_for('index'))

def get_gemini_response(input_text, prompt):
    model = genai.GenerativeModel("gemini-pro")
    content = {
        "parts": [
            {"text": input_text},
            {"text": prompt}
        ]
    }
    response = model.generate_content(content)
    plain_text_response = response.text.replace('*', '').replace('**', '')
    structured_text_response = '\n\n'.join(filter(None, plain_text_response.split('\n')))
    return structured_text_response

@app.route('/get_response', methods=['POST'])
def get_response():
    user_message = request.json['message']
    prompt = (
        "You are Saarthi, an AI-powered virtual assistant providing mental health and emotional support. "
        
    )

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