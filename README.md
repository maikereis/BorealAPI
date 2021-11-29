<h1> BorealAPi </h1>

This is an API made using FastAPI. This api has the following features:
    
    Create authorization token
    Return a received passed payload.
    Return a list of Breweries.

<br>
<h2> Install Requirements </h2>

    'pip install -r requirements.txt'


<br>
<h2> Setting Users database </h2>

We need to know who is a valid user of the API or not, the modules [authorization](security/authorization.py) and [authentication](security/authentication.py) takes charge of this verification, hence we need to set up a database to consult the user's credentials when necessary

Run the [script_create_api_users](script_create_api_users.py), and a sql_app.db file will be created on the root folder, the database content will be something like:


|id	|          email        |                      hashed_password	|                is_active |
| - | ----------------------| --------------------------------------------------------------| -| 
|1	| fake_email0@gmail.com	| $2b$12$jhCVlgWbi.IutE6sGCdEruFcbN1rWSRRbIB251Y6D8itUncinWLzG	| 1| 
|2	| fake_email1@gmail.com	| $2b$12$3BEm9YskktFgvOUCLwT2..yQ0E6MD.16jfO9ZxBti.UrWNgRdXrEy	| 1| 
|3	| fake_email2@gmail.com	| $2b$12$KigUNoxtKS2.uq7RIU09J..AlBYoktvnVoQXTmGPDEDigL7qAz1kG	| 1| 
|4	| fake_email3@gmail.com	| $2b$12$6LllFe7cqcxVVZafHLnB2uWytC8es8mS.TNaav1901RYp0oI7j/Lu	| 1| 
<br>
<h2> Setting Environment variables </h2>

The [security](security) module is responsible for _encoding_, and _decoding_ the JWT. To perform these tasks, it needs a **secret key**, **algorithm**, and a token **lifetime**, all are sensitive information, in order to store these variables, it uses pydantic settings and .env files.

The [config](security/config.py) file defines a class **AuthorizationSettings**, which when instantiated it searches in the file .env for the environment variables.

```python
/security/config.py:

class AuthorizationSettings(BaseSettings):
    secret_key: str
    algorithm: str
    lifetime: int = 60

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
```


Create a file **.env** with the following content: a key, a hash algorithm and the desirable token lifetime.


```python
/.env:

    SECRET_KEY="4677b25090805fd888f642f9df5691ce7d9deef2e8a8af150ebdf765286fa87e"
    ALGORITHM="HS256"
    LIFETIME_MINUTES=30
```
As example, you can use the following command to generate the SECRET_KEY:

    > openssl rand -hex 32

<br>
<h2> Start the API </h2>

To start the [BoralAPI](main.py):

    > uvicorn main:app --reload

The [Swagger UI](https://swagger.io/tools/swagger-ui/) for the applications will be available on:

    http://127.0.0.1:8000/docs 



<br>
<h2> Try Out </h2>

Open the Swagger UI for the Boreal API, there is the following functions:

    GET - Root
    POST - Request Token
    POST - Pass User
    GET - Get Breweries

<h3> GET - Root </h3>

Will just return a message if the server if running

<br>
<h3> POST - Request Token </h3>

Will return a new JWT for the API user. You must pass an username, and password the request the token, to test purposes use:

    username - fake_email0@gmail.com
    password - pass0

<br>
<h3>  POST - Pass User </h3>

Receives a payload and return the same payload, a token must be passed.

<br>
<h3>  GET - Get Breweries </h3>

Sends a GET request to the [BreweriesAPI](https://api.openbrewerydb.org/breweries/), and read the list of breweries and return their names. A token must be passed.
