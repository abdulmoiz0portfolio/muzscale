from flask import Flask, render_template, request, send_file, jsonify
import os
import requests
from werkzeug.utils import secure_filename
import uuid

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['OUTPUT_FOLDER'] = 'outputs'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'webp'}

# DeepAI API Key (users should set this as environment variable)
DEEPAI_API_KEY = os.environ.get('DEEPAI_API_KEY', 'YOUR_API_KEY_HERE')

# Create folders if they don't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upscale', methods=['POST'])
def upscale_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400
    
    file = request.files['image']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file type. Allowed: PNG, JPG, JPEG, WEBP'}), 400
    
    # Save uploaded file
    filename = secure_filename(file.filename)
    unique_filename = f"{uuid.uuid4().hex}_{filename}"
    input_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
    file.save(input_path)
    
    try:
        # Call DeepAI Super Resolution API
        response = requests.post(
            "https://api.deepai.org/api/waifu2x",
            files={'image': open(input_path, 'rb')},
            headers={'api-key': DEEPAI_API_KEY}
        )
        
        if response.status_code == 200:
            result = response.json()
            output_url = result.get('output_url')
            
            if output_url:
                # Download upscaled image
                output_filename = f"upscaled_{unique_filename}"
                output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)
                
                img_response = requests.get(output_url)
                with open(output_path, 'wb') as f:
                    f.write(img_response.content)
                
                return jsonify({
                    'success': True,
                    'output_filename': output_filename
                })
            else:
                return jsonify({'error': 'Failed to get output URL from API'}), 500
        else:
            return jsonify({'error': f'API error: {response.status_code}'}), 500
    
    except Exception as e:
        return jsonify({'error': f'Processing failed: {str(e)}'}), 500
    
    finally:
        # Clean up input file
        if os.path.exists(input_path):
            os.remove(input_path)

@app.route('/download/<filename>')
def download_file(filename):
    file_path = os.path.join(app.config['OUTPUT_FOLDER'], filename)
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    return jsonify({'error': 'File not found'}), 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
