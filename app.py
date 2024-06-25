from flask import Flask, request, send_file, jsonify, render_template
import os
import uuid  # For generating unique security keys

app = Flask(__name__)

UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Dictionary to store security keys for files
security_keys = {}

# Route for the home page
@app.route('/')
def index():
    return render_template('index.html')

# Route for file upload with security key
@app.route('/upload', methods=['POST'])
def upload_file():
    uploaded_file = request.files['file']
    security_key = request.form.get('security_key')

    if uploaded_file and security_key:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
        uploaded_file.save(file_path)
        security_keys[file_path] = security_key  # Store security key with file path
        return jsonify({'message': 'File uploaded successfully!', 'filename': uploaded_file.filename})
    else:
        return jsonify({'error': 'No file uploaded or security key provided!'})

# Route for file download with security key
@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    security_key = request.args.get('key')

    if file_path in security_keys and security_keys[file_path] == security_key:
        return send_file(file_path, as_attachment=True)
    else:
        return jsonify({'error': 'Invalid security key or file not found!'})

# Route for removing file with security key
@app.route('/remove/<filename>', methods=['DELETE'])
def remove_file(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    security_key = request.args.get('key')

    if file_path in security_keys and security_keys[file_path] == security_key:
        os.remove(file_path)
        del security_keys[file_path]
        return jsonify({'message': 'File removed successfully!'})
    else:
        return jsonify({'error': 'Invalid security key or file not found!'})

# Route for listing uploaded files
@app.route('/files', methods=['GET'])
def list_files():
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return jsonify(files)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
