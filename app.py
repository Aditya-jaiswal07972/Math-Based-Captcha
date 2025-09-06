# app.py
import os
import random
import io
import base64
import time

from flask import Flask, render_template_string, request, session, redirect, url_for, flash
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

app = Flask(__name__)
# Use an environment variable for production; fallback for quick testing:
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-change-me")

FONT_PATH = os.path.join(os.path.dirname(__file__), "captcha.ttf")  # ensure captcha.ttf exists


def generate_captcha():
    n1 = random.randint(0, 9)
    n2 = random.randint(0, 9)
    op = random.choice(["+", "-", "*"])

    if op == "+":
        ans = n1 + n2
    elif op == "-":
        ans = n1 - n2
    else:
        ans = n1 * n2

    expr_full = f"{n1} {op} {n2} = ?"
    expr_for_img = f"{n1}{op}{n2}"

    # Create a blank image
    img = Image.new("RGB", (300, 100), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)

    # Use provided captcha.ttf if available
    try:
        font = ImageFont.truetype(FONT_PATH, 100)  # TTF font
        bbox = draw.textbbox((0, 0), expr_for_img, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
    except Exception:
        # fallback to default font
        font = ImageFont.load_default()
        text_width, text_height = draw.textsize(expr_for_img, font=font)

    x = (img.width - text_width) // 2
    y = (img.height - text_height) // 2
    draw.text((x,y), expr_for_img, font=font, fill=(0, 0, 0))

    # Convert to base64 for embedding in HTML
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    b64 = base64.b64encode(buf.getvalue()).decode("ascii")

    return expr_full, ans, b64


PAGE = """
<!doctype html>
<title>Math CAPTCHA</title>
<style>
  body {
    font-family: 'Inter', sans-serif;
    background-color: #f4f7fa;
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
    margin: 0;
  }

  .container {
    background-color: white;
    padding: 30px;
    border-radius: 12px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    max-width: 400px;
    width: 100%;
  }

  h2 {
    text-align: center;
    font-size: 1.5rem;
    margin-bottom: 20px;
    color: #333;
  }

  .captcha-image {
    text-align: center;
    margin-bottom: 20px;
  }

  .captcha-image img {
    max-width: 100%;
    border: 1px solid #ddd;
    border-radius: 8px;
  }

  .message {
    margin: 15px 0;
    padding: 10px;
    background-color: #ffeb3b;
    color: #333;
    border-radius: 5px;
    font-size: 0.9rem;
    text-align: center;
    opacity: 0;
    animation: fadeIn 0.5s forwards;
    }
    @keyframes fadeIn {
     0% { opacity: 0; }
   100% { opacity: 1; }
  }
  .message strong {
    font-weight: bold;
  }

  form {
    display: flex;
    flex-direction: column;
    align-items: center;
  }

  .input-container {
    display: flex;
    justify-content: center;
    padding: 0 15px;
    width: 100%;
    max-width: 350px;
    margin-bottom: 20px;
  }

  .captcha-input {
    width: 100%;
    padding: 15px;
    border: 2px solid #ddd;
    border-radius: 8px;
    font-size: 1rem;
    text-align: center;
    outline: none;
    transition: border-color 0.3s ease;
  }

  .captcha-input:focus {
    border-color: #4CAF50;
    box-shadow: 0 0 8px rgba(76, 175, 80, 0.3);
  }

  .submit-container {
    width: 100%;
    max-width: 150px;
    margin-top: 10px;
  }

  .submit-btn {
    width: 100%;
    padding: 12px;
    background-color: #4CAF50;
    color: white;
    border: none;
    border-radius: 8px;
    font-size: 1rem;
    cursor: pointer;
    transition: background-color 0.3s ease;
  }

  .submit-btn:hover {
   background-color: #45a049;
   transition: background-color 0.3s ease, transform 0.1s ease;
   transform: scale(1.05);
}

    .submit-btn:active {
   background-color: #388e3c;
   transform: scale(1);
}


  ul {
    padding-left: 0;
    list-style: none;
  }

  li {
    margin: 5px 0;
  }
</style>

<div class="container">
  <h2>Solve the math captcha</h2>

  {% with messages = get_flashed_messages(with_categories=true) %}
    {% if messages %}
      <div class="message">
        <ul>
          {% for cat, msg in messages %}
            <li><strong>{{ msg }}</strong></li>
          {% endfor %}
        </ul>
      </div>
    {% endif %}
  {% endwith %}

  <form method="post">
    <div class="captcha-image">
      <img src="data:image/png;base64,{{ img_b64 }}" alt="captcha">
    </div>

    <div class="input-container">
      <input name="answer" placeholder="Enter result" autocomplete="off" type="text" class="captcha-input">
    </div>

    <div class="submit-container">
      <button type="submit" class="submit-btn">Submit</button>
    </div>
  </form>
</div>

"""



EXPIRY_SECONDS = 600  # 10 minutes

@app.route("/", methods=["GET", "POST"])
def index():
    verified_at = session.get("verified_at")

    # If already verified and still valid, skip captcha
    if verified_at and time.time() - verified_at < EXPIRY_SECONDS:
        return redirect(url_for("verified"))

    if request.method == "POST":
        user_answer = request.form.get("answer", "").strip()
        try:
            if "captcha_answer" in session and int(user_answer) == session["captcha_answer"]:
                session["verified_at"] = time.time()
                return redirect(url_for("verified"))
            else:
                flash("❌ Incorrect — try again.")
        except ValueError:
            flash("Please enter a valid number.")
        return redirect(url_for("index"))

    # Generate new captcha
    expr, ans, img_b64 = generate_captcha()
    session["captcha_answer"] = ans
    return render_template_string(PAGE, img_b64=img_b64)


@app.route("/verified")
def verified():
    verified_at = session.get("verified_at")

    # If expired or missing, just show captcha again (not redirect loop)
    if not verified_at or time.time() - verified_at >= EXPIRY_SECONDS:
        session.pop("verified_at", None)
        return """
        <!doctype html>
        <html>
        <head><meta http-equiv="refresh" content="2;url=/"></head>
        <body style="font-family:Arial; text-align:center; margin-top:20%;">
          <h2>⚠️ Verification expired</h2>
          <p>You’ll be redirected to captcha page...</p>
        </body>
        </html>
        """

    # Still verified: show success and redirect to The India Ledger
    return """
    <!doctype html>
    <html>
    <head>
      <meta http-equiv="refresh" content="2;url=https://theindialedger.web.app/">
      <title>Verified</title>
      <style>
        body {
          display: flex;
          justify-content: center;
          align-items: center;
          height: 100vh;
          background: #f4f7fa;
          font-family: Arial, sans-serif;
        }
        .box {
          text-align: center;
          background: white;
          padding: 30px;
          border-radius: 10px;
          box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }
        h2 { color: #4CAF50; }
      </style>
    </head>
    <body>
      <div class="box">
        <h2>✅ User verified</h2>
        <p>Redirecting to <strong>The India Ledger</strong>...</p>
      </div>
    </body>
    </html>
    """

