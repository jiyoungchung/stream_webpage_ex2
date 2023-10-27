import streamlit as st
import requests
import pandas as pd
import os, io
import xlsxwriter


# 페이지 기본 설명
st.set_page_config( 
    page_icon='📝',                  # 이모티콘 넣을 수 있는 곳
    page_title='글 요약 서비스',      # 페이지 제목
)
st.title("글 요약 웹 서비스")

# 다시 시작하면 새로고침 후에 실행됨: 정보 그래도 유지하고 싶다면 ?! (재호출 방지)
if "prev_uploaded_file" not in st.session_state:
    st.session_state["prev_uploaded_file"] = None
    st.session_state["prev_df"] = None


# backend
summarize_url = "http://localhost:8000/summarize"

def summarize(text):
    response = requests.post(summarize_url, json={"text":text})
    summary = response.json()["summary"]
    return summary

def summarize_df(df):
    global progress_bar  # progress_bar 증가
    total = len(df)

    news_lst = []
    for i, news_origin in enumerate(df["뉴스원문"], start=1):
        summary = summarize(news_origin)
        news_lst.append(summary)

        progress_bar.progress(i/total, text="progress")

    df['뉴스요약'] = news_lst

    return df

def to_excel(df):
    ''' 데이터프레임의 데이터를 넘기는 함수'''
    output = io.BytesIO()
    writer = pd.ExcelWriter(output, engine="xlsxwriter")
    df.to_excel(writer, sheet_name="Sheet1", index=False)
    # writer.save()
    writer.close()
    processed_data = output.getvalue()
    return processed_data

# tab 만들기
tab1, tab2 = st.tabs(["실시간", "파일 업로드"])

with tab1:
    input_text = st.text_area("여기에 텍스트를 입력하세요.", height=300)
    if st.button("요약"):
        if input_text:
            try:
                summary = summarize(input_text)
                st.success(summary)

            except:
                st.error("요청 오류가 발생했습니다.")
            
        else:
            st.warning("텍스트를 입력하세요.")

with tab2:
    uploaded_file = st.file_uploader("choose a file")

    if uploaded_file:  
        st.success("업로드 성공!")

        if uploaded_file == st.session_state["prev_uploaded_file"]:  # 만약 이전에 업로드한 파일과 동일하다면 ?!
            df = st.session_state["prev_df"]

        else:
            progress_bar = st.progress(0, text="progrss")

            # 뉴스 원본
            df = pd.read_excel(uploaded_file)
            # 뉴스 요약
            df = summarize_df(df)
            st.dataframe(df)

            st.session_state["prev_uploaded_file"] = uploaded_file
            st.session_state["prev_df"] = df

        file_base_name = os.path.splitext(os.path.basename(uploaded_file.name))[0]  # 파일 이름 가져오기
        st.download_button(
            label="Download",
            data=to_excel(df),
            file_name=f"{file_base_name}_summarized.xlsx"
        )