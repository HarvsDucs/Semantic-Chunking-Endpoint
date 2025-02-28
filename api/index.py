from flask import Flask, request, jsonify 
from langchain_experimental.text_splitter import SemanticChunker
from langchain_openai import OpenAIEmbeddings

from functools import wraps
import os 
from supabase import create_client, Client

app = Flask(__name__)

# Supabase configuration -  IMPORTANT: Use environment variables for security in production
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_ANON_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Function to fetch API key from Supabase
def get_api_key_from_supabase():
    try:
        response = supabase.table("api_keys").select("api_key").execute()
        if response.data and len(response.data) > 0:
            # Assuming you have only one API key in the table or want to use the first one
            # If you have multiple keys, you might need to adjust the query to select based on some criteria
            return response.data[0]["api_key"]
        else:
            print("Warning: No API key found in Supabase table 'api_keys'.") # Log this for debugging
            return None  # Or raise an exception if API key is mandatory
    except Exception as e:
        print(f"Error fetching API key from Supabase: {e}") # Log the error
        return None


# Decorator to check for API key fetched from Supabase
def require_api_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key_from_request = request.headers.get('X-API-Key')  # Or request.args.get('api_key')

        if not api_key_from_request:
            return jsonify({"message": "Unauthorized. API key is missing."}), 401

        api_key_from_db = get_api_key_from_supabase()

        if api_key_from_db and api_key_from_request == api_key_from_db:
            return f(*args, **kwargs)
        else:
            return jsonify({"message": "Unauthorized. Invalid API key."}), 401
    return decorated_function

    
@app.route('/')
def home():
    return 'Hello, World!'

@app.route('/about')
def about():
    return 'About'

@app.route('/test')
def test():
    return 'test'

@app.route('/process_text', methods=['POST'])
@require_api_key  # Apply the decorator to this endpoint
def process_text():
    try:
        data = request.get_json()  # Get JSON data from the request body

        if not data or 'text' not in data:
            return jsonify({'error': 'Missing text data in request body'}), 400

        text = data['text']

            # Initialize OpenAI Embeddings
        embeddings = OpenAIEmbeddings()  # You can adjust the model if needed

            # Initialize SemanticChunker
        text_splitter = SemanticChunker(embeddings=embeddings)

            # Perform semantic chunking
        chunks = text_splitter.split_text(text)

            # Return the chunks as a JSON response
        return jsonify({'chunks': chunks}), 200

    except Exception as e:
            print(f"An error occurred: {e}")  # Log the exception
            return jsonify({'error': str(e)}), 500  # Return a 500 error with the exception message

if __name__ == '__main__':
    app.run(debug=True)

