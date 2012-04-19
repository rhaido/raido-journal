from train_journal import db

print db

class TJUser(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(80), unique=True)
  email = db.Column(db.String(120), unique=True)
  passwd = db.Column(db.String(120))
  role = db.Column(db.Integer)

  def __init__(self, username, email):
    self.username = username
    self.email = email

  def __repr__(self):
    return '<User %r>' % self.username

#admin = TUser('admin', 'admin@example.com')
#guest = TUser('guest', 'guest@example.com')
#db.session.add(admin)
#db.session.add(guest)
#db.session.commit()


