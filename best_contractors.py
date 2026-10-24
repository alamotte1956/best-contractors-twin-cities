from flask import Flask, request, render_template_string
import os

app = Flask(__name__)

CONSUMER_AGREEMENT = """
By submitting this form you agree:
- Restoration Contractors MN will match you with one licensed Minnesota contractor
- We verify the contractor’s Minnesota license only — not insurance
- You are responsible for confirming the contractor carries insurance before work begins
- No shared leads — only one contractor will contact you
- All agreements are subject to Minnesota law (including the Home Solicitation Sales Act)
"""

BASE_CSS = """
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: system-ui, -apple-system, Segoe UI, Roboto, sans-serif; color: #0f172a; background: #fff; line-height: 1.5; }
.nav { padding: 18px 24px; display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #f1f5f9; }
.nav a { color: #0ea5e9; font-weight: 600; text-decoration: none; }
.nav a:hover { text-decoration: underline; }
.logo { font-weight: 700; font-size: 1.15rem; }
.hero { background: linear-gradient(160deg, #0f172a 0%, #1e3a8a 100%); color: white; padding: 80px 20px 60px; text-align: center; }
.hero h1 { font-size: 2.6rem; font-weight: 700; letter-spacing: -0.02em; margin-bottom: 12px; line-height: 1.15; }
.hero p { font-size: 1.2rem; opacity: 0.92; max-width: 560px; margin: 0 auto 28px; }
.badges { display: flex; gap: 8px; justify-content: center; flex-wrap: wrap; margin-bottom: 28px; }
.badge { background: rgba(255,255,255,0.12); padding: 6px 14px; border-radius: 999px; font-size: 0.85rem; font-weight: 500; }
.cta { display: inline-block; background: #0ea5e9; color: white; padding: 16px 32px; border-radius: 10px; font-weight: 600; text-decoration: none; font-size: 1.05rem; }
.cta:hover { background: #0284c7; }
.section { max-width: 900px; margin: 0 auto; padding: 60px 20px; }
h2 { text-align: center; font-size: 1.8rem; margin-bottom: 8px; }
.sub { text-align: center; color: #64748b; margin-bottom: 32px; }
.steps { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 24px; }
.step { text-align: center; }
.num { width: 42px; height: 42px; background: #0ea5e9; color: white; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto 12px; font-weight: 700; }
.form-wrap { background: #f8fafc; padding: 50px 20px; }
.form-card { background: white; border-radius: 16px; padding: 32px; max-width: 480px; margin: 0 auto; box-shadow: 0 8px 30px rgba(0,0,0,0.07); }
label { display: block; font-weight: 500; margin: 14px 0 6px; font-size: 0.95rem; }
input, select, textarea { width: 100%; padding: 13px; border: 1px solid #cbd5e1; border-radius: 8px; font-size: 16px; }
button { width: 100%; background: #0ea5e9; color: white; border: none; padding: 16px; border-radius: 8px; font-size: 17px; font-weight: 600; margin-top: 16px; cursor: pointer; }
button:hover { background: #0284c7; }
.agreement { border: 1px solid #e2e8f0; padding: 14px; margin: 14px 0; background: #f8fafc; font-size: 13.5px; border-radius: 8px; }
.note { background: #fef3c7; color: #854d0e; padding: 10px 14px; border-radius: 8px; margin-bottom: 14px; font-weight: 600; font-size: 0.95rem; }
.footer { text-align: center; padding: 30px 20px; color: #64748b; font-size: 0.9rem; }
@media (max-width: 640px) { .hero h1 { font-size: 2rem; } .hero { padding: 60px 16px 40px; } }
"""

HOME_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Best Contractors Twin Cities — One Pro. No Shared Leads.</title>
  <style>""" + BASE_CSS + """</style>
</head>
<body>
  <div class="nav">
    <div class="logo">Restoration Contractors MN</div>
    <a href="https://best-leads-sales-production.up.railway.app/signup" style="color:#0ea5e9;font-weight:600;text-decoration:none;">Contractor Signup</a>
  </div>
  <div class="hero">
    <div class="badges">
      <span class="badge">Exclusive Match</span>
      <span class="badge">One Contractor Only</span>
      <span class="badge">No Shared Leads</span>
    </div>
    <h1>Get One Licensed Contractor Today</h1>
    <p>Water damage, mold, roofing, or remodel? We match you with one vetted Twin Cities pro. Your phone won’t blow up.</p>
    <a href="#form" class="cta">Get My Contractor</a>
  </div>
  <div class="section">
    <h2>How It Works</h2>
    <p class="sub">Simple. Exclusive. Fast.</p>
    <div class="steps">
      <div class="step"><div class="num">1</div><strong>Tell Us</strong><p style="color:#64748b;margin-top:6px;">Describe the job and your ZIP.</p></div>
      <div class="step"><div class="num">2</div><strong>We Match</strong><p style="color:#64748b;margin-top:6px;">One verified contractor is selected.</p></div>
      <div class="step"><div class="num">3</div><strong>They Call</strong><p style="color:#64748b;margin-top:6px;">Only one pro contacts you.</p></div>
    </div>
  </div>
  <div class="form-wrap" id="form">
    <div class="form-card">
      <h2 style="text-align:left;font-size:1.5rem;margin-bottom:6px;">Request Help</h2>
      <p style="color:#64748b;margin-bottom:12px;">Exclusive matching. One contractor only.</p>
      <div class="note">Your information goes to one contractor only — no shared leads.</div>
      <form method="post">
        <label>Name</label><input name="name" required>
        <label>Phone</label><input name="phone" type="tel" required>
        <label>Email</label><input name="email" type="email" required>
        <label>ZIP Code</label><input name="zip" required>
        <label>Service</label>
        <select name="service" required>
          <option value="">What do you need?</option>
          <option>Water Damage</option>
          <option>Mold</option>
          <option>Roofing</option>
          <option>Bathroom Remodel</option>
          <option>Kitchen Remodel</option>
          <option>Other</option>
        </select>
        <label>Details</label><textarea name="details" rows="3" placeholder="Briefly describe the job"></textarea>
        <div class="agreement">
          <strong>Consumer Agreement</strong><br>
          {{ agreement }}
          <label style="display:block;margin-top:10px;">
            <input type="checkbox" name="agree" required style="width:auto;margin-right:6px;"> I agree to the Consumer Agreement
          </label>
        </div>
        <button type="submit">Get My Free Match Now</button>
      </form>
      <p style="text-align:center;font-size:13px;color:#64748b;margin-top:12px;">No obligation. One contractor. Fast response.</p>
    </div>
  </div>
  <div class="footer">
    <a href="/privacy">Privacy Policy</a> · <a href="/terms">Terms & Conditions</a><br>
    Restoration Contractors MN · Albert R LaMotte dba Restoration Contractors MN
  </div>
</body>
</html>
"""

THANKYOU_HTML = """
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
  <title>Thank You</title>
  <style>""" + BASE_CSS + """</style>
</head>
<body>
  <div class="hero" style="padding:70px 20px 50px;"><h1>Thank You!</h1></div>
  <div class="section" style="text-align:center;padding-top:30px;">
    <h2>Your request has been received</h2>
    <p style="font-size:1.1rem;margin:16px 0;">A licensed contractor will contact you shortly.</p>
    <p><strong>Only one contractor will call — no shared leads.</strong></p>
    <a href="/" class="cta" style="margin-top:20px;">Back to Home</a>
  </div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        if not request.form.get("agree"):
            return "You must agree to the terms to continue.", 400
        return render_template_string(THANKYOU_HTML)
    return render_template_string(HOME_HTML, agreement=CONSUMER_AGREEMENT)

@app.route("/privacy")
def privacy():
    return render_template_string("""
    <!DOCTYPE html><html><head><meta name="viewport" content="width=device-width,initial-scale=1"><title>Privacy Policy</title>
    <style>""" + BASE_CSS + """</style></head><body>
    <div class="section" style="padding-top:40px;"><div class="form-card">
      <h1>Privacy Policy</h1>
      <p style="margin:16px 0;">Restoration Contractors MN (Albert R LaMotte dba Restoration Contractors MN) collects name, phone, email, ZIP, and project details solely to match you with one exclusive contractor.</p>
      <p style="margin:16px 0;">We do not sell or share your information with multiple contractors. Data is used only for this matching service and required notifications.</p>
      <p style="margin:16px 0;">By submitting the form you consent to SMS and email contact related to your request.</p>
      <p><a href="/">← Back</a></p>
    </div></div></body></html>
    """)

@app.route("/terms")
def terms():
    return render_template_string("""
    <!DOCTYPE html><html><head><meta name="viewport" content="width=device-width,initial-scale=1"><title>Terms & Conditions</title>
    <style>""" + BASE_CSS + """</style></head><body>
    <div class="section" style="padding-top:40px;"><div class="form-card">
      <h1>Terms & Conditions</h1>
      <p style="margin:16px 0;">This service connects homeowners with independent contractors. We are not the contractor and do not perform the work.</p>
      <p style="margin:16px 0;">Leads are exclusive — only one contractor receives your contact information.</p>
      <p style="margin:16px 0;">Minnesota law applies. Home solicitation and consumer protection statutes are observed. You may cancel certain contracts as provided by Minnesota law.</p>
      <p style="margin:16px 0;">By using this site you agree that one vetted contractor will contact you regarding your request.</p>
      <p><a href="/">← Back</a></p>
    </div></div></body></html>
    """)

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    app.run(host="0.0.0.0", port=port, debug=False)
