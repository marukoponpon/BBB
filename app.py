from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import sqlite3

app = Flask(__name__)
app.secret_key = 'oneokrock_lyrics_key'
DATABASE = 'lyrics.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    search_query = request.args.get('q', '').strip()
    conn = get_db()
    cursor = conn.cursor()
    
    # 曲の検索または全取得
    if search_query:
        cursor.execute(
            'SELECT * FROM songs WHERE title LIKE ? OR album LIKE ? ORDER BY release_year DESC',
            (f'%{search_query}%', f'%{search_query}%')
        )
    else:
        cursor.execute('SELECT * FROM songs ORDER BY release_year DESC')
    songs = cursor.fetchall()
    
    # 最新の考察を取得（最大5件）
    cursor.execute('''
        SELECT i.*, s.title as song_title 
        FROM interpretations i 
        JOIN songs s ON i.song_id = s.id 
        ORDER BY i.created_at DESC 
        LIMIT 5
    ''')
    latest_interpretations = cursor.fetchall()
    
    conn.close()
    return render_template('index.html', songs=songs, latest_interpretations=latest_interpretations, search_query=search_query)

@app.route('/song/<int:song_id>', methods=['GET'])
def song_detail(song_id):
    conn = get_db()
    cursor = conn.cursor()
    
    # 曲情報を取得
    cursor.execute('SELECT * FROM songs WHERE id = ?', (song_id,))
    song = cursor.fetchone()
    
    if not song:
        conn.close()
        flash('指定された楽曲が見つかりませんでした。', 'error')
        return redirect(url_for('index'))
        
    # この曲に対する考察を取得（いいね数順、同じなら新しい順）
    cursor.execute(
        'SELECT * FROM interpretations WHERE song_id = ? ORDER BY likes DESC, created_at DESC',
        (song_id,)
    )
    interpretations = cursor.fetchall()
    conn.close()
    
    return render_template('song.html', song=song, interpretations=interpretations)

@app.route('/song/<int:song_id>/interpret', methods=['POST'])
def add_interpretation(song_id):
    contributor = request.form.get('contributor', '').strip() or '匿名OORer'
    section_title = request.form.get('section_title', '').strip()
    content = request.form.get('content', '').strip()
    
    if not section_title or not content:
        flash('考察対象のフレーズと考察内容は必須です。', 'error')
        return redirect(url_for('song_detail', song_id=song_id))
        
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO interpretations (song_id, contributor, section_title, content) VALUES (?, ?, ?, ?)',
        (song_id, contributor, section_title, content)
    )
    conn.commit()
    conn.close()
    
    flash('歌詞考察を投稿しました！熱い考察をありがとうございます。', 'success')
    return redirect(url_for('song_detail', song_id=song_id))

# いいね！機能（非同期API用）
@app.route('/interpretation/<int:interpret_id>/like', methods=['POST'])
def like_interpretation(interpret_id):
    conn = get_db()
    cursor = conn.cursor()
    
    # 存在確認
    cursor.execute('SELECT likes FROM interpretations WHERE id = ?', (interpret_id,))
    row = cursor.fetchone()
    
    if not row:
        conn.close()
        return jsonify({'success': False, 'message': '考察が見つかりませんでした。'}), 404
        
    new_likes = row['likes'] + 1
    cursor.execute('UPDATE interpretations SET likes = ? WHERE id = ?', (new_likes, interpret_id))
    conn.commit()
    conn.close()
    
    return jsonify({'success': True, 'likes': new_likes})

if __name__ == '__main__':
    # ポート5000で起動
    app.run(debug=True, host='0.0.0.0', port=5000)
