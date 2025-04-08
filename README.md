# flask-keycloak-mfa

# 🔐 Flask Authentication with Keycloak  

A secure and scalable Flask application integrated with **Keycloak** for Multi-Factor Authentication (MFA). This project demonstrates how to implement **OAuth 2.0/OpenID Connect (OIDC)** authentication in Flask using Keycloak as an identity provider.  

## ✨ Features  
✅ **Keycloak Integration** – Secure user authentication via Keycloak realms & clients.  
✅ **Role-Based Access Control (RBAC)** – Protect routes based on user roles.  
✅ **Flask Session Management** – Handle authenticated sessions securely.  



## 📖 Use Cases  
- Secure authentication  to Flask apps.  
- Focus to application functions, not models, databases, authentication and authorizations
- Multi-Factor Authentication (MFA), with Google or Windows authenticator.  
- User login and registrations

## 🚀 Quick Start  
1. Run Keycloak localy or in productions enviroment https://github.com/murat-polat/keycloak-deployment-example   
2. Clone the repo.  
3. Configure Keycloak  
4. Run and test the app at `http://localhost:5000`.  

---
 
### Clone this repository

`git clone https://github.com/murat-polat/flask-keycloak-mfa`

`cd flask-keycloak-mfa`


### Make a virtualenvironment and install requirements


`python -m pip install --upgrade pip `

`python -m venv env`

`env\Scripts\activate`

`pip install -r requirements.txt`

### Run Flask application 

`python app.py`
 
Application will run on the port 5000 http://localhost:5000/


To stop the aplication "CTRL + C"


## Keycloak configuration

In this section, we'll set up a Realm, Client, and Users in Keycloak for the Flask application. Once configured, all user authentication will be handled by Keycloak.

For detailed steps, expand the section below:

<details> <summary> Click to expand Keycloak configuration details </summary>
(Your detailed steps go here)


#### 1- Crerate new Realm:
![](/src/create_Realm1.png)

we will call Realm name "flask" (or any name do you want)
![](/src/create_Realm2.png)

Than click to "Create"

#### 2- Create OpenID Connect client for this Realm:
![](/src/create_Client1.png)
Client ID should be same name "flask" than click Next button
![](/src/create_Client2.png)
click to Next button
![](/src/create_client3.png)

Here must be Flask application URL. Which is http://localhost:5000

But for production must be your Flask application URL for eks. "https://app.yourdomain.com"
![](/src/create_Client4.png)

(Root URL, Valid redirect URIs, Valid post logout redirect URI,Web origins, Backchannel logout URL) = http://localhost:5000

Than click to Save button

#### 3- Create test User
All users will be saved in Postgres database in Keycloak
![](/src/create_User1.png)
Username: "flaskuser"
than click to "Save" button
![](/src/setUserPass1.png)

Now "flaskuser" needs password to login application via Keycloak

Users => Credentials => Set password

![](/src/setUserPass2.png)
Click to "Set password", create your password disable "Temporary" than "Save" 


### Back to the Flask application for Keycloak client konfigurations
All ready for test  now. But we have to configure KEYCLOAK_URL, KEYCLOAK_REALM, KEYCLOAK_CLIENT_ID In Flask application. 

KEYCLOAK_CLIENT_SECRET is important. We don't need this for Keycloak side for now.



`app.py`

```
# Keycloak Configuration
app.config["KEYCLOAK_URL"] = "https://YourDomain.com"  ### OR  http://localhost:8080 (if Keycloak runs localy)
app.config["KEYCLOAK_REALM"] = "flask"
app.config["KEYCLOAK_CLIENT_ID"] = "flask"
app.config["KEYCLOAK_CLIENT_SECRET"] = "your-client-secret"
app.config["KEYCLOAK_REDIRECT_URI"] = "http://localhost:5000/auth/callback"

```


</details>

---

### First login test


In this section, we'll login with test user "flaskuser" which we created in Keycloak. 


<details>

<summary> For detailed steps, expand the section below: </summary>

From Home/Index page http://localhost:5000 click to login:

![](/src/Login1.png)


![](/src/login2.png)


![](/src/login3.png)

All looking  good and working properly. We are on protected page "Profile" now.

To exit from the this page, click "loguot" 

![](/src/logout.png)

</details>