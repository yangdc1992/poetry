import json
import requests
import streamlit as st
from apig_sdk import signer

sig = signer.Signer()
sig.Key = st.secrets["ak"]
sig.Secret = st.secrets["sk"]

def poetry_gen(input_text, style):
    body_str = json.dumps({"text": input_text, "style": style})
    url = "https://23b3de61a2724abd858e01c718fae4b8.apig.cn-north-4.huaweicloudapis.com/v1/infers/5175b4cb-f6e2-45ec-a4e1-5c4b691c031a" + "/poetry/gen"
    r = signer.HttpRequest("POST", url, {"x-stage": "RELEASE","Content-Type":"application/json"}, body_str)
    sig.Sign(r)
    resp = requests.request(r.method, r.scheme + "://" + r.host + r.uri, headers=r.headers, data=r.body)

    print(resp.status_code, resp.reason)

    state = "fail"
    result = json.loads(resp.content.decode('utf-8'))
    if resp.status_code == 200:
        result = result["result"]
        state = "success"

    return state, result


st.subheader('藏头诗生成器')
st.write("藏头诗生成demo, 基于GPT2实现，后台服务部署在华为云")

user_input = st.text_input('请输入藏头诗开头: ')

style = st.radio("请选择生成样式", ('五言', '七言'))
style = 0 if style=="五言" else 1

if st.button('RUN'):
    state, result = poetry_gen(user_input, style)

    if state == "success":
        st.text_area(label="", value=result, height=120)
    else:
        st.error(result)