import streamlit as st
import os
from werkzeug.utils import secure_filename
import pytesseract
from PIL import Image
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler

# Configure the upload folder
UPLOAD_FOLDER = 'uploads'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Configure OCR
pytesseract.pytesseract.tesseract_cmd = r"E:\intern_proj\tesseract.exe"

# Configure scheduler
scheduler = BackgroundScheduler()
scheduler.start()

# Route for uploading image
def upload_image():
    uploaded_file = st.file_uploader("Upload Image", type=['png', 'jpg', 'jpeg'])
    if uploaded_file is not None:
        # Save the uploaded file
        filename = secure_filename(uploaded_file.name)
        filepath = os.path.join(UPLOAD_FOLDER, filename)

        with open(filepath, 'wb') as f:
            f.write(uploaded_file.read())

        # Extract data from the image
        extracted_data = extract_data(filepath)

        # Get the scheduled time from the form
        scheduled_time_str = st.text_input('Scheduled Time', value=datetime.now().strftime('%Y-%m-%dT%H:%M'))

        if st.button('Schedule Extraction'):
            if scheduled_time_str:
                scheduled_time = datetime.strptime(scheduled_time_str, '%Y-%m-%dT%H:%M')

                # Schedule the data extraction task
                scheduler.add_job(execute_extraction, 'date', run_date=scheduled_time, args=[extracted_data])

                st.write('Data extraction scheduled successfully')

# Function to extract data from image
def extract_data(image_path):
    image = Image.open(image_path)
    extracted_text = pytesseract.image_to_string(image)
    return extracted_text

# Function to execute data extraction task
def execute_extraction(extracted_data):
    # Perform any further processing with the extracted data
    # For example, save it to a database, send email notifications, etc.
    st.write(extracted_data)

def main():
    st.title('Image Upload')
    upload_image()

if __name__ == '__main__':
    main()
