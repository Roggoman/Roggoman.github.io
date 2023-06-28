from flask import Flask, render_template, url_for, request, redirect, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.utils import secure_filename
import os
import js2py
import time

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
UPLOAD_FOLDER = 'static/img/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
db = SQLAlchemy(app)
word = '0000'
with open("static/password.txt", "w") as file:
    file.write(word)
default_img = "img.png"
pas = None


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    intro = db.Column(db.Integer, nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    cover = db.Column(db.String(150), nullable=False,
                      default="static/img/img.png")

    def __repr__(self):
        return '<Article %r>' % self.id


def cover_list():
    art = Article.query.order_by(Article.date.desc()).all()
    lst = list()
    for i in art:
        lst.append(str(i.cover))
    return lst


@app.route('/')
@app.route('/home')
def index():
    return render_template("index.html")


@app.route('/uploads/<filename>')
def send_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/posts')
def posts():
    global pas
    global word
    if pas == word:
        return redirect('/admin/posts')
    else:
        articles = Article.query.order_by(Article.date.desc()).all()
        return render_template("post.html", articles=articles)


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/admin/red')
def red():
    global pas
    global word
    if pas == word:
        return render_template("red.html")
    else:
        return redirect("/admin")


@app.route('/admin/out')
def out():
    global pas
    global word
    if pas == word:
        pas = None
        return redirect("/home")
    else:
        return redirect("/admin")


@app.route('/admin', methods=['POST', 'GET'])
def admin():
    global pas
    global word
    if pas == word:
        return redirect("/admin/red")
    if request.method == 'POST':
        password = request.form['pass']
        if password == word:
            pas = password
            return redirect("/admin/red")
        else:
            pass
    return render_template("admin.html")


@app.route('/admin/posts')
def post_admin():
    global pas
    global word
    if pas == word:
        articles = Article.query.order_by(Article.date.desc()).all()
        return render_template("post_admin.html", articles=articles)
    else:
        return redirect("/admin")


@app.route('/posts/<int:id>')
def textpost(id):
    article = Article.query.get(id)
    return render_template("post_det.html", article=article)


@app.route('/admin/posts/<int:id>/delete')
def delete(id):
    global pas
    global word
    if pas == word:
        article = Article.query.get_or_404(id)
        fileAll = article.cover
        if len(article.cover) > 0:
            fileOld = article.cover[11:]
        else:
            fileOld = ""
        if not (fileOld == "") and not (fileOld == "img.png") and not (cover_list().count(fileAll) > 1):
            try:
                os.remove(os.path.join(
                    app.config['UPLOAD_FOLDER'], fileOld))
            except:
                return render_template('404.html')
        try:
            db.session.delete(article)
            db.session.commit()
            return redirect('/admin/posts')
        except:
            return render_template('404.html')
    else:
        return redirect("/admin")


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.route('/admin/posts/<int:id>/update', methods=['POST', 'GET'])
def update(id):
    global UPLOAD_FOLDER
    global pas
    global word
    if pas == word:
        article = Article.query.get_or_404(id)
        fileAll = article.cover
        fileOld = article.cover[11:]
        if request.method == 'POST':
            article.title = request.form['title']
            article.intro = request.form['intro']
            article.text = request.form['text']
            file = request.files['img']
            if not (fileOld == "") and not (fileOld == "img.png") and not (cover_list().count(fileAll) > 1):
                try:
                    os.remove(os.path.join(
                        app.config['UPLOAD_FOLDER'], fileOld))
                except:
                    return render_template('404.html')
            if file.filename == '':
                file.filename = default_img
            else:
                file.save(os.path.join(
                    app.config['UPLOAD_FOLDER'], file.filename))
            article.cover = UPLOAD_FOLDER + file.filename
            try:
                db.session.commit()
                return redirect('/admin/posts')
            except:
                return render_template('404.html')
        else:
            return render_template("update.html", article=article)
    else:
        return redirect("/admin")


@app.route('/admin/create', methods=['POST', 'GET'])
def create():
    global UPLOAD_FOLDER
    global pas
    global word
    if pas == word:
        if request.method == 'POST':
            title = request.form['title']
            intro = request.form['intro']
            text = request.form['text']
            file = request.files['img']
            if file.filename == '':
                file.filename = default_img
            else:
                file.save(os.path.join(
                    app.config['UPLOAD_FOLDER'], file.filename))
            article = Article(title=title, intro=intro,
                              text=text, cover=UPLOAD_FOLDER+file.filename)
            try:
                db.session.add(article)
                db.session.commit()
                return redirect('/admin/posts')
            except:
                return render_template('404.html')
        else:
            return render_template("create.html")
    else:
        return redirect("/admin")


if __name__ == "__main__":
    app.run(debug=True)
