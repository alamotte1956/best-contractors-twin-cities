from flask import Flask, request, render_template_string, redirect, url_for, session, flash
import sqlite3
import os
from datetime import datetime
import hashlib

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "change-this-secret-key")

DB_PATH = "consumer.db"

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as db:
        db.executescript("""
            CREATE TABLE IF NOT EXISTS leads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone TEXT NOT NULL,
                email TEXT NOT NULL,
                zip TEXT NOT NULL,
                service_type TEXT,
                details TEXT,
                created_at TEXT,
                status TEXT DEFAULT 'new'
            );
            CREATE TABLE IF NOT EXISTS settings (
                key TEXT PRIMARY KEY,
                value TEXT
            );
        """)
        db.execute("INSERT OR IGNORE INTO settings (key, value) VALUES ('company', 'Restoration Contractors MN')")

init_db()

HOME_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Best Contractors Twin Cities — One Pro. No Shared Leads.</title>
<style>
body { font-family: system-ui, sans-serif; margin: 0; background: #f8fafc; color: #1e293b; }
.hero { background: linear-gradient(135deg, #0f172a, #1e40af); color: white; padding: 60px 20px; text-align: center; }
.container { max-width: 700px; margin: 40px auto; padding: 20px; }
.card { background: white; border-radius: 12px; padding: 30px; box-shadow: 0 4px 20px rgba(0,0,0,0.08); }
input, select, textarea { width: 100%; padding: 12px; margin: 8px 0; border: 1px solid #cbd5e1; border-radius: 8px; box-sizing: border-box; }
button { width: 100%; background: #0ea5e9; color: white; border: none; padding: 16px; border-radius: 8px; font-size: 18px; cursor: pointer; }
.steps { display: flex; gap: 20px; margin: 40px 0; text-align: center; }
.step { flex: 1; }
footer { text-align: center; padding: 20px; font-size: 14px; color: #64748b; }
</style>
</head>
<body>
<div class="hero">
  <h1>Get One Licensed Contractor Today</h1>
  <p>Water damage, mold, roofing, or remodel? We match you with one vetted Twin Cities pro. Your phone won’t blow up.</p>
  <p><strong>Exclusive Match · One Contractor Only · No Shared Leads</strong></p>
</div>
<div class="container">
  <div class="steps">
    <div class="step"><h3>1. Tell Us</h3><p>Describe the job and your ZIP.</p></div>
    <div class="step"><h3>2. We Match</h3><p>One verified contractor is selected.</p></div>
    <div class="step"><h3>3. They Call</h3><p>Only one pro contacts you.</p></div>
  </div>
  <div class="card">
    <h2>Request Help</h2>
    <p>Exclusive matching. One contractor only.</p>
    <form method="post" action="/submit">
      <input name="name" placeholder="Full Name" required>
      <input name="phone" placeholder="Phone" required>
      <input name="email" type="email" placeholder="Email" required>
      <input name="zip" placeholder="ZIP Code" required pattern="[0-9]{5}">
      <select name="service_type" required>
        <option value="">Service Needed</option>
        <option>Water Damage / Mold</option>
        <option>Roofing</option>
        <option>Siding</option>
        <option>Windows</option>
        <option>Kitchen / Bath Remodel</option>
        <option>Addition</option>
        <option>Other</option>
      </select>
      <textarea name="details" rows="4" placeholder="What happened? Details of the job..."></textarea>
      <p style="font-size:13px; color:#475569;">
        <strong>Consumer Agreement</strong><br>
        By submitting you agree Restoration Contractors MN will match you with one licensed Minnesota contractor.
        We verify Minnesota license only — not insurance. You confirm insurance before work begins.
        No shared leads. Subject to Minnesota law (including Home Solicitation Sales Act).
      </p>
      <button type="submit">Get My Free Match Now</button>
    </form>
  </div>
</div>
<footer>
  <a href="/privacy">Privacy Policy</a> · <a href="/terms">Terms & Conditions</a><br>
  Restoration Contractors MN · Albert R LaMotte dba Restoration Contractors MN
</footer>
</body>
</html>
"""

@app.route("/")
def home():
    return HOME_HTML

@app.route("/submit", methods=["POST"])
def submit():
    data = {
        "name": request.form.get("name"),
        "phone": request.form.get("phone"),
        "email": request.form.get("email"),
        "zip": request.form.get("zip"),
        "service_type": request.form.get("service_type"),
        "details": request.form.get("details"),
        "created_at": datetime.utcnow().isoformat()
    }
    with get_db() as db:
        db.execute("""INSERT INTO leads (name, phone, email, zip, service_type, details, created_at)
                      VALUES (:name, :phone, :email, :zip, :service_type, :details, :created_at)""", data)
    return """
    <h2>Thank You!</h2>
    <p>Your request has been received. One contractor will contact you shortly.</p>
    <p>No shared leads — only one pro will call.</p>
    <a href="/">Back</a>
    """

@app.route("/privacy")
def privacy():
    return render_template_string("""
    <h1>Privacy Policy</h1>
    <p>We collect name, phone, email, ZIP, and project details solely to match you with one contractor.
    We do not share leads with multiple contractors. Data is used only for this matching service.
    Subject to Minnesota law.</p>
    <a href="/">Home</a>
    """)

@app.route("/terms")
def terms():
    return render_template_string("""
    <h1>Terms & Conditions</h1>
    <p>By submitting a request you agree to be matched with one independent Minnesota contractor.
    Restoration Contractors MN is a matching service only. We do not perform the work.
    All agreements governed by Minnesota law, including the Home Solicitation Sales Act where applicable.</p>
    <a href="/">Home</a>
    """)

@app.route("/seed")
def seed():
    demos = [
        ("Jane Smith", "612-555-0101", "jane@example.com", "55406", "Water Damage", "Basement flood"),
        ("Bob Johnson", "651-555-0202", "bob@example.com", "55344", "Roofing", "Missing shingles"),
        ("Alice Lee", "763-555-0303", "alice@example.com", "55345", "Kitchen Remodel", "Full gut"),
    ]
    with get_db() as db:
        for d in demos:
            db.execute("INSERT INTO leads (name, phone, email, zip, service_type, details, created_at) VALUES (?,?,?,?,?,?,?)",
                       (*d, datetime.utcnow().isoformat()))
    return "Seeded demo leads. <a href='/'>Home</a>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
