from flask import Flask, redirect, url_for, render_template, session, request
from authlib.integrations.flask_client import OAuth
from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
    logout_user,
    login_required,
    current_user,
)
import secrets
import os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY") or secrets.token_hex(24)

# Keycloak Configuration
#######  Don't forget to change your Keycloak URL below   ########

app.config["KEYCLOAK_URL"] = "Your Keycloak server URL here "  #  http://localhost:8080 (if Keycloak runs localy)
app.config["KEYCLOAK_REALM"] = "flask"
app.config["KEYCLOAK_CLIENT_ID"] = "flask"
app.config["KEYCLOAK_CLIENT_SECRET"] = "your-client-secret"
app.config["KEYCLOAK_REDIRECT_URI"] = "http://localhost:5000/auth/callback"

# OAuth Setup
oauth = OAuth(app)
keycloak = oauth.register(
    name="keycloak",
    client_id=app.config["KEYCLOAK_CLIENT_ID"],
    client_secret=app.config["KEYCLOAK_CLIENT_SECRET"],
    authorize_url=f"{app.config['KEYCLOAK_URL']}/realms/{app.config['KEYCLOAK_REALM']}/protocol/openid-connect/auth",
    access_token_url=f"{app.config['KEYCLOAK_URL']}/realms/{app.config['KEYCLOAK_REALM']}/protocol/openid-connect/token",
    client_kwargs={
        "scope": "openid email profile",
        "token_endpoint_auth_method": "client_secret_post",
    },
    jwks_uri=f"{app.config['KEYCLOAK_URL']}/realms/{app.config['KEYCLOAK_REALM']}/protocol/openid-connect/certs",
)

# Flask-Login Setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

class User(UserMixin):
    def __init__(self, id, username, email, roles):
        self.id = id
        self.username = username
        self.email = email
        self.roles = roles

    def has_role(self, role_name):
        return role_name in self.roles

@login_manager.user_loader
def load_user(user_id):
    if "user_info" in session:
        user_info = session["user_info"]
        return User(
            id=user_info["sub"],
            username=user_info.get("preferred_username"),
            email=user_info.get("email"),
            roles=session.get("roles", []),
        )
    return None

@app.route("/")
def home():
    return render_template("index.html", user=current_user)

@app.route("/login")
def login():
    # Generate a secure random nonce
    nonce = secrets.token_urlsafe(16)
    session['nonce'] = nonce
    
    redirect_uri = url_for("auth_callback", _external=True)
    return keycloak.authorize_redirect(
        redirect_uri=redirect_uri,
        nonce=nonce
    )

@app.route("/logout")
@login_required
def logout():
    id_token = session.get('id_token')
    
    # Clear Flask session and logout user
    logout_user()
    session.clear()
    
    # Build Keycloak logout URL
    logout_url = (
        f"{app.config['KEYCLOAK_URL']}/realms/{app.config['KEYCLOAK_REALM']}"
        f"/protocol/openid-connect/logout"
    )
    return redirect(logout_url)

@app.route("/auth/callback")
def auth_callback():
    try:
        # Get the token using the nonce from session
        token = keycloak.authorize_access_token()
        userinfo = keycloak.parse_id_token(token, nonce=session.get('nonce'))
        
        # Store user info in session
        session["user_info"] = userinfo
        session["roles"] = token.get('realm_access', {}).get('roles', [])
        
        # Create user and log in
        user = User(
            id=userinfo["sub"],
            username=userinfo.get("preferred_username"),
            email=userinfo.get("email"),
            roles=session["roles"],
        )
        login_user(user)
        
        # Clear the nonce after successful authentication
        session.pop('nonce', None)
        
        return redirect(url_for("profile"))
    except Exception as e:
        return f"Authentication failed: {str(e)}", 400

@app.route("/profile")
@login_required
def profile():
    return render_template("profile.html", user=current_user)

if __name__ == "__main__":
    app.run(debug=True)