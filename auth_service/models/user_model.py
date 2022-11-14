from ..extension.db import db


class UserModel(db.Model):
    def __init__(self, **kwargs) -> None:
        super(UserModel, self).__init__(**kwargs)

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String)
