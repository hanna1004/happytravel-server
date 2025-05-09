from flask import Flask, request, render_template
import sqlite3
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def index():
    return "Server is running!"

@app.route('/voucher')
def check_voucher():
    code = request.args.get("code", "").strip().upper()
    if not code:
        return "Thiếu mã voucher."

    conn = sqlite3.connect("C:/python/vouche/happy_travel_app/voucher.db")
    c = conn.cursor()
    c.execute("SELECT name, amount, remaining, used, used_date, date_to FROM vouchers WHERE code = ?", (code,))
    row = c.fetchone()
    conn.close()

    if not row:
        return render_template("invalid.html", code=code)

    name, amount, remaining, used, used_date, date_to = row
    if used:
        return render_template("used.html", code=code, name=name, used_date=used_date)
    else:
        return render_template("valid.html", code=code, name=name, remaining=remaining, date_to=date_to)
if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))  # Render sẽ gán PORT vào biến môi trường
    app.run(host='0.0.0.0', port=port)
