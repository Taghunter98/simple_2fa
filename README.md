# Simple 2FA System

---

## About

<p>A simple Flask-based Two-Factor Authentication system, that sends a code to the user's email for verification. This project demonstrates how to intergrate Flask with email sending, database interaction and implement a simple 2FA mechanism.
</p>

---

## Features

- User registration and login.
- Two-factor authentication (2FA) via email.
- Database storage of 2FA codes and status.
- Simple and clear frontend with HTML and JavaScript.
- Error handling and success messages for better UX.

---

## Prerequisits

Before you begin, ensure you have the following:

1. **Python 3.x**\
   Make sure you have Python 3.6+ installed. You can check your Python version by running:

   ```bash
   python --version
   ```

2. **Pip**

   Ensure you have pip installed to manage Python packages. You can verify this by running:

   ```bash
   pip --version
   ```

3. **Flask**

   The application uses the Flask web framework, which will be installed automatically when you run:

   ```bash
   pip install -r requirements.txt.
   ```

4. **MySQL Database (or another DB you use)**

   If you're using MySQL as the backend database, you'll need to have access to a MySQL server where you can create and manage your database. If you are using AWS RDS, ensure that your credentials and endpoint are set correctly in the .env file.

5. **SMTP Email Service**

   For the 2FA system to send emails, you'll need an SMTP service, such as Gmail or any other service that supports email sending via SMTP. Make sure you set up an email account and update the .env file with your credentials and the SMTP server details.

6. **A `.env` File**

   You will need to create a .env file in the root directory of the project, containing your sensitive environment variables such as email credentials, database credentials, and SMTP server details. A sample .env file structure might look like this:
   </p>

   ```bash
   DB_HOST='your-db-host'
   DB_USER='your-db-username'
   DB_PASSWORD='your-db-password'
   DB_NAME='your-db-name'
   EMAIL_USER='your-email@example.com'
   EMAIL_PASSWORD='your-email-password'
   SMTP_SERVER='smtp.example.com'
   SMTP_PORT=587
   ```

---

## Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/simple_2fa.git
   ```

2. **Create a virtual environment**

   ```bash
   python -m myenv
   source myenv/bin/activate
   ```

3. **Install dependencies**

   ```bash
   pip install requirements.txt
   ```

4. **Run the application**

   ```bash
   python send_2fa.py
   ```

5. **Navigate to `http://127.0.0.1:5000` in your browser to see the app in action**

---

## Setting up the Database

<p>Set up your database table with the following SQL:
</p>

```bash
CREATE TABLE two_factor_auth (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL,
    code VARCHAR(6) NOT NULL,
    expiration_time DATETIME NOT NULL,
    used BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

- `id` - The id for the entry.
- `email` - The user's email
- `code` - The 6 digit code
- `expiration_time` - The timestamp for expiration
- `used` - Boolean value to check if used
- `created_at` - Timestamp for code creation

---

## Usage

1. To generate a 2FA code, send a POST request to `/generate-2fa` with the user's email.
2. A 6-digit code will be sent to the user's email address.
3. The user can then go to the `/verify` page and enter the code to verify.

The system will respond with either a success or failure message.

---

## Contributions

Feel free to fork the repository, submit issues, or create pull requests. Contributions are welcome!

---

## License

This project is licensed under the MIT License.
