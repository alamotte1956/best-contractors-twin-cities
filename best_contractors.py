"""
Best Contractors in Twin Cities
Homeowner landing page and lead intake server.
"""
from flask import Flask, request, redirect, render_template_string, session
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "best-contractors-admin-2026")

ADMIN_USER = os.environ.get("ADMIN_USER", "admin")
ADMIN_PASS = os.environ.get("ADMIN_PASS", "changeme123")
SALES_URL = os.environ.get("SALES_URL", "https://best-leads-sales-production.up.railway.app")

# Serve the landing page
@app.route("/consumer_agreement")
def consumer_agreement():
    return """
    <html>
    <head><title>Consumer Agreement — Restoration Contractors MN</title>
    <style>body{font-family:system-ui;max-width:700px;margin:40px auto;padding:20px;line-height:1.6;}</style>
    </head>
    <body>
    <h1>Consumer Agreement</h1>
    <p><strong>Albert R LaMotte dba: Restoration Contractors MN</strong></p>
    <p>By submitting this form, you agree to the following under Minnesota law:</p>
    <ol>
      <li>You request that one licensed and insured contractor contact you about the project described.</li>
      <li>Your contact information will be shared only with the single contractor matched to your request. It will not be shared with multiple companies.</li>
      <li>You understand this is not a contract for work. Any work agreement is between you and the contractor.</li>
      <li>If you later enter a contract for work at your home, you may have the right to cancel within three business days under Minnesota’s Home Solicitation Sales Act (Minn. Stat. §§ 325G.06–325G.11).</li>
      <li>You authorize the matched contractor to contact you by phone, text, or email regarding this request, consistent with the Telephone Consumer Protection Act and Minnesota law.</li>
      <li>The matched contractor must hold any license required for the work under Minnesota Statutes Chapter 326B and maintain required insurance.</li>
      <li>Albert R LaMotte dba: Restoration Contractors MN is a lead matching service only. It is not a contractor, does not perform work, and is not a party to any contract between you and a contractor.</li>
      <li>Contractors are independent businesses. We do not guarantee the quality, timing, or outcome of their work.</li>
      <li>You release Albert R LaMotte dba: Restoration Contractors MN from any claims arising from the contractor’s workmanship, delays, pricing, or any dispute with the contractor.</li>
      <li>The service is provided “as is.” We do not warrant that a contractor will contact you or that the project will be completed.</li>
      <li>This agreement is governed by the laws of the State of Minnesota, including the Home Solicitation Sales Act and consumer protection statutes.</li>
    </ol>
    <p>By checking the box and submitting, you acknowledge that you have read and agree to these terms.</p>
    <p><a href="/">Back to form</a></p>
    </body>
    </html>
    """

@app.route("/")
def home():
    with open("best_contractors_twin_cities.html", "r", encoding="utf-8") as f:
        return f.read()

# Simple lead capture (stores in memory for now; can connect to sales DB later)
leads = []

@app.route("/submit", methods=["POST"])
def submit():
    data = request.form.to_dict()
    data["created"] = datetime.now().strftime("%Y-%m-%d %H:%M")
    data["status"] = "New"
    leads.append(data)

    # Thank-you page with conversion tracking
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
      <title>Thank You — Best Contractors in Twin Cities</title>
      <script async src="https://www.googletagmanager.com/gtag/js?id=AW-1005055868"></script>
      <script>
        window.dataLayer = window.dataLayer || [];
        function gtag(){{dataLayer.push(arguments);}}
        gtag('js', new Date());
        gtag('config', 'AW-1005055868');
        gtag('event', 'conversion', {{
          'send_to': 'AW-1005055868/lxJsCP2wwKIdEPzen98D'
        }});
      </script>
      <style>
        body {{ font-family: system-ui, sans-serif; max-width: 600px; margin: 60px auto; padding: 20px; text-align: center; }}
        .card {{ background: white; border-radius: 12px; padding: 32px; box-shadow: 0 4px 20px rgba(0,0,0,0.08); }}
        a {{ color: #1e40af; }}
      </style>
    </head>
    <body>
      <div class="card">
        <h2>Thank You, {data.get('name','')}!</h2>
        <p style="background:#dcfce7; padding:12px; border-radius:8px; font-weight:600;">Your request has been submitted successfully.</p>
        <p>A licensed local contractor will contact you shortly.</p>
        <p>Your information was sent to one contractor only — no shared leads.</p>
        <p style="font-size:0.9rem; color:#64748b;">Your contact details are used only for this request and are not sold or shared with multiple companies.</p>
        <p><a href="/">Submit another request</a> · <a href="/consumer_agreement">View agreement</a></p>
      </div>
    </body>
    </html>
    """

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form.get("username") == ADMIN_USER and request.form.get("password") == ADMIN_PASS:
            session["admin"] = True
            return redirect("/admin")
        return "<h2>Login failed</h2><p><a href='/login'>Try again</a></p>"
    return """
    <!DOCTYPE html>
    <html>
    <head><title>Admin Login</title>
    <style>
      body { font-family: system-ui; max-width: 400px; margin: 80px auto; padding: 20px; }
      input { width: 100%; padding: 10px; margin: 8px 0; border: 1px solid #ccc; border-radius: 6px; }
      button { width: 100%; padding: 12px; background: #1e40af; color: white; border: none; border-radius: 6px; font-size: 16px; }
    </style>
    </head>
    <body>
      <h2>Best Contractors Admin</h2>
      <form method="POST">
        <input name="username" placeholder="Username" required>
        <input name="password" type="password" placeholder="Password" required>
        <button type="submit">Log in</button>
      </form>
    </body>
    </html>
    """

@app.route("/logout")
def logout():
    session.pop("admin", None)
    return redirect("/login")

def require_admin():
    if not session.get("admin"):
        return redirect("/login")
    return None

@app.route("/admin")
def admin():
    redir = require_admin()
    if redir:
        return redir
    if not leads:
        return """
        <div style="font-family:system-ui; max-width:900px; margin:40px auto; padding:20px;">
          <h1>Best Contractors Admin</h1>
          <p>No leads yet.</p>
          <a href="/">Back to form</a>
        </div>
        """
    rows = ""
    for i, l in enumerate(reversed(leads)):
        idx = len(leads) - 1 - i
        status_color = {"New": "#fef9c3", "Contacted": "#dbeafe", "Sold": "#dcfce7", "Lost": "#fee2e2"}.get(l.get("status","New"), "#f1f5f9")
        rows += f"""
        <tr style="background:{status_color}">
          <td>{l.get('created')}</td>
          <td>{l.get('service_type','')}</td>
          <td>{l.get('urgency','')}</td>
          <td>{l.get('zip','')}</td>
          <td>{l.get('name','')}<br><small>{l.get('phone','')}<br>{l.get('email','')}</small></td>
          <td>{l.get('details','')[:80]}</td>
          <td>
            <form method="POST" action="/update_status" style="display:inline;">
              <input type="hidden" name="idx" value="{idx}">
              <select name="status" onchange="this.form.submit()">
                <option {'selected' if l.get('status')=='New' else ''}>New</option>
                <option {'selected' if l.get('status')=='Contacted' else ''}>Contacted</option>
                <option {'selected' if l.get('status')=='Sold' else ''}>Sold</option>
                <option {'selected' if l.get('status')=='Lost' else ''}>Lost</option>
              </select>
            </form>
          </td>
        </tr>
        """
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
      <title>Admin — Best Contractors</title>
      <meta name="viewport" content="width=device-width, initial-scale=1">
      <style>
        body {{ font-family: system-ui, sans-serif; max-width: 1100px; margin: 30px auto; padding: 16px; background: #f8fafc; }}
        table {{ width: 100%; border-collapse: collapse; background: white; }}
        th, td {{ padding: 10px; border-bottom: 1px solid #e2e8f0; text-align: left; font-size: 0.9rem; vertical-align: top; }}
        th {{ background: #0f172a; color: white; }}
        a {{ color: #1e40af; }}
      </style>
    </head>
    <body>
      <h1>Best Contractors Admin</h1>
      <p><a href="/">Homeowner form</a> · <a href="/logout">Log out</a> · Total leads: {len(leads)}</p>
      <table>
        <tr><th>Received</th><th>Service</th><th>Urgency</th><th>ZIP</th><th>Contact</th><th>Details</th><th>Status</th></tr>
        {rows}
      </table>
    </body>
    </html>
    """

@app.route("/update_status", methods=["POST"])
def update_status():
    redir = require_admin()
    if redir:
        return redir
    idx = int(request.form.get("idx", -1))
    new_status = request.form.get("status")
    if 0 <= idx < len(leads) and new_status in ("New", "Contacted", "Sold", "Lost"):
        leads[idx]["status"] = new_status
    return redirect("/admin")

@app.route("/leads")
def view_leads():
    return redirect("/admin")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
