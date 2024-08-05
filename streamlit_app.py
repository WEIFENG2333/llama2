import streamlit as st
import requests
import json

st.session_state.book_data = None
st.set_page_config(layout="wide")

@st.cache_data
def search(search_info, page):
    search_url = 'https://bookapi.bkfeng.top/proxy?targeturl=https://api.ylibrary.org/api/search/'
    search_url = 'https://bookapi.bkfeng.top/search'
    search_json = {
        'query': search_info,
        'page': page
    }
    req = requests.post(search_url, json=search_json, timeout=10)
    return req.json()


@st.cache_data
def detail(search_id, source):
    detail_url = 'https://bookapi.bkfeng.top/proxy?targeturl=https://api.ylibrary.org/api/detail/'
    detail_json = {
        'id': search_id,
        'source': source
    }
    try:
        req = requests.post(detail_url, json=detail_json, timeout=3)
        return req.json()
    except:
        return {"title": search_id, "md5": "", "filesize": 50000000, "extension": "zip"}


st.title("本卡风书籍搜索")

# * search bar and text input
col1, col2 = st.columns([0.9, 0.1])
with col1:
    query = st.text_input(
        label="query", key="query", label_visibility="collapsed", placeholder="输入搜索关键词")
with col2:
    search_button = st.button(label="搜索", key="search_button")

# st.write(query)
if query and search_button:
    book_data = search(query, 1)
    # st.write(book_data)
    # st.write(book_data)
    st.session_state.book_data = book_data['data']

if st.session_state.book_data:
    st.write("搜索结果：")
    for i in st.session_state.book_data:
        with st.container(border=True):
            img_col, detail_col, button = st.columns([0.1, 0.7, 0.2])
            with img_col:
                if i.get('cover'):
                    st.image(i.get('cover', 'https://bookapi.bkfeng.top/static/img/cover.jpg'), use_column_width=True)
            with detail_col:
                st.write(f"### {i.get('title', '未知')}")
                st.write(f"**出版社：** {i.get('publisher', '未知')} ")
                st.write(f" **作者：** {i.get('author', '未知')}")
                st.write(f"**文件大小：** {i.get('filesize', '未知')}")
            with button:
                if st.button(label="下载", key=i.get('id')):
                    st.write("下载中...")
                    download_url = detail(i.get('id'), i.get('source'))
                    st.write(download_url)
                    st.write(f"下载链接：[{download_url.get('title', '未知')}](https://bookapi.bkfeng.top/download?md5={download_url.get('md5', '')}&extension={download_url.get('extension', '')})")

# * pagination
# st.write("上一页")
# st.write("1")
# st.write("2")
# st.write("3")
