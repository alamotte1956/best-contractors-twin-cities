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
        # In production this would forward the lead to the sales system
        return """
        <!DOCTYPE html>
        <html>
        <head>
          <title>Thank You</title>
          <meta name="viewport" content="width=device-width, initial-scale=1">
          <style>
            body { font-family: system-ui, sans-serif; max-width: 600px; margin: 60px auto; padding: 20px; text-align: center; }
          </style>
        </head>
        <body>
          <h2>Thank you!</h2>
          <p>A licensed contractor will contact you shortly.</p>
          <p>Only one contractor will call — no shared leads.</p>
        </body>
        </html>
        """
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
      <title>Best Contractors in Twin Cities</title>
      <meta name="viewport" content="width=device-width, initial-scale=1">
      <style>
        body { font-family: system-ui, sans-serif; max-width: 600px; margin: 40px auto; padding: 20px; line-height: 1.5; }
        input, select, textarea, button { width: 100%; padding: 12px; margin: 8px 0; box-sizing: border-box; border-radius: 6px; border: 1px solid #ccc; }
        button { background: #0ea5e9; color: white; border: none; font-size: 16px; cursor: pointer; }
        .agreement { border: 1px solid #ccc; padding: 15px; margin: 15px 0; background: #f9f9f9; font-size: 14px; }
        h1 { color: #0f172a; }
      </style>
    </head>
    <body>
      <h1>One Licensed Contractor. No Shared Leads.</h1>
      <p>Tell us about the job. We match you with one licensed local contractor. No phone blow-up.</p>
      <form method="post">
        <input name="name" placeholder="Your Name" required>
        <input name="phone" placeholder="Phone" required>
        <input name="email" type="email" placeholder="Email" required>
        <input name="zip" placeholder="ZIP Code" required>
        <select name="service" required>
          <option value="">Service needed</option>
          <option>Water Damage</option>
          <option>Mold</option>
          <option>Roofing</option>
          <option>Bathroom Remodel</option>
          <option>Kitchen Remodel</option>
          <option>Other</option>
        </select>
        <textarea name="details" placeholder="Describe the job" rows="4"></textarea>
        <div class="agreement">
          <strong>Consumer Agreement</strong><br>
          {{ agreement }}
          <label style="display:block; margin-top:10px;">
            <input type="checkbox" name="agree" required> I agree to the Consumer Agreement
          </label>
        </div>
        <button type="submit">Get My Contractor</button>
      </form>
    </body>
    </html>
    """, agreement=CONSUMER_AGREEMENT)

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    app.run(host="0.0.0.0", port=port, debug=False)
