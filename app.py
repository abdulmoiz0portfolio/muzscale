from flask import Flask, render_template, request, send_file, jsonify
import os
import io
import requests
from werkzeug.utils import secure_filename
import uuid
from PIL import Image, ImageFilter

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['OUTPUT_FOLDER'] = 'outputs'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'webp'}

# Optional external API key
DEEPAI_API_KEY = os.environ.get('DEEPAI_API_KEY')

# Create folders if they don't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/health')
def health():
    return jsonify({'status': 'ok'})

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/upscale', methods=['POST'])
def api_upscale():
    # Accept canvas PNG or file upload as 'image'
    if 'image' not in request.files:
        return jsonify({'error': 'No image part'}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    if not allowed_file(file.filename) and file.mimetype not in ('image/png', 'image/jpeg', 'image/webp'):
        return jsonify({'error': 'Invalid file type'}), 400

    filename = secure_filename(file.filename or f"upload_{uuid.uuid4().hex}.png")
    unique_filename = f"{uuid.uuid4().hex}_{filename}"
    input_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
    file.save(input_path)

    try:
        output_filename = f"upscaled_{unique_filename}.png"
        output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)

        # If external API key present, try DeepAI (waifu2x) for upscaling
        if DEEPAI_API_KEY:
            with open(input_path, 'rb') as f:
                resp = requests.post(
                    'https://api.deepai.org/api/waifu2x',
                    files={'image': f},
                    headers={'api-key': DEEPAI_API_KEY},
                    timeout=120,
                )
            if resp.ok:
                data = resp.json()
                url = data.get('output_url')
                if url:
                    img_resp = requests.get(url, timeout=120)
                    with open(output_path, 'wb') as out:
                        out.write(img_resp.content)
                else:
                    return jsonify({'error': 'No output URL from upscaler'}), 502
            else:
                return jsonify({'error': f'Upscale API error {resp.status_code}'}), 502
        else:
            # Fallback: simple PIL-based 2x upscale with optional filters (demo)
            with Image.open(input_path) as img:
                # Apply basic filters based on incoming form fields
                brightness = int(float(request.form.get('brightness', 100)))
                contrast = int(float(request.form.get('contrast', 100)))
                saturation = int(float(request.form.get('saturation', 100)))
                blur = int(float(request.form.get('blur', 0)))
                grayscale = int(float(request.form.get('grayscale', 0)))
                sepia = int(float(request.form.get('sepia', 0)))
                rotate = float(request.form.get('rotate', 0))
                flipH = request.form.get('flipH', 'false') == 'true'
                flipV = request.form.get('flipV', 'false') == 'true'

                # PIL does not support CSS-like pipeline directly; keep it minimal demo
                if grayscale > 0:
                    img = img.convert('L').convert('RGB')
                if blur > 0:
                    img = img.filter(ImageFilter.GaussianBlur(radius=max(0, blur)))
                if rotate:
                    img = img.rotate(-rotate, expand=True)
                if flipH:
                    img = img.transpose(Image.FLIP_LEFT_RIGHT)
                if flipV:
                    img = img.transpose(Image.FLIP_TOP_BOTTOM)

                # Simple 2x upscale using Lanczos
                w, h = img.size
                img = img.resize((int(w * 2), int(h * 2)), Image.LANCZOS)
                img.save(output_path, format='PNG')

        # Return file as binary
        return send_file(output_path, as_attachment=False, mimetype='image/png')
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if os.path.exists(input_path):
            try:
                os.remove(input_path)
            except Exception:
                pass

@app.route('/download/<path:filename>')
def download_file(filename):
    file_path = os.path.join(app.config['OUTPUT_FOLDER'], filename)
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    return jsonify({'error': 'File not found'}), 404

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
