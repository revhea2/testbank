from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from backend import db, ma

class User(db.Mode):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False, unique=True)
    password = Column(String(80), nullable=False)

    def __init__(self, first_name, last_name, email, password):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password

    def __repr__(self):
        return '<User %r>' % self.name

    @staticmethod
    def get_schema():
        return UserSchema()


class UserSchema(ma.Schema):
    class Meta:

        fields = ('id', 'first_name', 'last_name',
                  'email')

