import streamlit as st
import requests
from datetime import datetime

API_KEY = st.secrets["GROQ_API_KEY"]

st.set_page_config(
    page_title="مساعدي الذكي",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="expanded"
)

# 🎨 CSS
st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stApp {background-color: #000000;}
    
    .main-title {
        text-align: center;
        font-size: 2rem;
        font-weight: bold;
        color: #E7E9EA;
        margin-bottom: 0.3rem;
    }
    .sub-title {
        text-align: center;
        color: #71767B;
        font-size: 0.9rem;
        margin-bottom: 2rem;
    }
    
    .stChatInput textarea {
        background-color: #16181C !important;
        color: #E7E9EA !important;
        border: 1px solid #2F3336 !important;
        border-radius: 25px !important;
        padding: 15px 20px !important;
    }
    
    .stChatMessage {background-color: transparent !important;}
    [data-testid="chatAvatarIcon-user"] {background-color: #1D9BF0 !important;}
    [data-testid="chatAvatarIcon-assistant"] {background-color: #FF6B00 !important;}
    
    .suggestion-btn button {
        background-color: #16181C !important;
        color: #E7E9EA !important;
        border: 1px solid #2F3336 !important;
        border-radius: 20px !important;
        padding: 10px 15px !important;
        font-size: 0.85rem !important;
        width: 100% !important;
    }
    .suggestion-btn button:hover {
        border-color: #1D9BF0 !important;
    }
</style>
""", unsafe_allow_html=True)

# 🎭 الشخصيات
PERSONAS = {
    "مساعد عام": "أنت مساعد ذكي عربي، بترد بإيجاز ومفيد بالعربي المصري.",
    "مبرمج": "أنت مبرمج محترف، بتساعد في كتابة وتصحيح الأكواد. اشرح بالعربي المصري وبساطة.",
    "مدرس": "أنت مدرس صبور، بتبسط المعلومات المعقدة بأمثلة بسيطة. اشرح بالعربي المصري.",
    "مترجم": "أنت مترجم محترف، بتترجم بين العربية والإنجليزية بدقة. ارد باللغة المطلوبة."
}

# ⚙️ الموديلات
MODELS = {
    "GPT-OSS 120B (قوي)": "openai/gpt-oss-120b",
    "GPT-OSS 20B (سريع)": "openai/gpt-oss-20b",
    "Qwen 3.8 27B": "qwen/qwen3.8-27b"
}

# 🧠 Session State
if "messages" not in st.session_state:
    st.session_state.messages = []
if "persona" not in st.session_state:
    st.session_state.persona = "مساعد عام"
if "model" not in st.session_state:
    st.session_state.model = "GPT-OSS 120B (قوي)"
if "start_time" not in st.session_state:
    st.session_state.start_time = datetime.now()

# 📊 الشريط الجانبي
with st.sidebar:
    st.markdown("### 🤖 مساعدي الذكي")
    st.markdown("---")
    
    if st.button("✨ محادثة جديدة", use_container_width=True):
        st.session_state.messages = []
        st.session_state.start_time = datetime.now()
        st.rerun()
    
    st.markdown("---")
    st.markdown("### 🎭 الشخصية")
    persona = st.selectbox(
        "اختار شخصية:",
        list(PERSONAS.keys()),
        index=list(PERSONAS.keys()).index(st.session_state.persona),
        label_visibility="collapsed"
    )
    st.session_state.persona = persona
    
    st.markdown("### ⚙️ الموديل")
    model = st.selectbox(
        "اختار الموديل:",
        list(MODELS.keys()),
        index=list(MODELS.keys()).index(st.session_state.model),
        label_visibility="collapsed"
    )
    st.session_state.model = model
    
    st.markdown("---")
    st.markdown("### 📊 إحصائيات")
    st.metric("عدد الرسائل", len(st.session_state.messages))
    
    elapsed = datetime.now() - st.session_state.start_time
    minutes = int(elapsed.total_seconds() // 60)
    st.metric("مدة المحادثة", f"{minutes} دقيقة")
    
    st.markdown("---")
    
    if st.session_state.messages:
        chat_text = ""
        for msg in st.session_state.messages:
            role = "أنت" if msg["role"] == "user" else "المساعد"
            chat_text += f"{role}: {msg['content']}\n\n"
        
        st.download_button(
            "📥 تحميل المحادثة",
            chat_text,
            file_name=f"chat_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
            use_container_width=True
        )
    
    st.markdown("---")
    st.caption("صُنع بواسطة أحمد 💪")
    st.caption("مدعوم بـ Groq API ⚡")

# 🎨 العنوان
st.markdown('<h1 class="main-title">مساعدي الذكي</h1>', unsafe_allow_html=True)
st.markdown(f'<p class="sub-title">{st.session_state.persona} • {st.session_state.model}</p>', unsafe_allow_html=True)

# 📜 عرض الرسائل
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 💡 أزرار الاقتراحات (لو المحادثة فاضية)
if len(st.session_state.messages) == 0:
    st.markdown("### 💡 جرب تسأل:")
    
    col1, col2 = st.columns(2)
    suggestions = [
        "اشرحلي يعني إيه ذكاء اصطناعي",
        "اكتبلي كود Python بسيط",
        "ساعدني في حل معادلة رياضية",
        "ترجملي جملة للإنجليزي"
    ]
    
    for i, suggestion in enumerate(suggestions):
        col = col1 if i % 2 == 0 else col2
        with col:
            st.markdown('<div class="suggestion-btn">', unsafe_allow_html=True)
            if st.button(suggestion, key=f"sug_{i}", use_container_width=True):
                st.session_state.messages.append({"role": "user", "content": suggestion})
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

# 💬 الإدخال
if prompt := st.chat_input("اسأل عن أي شيء..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.rerun()

# 🤖 الرد
if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
    with st.chat_message("assistant"):
        with st.spinner("بفكر..."):
            try:
                url = "https://api.groq.com/openai/v1/chat/completions"
                headers = {
                    "Authorization": "Bearer " + API_KEY,
                    "Content-Type": "application/json"
                }
                
                system_prompt = PERSONAS[st.session_state.persona]
                model_id = MODELS[st.session_state.model]
                
                data = {
                    "model": model_id,
                    "messages": [
                        {"role": "system", "content": system_prompt}
                    ] + st.session_state.messages
                }
                
                response = requests.post(url, headers=headers, json=data, timeout=60)
                result = response.json()
                
                if "choices" in result:
                    answer = result["choices"][0]["message"]["content"]
                else:
                    answer = "❌ خطأ: " + str(result)
            except Exception as e:
                answer = "❌ مشكلة في الاتصال: " + str(e)
            
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
            st.rerun()
