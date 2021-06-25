from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from wtforms import TextAreaField, StringField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Length
from flask_wtf import FlaskForm


app = Flask(__name__)
app.config['SECRET_KEY'] = 'asdf1231laskdfjlkjelkrjdlfk123wfasdfajldflkdflasjfdsfadfadf'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db = SQLAlchemy(app)


class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    title = db.Column(db.String(140), unique=False, nullable=False)
    body = db.Column(db.String(2500), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username


class PostForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=1, max=80)])
    title = StringField('Title', validators=[DataRequired(), Length(min=1, max=140)])
    body = TextAreaField('Body', validators=[DataRequired(), Length(min=1, max=2500)])
    submit = SubmitField()

    def validate_username(self, username):
        username = Posts.query.filter_by(username=username.data).first()
        print(username)
        if username is not None:
            raise ValidationError('This username is taken. Please choose a different one.')


@app.route('/')
def index():
    posts = Posts.query.all()
    return render_template('index.html', title='Bootstrap Modal', posts=posts)


@app.route('/add', methods=['POST', 'GET'])
def add():
    form = PostForm()
    print('Form add')
    if form.validate_on_submit():
        new_post = Posts(username=form.username.data,
                        title=form.title.data,
                        body=form.body.data)
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('addForm.html', title='Add post', form=form)

@app.route('/delete/<int:post_id>', methods=['POST', 'GET'])
def delete_post(post_id):
    post = Posts.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=False)
