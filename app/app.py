from flask import Flask, render_template, request, redirect
import time
import os

app = Flask(__name__)

log_file_path = '/app/log/app-log.txt'
deleted_log_file_path = '/app/log/deleted-entries-log.txt'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        log_action()
        return redirect('/')

    log_data = read_log()
    if len(log_data) > 6:
        log_data = log_data[:6]

    return render_template('index.html', log_data=log_data)

@app.route('/delete/<int:index>', methods=['POST'])
def delete_entry(index):
    log_data = read_log()
    if 0 <= index < len(log_data):
        deleted_entry = log_data[index]
        del log_data[index]
        write_log(log_data)
        log_deleted_entry(deleted_entry)
    return redirect('/')

def log_action():
    current_time = time.strftime('%d-%m-%Y %H:%M:%S')
    log_data = read_log()
    log_data.insert(0, current_time)
    write_log(log_data)

def read_log():
    if os.path.exists(log_file_path):
        with open(log_file_path, 'r') as log_file:
            log_data = log_file.read().splitlines()
        return log_data
    else:
        return []

def write_log(log_data):
    with open(log_file_path, 'w') as log_file:
        for entry in log_data:
            log_file.write(entry + '\n')

def log_deleted_entry(entry):
    existing_entries = []
    if os.path.exists(deleted_log_file_path):
        try:
            with open(deleted_log_file_path, 'r') as deleted_log_file:
                existing_entries = deleted_log_file.read().splitlines()
        except IOError:
            print(f"Warning: Could not read from {deleted_log_file_path}")

    existing_entries.insert(0, entry)
    
    try:
        with open(deleted_log_file_path, 'w') as deleted_log_file:
            for entry in existing_entries:
                deleted_log_file.write(entry + '\n')
    except IOError:
        print(f"Error: Could not write to {deleted_log_file_path}")

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)