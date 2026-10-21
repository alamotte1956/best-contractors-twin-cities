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

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        if not request.form.get("agree"):
            return "You must agree to the terms to continue.", 400
        return """
        <!DOCTYPE html>
        <html>
        <head>
          <title>Thank You</title>
          <meta name="viewport" content="width=device-width, initial-scale=1">
          <style>
            body { font-family: system-ui, sans-serif; max-width: 600px; margin: 60px auto; padding: 20px; text-align: center; }
            .cta { background: #0ea5e9; color: white; padding: 14px 28px; text-decoration: none; border-radius: 8px; display: inline-block; margin-top: 20px; }
          </style>
        </head>
        <body>
          <h2>Thank you!</h2>
          <p>A licensed contractor will contact you shortly.</p>
          <p><strong>Only one contractor will call — no shared leads.</strong></p>
        </body>
        </html>
        """
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
      <title>Best Contractors in Twin Cities — Get Help Today</title>
      <meta name="viewport" content="width=device-width, initial-scale=1">
      <style>
        body { font-family: system-ui, sans-serif; max-width: 640px; margin: 30px auto; padding: 20px; line-height: 1.6; color: #1e293b; }
        h1 { color: #0f172a; font-size: 28px; margin-bottom: 10px; }
        .sub { font-size: 18px; color: #334155; margin-bottom: 20px; }
        .benefits { background: #f1f5f9; padding: 15px; border-radius: 10px; margin: 20px 0; }
        .benefits li { margin: 6px 0; }
        input, select, textarea, button { width: 100%; padding: 14px; margin: 8px 0; box-sizing: border-box; border-radius: 8px; border: 1px solid #cbd5e1; font-size: 16px; }
        button { background: #0ea5e9; color: white; border: none; font-size: 18px; font-weight: 600; cursor: pointer; margin-top: 10px; }
        button:hover { background: #0284c7; }
        .agreement { border: 1px solid #e2e8f0; padding: 15px; margin: 15px 0; background: #f8fafc; font-size: 14px; border-radius: 8px; }
        .urgency { color: #dc2626; font-weight: 600; }
      </style>
    </head>
    <body>
      <h1>Get One Licensed Contractor Today</h1>
      <p class="sub">Water damage, mold, roofing, or remodel? Tell us what you need. We match you with <strong>one licensed local contractor</strong> — no phone blow-up.</p>

      <div class="benefits">
        <strong>Why homeowners choose us:</strong>
        <ul>
          <li>Only one contractor contacts you</li>
          <li>Licensed Minnesota contractors only</li>
          <li>Fast response on urgent jobs</li>
          <li>No shared leads</li>
        </ul>
      </div>

      <p class="urgency">Limited openings for exclusive matches this week.</p>

      <form method="post">
        <input name="name" placeholder="Your Name" required>
        <input name="phone" placeholder="Phone" required>
        <input name="email" type="email" placeholder="Email" required>
        <input name="zip" placeholder="ZIP Code" required>
        <select name="service" required>
          <option value="">What do you need help with?</option>
          <option>Water Damage</option>
          <option>Mold</option>
          <option>Roofing</option>
          <option>Bathroom Remodel</option>
          <option>Kitchen Remodel</option>
          <option>Other</option>
        </select>
        <textarea name="details" placeholder="Briefly describe the job" rows="4"></textarea>
        <div class="agreement">
          <strong>Consumer Agreement</strong><br>
          {{ agreement }}
          <label style="display:block; margin-top:10px;">
            <input type="checkbox" name="agree" required> I agree to the Consumer Agreement
          </label>
        </div>
        <button type="submit">Get My Free Match Now</button>
      </form>
      <p style="text-align:center; font-size:14px; color:#64748b; margin-top:15px;">No obligation. One contractor. Fast response.</p>
    </body>
    </html>
    """, agreement=CONSUMER_AGREEMENT)

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    app.run(host="0.0.0.0", port=port, debug=False)
