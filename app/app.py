from flask import Flask, render_template, request, redirect
import time
import os

app = Flask(__name__)

log_file_path = '/app/log/app-log.txt'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        log_action()
        return redirect('/')

    log_data = read_log()
    if len(log_data) > 6:
        log_data = log_data[:6]

    return render_template('index.html', log_data=log_data)

@app.route('/delete', methods=['POST'])
def delete_entry():
    log_data = read_log()
    if log_data:
        log_data.pop(0)
        write_log(log_data)
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

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
