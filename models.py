from jogoteca import db


class Games(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    category = db.Column(db.String(40), nullable=False)
    console = db.Column(db.String(20), nullable=False)
    
    def __repr__(self):
        return '<Name %r>' % self.name


class Users(db.Model):
    name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100),primary_key=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    
    def __repr__(self):
        return '<Name %r>' % self.name