<div align="center">

  <img src="https://capsule-render.vercel.app/api?type=waving&color=0:3C3B3F,100:605C3C&height=250&section=header&text=Smart%20Notes%20Backend&fontSize=70&fontAlign=50&fontAlignY=35&animation=fadeIn&desc=Secure%20REST%20API%20with%20OTP%20&descAlign=50&descAlignY=60&descSize=20" alt="Smart Notes Backend Header" width="100%" />

<div align="center">
  <a href="https://git.io/typing-svg">
    <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=600&size=22&pause=1000&color=F7F7F7&background=0D1117&center=true&vCenter=true&width=600&lines=Django+Rest+Framework+Powered+%F0%9F%9A%80;Secure+Token+Authentication+%F0%9F%94%91;Email+OTP+Verification+%F0%9F%93%A7;Password+Reset+%26+Recovery+%F0%9F%94%90;Robust+Account+Management..." alt="Typing Animation" />
  </a>
</div>
  
  <br>

  <p align="center">
    <img src="https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white" alt="Django" />
    <img src="https://img.shields.io/badge/Rest_Framework-A30000?style=for-the-badge&logo=django&logoColor=white" alt="DRF" />
    <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
    <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="License" />
  </p>

</div>

---

## 📖 About The Project

**Smart Notes Backend** is the secure Authentication & User Management foundation for the Smart Notes ecosystem. It serves as a robust boilerplate for any Django project requiring secure Email-OTP based login. It is a production-ready RESTful API built to handle secure user data, authentication flows, and real-time validation.

Unlike simple tutorials, this backend implements **Real-World Security Patterns**:
* **🔐 Token-Based Auth:** Stateless authentication compatible with Flutter/React Native.
* **📧 OTP Verification:** Prevents fake accounts by validating emails via SMTP (Gmail).
* **🔄 Password Recovery:** Secure "Forgot Password" flow using OTP verification.
* **🛡️ Encryption:** Industry-standard `pbkdf2_sha256` password hashing.
* **💀 2-Step Deletion:** "Request & Confirm" logic to prevent accidental data loss.

<br>

## 🛠️ Tech Stack & Tools

<div align="center">
  <a href="https://skillicons.dev">
    <img src="https://skillicons.dev/icons?i=django,python,sqlite,postman,vscode,git,github&perline=7" />
  </a>
</div>

<br>

## ⚡ Quick Start Guide

Follow these steps to get the server running on your local machine.

### 1. Clone & Install
```bash
# Clone the repository
git clone [https://github.com/YOUR_USERNAME/smart-notes-backend.git](https://github.com/YOUR_USERNAME/smart-notes-backend.git)

# Enter directory
cd smart-notes-backend

# Create Virtual Environment
python -m venv venv

# Activate Virtual Environment
# Windows:
.\venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

```

### 2. Configure Secrets

Create a `.env` file in the root directory (next to `manage.py`) and add your keys:

```ini
DEBUG=True
SECRET_KEY=django-insecure-your-key-here
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

```

### 3. Ignite Server

```bash
# Apply database migrations
python manage.py migrate

# Run the local server
python manage.py runserver

```

## 📡 API Endpoints Documentation

| Method | Endpoint | Access | Functionality |
| --- | --- | --- | --- |
| **Auth & Registration** |  |  |  |
| `POST` | `/api/auth/register/` | 🔓 Public | Creates a new user (Inactive state) |
| `POST` | `/api/auth/verify-otp/` | 🔓 Public | Verifies email via 6-digit OTP code |
| `POST` | `/api/auth/resend-otp/` | 🔓 Public | Resends activation OTP if expired |
| `POST` | `/api/auth/login/` | 🔓 Public | Returns `Token` for authenticated requests |
| **Password Management** |  |  |  |
| `POST` | `/api/auth/password-reset-request/` | 🔓 Public | Sends OTP to email for password reset |
| `POST` | `/api/auth/password-reset-confirm/` | 🔓 Public | Sets new password using valid OTP |
| **Account Management** |  |  |  |
| `POST` | `/api/auth/delete-account-request/` | 🔐 Auth | Sends a security OTP to registered email |
| `DELETE` | `/api/auth/delete-account-confirm/` | 🔐 Auth | Permanently wipes user data from DB |

> **Note:** Endpoints marked **🔐 Auth** require the header: `Authorization: Token <your_token>`

## 🚀 Roadmap

* ✅ **Secure Email/Password Registration**
* Implemented custom user model with email-first authentication.


* ✅ **OTP Email Verification (SMTP)**
* Integrated Gmail SMTP for real-time 6-digit code validation.


* ✅ **Password Recovery System**
* Added secure flow to reset forgotten passwords via OTP.


* ✅ **Token Generation (Login)**
* Stateless authentication using Django Rest Framework Tokens.


* ✅ **Account Deletion (2-Step Security)**
* "Request & Confirm" pattern to prevent accidental data loss.


* 🚧 **Notes CRUD Operations** (Coming Soon)
* Full Create, Read, Update, Delete functionality for user notes.


* 🚧 **Premium Subscription Logic** (Coming Soon)
* Middleware to enforce the 20-note limit for free tier users.



## 📂 Project Structure

```text
smart_notes_backend/
├── apps/
│   └── accounts/          # User Auth, OTP & Password Logic
├── config/                # Project Settings & URLs
├── .env                   # Secret Keys (Ignored by Git)
├── manage.py              # CLI Utility
└── requirements.txt       # Dependencies

```

<div align="center">

<h3>👤 Author</h3>

<p><b>Muhammad Zaid</b></p>

<p>
<a href="https://www.linkedin.com/in/muhammad-zaid-945b01337/" target="_blank">
<img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white" alt="Connect on LinkedIn"/>
</a>
<a href="https://github.com/mzaid-dev" target="_blank">
<img src="https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white" alt="Follow on GitHub"/>
</a>
<a href="https://mail.google.com/mail/?view=cm&fs=1&to=dev.mzaid@gmail.com" target="_blank">
<img src="https://img.shields.io/badge/Email_Me-D14836?style=for-the-badge&logo=gmail&logoColor=white" alt="Email Me"/>
</a>
</p>

<sub><i>Built with ❤️ for the Open Source Community</i></sub>

</div>

```
