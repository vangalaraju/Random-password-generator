from flask import Flask, render_template, request, jsonify
import random
import string

app = Flask(__name__)

def generate_random_password(length, use_letters, use_numbers, use_symbols):
    """Generates a random password based on the given criteria."""
    characters = ''
    if use_letters:
        characters += string.ascii_letters  # Contains both uppercase and lowercase letters
    if use_numbers:
        characters += string.digits  # Contains digits 0-9
    if use_symbols:
        characters += string.punctuation  # Contains various punctuation symbols

    if not characters:
        return "Error: No character types selected."

    # Randomization: Selecting random characters from the combined set
    password = ''.join(random.choice(characters) for _ in range(length))
    return password

@app.route('/generate-password', methods=['POST'])
def generate_password_route():
    """Handles the password generation request from the frontend."""
    try:
        data = request.get_json()  # Get the data sent from the JavaScript fetch
        password_length = int(data['passwordLength'])
        use_letters = bool(data['includeLetters'])
        use_numbers = bool(data['includeNumbers'])
        use_symbols = bool(data['includeSymbols'])

        # Input validation (same as before, but raising exceptions)
        if password_length <= 0:
            raise ValueError("Password length must be a positive integer.")

        if not (use_letters or use_numbers or use_symbols):
            raise ValueError("You must select at least one character type.")

        generated_password = generate_random_password(
            length=password_length,
            use_letters=use_letters,
            use_numbers=use_numbers,
            use_symbols=use_symbols
        )
        return jsonify({'password': generated_password})  # Send back JSON
    except (ValueError, KeyError) as e:
        # Handle errors and send a JSON response
        return jsonify({'error': str(e)}), 400  # 400 Bad Request

@app.route('/')
def index():
    return render_template('index password .html')  # Serve the HTML page
  
if __name__ == "__main__":
    app.run(debug=True)
