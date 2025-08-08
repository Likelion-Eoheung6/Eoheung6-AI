from flask import request
import jwt
import os
from dotenv import load_dotenv

class JwtParser:
    def __init__(self, request):
        self.request = request

    def parse(self):    
        auth_header = self.request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
        else:
            token = None
        return token
    
class JwtDecorder:
    def __init__(self, token):
        load_dotenv()
        self.secret_key = os.getenv("JWT_SECRET")
        self.token = token
    def decode(self):
        payload = jwt.decode(self.token, self.secret_key, algorithms=["HS512"])
        
        return payload