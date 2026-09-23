Python
import os
import time
import streamlit as st
from google import genai
from datetime import datetime

# 1. วาง st.set_page_config เป็นคำสั่งแรกสุดเสมอ
st.set_page_config(page_title='Horoscope', page_icon='🔮')

def generate_gemini_answer(prompt, system_prompt="", is_json=False):
    gemini_api_key = st.secrets.get("GEMINI_API_KEY") or os.environ.get("GEMINI_API_KEY")
    if not gemini_api_key:
        return "Error: ไม่พบ GEMINI_API_KEY กรุณาตั้งค่าใน Streamlit Secrets"
    
    # บังคับใช้โมเดลเสถียรมาตรฐานเรียงตามลำดับป้องกัน Secrets ค้างชื่อผิด
    models_to_try = ["gemini-2.5-flash", "gemini-1.5-flash", "gemini-2.0-flash"]

    gmn_client = genai.Client(api_key=gemini_api_key)
    output_type = "application/json" if is_json else "text/plain"

    last_error = ""
    for model_name in models_to_try:
        for attempt in range(3):
            try:
                response = gmn_client.models.generate_content(
                    model=model_name,
                    config=genai.types.GenerateContentConfig(
                        system_instruction=system_prompt,
                        response_mime_type=output_type
                    ),
                    contents=prompt
                )
                return response.text
            except Exception as e:
                last_error = str(e)
                if "503" in last_error or "UNAVAILABLE" in last_error or "429" in last_error:
                    time.sleep(2)
                    continue
                else:
                    break

    return f"Error: เซิร์ฟเวอร์ Gemini มีผู้ใช้งานแน่นชั่วคราว กรุณากดปุ่มใหม่อีกครั้งในอีก 5-10 วินาที ({last_error})"

def horo_tell(l4phone, question, time_diff):
    total_num = sum([int(i) for i in l4phone])
    now = datetime.now()
    cf = now.strftime("%A, %B %d, %Y")

    # รวม Prompt เป็นคำขอเดียว ไม่ต้องยิง API 2 รอบ
    if question and time_diff:
        teller_prompt = f"""
**Role:** You are a mystical and insightful Numerologist.
**Task:** 1) Interpret base destiny from mobile numbers. 2) Predict future outcome for user's question within the timeframe.

**Input Data:**
- Current Date: {cf}
- Last 4 Digits: {l4phone} (Total Sum: {total_num})
- Career Pair: {l4phone[:2]}, Finance Pair: {l4phone[1:-1]}, Love Pair: {l4phone[-2:]}
- Timeframe: Next {time_diff}
- Specific Question: "{question}"

**Constraints:**
1. Length: 1-2 short sentences per bullet.
2. Output format: English first, followed by Thai.

**Response Format:**

**[ENGLISH]**
**Base Destiny**
- **Career ({l4phone[:2]}):** [Short prediction]
- **Finance ({l4phone[1:-1]}):** [Short prediction]
- **Love ({l4phone[-2]}):** [Short prediction]

**Future Prediction (Next {time_diff})**
- **Outcome:** [Direct prediction for "{question}"]
- **Advice:** [Key advice/caution]

---
**[THAI]**
**พื้นดวงชะตา**
- **การงาน ({l4phone[:2]}):** [คำทำนายสั้นๆ]
- **การเงิน ({l4phone[1:-1]}):** [คำทำนายสั้นๆ]
- **ความรัก ({l4phone[-2]}):** [คำทำนายสั้นๆ]

**คำทำนายอนาคต (ในอีก {time_diff})**
- **ผลลัพธ์:** [คำทำนายตรงๆ สำหรับคำถาม "{question}"]
- **ข้อควรระวัง & คำแนะนำ:** [คำแนะนำสั้นๆ]
"""
    else:
        teller_prompt = f"""
**Role:** You are a mystical Numerologist with an engaging, narrative style.
**Task:** Interpret destiny based on the last 4 digits of a phone number.

**Input Data:**
- Total Sum: {total_num}
- Career Pair: {l4phone[:2]}, Finance Pair: {l4phone[1:-1]}, Love Pair: {l4phone[-2:]}

**Response Format:**

**[ENGLISH]**
**Core Definition:** [Short phrase]
- **Career ({l4phone[:2]}):** [1-2 sentences]
- **Finance ({l4phone[1:-1]}):** [1-2 sentences]
- **Love ({l4phone[-2]}):** [1-2 sentences]

---
**[THAI]**
**นิยามภาพรวม:** [วลีสั้นๆ]
- **ภาพรวมการงาน ({l4phone[:2]}):** [1-2 ประโยค]
- **ภาพรวมการเงิน ({l4phone[1:-1]}):** [1-2 ประโยค]
- **ภาพรวมความรัก ({l4phone[-2]}):** [1-2 ประโยค]
"""

    return generate_gemini_answer(teller_prompt)

# Session State Initialization
if 'answer' not in st.session_state:
    st.session_state['answer'] = ''

st.title('ดูดวงเบอร์โทรศัพท์4ตัวท้ายพร้อมคำทำนาย by Fariszme')
st.subheader("Let's predict your basic destiny and future.")
st.subheader("มาดูดวงชะตาและทำนายอนาคตกันเถอะ")

col11, col12 = st.columns([2, 1])
user_l4phone = col11.text_input(':red[*]Mobile Number Numerology (Last 4 Digits)\n\nพื้นดวงจากเลขท้ายมือถือ 4 ตัว:', max_chars=4, placeholder='XXXX')
col12.write(':full_moon::waning_gibbous_moon::last_quarter_moon::waning_crescent_moon::new_moon::waxing_crescent_moon::first_quarter_moon::waxing_gibbous_moon::full_moon:')
st.divider()

col21, col22 = st.columns([2, 1])
user_question = col21.text_input('What you want to know\n\nคำถามที่อยากจะรู้:', placeholder='กรอกข้อความที่อยากจะรู้')
time_diff = col22.selectbox('Upcoming events in the next...\n\nที่จะเกิดขึ้นข้างหน้าในอีก:', ['', '3 day/3 วัน', '7 day/7 วัน', '15 day/15 วัน', '30 day/30 วัน'])

if st.button("Interpret"):
    if user_l4phone:
        if user_l4phone.isdigit() and len(user_l4phone) == 4:
            with st.spinner('Interpreting...'):
                answer = horo_tell(user_l4phone, user_question, time_diff)
                st.session_state['answer'] = answer
        else:
            st.warning('Please enter valid 4 digits./กรุณากรอกเลขท้ายมือถือให้ครบ 4 หลัก')
            st.session_state['answer'] = ""
    else:
        st.warning('Please enter the last 4 digits./กรุณากรอกเลขท้ายมือถือ 4 ตัวด้วย')
        st.session_state['answer'] = ""

if st.session_state['answer']:
    st.write(st.session_state['answer'])
