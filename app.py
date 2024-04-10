from flask import Flask, request, render_template_string, send_file, session
import os
import re
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# Ensure there's a directory for uploaded and converted files
BASE_UPLOAD_FOLDER = 'uploads'
if not os.path.exists(BASE_UPLOAD_FOLDER):
    os.makedirs(BASE_UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = BASE_UPLOAD_FOLDER

def convert_to_vw(value, unit):
    base_width = 1920  # Base width for 100vw
    px_conversion = 100 / base_width  # Conversion factor for px to vw

    if unit == 'px':
        return f"{float(value) * px_conversion:.3f}".rstrip('0').rstrip('.') + 'vw'
    elif unit in ['em', 'rem']:
        return f"{float(value) * 16 * px_conversion:.3f}".rstrip('0').rstrip('.') + 'vw'
    return value + unit

def convert_to_vw_in_content(content):
    pattern = re.compile(r'(\d*\.?\d+)(px|em|rem)')
    content = content.replace('\r\n', '\n').replace('\r', '\n')
    return pattern.sub(lambda m: convert_to_vw(*m.groups()), content)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'No file part'

        file = request.files['file']

        if file.filename == '':
            return 'No selected file'

        if file and (file.filename.endswith('.less') or file.filename.endswith('.css')):
            file_extension = '.less' if file.filename.endswith('.less') else '.css'
            content = file.read().decode('utf-8')
            converted_content = convert_to_vw_in_content(content)

            # Save the converted content to a temporary file with the same extension as the uploaded file
            filename = secrets.token_hex(8) + file_extension
            temp_file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            with open(temp_file_path, 'w') as temp_file:
                temp_file.write(converted_content)

            # Store the filename in the user's session for download
            session['download_filename'] = filename

            # Render a new HTML page with the converted content and options to copy or download
            return render_template_string('''
                <!doctype html>
                <html lang="en">
                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <title>Converted Content</title>
                    <script>
                        function copyToClipboard() {
                            var content = document.getElementById('converted-content');
                            navigator.clipboard.writeText(content.innerText);
                        }
                    </script>
                </head>
                <body>
                    <h1>Converted Content</h1>
                    <button onclick="copyToClipboard()">Copy to Clipboard</button>
                    <pre id="converted-content">{{ converted_content }}</pre>
                </body>
                </html>
            ''', converted_content=converted_content)

    return render_template_string('''
        <!doctype html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>LESS/CSS to VW Converter</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    background-color: #f4f4f4;
                    margin: 0;
                    padding: 20px;
                    display: flex;
                    justify-content: center;
                    height: 100vh;
                }
                .container {
                    background: white;
                    padding: 20px;
                    border-radius: 8px;
                    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
                }
                h1 {
                    color: #333;
                }
                form {
                    margin-top: 20px;
                }
                input[type=file] {
                    display: block;
                    margin-bottom: 10px;
                }
                input[type=submit] {
                    background-color: #007bff;
                    color: white;
                    border: none;
                    padding: 10px 20px;
                    cursor: pointer;
                    border-radius: 5px;
                }
                input[type=submit]:hover {
                    background-color: #0056b3;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Upload LESS or CSS File for Conversion</h1>
                <form method=post enctype=multipart/form-data>
                    <input type=file name=file> 
                    <input type=submit value=Convert>
                </form>
            </div>
        </body>
        </html>
        ''')

@app.route('/download', methods=['GET'])
def download():
    # Retrieve the filename from the user's session
    filename = session.get('download_filename', '')
    if not filename:
        return "File not found", 404

    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if not os.path.exists(file_path):
        return "File not found", 404

    return send_file(file_path, as_attachment=True, download_name=filename)

if __name__ == '__main__':
    app.run(debug=True)
