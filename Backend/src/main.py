from flask import Flask, request, jsonify
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

# Twilio Configuration
TWILIO_ACCOUNT_SID = "your_account_sid"
TWILIO_AUTH_TOKEN = "your_auth_token"
TWILIO_PHONE_NUMBER = "your_twilio_phone_number"

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

# In-memory database for simplicity (use a real database in production)
numbers = {}  # Store available numbers and their messages

@app.route("/register_number", methods=["POST"])
def register_number():
    """Register a new Twilio number to be used."""
    number = request.json.get("number")
    if number in numbers:
        return jsonify({"error": "Number already registered."}), 400

    numbers[number] = []  # Initialize with an empty message list
    return jsonify({"message": f"Number {number} registered successfully."}), 201

@app.route("/incoming_sms", methods=["POST"])
def incoming_sms():
    """Handle incoming SMS from Twilio Webhook."""
    from_number = request.form.get("From")
    to_number = request.form.get("To")
    body = request.form.get("Body")

    if to_number in numbers:
        numbers[to_number].append({"from": from_number, "body": body})
        return str(MessagingResponse()), 200
    
    return jsonify({"error": "Number not registered."}), 404

@app.route("/messages/<number>", methods=["GET"])
def get_messages(number):
    """Retrieve all messages for a specific number."""
    if number not in numbers:
        return jsonify({"error": "Number not found."}), 404

    return jsonify({"messages": numbers[number]}), 200

@app.route("/available_numbers", methods=["GET"])
def available_numbers():
    """List all registered numbers."""
    return jsonify({"numbers": list(numbers.keys())}), 200

if __name__ == "__main__":
    app.run(debug=True)
