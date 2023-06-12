from flask import Flask, render_template, request
import os 
from werkzeug.utils import secure_filename
import pytesseract
from PIL import Image
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)

# Configure the upload folder
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Configure OCR
pytesseract.pytesseract.tesseract_cmd = r"E:\intern_proj\tesseract.exe"

# Configure scheduler
scheduler = BackgroundScheduler()
scheduler.start()

# Route for uploading image
@app.route('/', methods=['GET', 'POST'])
def upload_image():
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'file' not in request.files:
            return 'No file uploaded'

        file = request.files['file']

        if file.filename == '':
            return 'No selected file'

        if file:
            # Save the uploaded file
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            # Extract data from the image
            extracted_data = extract_data(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            # Get the scheduled time from the form
            scheduled_time_str = request.form['scheduled_time']
            scheduled_time = datetime.strptime(scheduled_time_str, '%Y-%m-%dT%H:%M')

            # Schedule the data extraction task
            scheduler.add_job(execute_extraction, 'date', run_date=scheduled_time, args=[extracted_data])

            return 'Data extraction scheduled successfully'

    return render_template('upload.html')

# Function to extract data from image
def extract_data(image_path):
    image = Image.open(image_path)
    extracted_text = pytesseract.image_to_string(image)
    return extracted_text

# Function to execute data extraction task
def execute_extraction(extracted_data):
    # Perform any further processing with the extracted data
    # For example, save it to a database, send email notifications, etc.
    print(extracted_data)

if __name__ == '__main__':
    app.run(debug=True)

