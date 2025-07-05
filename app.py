from flask import Flask, render_template, send_file
import sqlite3
import csv
from io import StringIO
from io import BytesIO

app = Flask(__name__)

def get_latest_results():
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    c.execute('''
        SELECT name, host, status, latency, MAX(timestamp)
        FROM results
        GROUP BY host
        ORDER BY name
    ''')
    rows = c.fetchall()
    conn.close()
    return rows

@app.route('/')
def dashboard():
    results = get_latest_results()
    return render_template('dashboard.html', results=results)


@app.route('/export/csv')
def export_csv():
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    c.execute('SELECT name, host, status, latency, timestamp FROM results ORDER BY timestamp DESC')
    rows = c.fetchall()
    conn.close()

    # Use StringIO for CSV text, then encode to bytes
    csv_text = StringIO()
    writer = csv.writer(csv_text)
    writer.writerow(['Name', 'Host', 'Status', 'Latency', 'Timestamp'])
    writer.writerows(rows)

    # Convert to BytesIO for Flask
    csv_bytes = BytesIO()
    csv_bytes.write(csv_text.getvalue().encode('utf-8'))
    csv_bytes.seek(0)

    return send_file(
        csv_bytes,
        mimetype='text/csv',
        as_attachment=True,
        download_name='network_logs.csv'
    )


if __name__ == '__main__':
    app.run(debug=True)
