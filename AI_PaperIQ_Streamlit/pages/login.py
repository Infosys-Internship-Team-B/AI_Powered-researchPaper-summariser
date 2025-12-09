import streamlit as st
from firebase_admin import auth, firestore
from firebase_config import db
import requests
import json
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

if st.session_state.get("authenticated", False):
     st.switch_page("pages/app.py")
# ---------------------------------------------------
# FIREBASE REST API CONFIGURATION
# ---------------------------------------------------
# Get your Web API Key from Firebase Console > Project Settings > Web API Key
FIREBASE_WEB_API_KEY = os.getenv("FIREBASE_WEB_API_KEY", "YOUR_FIREBASE_WEB_API_KEY")

# Validate API Key
if FIREBASE_WEB_API_KEY == "YOUR_FIREBASE_WEB_API_KEY" or not FIREBASE_WEB_API_KEY:
    st.error("⚠️ Firebase Web API Key not configured. Please check your .env file or update login.py")
    st.stop()

FIREBASE_AUTH_URL = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={FIREBASE_WEB_API_KEY}"
FIREBASE_SIGNUP_URL = f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={FIREBASE_WEB_API_KEY}"
FIREBASE_RESET_URL = f"https://identitytoolkit.googleapis.com/v1/accounts:sendOobCode?key={FIREBASE_WEB_API_KEY}"

# ---------------------------------------------------
# PAGE SETTINGS
# ---------------------------------------------------
st.set_page_config(
    page_title="AI PaperIQ – Login",
    page_icon="🧠",
    layout="centered",
)

# ---------------------------------------------------
# SESSION STATE
# ---------------------------------------------------
if "active_tab" not in st.session_state:
    st.session_state.active_tab = "signin"

if "show_pass_signup" not in st.session_state:
    st.session_state.show_pass_signup = False

# ---------------------------------------------------
# AUTHENTICATION FUNCTIONS
# ---------------------------------------------------
def sign_in_with_email_password(email, password):
    """Sign in user with email and password using Firebase REST API"""
    try:
        payload = {
            "email": email,
            "password": password,
            "returnSecureToken": True
        }
        response = requests.post(FIREBASE_AUTH_URL, json=payload)
        data = response.json()
        
        if response.status_code == 200:
            return {"success": True, "data": data}
        else:
            error_message = data.get("error", {}).get("message", "Unknown error")
            return {"success": False, "error": error_message}
    except Exception as e:
        return {"success": False, "error": str(e)}

def sign_up_with_email_password(email, password, display_name):
    """Create new user with email and password using Firebase REST API"""
    try:
        payload = {
            "email": email,
            "password": password,
            "returnSecureToken": True
        }
        response = requests.post(FIREBASE_SIGNUP_URL, json=payload)
        data = response.json()
        
        if response.status_code == 200:
            # Store additional user data in Firestore
            user_id = data.get("localId")
            db.collection("users").document(user_id).set({
                "name": display_name,
                "email": email,
                "created_at": datetime.now().isoformat(),
                "uid": user_id
            })
            return {"success": True, "data": data}
        else:
            error_message = data.get("error", {}).get("message", "Unknown error")
            return {"success": False, "error": error_message}
    except Exception as e:
        return {"success": False, "error": str(e)}

def send_password_reset_email(email):
    """Send password reset email using Firebase REST API"""
    try:
        payload = {
            "requestType": "PASSWORD_RESET",
            "email": email
        }
        response = requests.post(FIREBASE_RESET_URL, json=payload)
        data = response.json()
        
        if response.status_code == 200:
            return {"success": True}
        else:
            error_message = data.get("error", {}).get("message", "Unknown error")
            return {"success": False, "error": error_message}
    except Exception as e:
        return {"success": False, "error": str(e)}

def parse_firebase_error(error_msg):
    """Convert Firebase error messages to user-friendly messages"""
    error_map = {
        "EMAIL_NOT_FOUND": "No account found with this email address",
        "INVALID_PASSWORD": "Incorrect password",
        "USER_DISABLED": "This account has been disabled",
        "EMAIL_EXISTS": "This email is already registered",
        "INVALID_EMAIL": "Invalid email address",
        "WEAK_PASSWORD": "Password should be at least 6 characters",
        "TOO_MANY_ATTEMPTS_TRY_LATER": "Too many attempts. Please try again later"
    }
    return error_map.get(error_msg, f"Authentication error: {error_msg}")

# ---------------------------------------------------
# TAB SWITCHING
# ---------------------------------------------------
def switch_tab(tab):
    st.session_state.active_tab = tab
    st.rerun()

# ---------------------------------------------------
# GLOBAL CSS — MATCHING HOME.PY THEME
# ---------------------------------------------------
st.markdown("""
<style>
/* Remove Streamlit branding */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* Background matching home.py */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #020617 0%, #0a0e27 50%, #020617 100%);
    min-height: 100vh;
    position: relative;
}

/* Large background watermark */
[data-testid="stAppViewContainer"]::before {
    content: '';
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: 600px;
    height: 600px;
    background-image: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><text y="70" font-size="80" fill="%23ffffff" opacity="0.03" font-weight="900" font-family="system-ui">🧠</text></svg>');
    background-repeat: no-repeat;
    background-position: center;
    background-size: contain;
    pointer-events: none;
    z-index: 0;
}

/* PaperIQ text watermark */
[data-testid="stAppViewContainer"]::after {
    content: 'PaperIQ';
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    font-size: 8rem;
    font-weight: 900;
    color: rgba(59, 130, 246, 0.03);
    pointer-events: none;
    z-index: 0;
    letter-spacing: 0.1em;
}

.block-container {
    padding-top: 2rem !important;
    padding-bottom: 2rem !important;
    position: relative;
    z-index: 1;
}

/* Logo Section */
.login-header {
    text-align: center;
    margin-bottom: 2rem;
    position: relative;
    z-index: 2;
}

.login-logo {
    width: 50px;
    height: 50px;
    border-radius: 12px;
    background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 50%, #ec4899 100%);
    display: inline-flex;
    align-items: center;
    justify-content: center;
    font-size: 1.5rem;
    box-shadow: 0 4px 20px rgba(59, 130, 246, 0.4);
    margin-bottom: 1rem;
}

.login-brand {
    font-size: 1.6rem;
    font-weight: 700;
    background: linear-gradient(135deg, #60a5fa 0%, #a78bfa 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.5rem;
}

/* Glassy login card */
.login-card {
    width: 100%;
    max-width: 460px;
    padding: 2.5rem 2.5rem;
    background: linear-gradient(145deg, rgba(15, 23, 42, 0.6), rgba(2, 6, 23, 0.8));
    border: 1px solid rgba(59, 130, 246, 0.3);
    border-radius: 24px;
    backdrop-filter: blur(15px);
    margin: 0 auto;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    animation: fadeInUp 0.6s ease-out;
    position: relative;
    z-index: 2;
}

@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translateY(30px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

/* Title matching home.py */
.login-title {
    font-size: 2rem;
    font-weight: 800;
    text-align: center;
    background: linear-gradient(135deg, #e0f2fe 0%, #bfdbfe 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.5rem;
}

/* Subtitle */
.login-subtitle {
    text-align: center;
    color: #94a3b8;
    font-size: 1rem;
    margin-bottom: 2rem;
    line-height: 1.6;
}

/* Input labels */
label {
    color: #e5e7eb !important;
    font-weight: 500 !important;
    font-size: 0.95rem !important;
    margin-bottom: 0.5rem !important;
}

/* Input fields */
input {
    background: rgba(15, 23, 42, 0.8) !important;
    color: #e2e8f0 !important;
    border-radius: 12px !important;
    border: 1px solid rgba(148, 163, 184, 0.3) !important;
    padding: 0.75rem !important;
    font-size: 1rem !important;
    transition: all 0.3s !important;
}

input:focus {
    border-color: rgba(59, 130, 246, 0.6) !important;
    box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1) !important;
    outline: none !important;
}

/* Button matching home.py */
.stButton>button {
    width: 100%;
    padding: 0.85rem 1.5rem !important;
    border-radius: 12px !important;
    background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%) !important;
    border: none !important;
    color: white !important;
    font-weight: 700 !important;
    font-size: 1.05rem !important;
    box-shadow: 0 4px 15px rgba(59, 130, 246, 0.4) !important;
    transition: all 0.3s !important;
    margin-top: 0.5rem !important;
}

.stButton>button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(59, 130, 246, 0.6) !important;
}

/* Links */
.auth-link {
    text-align: center;
    margin-top: 1.5rem;
    color: #94a3b8;
    font-size: 0.95rem;
}

.auth-link a {
    color: #60a5fa;
    text-decoration: none;
    font-weight: 600;
    cursor: pointer;
    transition: color 0.3s;
}

.auth-link a:hover {
    color: #93c5fd;
    text-decoration: underline;
}

/* Divider */
.divider {
    text-align: center;
    margin: 1.5rem 0;
    color: #6b7280;
    font-size: 0.9rem;
    position: relative;
}

.divider::before,
.divider::after {
    content: '';
    position: absolute;
    top: 50%;
    width: 40%;
    height: 1px;
    background: rgba(148, 163, 184, 0.3);
}

.divider::before {
    left: 0;
}

.divider::after {
    right: 0;
}

/* Success/Error messages */
.stSuccess, .stError {
    border-radius: 10px !important;
    padding: 0.75rem 1rem !important;
    font-size: 0.95rem !important;
}

@media (max-width: 600px) {
    .login-card {
        padding: 2rem 1.5rem;
    }
    .login-title {
        font-size: 1.75rem;
    }
}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# HEADER WITH LOGO
# ---------------------------------------------------
st.markdown("""
<div class="login-header">
    <div class="login-logo">🧠</div>
    <div class="login-brand">AI PaperIQ</div>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# MAIN LOGIN CARD
# ---------------------------------------------------
st.markdown("<div class='login-card'>", unsafe_allow_html=True)

# ----------- SIGN IN -----------
if st.session_state.active_tab == "signin":
    
    st.markdown("<div class='login-title'>Welcome Back</div>", unsafe_allow_html=True)
    st.markdown("<p class='login-subtitle'>Sign in to continue your research journey</p>", unsafe_allow_html=True)
    
    # Email input
    email = st.text_input("Email", placeholder="you@example.com", key="signin_email")
    
    # Password input
    password = st.text_input(
        "Password", 
        type="password",
        placeholder="Enter your password",
        key="signin_password"
    )
    
    # Sign in button
    if st.button("Sign In", key="signin_btn"):
        if not email or not password:
            st.error("❌ Please fill in all fields")
        else:
            with st.spinner("Signing in..."):
                result = sign_in_with_email_password(email, password)
                
                if result["success"]:
                    # Get user data from Firestore
                    user_id = result["data"]["localId"]
                    user_doc = db.collection("users").document(user_id).get()
                    
                    if user_doc.exists:
                        user_data = user_doc.to_dict()
                        
                        # Set session state
                        st.session_state.authenticated = True
                        st.session_state.user_id = user_id
                        st.session_state.user_email = email
                        st.session_state.user_name = user_data.get("name", "User")
                        st.session_state.id_token = result["data"]["idToken"]
                        
                        st.success("✅ Login successful! Redirecting...")
                        st.balloons()
                        
                        st.switch_page("pages/app.py") 
                    else:
                        st.error("❌ User data not found")
                else:
                    error_msg = parse_firebase_error(result["error"])
                    st.error(f"❌ {error_msg}")
    
    # Links
    st.markdown("<div class='divider'>or</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Forgot Password?", key="goto_forgot"):
            switch_tab("forgot")
    with col2:
        if st.button("Create Account", key="goto_signup"):
            switch_tab("signup")

# ----------- SIGN UP -----------
elif st.session_state.active_tab == "signup":
    
    st.markdown("<div class='login-title'>Create Account</div>", unsafe_allow_html=True)
    st.markdown("<p class='login-subtitle'>Join AI PaperIQ and start summarizing research papers</p>", unsafe_allow_html=True)
    
    # Show/hide password checkbox (moved to top to prevent rerun issues)
    col1, col2 = st.columns([3, 1])
    with col1:
        st.write("")  # Spacer
    with col2:
        show_pass = st.checkbox("Show Passwords", key="show_signup", value=st.session_state.get("show_pass_signup", False))
        st.session_state.show_pass_signup = show_pass
    
    # Full name input
    fullname = st.text_input("Full Name", placeholder="John Doe", key="signup_name", value="")
    
    # Email input
    email = st.text_input("Email", placeholder="you@example.com", key="signup_email", value="")
    
    # Password inputs
    password_type = "default" if st.session_state.show_pass_signup else "password"
    
    password1 = st.text_input(
        "Password", 
        type=password_type,
        placeholder="Minimum 6 characters",
        key="signup_pass1",
        value=""
    )
    
    password2 = st.text_input(
        "Confirm Password", 
        type=password_type,
        placeholder="Re-enter your password",
        key="signup_pass2",
        value=""
    )
    
    st.write("")  # Spacer
    
    # Create account button
    if st.button("Create Account", key="signup_btn", use_container_width=True):
        # Check if fields are filled
        if not fullname or not fullname.strip():
            st.error("❌ Please enter your full name")
        elif not email or not email.strip():
            st.error("❌ Please enter your email")
        elif not password1 or not password1.strip():
            st.error("❌ Please enter a password")
        elif not password2 or not password2.strip():
            st.error("❌ Please confirm your password")
        elif len(password1) < 6:
            st.error("❌ Password must be at least 6 characters")
        elif password1 != password2:
            st.error("❌ Passwords do not match")
        else:
            with st.spinner("Creating account..."):
                result = sign_up_with_email_password(email, password1, fullname)
                
                if result["success"]:
                    # Auto-login after signup
                    user_id = result["data"]["localId"]
                    
                    st.session_state.authenticated = True
                    st.session_state.user_id = user_id
                    st.session_state.user_email = email
                    st.session_state.user_name = fullname
                    st.session_state.id_token = result["data"]["idToken"]
                    
                    st.success("✅ Account created successfully!")
                    st.balloons()
                    
                    # Redirect to app
                    st.switch_page("pages/app.py")
                else:
                    error_msg = parse_firebase_error(result["error"])
                    st.error(f"❌ {error_msg}")
    
    # Link to sign in
    st.markdown("<div class='divider'>or</div>", unsafe_allow_html=True)
    
    if st.button("Already have an account? Sign In", key="goto_signin_from_signup", use_container_width=True):
        switch_tab("signin")

# ----------- FORGOT PASSWORD -----------
elif st.session_state.active_tab == "forgot":
    
    st.markdown("<div class='login-title'>Reset Password</div>", unsafe_allow_html=True)
    st.markdown("<p class='login-subtitle'>Enter your email to receive a password reset link</p>", unsafe_allow_html=True)
    
    # Email input
    email = st.text_input("Email", placeholder="you@example.com", key="forgot_email")
    
    # Send reset link button
    if st.button("Send Reset Link", key="reset_btn"):
        if not email:
            st.error("❌ Please enter your email")
        else:
            with st.spinner("Sending reset link..."):
                result = send_password_reset_email(email)
                
                if result["success"]:
                    st.success("✅ Password reset link sent to your email!")
                    st.info("📧 Please check your inbox and follow the instructions.")
                else:
                    error_msg = parse_firebase_error(result["error"])
                    st.error(f"❌ {error_msg}")
    
    # Back to sign in
    st.markdown("<div class='divider'>or</div>", unsafe_allow_html=True)
    
    if st.button("Back to Sign In", key="goto_signin_from_forgot"):
        switch_tab("signin")

st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------------------------------
# BACK TO HOME BUTTON  
# ---------------------------------------------------
st.markdown("---")
col_back = st.columns([1, 3, 1])
with col_back[1]:
    if st.button("← Back to Home", use_container_width=True):
        st.switch_page("home.py")

# ---------------------------------------------------
# FOOTER
# ---------------------------------------------------
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("""
<p style='text-align: center; color: #6b7280; font-size: 0.9rem;'>
    © 2024 AI PaperIQ · Built with ❤️ using Streamlit & Gemini AI
</p>
""", unsafe_allow_html=True)