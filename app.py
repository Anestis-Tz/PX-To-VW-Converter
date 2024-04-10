# from flask import Flask, request, send_file, render_template_string
# import os
# import re

# app = Flask(__name__)

# # Ensure there's a directory for uploaded and converted files
# UPLOAD_FOLDER = 'uploads'
# if not os.path.exists(UPLOAD_FOLDER):
#     os.makedirs(UPLOAD_FOLDER)

# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# def convert_to_vw(value, unit):
#     # You might need to adjust the base width to match the design of the website
#     base_width = 1920  # Base width for 100vw
#     px_conversion = 100 / base_width  # Conversion factor for px to vw

#     if unit == 'px':
#         return f"{float(value) * px_conversion:.3f}".rstrip('0').rstrip('.') + 'vw'
#     elif unit in ['em', 'rem']:
#         return f"{float(value) * 16 * px_conversion:.3f}".rstrip('0').rstrip('.') + 'vw'
#     return value + unit

# def convert_to_vw_in_content(content):
#     pattern = re.compile(r'(\d*\.?\d+)(px|em|rem)')
#     return pattern.sub(lambda m: convert_to_vw(*m.groups()), content)

# @app.route('/', methods=['GET', 'POST'])
# def upload_file():
#     if request.method == 'POST':
#         if 'file' not in request.files:
#             return 'No file part'

#         file = request.files['file']

#         if file.filename == '':
#             return 'No selected file'

#         if file and file.filename.endswith('.less'):
#             filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
#             file.save(filepath)

#             with open(filepath, 'r') as f:
#                 content = f.read()
#                 converted_content = convert_to_vw_in_content(content)

#             converted_filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'converted_' + file.filename)
#             with open(converted_filepath, 'w') as f:
#                 f.write(converted_content)

#             return send_file(converted_filepath, as_attachment=True)

#     return render_template_string('''
#     <!doctype html>
#     <html lang="en">
#     <head>
#         <meta charset="UTF-8">
#         <meta name="viewport" content="width=device-width, initial-scale=1.0">
#         <title>LESS to VW Converter</title>
#         <style>
#             body {
#                 font-family: Arial, sans-serif;
#                 background-color: #f4f4f4;
#                 margin: 0;
#                 padding: 20px;
#                 display: flex;
#                 justify-content: center;
#                 height: 100vh;
#             }
#             .container {
#                 background: white;
#                 padding: 20px;
#                 border-radius: 8px;
#                 box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
#             }
#             h1 {
#                 color: #333;
#             }
#             form {
#                 margin-top: 20px;
#             }
#             input[type=file] {
#                 display: block;
#                 margin-bottom: 10px;
#             }
#             input[type=submit] {
#                 background-color: #007bff;
#                 color: white;
#                 border: none;
#                 padding: 10px 20px;
#                 cursor: pointer;
#                 border-radius: 5px;
#             }
#             input[type=submit]:hover {
#                 background-color: #0056b3;
#             }
#         </style>
#     </head>
#     <body>
#         <div class="container">
#             <h1>Upload LESS File for Conversion</h1>
#             <form method=post enctype=multipart/form-data>
#                 <input type=file name=file>
#                 <input type=submit value=Convert>
#             </form>
#         </div>
#     </body>
#     </html>
#     ''')

# if __name__ == '__main__':
#     app.run(debug=True)

from flask import Flask, request, send_file, render_template_string
import os
import re

app = Flask(__name__)

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
    return pattern.sub(lambda m: convert_to_vw(*m.groups()), content)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'No file part'

        file = request.files['file']

        if file.filename == '':
            return 'No selected file'

        if file and file.filename.endswith('.less'):
            # Create a unique folder for the uploaded file
            unique_folder = file.filename.rsplit('.', 1)[0]
            unique_folder_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_folder)
            if not os.path.exists(unique_folder_path):
                os.makedirs(unique_folder_path)

            # Save the original file
            filepath = os.path.join(unique_folder_path, file.filename)
            file.save(filepath)

            # Read, convert, and save the converted file
            with open(filepath, 'r') as f:
                content = f.read()
                converted_content = convert_to_vw_in_content(content)

            converted_filepath = os.path.join(unique_folder_path, 'converted_' + file.filename)
            with open(converted_filepath, 'w') as f:
                f.write(converted_content)

            # Send the converted file to the user
            return send_file(converted_filepath, as_attachment=True)

    return render_template_string('''
    <!doctype html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>LESS to VW Converter</title>
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
            <h1>Upload LESS File for Conversion</h1>
            <form method=post enctype=multipart/form-data>
                <input type=file name=file>
                <input type=submit value=Convert>
            </form>
        </div>
    </body>
    </html>
    ''')

if __name__ == '__main__':
    app.run(debug=True)

