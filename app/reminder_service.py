import smtplib
from email.mime.text import MIMEText
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
import os

# Email configuration
SMTP_SERVER = os.environ.get('SMTP_SERVER', 'smtp.gmail.com')
SMTP_PORT = int(os.environ.get('SMTP_PORT', 587))
SENDER_EMAIL = os.environ.get('SENDER_EMAIL', 'shitmail1q@gmail.com')
SENDER_PASSWORD = os.environ.get('SENDER_PASSWORD', 'cjfk zrgx nsnh rcgd')
RECIPIENT_EMAIL = os.environ.get('RECIPIENT_EMAIL', 'eli.bukin@gmail.com')

def send_reminder_email():
    from app import read_log  # Import here to avoid circular import

    log_data = read_log()
    if log_data:
        last_entry_time = datetime.strptime(log_data[0], '%d-%m-%Y %H:%M:%S')
        if datetime.now() - last_entry_time > timedelta(minutes=5):
            subject = "Medication Reminder"
            body = "Reminder number one"
            msg = MIMEText(body)
            msg['Subject'] = subject
            msg['From'] = SENDER_EMAIL
            msg['To'] = RECIPIENT_EMAIL

            with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
                server.starttls()
                server.login(SENDER_EMAIL, SENDER_PASSWORD)
                server.send_message(msg)
            print("Reminder email sent")
        else:
            print("No need to send reminder")
    else:
        print("No log data available")

def start_reminder_service():
    scheduler = BackgroundScheduler()
    scheduler.add_job(send_reminder_email, 'interval', minutes=5, id='send_reminder_email')
    scheduler.start()
    print("Reminder service started")
    return scheduler

if __name__ == '__main__':
    start_reminder_service()
    try:
        # This is here to simulate application activity (which keeps the main thread alive).
        while True:
            pass
    except (KeyboardInterrupt, SystemExit):
        pass