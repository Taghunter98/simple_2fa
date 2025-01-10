import os
from flask import Flask, request, jsonify
from flask_mail import Mail, Message
from flask_cors import CORS
from dotenv import load_dotenv
import pyotp
import datetime
import ssl
import mysql.connector

# Load .env variables
load_dotenv('/home/josh/Documents/Projects/simple_2fa/db_info.env')

app = Flask(__name__)
CORS(app, resources={r"/*":{"origins": "*"}})

# Flask-Mail config
app.config['MAIL_SERVER'] = os.getenv('SMTP_SERVER')
app.config['MAIL_PORT'] = int(os.getenv('SMTP_PORT'))
app.config['MAIL_USERNAME'] = os.getenv('EMAIL_USER')
app.config['MAIL_PASSWORD'] = os.getenv('EMAIL_PASSWORD')
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

mail = Mail(app)

# MySQL setup
DB_HOST = os.getenv('DB_HOST')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')
DB_SSL_PATH = os.getenv('DB_SSL_PATH')

# Get connection
def get_db_connection():
    connection = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        ssl_ca=DB_SSL_PATH
    )
    return connection

# Generate and send 2FA code
@app.route('/generate-2fa', methods=['POST'])
def generate_2fa():
    data = request.get_json()
    email = data.get('email')
    
    if not email:
        return jsonify({"error": "email is required"}), 400
    
    # Generate a 6 digit TOTP code
    secret = pyotp.random_base32() # Save securely per user
    totp = pyotp.TOTP(secret)
    code = totp.now()
    
    # Save timestamp in database for validation
    expiration_time = datetime.datetime.now() + datetime.timedelta(seconds=60)
    
    try:
        # Store code and expiration date in db
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO two_factor_auth (email, code, expiration_time) 
            VALUES (%s, %s, %s)
        """, (email, code, expiration_time))
        connection.commit()
        cursor.close()
        connection.close()
        
        # Send email
        msg = Message("Your 2FA Code", sender=os.getenv("EMAIL_USER"), recipients=[email])
        msg.body = f"Your 2FA code is: {code}. It is valid for 1 minute."
        mail.send(msg)
        
        return jsonify({"message": "2FA code sent successfully."}), 300
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/2fa')
def show_2fa():
    return render_template('2fa.html')

@app.route('/verify', methods=['POST'])
def verify_2fa():
    user_code = request.form.get('code')
    
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        
        # Match code in database
        cursor.execute("""
            SELECT * FROM two_factor_auth
            WHERE code = %s AND used = FALSE
            ORDER BY created_at DESC
            LIMIT 1
        """, (user_code,))
        
        result = cursor.fetchone()
        
        if not result:
            return jsonify({"error": "Invalid or expired 2FA code."}), 400
        
        # Values
        stored_code = result['code']
        expiration_time = result['expiration_time']
        
        # Check if expired code
        if datetime.datetime.now() > expiration_time:
            return jsonify({"error": "2FA code has expired."})
        
        # Check if code matches
        if user_code == stored_code:
            # Mark the code as used
            cursor.execute("""
                UPDATE two_factor_auth SET used = TRUE WHERE id = %s
            """, (result['id'],))
            connection.commit()
            cursor.close()
            connection.close()
            
            return jsonify({"message": "2FA verification successful!"}), 200
        else:
            return jsonify({"message": "Invalid code. Please try again."}), 400
    except mysql.connector.Error as err:
        return jsonify({"error": f"Database error: {str(err)}"})

# Run application
if __name__ == "__main__":
    app.run(debug=True)