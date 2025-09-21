import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import duckdb as ddb
import streamlit as st
import os

st.title('Hapiness reserch')

# 1つ目の文字列入力欄
st.header('音声日記')
data_input_1 = st.text_input('テキストを入力してください', key='text_a')

# 2つ目の文字列入力欄
st.header('今日の幸せ')
data_input_2 = st.text_input('別のテキストを入力してください', key='text_b')

# 3つ目の数値入力欄
st.header('今日の幸せポイント')
data_input_3 = st.number_input('数値を入力してください', key='number_c')

# 入力された内容を画面に表示
st.write('---')
st.write('### 入力結果')
st.write(f'音声日記: {data_input_1}')
st.write(f'今日の幸せ: {data_input_2}')
st.write(f'今日の幸せポイント: {data_input_3}')

# Renderでは /var/data がある → そこに保存
# ローカルで動かすときはカレントディレクトリに保存
DB_PATH = "/var/data/log_k1.duckdb" if os.path.isdir("/var/data") else "log_k1.duckdb"

con_k1 = ddb.connect(DB_PATH)

# DuckDBにテーブルがなければ作成
con_k1.execute("""
    CREATE TABLE IF NOT EXISTS log_k1 (
        日付 TIMESTAMP,
        音声日記 TEXT,
        今日の幸せ TEXT,
        幸せポイント DOUBLE
    )
""")

# 保存ボタン
if st.button("DBへ保存する"):
    # DataFrameにまとめる
    df = pd.DataFrame([{
        "日付": pd.Timestamp.now(),
        "音声日記": data_input_1,
        "今日の幸せ": data_input_2,
        "幸せポイント": data_input_3
    }])
    # dfを一時テーブルとして登録
    con_k1.register("df_view", df)

    # データを挿入
    con_k1.execute("INSERT INTO log_k1 SELECT * FROM df_view")
    st.success("DuckDBに保存しました！")

st.divider()
st.subheader("DB確認")

# 最近5件（新しい順）
if st.button("最近5件"):

    st.write("最近5件")
    st.dataframe(con_k1.execute(
        "SELECT * FROM log_k1 ORDER BY 日付 DESC LIMIT 5"
    ).df())

# 全部（新しい順）
if st.button("全部"):
    # 全部（新しい順）
    st.write("全部")
    st.dataframe(con_k1.execute(
        "SELECT * FROM log_k1 ORDER BY 日付 DESC"
    ).df())

