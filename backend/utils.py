import bcrypt, jwt, datetime, requests
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

SECRET_KEY = "your-secret"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(plain, hashed):
    return bcrypt.checkpw(plain.encode(), hashed.encode())

def create_token(user_id):
    payload = {"sub": user_id, "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)}
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return type("User", (), {"id": payload["sub"]})
    except:
        raise HTTPException(status_code=401, detail="Invalid token")

def ollama_chat(prompt):
    response = requests.post("http://localhost:11434/api/generate", json={"model": "mistral", "prompt": prompt})
    return response.json()["response"]
