# from flask import request, Flask, redirect, send_from_directory, render_template_string
from flask import Flask, request, send_from_directory, render_template_string, redirect, render_template
import os

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 200 * 1024 * 1024  # 100 MB limit
UPLOAD_FOLDER = 'uploads'  # Folder to store uploaded filesx
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Create the folder if it doesn't exist

# Route for the home page (file upload form)
@app.route('/', methods=['GET', 'POST'])
def upload_file():
    message = None
    # message = None
    if request.method == 'POST':
        # Check if a file is included in the request
        if 'file' not in request.files:
            message = "No file part"
        else:
            file = request.files['file']
            # Check if a file is selected
            if file.filename == '':
                message = "No selected file"
            else:
                # Save the file to the uploads folder
                file.save(os.path.join(UPLOAD_FOLDER, file.filename))
                message = f"File '{file.filename}' uploaded successfully!"
    return render_template('home.html', message = message)
    # Render the upload form
    # return '''
    # <!doctype html>
    # <title>Upload File</title>
    # <h1>Upload a File</h1>
    # <form method=post enctype=multipart/form-data>
    #   <input type=file name=file>
    #   <input type=submit value=Upload>
    # </form>
    # <p><a href="/files">View Uploaded Files</a></p>
    # '''

# Route to list all uploaded files
@app.route('/files')
def list_files():
    files = os.listdir(UPLOAD_FOLDER)
    return render_template('files.html', files=files)

# Route to download a file
@app.route('/download/<filename>')
def download_file(filename):
    files = os.listdir(UPLOAD_FOLDER)
    return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)