from flask import Flask, render_template, request
import smtplib
from email.message import EmailMessage
import os
from dotenv import load_dotenv

# .env dosyasını yükle
load_dotenv()

app = Flask(__name__)

# ENV değişkenleri
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
RECEIVER_EMAIL = os.getenv("RECEIVER_EMAIL")


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        message = request.form["message"]

        # === Gelen mesaj (sana) ===
        msg = EmailMessage()
        msg["Subject"] = "Yeni İletişim Formu"
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = RECEIVER_EMAIL
        msg.set_content(
            f"Ad: {name}\n"
            f"Email: {email}\n\n"
            f"Mesaj:\n{message}"
        )

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)

        # === Otomatik cevap (kullanıcıya) ===
        reply = EmailMessage()
        reply["Subject"] = "Mesajınız alındı"
        reply["From"] = EMAIL_ADDRESS
        reply["To"] = email
        reply.set_content(
            f"""Merhaba {name},

Mesajınızı aldık.
En kısa sürede size dönüş yapacağız.

İyi günler.
"""
        )

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(reply)

        return "Mesaj gönderildi ✅"

    return render_template("index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
