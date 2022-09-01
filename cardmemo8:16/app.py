#python3 -m venv .venv 가상환경설정
from pydoc import doc
from turtle import title
from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient

client = MongoClient('mongodb://haein:haein@43.200.3.162',27017)
#client = MongoClient('localhost',27017)
db = client.jungle
app = Flask(__name__)

## HTML을 주는 부분
@app.route('/')
def home():
    return render_template('index.html')

## API 역할을 하는 부분
@app.route('/api/review', methods=['POST'])
def write_review():
    
    title_receive = request.form['title_give']
    review_receive = request.form['review_give']

    print(title_receive, review_receive)

    # 가져온 데이터를 DB에 저장하기
    doc = {
        'title': title_receive,
        'review': review_receive
    }
    db.alonememo.insert_one(doc)
    
    return jsonify({'msg': '저장 완료'})

    
@app.route('/api/delete', methods=['POST'])
def delete():
    for key, val in request.form.items():
        print(key)
        if key == 'title_give':
            title_receive = val
        elif key == 'review_give':
            review_receive = val
    #review_receive = request.form['review_give']
    print(title_receive)
    db.alonememo.delete_one({'title': title_receive})#,'review':review_receive})
    return jsonify({'msg': '삭제 완료!'})

## GET API
@app.route('/api/review', methods=['GET'])
def read_reviews():
    #DB에서 데이터 읽어오기
    reviews = list(db.alonememo.find({}, {'_id': 0}))
    #읽어온 데이터를 클라이언트로 return
    return jsonify({'result': 'success','all_reviews': reviews})


@app.route('/api/edit', methods=['POST'])
def edit_memo():
    new_title_receive = request.form['new_title_give']
    new_review_receive = request.form['new_review_give']
    title_receive = request.form['title_give']
    review_receive = request.form['review_give']

    print(new_title_receive, new_review_receive, title_receive, review_receive)
    
    db.alonememo.update_one({'title' : title_receive , "review": review_receive}, {'$set': {"title": new_title_receive, "review" : new_review_receive}})

    return {"msg" : "수정완료"}

if __name__ == '__main__':

    app.run('0.0.0.0', port=5000, debug=True)