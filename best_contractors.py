"""
Best Contractors in Twin Cities
Homeowner landing page and lead intake server.
"""
from flask import Flask, request, redirect, render_template_string
import os
from datetime import datetime

app = Flask(__name__)

# Serve the landing page
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
        <p>Your request has been received. A licensed local contractor will contact you shortly.</p>
        <p>Your information was sent to one contractor only — no shared leads.</p>
        <p><a href="/">Submit another request</a></p>
      </div>
    </body>
    </html>
    """

@app.route("/leads")
def view_leads():
    if not leads:
        return "<h2>No leads yet</h2><a href='/'>Back</a>"
    rows = "".join(
        f"<tr><td>{l.get('created')}</td><td>{l.get('service_type')}</td><td>{l.get('zip')}</td><td>{l.get('name')}</td><td>{l.get('phone')}</td></tr>"
        for l in reversed(leads)
    )
    return f"""
    <h2>Leads</h2>
    <table border="1" cellpadding="8">
      <tr><th>Time</th><th>Service</th><th>ZIP</th><th>Name</th><th>Phone</th></tr>
      {rows}
    </table>
    <p><a href="/">Back</a></p>
    """

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
