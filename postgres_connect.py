# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy


# app = Flask(__name__)

# # Configure the PostgreSQL database URI
# # app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@host:port/database_name'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://abhilasa:Yp7MrmnmOD6PqxyPRz4dnYsiQJXGDZJV@dpg-cqn4be5svqrc73fj6gtg-a.singapore-postgres.render.com/farm_market'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# # Create the SQLAlchemy object
# db = SQLAlchemy(app)

# # Define your models here
# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(80), unique=True, nullable=False)
#     email = db.Column(db.String(120), unique=True, nullable=False)

# # Create the database tables
# with app.app_context():
#     db.create_all()

# if __name__ == '__main__':
#     app.run(debug=True)
