import streamlit as st
from openai import OpenAI 

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.header('장학금 안내 서비스')

if 'sector' not in st.session_state:
    st.session_state['sector'] = ""
if 'initialized' not in st.session_state:
    st.session_state['initialized'] = False

sector_query = st.text_input('장학금 관련 알고 싶은 정보를 입력해주세요. ex: 학자금 대출, 기부 장학금, 취업연계 장학금 등')

if sector_query and not st.session_state['initialized']:
    PROMPT_TO_CHECK_SECTOR = """
    You are tasked with mapping the user's query to the sector of scholarship. Your answer has to be one of the following: 
    1. 학자금 대출
    2. 기부 장학금
    3. 취업연계 장학금
    4. 기타
    
    Your response has to be in Korean and only include one of the above options. Don't include any explanations nor other words than the name of the sector you chosed. 
    
    Examples of answers: 
    학자금 대출,
    기부 장학금,
    취업연계 장학금,
    기타
    """
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": PROMPT_TO_CHECK_SECTOR}, {"role": "user", "content": sector_query}],
        temperature=0,
    )
    st.session_state['sector'] = response.choices[0].message.content
    st.session_state['initialized'] = True

if st.session_state['sector'] == '학자금 대출':
    with st.form(key='loan_scholarship'):
        st.write('학자금 대출 관련 안내를 위해 필요한 정보를 입력해주세요.')
        

if st.session_state['sector'] == '기부 장학금':
    pass

if st.session_state['sector'] == '취업연계 장학금':
    pass

if st.session_state['sector'] == '기타':
    pass