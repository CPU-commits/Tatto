from pydantic import BaseModel
from datetime import datetime
import bcrypt

class User(BaseModel):
    role: str # Solo debería aceptar Tatuador, Cliente y Dueño de estudio
    email: str
    password: str
    name: str
    def to_model(self):
        return {
            'role': self.role,
            'email': self.email,
            'password': bcrypt.hashpw(
                password=bytes(self.password, 'utf-8'),
                salt=bcrypt.gensalt(),
            ),
            'name': self.name,
            'date': datetime.utcnow(),
        }


class UserUpdate(BaseModel):
    method : str
    data : str
   