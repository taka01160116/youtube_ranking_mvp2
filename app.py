import streamlit as st
import pandas as pd

# ページ設定
st.set_page_config(page_title="YouTubeジャンル別急上昇チャンネルランキング", layout="wide")
st.title("📊 YouTubeジャンル別急上昇チャンネルランキング")
st.caption("直近30日間の総再生数で上位チャンネルを表示し、代表トレンド動画も紹介")

@st.cache_data
def load_data():
    return pd.read_csv("data/channel_video_data.csv", encoding="utf-8-sig")

df = load_data()

# --- ジャンルリスト取得 ---
genres = sorted(df["ジャンル"].unique())
groups = ["5万人未満", "5万人以上"]

# --- サイドバーのジャンルナビゲーション ---
with st.sidebar:
    st.markdown(
        """
        <div style="background:#b03a2e;padding:20px 0 14px 0;border-radius:8px;text-align:center;margin-bottom:10px;">
            <span style="color:white;font-weight:bold;font-size:1.3em;letter-spacing:2px;">ギャラリー</span>
        </div>
        """,
        unsafe_allow_html=True
    )
    selected_genre = st.radio(
        "ジャンルを選択", 
        genres, 
        index=0, 
        key="genre_radio", 
        label_visibility="collapsed"
    )

selected_group = st.radio("登録者数グループ", groups, horizontal=True)

filtered_df = df[(df["ジャンル"] == selected_genre) & (df["グループ"] == selected_group)]
filtered_df = filtered_df.sort_values(by="過去30日再生数", ascending=False)

st.markdown(f"### 🎯 ジャンル「{selected_genre}」・登録者数「{selected_group}」の上位チャンネル")

# バッジカラーの設定
def get_badge_style(rank):
    if rank == 1:
        color = "#FFD700"
        txt = "🥇"
    elif rank == 2:
        color = "#C0C0C0"
        txt = "🥈"
    elif rank == 3:
        color = "#CD7F32"
        txt = "🥉"
    else:
        color = "#b03a2e"
        txt = ""
    return f'<div style="font-size:1.5em;font-weight:bold;color:#fff;background:{color};padding:2px 18px 2px 10px;display:inline-block;border-radius:10px 10px 10px 0;margin-bottom:2px;">{txt} {rank}位</div>'

if filtered_df.empty:
    st.warning("該当するチャンネルがありません。")
else:
    rows = list(filtered_df.iterrows())
    for i in range(0, len(rows), 2):
        cols = st.columns(2)
        for j in range(2):
            if i + j < len(rows):
                idx, row = rows[i + j]
                rank = i + j + 1
                with cols[j]:
                    with st.container():
                        st.markdown(get_badge_style(rank), unsafe_allow_html=True)
                        channel_url = f"https://www.youtube.com/channel/{row['チャンネルID']}"
                        video_url = f"https://www.youtube.com/watch?v={row['トレンド動画ID']}"
                        st.markdown(
                            f"#### [{row['チャンネル名']}]({channel_url})（登録者数：{row['登録者数']:,}人 / 直近30日間の総再生数：{row['過去30日再生数']:,}回）"
                        )
                        st.markdown(
                            f'<a href="{video_url}" target="_blank"><img src="{row["サムネイルURL"]}" width="360" style="border-radius:10px;border:2px solid #b03a2e"></a>',
                            unsafe_allow_html=True
                        )
                        st.markdown(
                            f"**🎥 トレンド動画**：[ {row['トレンド動画タイトル']} ]({video_url})  \n"
                            f"📅 投稿日：{row['トレンド投稿日']}  \n"
                            f"👁️ 再生数：{row['トレンド動画再生数']:,}回"
                        )
