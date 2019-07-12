## First Migrate
`
python manage.py makemigrations
python manage.py migrate
`

# Custom User Registration

# Register user
http://127.0.0.1:8000/api/v1/users/

## Input
<pre>
{
	"user":{
		"name": "ShyamBabu",
		"email":"shyambabu@gmail.com",
		"password":"shyam12345",
		"phone_number": 9876543210,
		"age":21,
		"gender":"male"
	}
}
</pre>

## Output
<pre>
{
    "user": {
        "id": 1,
        "name": "ShyamBabu",
        "email": "shyambabu@gmail.com",
        "phone_number": "9876543210",
        "age": 21,
        "gender": "male",
        "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6NiwiZXhwIjoxNTY4MTA4Mjc2fQ.jXVKOkObyN5AH4x8EpMX6bgFvJHA6kbgko3Wav49Hqc"
    }
}
</pre>

---

# Login User 

http://127.0.0.1:8000/api/v1/users/login/

## Input 

<pre>
{
	"user":{
		"email":"shyambabu@gmail.com",
		"password":"shyam12345"
	}
}
</pre>

## Output

<pre>
{
    "user": {
        "email": "shyambabu@gmail.com",
        "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6NiwiZXhwIjoxNTY4MTA4MzI0fQ.fvJjY42BuSA2efOBgTclIOicAf2Maf-i2YxKLrjKYBc"
    }
}
</pre>

---

# Get Logged In User

http://127.0.0.1:8000/api/v1/user/

#### Headers

<pre>
Key				Value
Authorization	Token eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6NiwiZXhwIjoxNTY4MTA4MzI0fQ.fvJjY42BuSA2efOBgTclIOicAf2Maf-i2YxKLrjKYBc

key             type   access_key
</pre>

## Output
<pre>
{
    "user": {
        "id": 1,
        "email": "shyambabu@gmail.com",
        "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MiwiZXhwIjoxNTY4MTEyNzUyfQ.zY-fxAKocgTZXcleEd9PnvbRtxUrrli5P6xn0EPVrMI",
        "name": "ShyamBabu"
    }
}
</pre>

---

# Facebook Authentication API

### Now go to django admin and add a new Application.
- client_id and client_secret shouldn't be changed
- user should be your superuser
- redirect_uris should be left blank
- client_type should be set to confidential
- authorization_grant_type should be set to 'Resource owner password-based'
- name can be set to whatever you want


### To Create this dynamically, Check api > social 


## GET Access Key
http://localhost:8000/social/auth/token

## Input Data
<pre>
{
	"username": "shyambabu@gmail.com",
	"password": "shyam12345",
	"client_id": "R56sborWjWtAqIajntdXAVjcqzUrqREDB9AfD40k",
	"client_secret": "WaKWRq6AJKBfSfteHZC6uc8rAQ3aloiWgnf3wsSsTPXERmJguKMjRVZLvisVXxhPqIuOkEjKngEBPQDhswo8nksI919Xm62lCCe4vILwOH4IrQFgwzSrMlU7WefcjvDC",
	"grant_type": "password"
}
</pre>

## Output

<pre>
{
    "access_token": "M5SbatG3IGJco2Df3DhE31Eh1wd52A",
    "expires_in": 36000,
    "token_type": "Bearer",
    "scope": "read write",
    "refresh_token": "fm7tjcABcdr1Bw8oZxLkOtrvm50TfX"
}
</pre>

---


# OR GET Converted TOKEN

http://localhost:8000/social/auth/convert-token

## Input Data
<pre>
{
	"grant_type": "convert_token",
	"client_id": "R56sborWjWtAqIajntdXAVjcqzUrqREDB9AfD40k",
	"backend":"facebook",
	"token": "EAAGKRJG8eL8BAOzTNWcW6TCi5PBczNMzZBFCJSoXpXKY1u1K1JROUw0R9ZBgebeXBhcF5tZAmayZB3CG21h6HZAlXYfhZBxYtfBUQYvfes4wpYwbZCp70shvXnTEyRKDF19jG2E1eWkYwEOrPhNocq1Q8xMvlyWW3ZCWZANIO2Bg3b0e2mgzkPZCNPHaF7xBGq3P35kQZBt8DxUvTETuhZCSBYtV"
}
</pre>

Note: token -> It is given by auth provider like - Facebook, Instagram

## Output
<pre>
{
    "access_token": "M5SbatG3IGJco2Df3DhE31Eh1wd52A",
    "expires_in": 36000,
    "token_type": "Bearer",
    "scope": "read",
    "refresh_token": "fm7tjcABcdr1Bw8oZxLkOtrvm50TfX"
}
</pre>

### If you pass wrong backend instead Facebook 
### Output
<pre>
{
    "error": "access_denied",
    "error_description": "Authentication process canceled"
}
</pre>


---

# Check LoggedIn or Not

http://127.0.0.1:8000/api/v1/user/
OR
http://127.0.0.1:8000/social/users/me/

#### Headers
<pre>
Key				Value
Authorization	Bearer M5SbatG3IGJco2Df3DhE31Eh1wd52A

key             type   access_key
</pre>

## Output
<pre>
{
    "user": {
        "id": 1,
        "email": "shyambabu@gmail.com",
        "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MiwiZXhwIjoxNTY4MTEyNzUyfQ.zY-fxAKocgTZXcleEd9PnvbRtxUrrli5P6xn0EPVrMI",
        "name": "ShyamBabu"
    }
}
</pre>

# Instagram Authentication API

## Same as Facebook Authentication

