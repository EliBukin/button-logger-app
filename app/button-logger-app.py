from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import os

app = Flask(__name__)

# Initialize a list to store button press times
button_press_times = []

# Define the log file path within the /app/log folder
log_folder = "/app/log"
log_file_name = "button_press_log.txt"
log_file_path = os.path.join(log_folder, log_file_name)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'delete_last' in request.form:
            # Delete the last entry when the "Delete Last Entry" button is clicked
            if button_press_times:
                button_press_times.pop(0)  # Remove the first entry (latest) from the list
        else:
            # Add the current date and time to the list when the "Confirm taking meds" button is pressed
            timestamp = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
            button_press_times.insert(0, timestamp)  # Insert the latest entry at the beginning of the list

            # Log the button press to the log file
            with open(log_file_path, 'a') as log_file:
                log_file.write(f"Button Pressed: {timestamp}\n")

            # Redirect to a new URL to avoid form resubmission
            return redirect(url_for('index'))

    return render_template('index.html', button_press_times=button_press_times)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
