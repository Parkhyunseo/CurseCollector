#from flask import Flask
import os
import sqlite3
import random
from flask import * 
from http_method_override_middleware import HTTPMethodOverrideMiddleware

success_ment = [ "축하해요. 대단한 욕쟁이시네요!",
"말이 너무 심하셔서 상처 받을 뻔 했어요.", 
"데이터 수집에 도움을 주셔서 감사합니다!",
"정말 참신해요!!",
"게임에서 채팅금지 좀 받아본 실력이네요."]

fail_ment = ["필터링에 걸렸습니다.", 
"욕 정말 못하시네요.", 
"할 줄 아는 욕이 그것밖에 없나요?",
"안타깝게 실패!",
"창의력을 좀 더 발휘해보세요!"]

DATABSE = "data/db_v1.db"
filter_file = "data/curses.txt"

file = 'index.html'

app = Flask(__name__)
app.wsgi_app = HTTPMethodOverrideMiddleware(app.wsgi_app)
filters = []
curses = []

@app.before_first_request
def init_db():
    if os.path.exists(os.path.join(os.getcwd(), DATABSE)):
        g._database = sqlite3.connect(DATABSE)
        for item in query_db('select * from curse'):
            print(item)
            indices = [ i for i in range(len(item[1]))]
            filtering = []
            for i in range(len(item[1])//2):
                select = random.choice(indices)
                indices.remove(select)
                filtering.append(select)
                
            curse = ""
            for i in range(len(item[1])):
                if i not in filtering: 
                    curse += item[1][i]
                else:
                    curse += '*'
                
            curses.append(curse)

@app.before_first_request
def load_filter():
    global filters
    
    with open(filter_file) as f:
        content = f.read()
        filters = content.split(',')

def get_ment(success:bool) -> str:
    if success:
        index = random.randint(0, len(success_ment)-1)
        return success_ment[index]
    else:
        index = random.randint(0, len(fail_ment)-1)
        return fail_ment[index]
    
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
    return (rv[0] if rv else None) if one else rv

@app.route("/")
def home_page():
    return render_template(file, curses=range(100))

@app.route("/add_message")
def add_message():
    curse = request.args.get('message', 0, type=str)
    
    print(len(filters))
    
    for word in filters:
        if word in curse:
            return jsonify({
                'success':0,
                'reason':get_ment(False),
            })
    
    with get_db() as con:
        cur = con.cursor()
        cur.execute('insert into curse (text, iscurse) values (?, ?)', (curse,  1))
        con.commit()
        
    for item in query_db('select * from curse'):
        print(item)
        
    return jsonify({
        'success':1,
        'reason':get_ment(True),
    })
    
if __name__=="__main__":
    app.run(host=os.getenv('IP', '0.0.0.0'), port=int(os.getenv('PORT', 8080)))