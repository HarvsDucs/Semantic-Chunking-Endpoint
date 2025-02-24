from flask import Flask, request, jsonify

app = Flask(__name__)

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
def process_text():
    try:
        data = request.get_json()  # Get JSON data from the request body

        # if not data or 'text' not in data:
        #     return jsonify({'error': 'Missing text data in request body'}), 400

        # text = data['text']

        #     # Initialize OpenAI Embeddings
        # embeddings = OpenAIEmbeddings()  # You can adjust the model if needed

        #     # Initialize SemanticChunker
        # text_splitter = SemanticChunker(embeddings=embeddings)

        #     # Perform semantic chunking
        # chunks = text_splitter.split_text(text)

        #     # Return the chunks as a JSON response
        # return jsonify({'chunks': chunks}), 200
        return data

    except Exception as e:
            print(f"An error occurred: {e}")  # Log the exception
            return jsonify({'error': str(e)}), 500  # Return a 500 error with the exception message


