from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
import hashlib

app = Flask(__name__)
app.secret_key = 'shindanmaker_secret_key'  # 簡易的なセッション・フラッシュメッセージ用
DATABASE = 'shindan.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # 辞書ライクにアクセスできるようにする
    return conn

# 名前から決定論的なインデックスを生成する関数
def get_deterministic_index(name, max_val):
    # 名前をMD5でハッシュ化
    hasher = hashlib.md5(name.encode('utf-8'))
    # ハッシュ値（16進数文字列）の整数表現を取得
    hash_int = int(hasher.hexdigest(), 16)
    return hash_int % max_val

@app.route('/')
def index():
    conn = get_db()
    cursor = conn.cursor()
    # 最新の診断から順に取得
    cursor.execute('SELECT id, title, description, created_at FROM shindans ORDER BY id DESC')
    shindans = cursor.fetchall()
    conn.close()
    return render_template('index.html', shindans=shindans)

@app.route('/shindan/<int:shindan_id>', methods=['GET', 'POST'])
def shindan_detail(shindan_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM shindans WHERE id = ?', (shindan_id,))
    shindan = cursor.fetchone()
    conn.close()

    if not shindan:
        flash('指定された診断が見つかりませんでした。', 'error')
        return redirect(url_for('index'))

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        if not name:
            flash('名前を入力してください。', 'warning')
            return redirect(url_for('shindan_detail', shindan_id=shindan_id))
        # 結果表示画面へリダイレクト（クエリパラメータで名前を渡す）
        return redirect(url_for('shindan_result', shindan_id=shindan_id, name=name))

    return render_template('shindan.html', shindan=shindan)

@app.route('/shindan/<int:shindan_id>/result')
def shindan_result(shindan_id):
    name = request.args.get('name', '').strip()
    if not name:
        flash('名前を入力してください。', 'warning')
        return redirect(url_for('shindan_detail', shindan_id=shindan_id))

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM shindans WHERE id = ?', (shindan_id,))
    shindan = cursor.fetchone()
    conn.close()

    if not shindan:
        flash('指定された診断が見つかりませんでした。', 'error')
        return redirect(url_for('index'))

    # 結果テキストをパース（改行区切り）
    results_list = [r.strip() for r in shindan['results'].split('\n') if r.strip()]
    if not results_list:
        result_text = "診断結果のパターンが設定されていません。"
    else:
        # 名前から決定された結果を選択
        idx = get_deterministic_index(name, len(results_list))
        selected_pattern = results_list[idx]
        # [name]プレースホルダーを入力された名前に置き換える
        result_text = selected_pattern.replace('[name]', name)

    return render_template('result.html', shindan=shindan, name=name, result_text=result_text)

@app.route('/create', methods=['GET', 'POST'])
def create_shindan():
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        results = request.form.get('results', '').strip()

        if not title or not description or not results:
            flash('すべての項目を入力してください。', 'error')
            return render_template('create.html', title=title, description=description, results=results)

        # 最低2つの結果パターンを要求
        results_list = [r.strip() for r in results.split('\n') if r.strip()]
        if len(results_list) < 2:
            flash('診断結果は改行で区切って、最低2パターン以上入力してください。', 'error')
            return render_template('create.html', title=title, description=description, results=results)

        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO shindans (title, description, results) VALUES (?, ?, ?)',
            (title, description, results)
        )
        conn.commit()
        new_id = cursor.lastrowid
        conn.close()

        flash('診断を新しく作成しました！', 'success')
        return redirect(url_for('shindan_detail', shindan_id=new_id))

    return render_template('create.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
