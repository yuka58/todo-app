from flask import Flask, render_template, request, redirect
import sqlite3
import os
from datetime import datetime

# Flaskアプリケーションの初期化
app = Flask(__name__)
DB_FILE = 'todo.db'

# DB初期化（最初に1回だけテーブルを作る）
def init_db():
    if not os.path.exists(DB_FILE):
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute('CREATE TABLE tasks (id INTEGER PRIMARY KEY AUTOINCREMENT, content TEXT, done BOOLEAN)')
        conn.commit()
        conn.close()

# タスクを全部取得
def get_tasks():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('SELECT id, content, done, date FROM tasks')
    tasks = [{'id': row[0], 'content': row[1], 'done': row[2], 'date': row[3]} for row in c.fetchall()]
    conn.close()
    return tasks

# タスクを追加
def add_task(content):
    date_str = datetime.now().strftime('%Y-%m-%d')  # 現在日付を文字列に
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('INSERT INTO tasks (content, done, date) VALUES (?, ?, ?)', (content, False, date_str))
    conn.commit()
    conn.close()

# タスクを完了にする
def complete_task(task_id):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('UPDATE tasks SET done = ? WHERE id = ?', (True, task_id))
    conn.commit()
    conn.close()

# ルーティングの設定
@app.route('/')
def index():
    tasks = get_tasks()
    return render_template('index.html', tasks=tasks)

# タスク追加のルート
@app.route('/add', methods=['POST'])
def add():
    task_content = request.form['task']
    if task_content:
        add_task(task_content)
    return redirect('/')

# タスク完了のルート
@app.route('/complete/<int:task_id>')
def complete(task_id):
    complete_task(task_id)
    return redirect('/')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)

#if __name__ == '__main__':
 #   init_db()
  #  app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))


# 一度だけ実行してDBを再作成する初期化コード
import os

if os.path.exists("todo.db"):
    os.remove("todo.db")

with sqlite3.connect("todo.db") as conn:
    c = conn.cursor()
    c.execute('''
        CREATE TABLE tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL,
            done BOOLEAN NOT NULL,
            date TEXT NOT NULL
        )
    ''')
    conn.commit()
print("✅ todo.db を再作成しました！")
