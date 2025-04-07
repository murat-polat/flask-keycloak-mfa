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




### Back to the Flask application for Keycloak client konfigurations

app.py

```

# Keycloak Configuration
app.config["KEYCLOAK_URL"] = "https://YourDomain.com"  ### OR  http://localhost:8080 (if Keycloak runs localy)
app.config["KEYCLOAK_REALM"] = "flask"
app.config["KEYCLOAK_CLIENT_ID"] = "flask"
app.config["KEYCLOAK_CLIENT_SECRET"] = "your-client-secret"
app.config["KEYCLOAK_REDIRECT_URI"] = "http://localhost:5000/auth/callback"




```


