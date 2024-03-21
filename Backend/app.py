from flask import Flask, request, jsonify
from chatbot2 import get_bot_response
from flask_cors import CORS
import sys, os
from checkAndStoreFile import checkAndStoreFile
from chatbotChange import chatbotChange

app = Flask(__name__)
CORS(app)


@app.route('/chat', methods=['POST'])
def chat():
    message = request.json['message']
    # context = request.json.get('context', '')
    response = get_bot_response(message)
    return jsonify({'response': response})


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part', 400
    file = request.files['file']
    if file.filename == '':
        return 'No selected file', 400

    uploaded = checkAndStoreFile(file)

    if uploaded.startswith('Success:'):
        # The file was uploaded successfully
        return uploaded, 200
    else:
        # There was an error with the file upload
        return uploaded, 400

@app.route('/files', methods=['GET'])
def list_files():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    upload_dir = os.path.join(BASE_DIR, 'UploadedFiles')
    if not os.path.exists(upload_dir):
        return jsonify({'error': 'UploadedFiles directory not found.'}), 404
    try:
        files = [f for f in os.listdir(upload_dir) if os.path.isfile(os.path.join(upload_dir, f)) and not f.endswith('.pkl')]
        return jsonify(files), 200
    except Exception as e:
        return jsonify({'error': f'Could not list files: {str(e)}'}), 500
    

@app.route('/chatbot/<filename>', methods=['GET'])
def chatbot_api(filename):
    try:
        filename_without_ext, _ = os.path.splitext(filename)
        result_message = chatbotChange(filename_without_ext)
        return jsonify({'message': result_message}), 200
    except Exception as e:
        # Handle any unexpected error
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500



if __name__ == '__main__':
    print(sys.path)  # This will print the system path, for debugging
    app.run(debug=True)
