import streamlit as st
from google import genai
from google.genai import types
from datetime import datetime

gemini_api_key = 'API Key'
client = genai.Client(api_key=gemini_api_key)

def generate_gemini_answer(prompt):
    response = client.models.generate_content(
        model='gemini-2.5-flash-lite', contents=prompt
    )
    return response.text
# test = generate_gemini_answer("who are tonton songwut?")

def horo_tell(l4phone, question, time_diff):
    total_num = sum([int(i) for i in l4phone])
    teller_prompt = f"""
**Role:** You are a mystical Numerologist with an engaging, narrative style.
**Task:** Interpret the destiny based on the last 4 digits of a phone number.

**Input Data:**
- **Total Sum:** {total_num}
- **Career Pair:** {l4phone[:2]}
- **Finance Pair:** {l4phone[1:-1]}
- **Love Pair:** {l4phone[-2:]}

**Constraints:**
1. **Length:** Strictly 1-2 short sentences per bullet point.
2. **Formatting:** Use **Bold** ONLY for the headers. Do NOT use bold, italics, or any markdown in the body text.
3. **Language:** Output in English first, followed by Thai.

**Response Format:**

**[ENGLISH]**
**Core Definition**
[A short, catchy phrase describing the person]

**Career Overview**
- [Sentence 1-2 about career based on {l4phone[:2]}]
- [Sentence 1-2 extending the prediction]

**Finance Overview**
- [Sentence 1-2 about finance based on {l4phone[1:-1]}]
- [Sentence 1-2 extending the prediction]

**Love Overview**
- [Sentence 1-2 about love based on {l4phone[-2:]}]
- [Sentence 1-2 extending the prediction]

**Conclusion**
- [Summary sentence 1]
- [Summary sentence 2]

**[THAI]**
**นิยามภาพรวมเป็นคำสั้นๆ**
[วลีสั้นๆ ที่จำกัดความตัวตน]

**ภาพรวมการงาน**
- [ประโยคสั้นๆ ทำนายการงานจากเลข {l4phone[:2]}]
- [ประโยคสั้นๆ ขยายความ]

**ภาพรวมการเงิน**
- [ประโยคสั้นๆ ทำนายการเงินจากเลข {l4phone[1:-1]}]
- [ประโยคสั้นๆ ขยายความ]

**ภาพรวมความรัก**
- [ประโยคสั้นๆ ทำนายความรักจากเลข {l4phone[-2:]}]
- [ประโยคสั้นๆ ขยายความ]

**บทสรุป**
- [ประโยคสรุปที่ 1]
- [ประโยคสรุปที่ 2]
"""
    result = generate_gemini_answer(teller_prompt)
    
    if question and time_diff:
        now = datetime.now()
        cf = now.strftime("Today is %A, %B %d, %Y")
        forture_prompt = f""""
**Role:** You are a mystical and insightful Numerologist.
**Task:** Predict the future outcome based on the user's numerology chart and current situation.

**Input Context:**
- **Current Date:** {cf}
- **Timeframe for Prediction:** Next {time_diff}
- **User's Specific Question:** "{question}"
- **User's Base Numerology (Reference):** "{result}"

**Instructions:**
1. Analyze the "Base Numerology" regarding the "Question" to predict the outcome within the "Timeframe".
2. Keep the tone mystical but conciseness is key.
3. **Constraint:** Use only 1-2 short sentences per section.
4. Output must be in **English** followed by **Thai**.

**Output Format:**

---
**[ENGLISH]**
**Short Definition**
[A catchy 3-5 word phrase defining the answer]

**Outcome Overview**
- [Sentence 1: The direct prediction based on the timeframe]
- [Sentence 2: How the base numerology supports this]

**Caution & Advice**
- [Sentence 1: What to watch out for]
- [Sentence 2: A quick advice to handle it]

---
**[THAI]**
**นิยามคำตอบสั้นๆ**
[วลีสั้นๆ 3-5 คำ ที่สรุปคำตอบ]

**ภาพรวมผลลัพธ์**
- [ประโยคที่ 1: คำทำนายตรงๆ สำหรับช่วงเวลานี้]
- [ประโยคที่ 2: เชื่อมโยงกับพื้นดวงที่มี]

**ข้อควรระวัง**
- [ประโยคที่ 1: สิ่งที่ต้องระวัง]
- [ประโยคที่ 2: คำแนะนำสั้นๆ ในการรับมือ]
---
"""
        result_2 = generate_gemini_answer(forture_prompt)
        return result_2
    return result

if 'answer' not in st.session_state:
    st.session_state['answer'] = ''

st.set_page_config(page_title='Horoscope')
st.title('Horoscope')
st.subheader("Let's predict your basic destiny and future.")
st.subheader("มาดูดวงชะตาและทำนายอนาคตกันเถอะ")

col11, col12 = st.columns([2,1], vertical_alignment="bottom")
user_l4phone = col11.text_input(':red[*]Mobile Number Numerology (Last 4 Digits)\n\nพื้นดวงจากเลขท้ายมือถือ 4 ตัว:',max_chars=4,placeholder='XXXX')
col12.write(':full_moon::waning_gibbous_moon::last_quarter_moon::waning_crescent_moon::new_moon::waxing_crescent_moon::first_quarter_moon::waxing_gibbous_moon::full_moon:')
st.divider()

col21, col22 = st.columns([2,1])
user_question = col21.text_input('What you want to know\n\nคำถามที่อยากจะรู้:',placeholder='Winning Number Prediction (Last 2 Digits)/เลขสองตัวท้ายที่จะออก')
time_diff = col22.selectbox('Upcoming events in the next...\n\nที่จะเกิดขึ้นข้างหน้าในอีก:', ['','3 day/3 วัน','7 day/7 วัน','15 day/15 วัน','30 day/30 วัน'])

if st.button("Interpret"):
    if user_l4phone:
        if user_l4phone.isdigit():
            with st.spinner('Interpreting...'):
                answer = horo_tell(user_l4phone, user_question, time_diff)
                st.session_state['answer'] = answer
        else:
            st.warning('Please enter the last 4 digits./กรุณากรอกเลขท้ายมือถือ 4 ตัวด้วย')
            st.session_state['answer'] = ""
    else:
        st.warning('Please enter the last 4 digits./กรุณากรอกเลขท้ายมือถือ 4 ตัวด้วย')
        st.session_state['answer'] = ""
st.write(st.session_state['answer'])