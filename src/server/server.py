#from flask import Flask
import os
import sqlite3
from flask import * 
from http_method_override_middleware import HTTPMethodOverrideMiddleware

DATABSE = "data/database.db"

file = 'index.html'

app = Flask(__name__)
app.wsgi_app = HTTPMethodOverrideMiddleware(app.wsgi_app)

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABSE)
    return db
    
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rev

posts = []

@app.route("/")
def home_page():
    return render_template(file)
    
@app.route("/send", methods=['POST'])
def send_message(message):
    request.form['message']
    posts.append(post)
    posts = db.posts
    
    post_id = posts.insert(post)
    online_users = mongo.db.users.find({"online": True})
    return render_template(templates + file, online_users=online_users)
    
if __name__=="__main__":
    app.run(host=os.getenv('IP', '0.0.0.0'), port=int(os.getenv('PORT', 8080)))