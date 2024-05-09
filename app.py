
from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Integer, String, Float
from datetime import datetime
from flask import Flask, request, jsonify, make_response



app = Flask(__name__)



# CREATE DATABASE
class Base(DeclarativeBase):
    pass
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///small_business.db"
db = SQLAlchemy(model_class=Base)
db.init_app(app)



class Posts(db.Model):
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True, index=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    image_file = db.Column(db.String(250), nullable=False)
    subtitle = db.Column(db.Text, nullable=False)
    quote_text = db.Column(db.Text, nullable=True)
    body = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f'<Posts {self.title}>'


    def json(self):
        return {'id': self.id, 'title': self.title, 'subtitle': self.subtitle, 'image_file': self.image_file,
                'quote_text': self.quote_text, 'body': self.body, 'date_posted': self.date_posted}


with app.app_context():
    db.create_all()



@app.route('/posts', methods=['GET'])
def home():
    try:
        posts = Posts.query.all()
        return make_response(jsonify([post.json() for post in posts]), 200)
    except TypeError:
        return make_response(jsonify({'message': 'error getting posts'}), 500)




@app.route("/add_post", methods=["POST"])
def add_post():
    try:
        data = request.get_json()
        post = Posts(
            title=data['title'],
            subtitle=data['subtitle'],
            quote_text=data['quote_text'],
            body=data['body'],
            image_file=data['image_file'],
         
        )
        db.session.add(post)
        db.session.commit()
        return make_response(jsonify({'message': 'post created'}), 201)
    except TypeError:
        return make_response(jsonify({'message': 'error creating post'}), 500)


@app.route("/post/<int:id>", methods=["POST", "PUT"])
def update(id):
    try:

        if request.method == "POST":

            post = Posts.query.get_or_404(int(id))
            data = request.get_json()

            post.title = data['title']
            post.subtitle = data['subtitle']
            post.quote_text = data['quote_text']
            post.body = data['body']
            post.image_file = data['image_file']

            db.session.commit()
            return make_response(jsonify({'message': 'post updated'}), 200)

    except TypeError:
        return make_response(jsonify({'message': 'error updating post'}), 500)



@app.route('/post/<int:id>', methods=['GET'])
def show(id):
  try:
    post = Posts.query.filter_by(id=id).first()
    if post is not None:
      return make_response(jsonify({'post': post.json()}), 200)
  except TypeError:
    return make_response(jsonify({'message': 'error getting post'}), 500)



@app.route('/post/<int:id>', methods=['DELETE'])
def delete(id):
    try:
        post = Posts.query.filter_by(id=id).first()
        db.session.delete(post)
        db.session.commit()
        return make_response(jsonify({'message': 'post successfully deleted'}), 201)
    except TypeError:
        return make_response(jsonify({'message': 'error deleting post'}), 500)




if __name__ == '__main__':
    app.run(debug=True, port=5002)

