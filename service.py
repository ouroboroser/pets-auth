from sqlalchemy import or_
import bcrypt
from app import db
from user import User

class AuthService:
    def getusers(self):
        users = db.session.query(User).all()
        print(users)
        return users
    def signup(self, user):
        data = db.session.query(User).filter(
            or_(
                User.username == user['username'],
                User.email == user['email']
            )
        ).first()
        if data is not None:
            raise Exception('user already exists')
        else:
            origin_password = user['password'].encode('utf-8')
            hash_password = bcrypt.hashpw(origin_password, bcrypt.gensalt(10))
            user = User(username=user['username'], email=user['email'], password=hash_password)
            db.session.add(user)
            db.session.commit()
            return 'OK'
    def update(self):
        return 'update user'
    def delete(self):
        return  'delete user'