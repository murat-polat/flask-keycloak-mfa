# flask-keycloak-mfa
flask-keycloak-example
`

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

Root URL, Valid redirect URIs, Valid post logout redirect URI,Web origins, Backchannel logout URL = http://localhost:5000

Than click to Save button

#### 3- Create test User
All users will be saved in Postgres database in Keycloak
![](/src/create_User1.png)
Username: flaskuser
than click to Save button
![](/src/setUserPass1.png)

Now flaskuser needs password to login application via Keycloak
Users => Credentials => Set password

![](/src/setUserPass2.png)
Click to "Set password", create your password disable "Temporary" than "Save" 


### Back to the Flask application for Keycloak client konfigurations
All ready for test  now. But we have to configure KEYCLOAK_URL, KEYCLOAK_REALM, KEYCLOAK_CLIENT_ID In Flask application. 
KEYCLOAK_CLIENT_SECRET is important, for now we don't need this in Keycloak site.

KEYCLOAK_URL = "https://YourDomain.com"  ### OR  http://localhost:8080 (if Keycloak runs localy)
KEYCLOAK_REALM = "flask"
KEYCLOAK_CLIENT_ID = "flask"


`app.py`

```

# Keycloak Configuration
app.config["KEYCLOAK_URL"] = "https://YourDomain.com"  ### OR  http://localhost:8080 (if Keycloak runs localy)
app.config["KEYCLOAK_REALM"] = "flask"
app.config["KEYCLOAK_CLIENT_ID"] = "flask"
app.config["KEYCLOAK_CLIENT_SECRET"] = "your-client-secret"
app.config["KEYCLOAK_REDIRECT_URI"] = "http://localhost:5000/auth/callback"




```


