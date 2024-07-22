from flask import Flask, render_template, request, jsonify
from datetime import datetime, time
import threading
import smtplib
from email.mime.text import MIMEText
import os
import json
from dotenv import load_dotenv
from logging.config import dictConfig
import logging

def get_last_log_entries(n=5):
    ensure_log_file_exists()
    with open(LOG_FILE, 'r') as f:
        lines = f.readlines()
    return [line.strip() for line in lines[:n]]

# Configure logging
dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})

# Load environment variables
load_dotenv()

app = Flask(__name__, static_folder='static', template_folder='templates')

CONFIG_FILE = '/app/app-data/config.json'
LOG_FILE = '/app/app-data/button_log.txt'

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    return {
        'sender_email': os.getenv('SENDER_EMAIL'),
        'recipient_email': os.getenv('RECIPIENT_EMAIL'),
        'email_password': os.getenv('EMAIL_PASSWORD'),
        'time_slots': ['14:00', '02:00'],
        'reminder_intervals': [60, 90, 180],
        'email_enabled': True  # Add this line to set a default value
    }

def save_config(config):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f)

config = load_config()

def ensure_log_file_exists():
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'w') as f:
            f.write(datetime.now().strftime('%Y-%m-%d %H:%M:%S\n'))

def send_email_notification(subject, body):
    if not config['email_enabled']:
        app.logger.info(f"Email not sent (disabled): {subject}")
        return

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = config['sender_email']
    msg['To'] = config['recipient_email']

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(config['sender_email'], config['email_password'])
            server.sendmail(config['sender_email'], config['recipient_email'], msg.as_string())
        app.logger.info(f"Email sent: {subject}")
    except Exception as e:
        app.logger.error(f"Failed to send email: {str(e)}")

def log_button_push(send_email=True):
    ensure_log_file_exists()
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(LOG_FILE, 'r+') as f:
        content = f.read()
        f.seek(0, 0)
        f.write(timestamp + '\n' + content)
    if send_email:
        send_email_notification('Button Pushed', f'Button was pushed at {timestamp}')
    app.logger.info(f"Button pushed at {timestamp}. Email sent: {send_email}")

def check_button_push():
    while True:
        now = datetime.now().time()
        for slot in [datetime.strptime(ts, "%H:%M").time() for ts in config['time_slots']]:
            if now.hour == slot.hour and now.minute == slot.minute:
                for interval in config['reminder_intervals']:
                    threading.Timer(interval * 60, send_reminder, args=[interval]).start()
        threading.Event().wait(60)  # Check every minute

def send_reminder(interval):
    ensure_log_file_exists()
    with open(LOG_FILE, 'r') as f:
        last_push = datetime.strptime(f.readline().strip(), '%Y-%m-%d %H:%M:%S')
    
    if (datetime.now() - last_push).total_seconds() > interval * 60:
        if interval == config['reminder_intervals'][0]:
            send_email('First Reminder', 'This is the first reminder, do the thing.')
        elif interval == config['reminder_intervals'][1]:
            send_email('Second Reminder', 'This is the second reminder, get on with it now!')
        elif interval == config['reminder_intervals'][2]:
            send_email('Missed Button Push', 'You skipped one, NOT GOOD!')

@app.route('/')
def home():
    last_entries = get_last_log_entries()
    return render_template('index.html', config=config, last_entries=last_entries)

@app.route('/push_button', methods=['POST'])
def push_button():
    data = request.json
    send_email = data.get('send_email', True)
    log_button_push(send_email)
    return jsonify({'status': 'success', 'message': f'Button pushed successfully. Email sent: {send_email}'})

@app.route('/update_config', methods=['POST'])
def update_config():
    global config
    new_config = request.json
    
    # Validate the incoming configuration
    if not validate_config(new_config):
        return jsonify({'status': 'error', 'message': 'Invalid configuration data'}), 400

    # Update only the provided configuration fields
    config.update(new_config)
    save_config(config)
    app.logger.info(f"Configuration updated: {new_config.keys()}")
    return jsonify({'status': 'success'})

def validate_config(new_config):
    # Validate email configuration
    if 'sender_email' in new_config:
        if not all(key in new_config for key in ['sender_email', 'recipient_email', 'email_password']):
            return False
        if not all(isinstance(new_config[key], str) for key in ['sender_email', 'recipient_email', 'email_password']):
            return False
    
    # Validate email_enabled
    if 'email_enabled' in new_config:
        if not isinstance(new_config['email_enabled'], bool):
            return False

    # Validate time configuration
    if 'time_slots' in new_config:
        if not all(key in new_config for key in ['time_slots', 'reminder_intervals']):
            return False
        if not isinstance(new_config['time_slots'], list) or len(new_config['time_slots']) != 2:
            return False
        if not isinstance(new_config['reminder_intervals'], list) or len(new_config['reminder_intervals']) != 3:
            return False
        if not all(isinstance(slot, str) for slot in new_config['time_slots']):
            return False
        if not all(isinstance(interval, int) for interval in new_config['reminder_intervals']):
            return False

    return True

def create_app():
    ensure_log_file_exists()
    threading.Thread(target=check_button_push, daemon=True).start()
    return app

if __name__ == '__main__':
    create_app().run(debug=False)
