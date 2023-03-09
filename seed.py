from app import db
from models import User, Feedback, bcrypt

db.drop_all()
db.create_all()

# create users
user1 = User.register('user1', 'password', 'user1@gmail.com', 'John', 'Doe')
user2 = User.register('user2', 'password', 'user2@gmail.com', 'Jane', 'Doe')

# create feedback
feedback1 = Feedback(title='Feedback 1',
                     content='This is feedback 1', user=user1)
feedback2 = Feedback(title='Feedback 2',
                     content='This is feedback 2', user=user1)
feedback3 = Feedback(title='Feedback 3',
                     content='This is feedback 3', user=user2)

# add to session and commit
db.session.add_all([user1, user2, feedback1, feedback2, feedback3])
db.session.commit()
