import streamlit as st
import requests

API_KEY = st.secrets["GROQ_API_KEY"]

st.set_page_config(
    page_title="مساعدي الذكي",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 مساعدي الذكي")
st.caption("مساعد ذكاء اصطناعي عربي")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("اكتب سؤالك هنا..."):
    
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        with st.spinner("بفكر..."):
            try:
                url = "https://api.groq.com/openai/v1/chat/completions"
                headers = {
                    "Authorization": "Bearer " + API_KEY,
                    "Content-Type": "application/json"
                }
                data = {
                    "model": "openai/gpt-oss-120b",
                    "messages": [
                        {"role": "system", "content": "أنت مساعد ذكي عربي، بترد بإيجاز ومفيد بالعربي المصري."}
                    ] + st.session_state.messages
                }
                
                response = requests.post(url, headers=headers, json=data, timeout=30)
                result = response.json()
                
                if "choices" in result:
                    answer = result["choices"][0]["message"]["content"]
                else:
                    answer = "❌ خطأ: " + str(result)
            except Exception as e:
                answer = "❌ مشكلة في الاتصال: " + str(e)
            
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
