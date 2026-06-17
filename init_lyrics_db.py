import sqlite3
import os

DATABASE = 'lyrics.db'

def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # 既存テーブルを一度削除して再作成（リビルド）
    cursor.execute('DROP TABLE IF EXISTS interpretations')
    cursor.execute('DROP TABLE IF EXISTS songs')
    
    # 楽曲テーブル
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS songs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            album TEXT NOT NULL,
            release_year INTEGER NOT NULL,
            youtube_url TEXT,
            description TEXT NOT NULL
        )
    ''')
    
    # 考察テーブル
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS interpretations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            song_id INTEGER NOT NULL,
            contributor TEXT NOT NULL,
            section_title TEXT NOT NULL,
            content TEXT NOT NULL,
            likes INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (song_id) REFERENCES songs(id)
        )
    ''')
    
    # 楽曲データの挿入 (既存3曲 + 新規8曲 = 計11曲)
    songs = [
        # 既存曲
        (
            "Wherever you are",
            "Nicheシンドローム",
            2010,
            "https://www.youtube.com/embed/ER97G7C5Nac",
            "ボーカルTakaが友人の結婚式のために書き下ろしたとされ、今や結婚式の定番となった究極のラブソング。全編を通して、最愛の人に対する永遠の誓いと無条件の愛がストレートに歌われています。"
        ),
        (
            "The Beginning",
            "人生×僕=",
            2012,
            "https://www.youtube.com/embed/Hh9yZWeTmVM",
            "映画『るろうに剣心』の主題歌として書き下ろされ、ONE OK ROCKの代表曲となった重厚で疾走感あふれるロックナンバー。「始まり」や「諦めない意志」をテーマに、葛藤しながらも自らの未来を切り拓く姿を描いています。"
        ),
        (
            "Wasted Nights",
            "Eye of the Storm",
            2019,
            "https://www.youtube.com/embed/bOZC-yxnF1Y",
            "映画『キングダム』の主題歌。オーケストラを取り入れた壮大なスケール感のサウンドと、「後悔のない人生を送る」「無駄な夜は過ごさない」という力強いメッセージが聴く人の背中を押す名曲です。"
        ),
        # 追加指定曲
        (
            "Detox",
            "Luxury Disease",
            2022,
            "https://www.youtube.com/embed/zH0F6L-0iNs",
            "アルバム『Luxury Disease』に収録されている、エッジの効いたギターリフと疾走感あふれるロックナンバー。心に溜まった葛藤や日常の毒素（Detox）を吐き出し、自分自身を解放する強いメッセージが込められています。"
        ),
        # その他有名曲7曲
        (
            "完全感覚Dreamer",
            "Nicheシンドローム",
            2010,
            "https://www.youtube.com/embed/xGbxsiBZUPI",
            "ONE OK ROCKの名を世に広く知らしめた衝動的なキラーチューン。圧倒的なエネルギーと疾走感で、「理屈抜きに、自分の感覚だけを信じて突き進む」という強い決意とハングリー精神が叫ばれています。"
        ),
        (
            "Mighty Long Fall",
            "35xxxv",
            2015,
            "https://www.youtube.com/embed/UjZqcDYbvAE",
            "映画『るろうに剣心 京都大火編』主題歌。重厚なEDMサウンドとラウドロックを融合させた、バンドの過渡期を象徴する爆発力のあるナンバー。抗えない運命や人生の急激な変化に直面する葛藤を描いています。"
        ),
        (
            "Clock Strikes",
            "人生×僕=",
            2013,
            "https://www.youtube.com/embed/6YZgl2OaLic",
            "スタジアムに響き渡るような壮大なコーラスと美しくエモーショナルなメロディが特徴の名曲。「時間は決して止まらない、だからこそ今を全力で生きる」という普遍的なテーマをポジティブに歌い上げています。"
        ),
        (
            "C.h.a.o.s.m.y.t.h.",
            "残響リファレンス",
            2011,
            "https://www.youtube.com/embed/C-xF2MAFw5s",
            "Takaの親しい友人たちの頭文字（イニシャル）を繋げて名付けられた、友情と新たな旅立ちを歌った感動的なロックバラード。それぞれの道を歩み始めても、互いに過ごした時間と絆は永遠であることを誓う一曲。"
        ),
        (
            "We are",
            "Ambitions",
            2017,
            "https://www.youtube.com/embed/CRLLt70C-aU",
            "NHKの「18祭（フェス）」のために制作され、若者たちの心を掴んだアンセム。葛藤や孤独を抱える世代に向けて、「私たちはここにいる（We are）」と声を上げ、自分らしく生きることを鼓舞する力強いメッセージソングです。"
        ),
        (
            "Re:make",
            "残響リファレンス",
            2011,
            "https://www.youtube.com/embed/6Ym_w8f2H3g",
            "初期〜中期の衝動的なロックサウンドを象徴するスピーディーなキラーチューン。過去の過ちやしがらみを脱ぎ捨てて、自分自身を新しく作り直す（Re:make）という強い意志が込められています。"
        ),
        (
            "Delusion:All",
            "Delusion:All (Single)",
            2024,
            "https://www.youtube.com/embed/g3Z3JkQO1_g",
            "映画『キングダム 大将軍の帰還』主題歌。現代社会の混沌やSNSなどでの衝突、溢れかえる妄想（Delusion）に惑わされず、自らの目と心で真実を見出そうとする強い闘争心と覚悟が描かれています。"
        )
    ]
    
    cursor.executemany('''
        INSERT INTO songs (title, album, release_year, youtube_url, description)
        VALUES (?, ?, ?, ?, ?)
    ''', songs)
    
    # サンプル考察データの挿入
    # 挿入された楽曲のIDを取得
    cursor.execute('SELECT id, title FROM songs')
    song_ids = {row[1]: row[0] for row in cursor.fetchall()}
    
    interpretations = [
        (
            song_ids["Wherever you are"],
            "OORer_TakaLove",
            "「Wherever you are, I always make you smile」の部分について",
            "このフレーズは「君がどこにいようと、僕はいつも君を笑顔にする」という直訳になりますが、単なる恋愛初期の熱い気持ちだけでなく、どんなに遠く離れていても、あるいは人生の困難に直面していても『僕が君を守り抜く』という絶対的な覚悟が感じられます。英語と日本語が絶妙にミックスされることで、感情がよりストレートに響きますね。",
            12
        ),
        (
            song_ids["Wherever you are"],
            "RockSpirits",
            "「愛してるよ」というダイレクトな日本語歌詞の効果",
            "普段は英語詞を多用し、どこか抽象的でスタイリッシュな表現が多いONE OK ROCKが、サビの最後で「愛してるよ 2人は一つに」と非常にシンプルで飾らない日本語を歌うところに最大の魅力があります。洋楽ライクなメロディの中に、あえて泥臭いほどの日本語を載せることで、リスナーの心に一番突き刺さる演出になっていると思います。",
            8
        ),
        (
            song_ids["The Beginning"],
            "LiarMask",
            "「Just give me a reason to keep my heart beating」に込められた意味",
            "るろうに剣心の主人公・緋村剣心の心境とシンクロしているように感じます。「僕の心臓を動かし続けるための理由（＝生きる意味）をくれ」という悲痛とも取れる叫びは、過去の罪（人斬り抜刀斎）を背負いながらも、大切な人を守るために再び立ち上がろうとする強烈な生への執着を表しているのではないでしょうか。",
            15
        ),
        (
            song_ids["Wasted Nights"],
            "KingdomFan",
            "「Don't wanna waste another night」の現代的メッセージ",
            "この曲は、単に『夜遊びを楽しもう』という意味ではなく、『一度きりの人生、立ち止まってくすぶっている時間なんて1秒もない』という強い自己啓発的なメッセージだと解釈しています。Eye of the Stormというアルバム全体のテーマである「嵐の目（自分の中心）で生きる」を最も体現している曲だと思います。",
            10
        ),
        (
            song_ids["Detox"],
            "OORer_Disease",
            "「Detox」のサビとアルバム全体のテーマ性のリンク",
            "『Luxury Disease（贅沢な病）』というアルバムタイトルに対して、この「Detox（解毒）」はまさにその病から脱出するための自己探求ソングだと思います。サビの疾走感は、絡みついたしがらみや『毒』を振り払って一気に駆け抜けるような爽快感があり、ライブで最も化ける曲の一つだと思います！",
            9
        ),
        (
            song_ids["完全感覚Dreamer"],
            "LegendFan",
            "「完全感覚」という言葉の意味",
            "理論や計算ではなく、本能と衝動だけで動いていることを表す言葉だと思います。周りから『無謀だ』と言われようが、自分自身の感覚だけを信じて夢を追いかける姿は、まさに当時のONE OK ROCKそのもの。何年経っても色褪せないエネルギーがここにはあります。",
            24
        ),
        (
            song_ids["Delusion:All"],
            "KingdomNew",
            "「Delusion:All」における争いの虚しさの考察",
            "曲名の「Delusion:All（すべては妄想）」が示す通り、争い合う人々がそれぞれ掲げる正義や主張が、俯瞰してみればただの『妄想』に過ぎないのではないか、という現代社会の対立への鋭い風刺を感じます。激しいサウンドの中にどこか冷徹で知的な視点が混ざっているのが非常に深いです。",
            18
        )
    ]
    
    cursor.executemany('''
        INSERT INTO interpretations (song_id, contributor, section_title, content, likes)
        VALUES (?, ?, ?, ?, ?)
    ''', interpretations)
    
    conn.commit()
    conn.close()
    print("Lyrics database rebuild and seed successfully.")

if __name__ == '__main__':
    init_db()
