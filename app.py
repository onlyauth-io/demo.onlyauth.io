"""Example code to generate OnlyAuth JWT"""
import os
import requests
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

# Replace the API secret with your secret from OnlyAuth
SECRET_KEY = os.environ.get('ONLYAUTH_API_SECRET')

# Public API endpoint to retrieve JWT to embed into the iframe
API_URL = 'https://api.onlyauth.io/server/access-tokens/new'

# Endpoint to generate and retrieve JWT


@app.route('/', methods=['POST'])
def generate_and_retrieve_jwt():
    """POST METHOD to call OnlyAuth API to embedd JWT """
    if not SECRET_KEY:
        return jsonify({'message': 'OnlyAuth API key not found'}), 500

    # These values should be collected from db instead of a form
    phone_number = request.form.get('phone_number')
    user_id = request.form.get('user_id')

    # Replace app_id and client_id with respective values from your account
    app_id = "APPX-123"
    client_id = "CLNT-456"

    if not phone_number:
        return jsonify({'message': 'Phone number was not found'}), 400
    if not user_id:
        return jsonify({'message': 'User ID was not found'}), 400

    payload = {
        'app_id': app_id,
        'redirect_uri': "https://www.onlyauth.io/success?",  # Update to your URL
        'language': 'en-us',
        'region': 'us1',
        'end_user_phone_number': phone_number,
        'end_user_uuid': user_id,
        'client_id': client_id
    }

    # Retrieve JWT from public API using Bearer token authentication
    headers = {'Authorization': f'Bearer {SECRET_KEY}'}
    response = requests.post(API_URL, headers=headers, data=payload, timeout=10)

    if response.status_code != 200:
        app.logger.error("API Error: %s", response.text)

        # Parse response for specific error messages
        error_response = response.json()
        error_messages = error_response.get('errors', ['Unknown error'])
        error_message = '; '.join(error_messages)

        return jsonify({'message': f'Failed to retrieve JWT from API: {error_message}'}), 500

    response_json = response.json()
    api_jwt = response_json.get('token')

    if not api_jwt:
        return jsonify({'message': 'API did not return a token'}), 500

    return render_template('integration.html', token=api_jwt, app_id=app_id)


@app.route('/', methods=['GET'])
def index():
    """Just return the HTML file"""
    return render_template("index.html")
