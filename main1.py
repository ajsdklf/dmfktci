import streamlit as st 
import time
import json
import random

st.title("🏠 맞춤형 정부지원 서비스 추천 시스템")
st.write("10,056개의 정부지원 서비스 중에서 당신에게 꼭 맞는 서비스를 찾아드립니다.")

# Load sample data 
with open('database/exp17_db_compiling_with_age_restriction.json', 'r', encoding='utf-8') as f:
    services_db = json.load(f)

# 초기 상태 설정
if 'stage' not in st.session_state:
    st.session_state.stage = 0
    st.session_state.filtered_services = services_db # Just take first 10 services
    st.session_state.search_query = ""
    st.session_state.user_age = 0

# 첫 번째 단계: 서비스 종류 입력  
if st.session_state.stage == 0:
    service_type = st.text_input("찾으시는 서비스 종류를 입력해주세요:", placeholder="예: 주택청약, 취업지원, 소득지원")
    
    if service_type and service_type.strip():
        st.session_state.search_query = service_type
        with st.spinner('데이터베이스 검색 중...'):
            # Fake filtering - just randomly select services
            num_to_select = random.randint(300,400)
            filtered = random.sample(services_db, min(num_to_select, len(services_db)))
            st.session_state.filtered_services = filtered
            time.sleep(4.5)
            
        st.success(f"10,056개의 문서 중 {len(filtered)}개의 관련 문서를 찾았습니다.")
        st.session_state.stage = 1
        st.rerun()

# 두 번째 단계: 나이 입력
elif st.session_state.stage == 1:
    st.info(f"{len(st.session_state.filtered_services)}개의 문서가 검토 대상입니다.")
    age = st.number_input("나이를 입력해주세요:", min_value=0, max_value=120)
    
    if age > 0:
        st.session_state.user_age = age
        with st.spinner('나이 기반 필터링 중...'):
            # Fake age filtering
            num_to_remove = random.randint(150,250)
            num_to_keep = max(len(st.session_state.filtered_services) - num_to_remove, 1)
            filtered = random.sample(st.session_state.filtered_services, num_to_keep)
            st.session_state.filtered_services = filtered
            time.sleep(5)
            
        st.success(f"{len(filtered)}개의 적합한 서비스를 찾았습니다.")
        st.session_state.stage = 2
        st.rerun()

# 세 번째 단계: 첫 번째 자연어 요구사항
elif st.session_state.stage == 2:
    st.info(f"{len(st.session_state.filtered_services)}개의 문서가 검토 대상입니다.")
    requirement1 = st.text_area("귀하의 요구사항을 자유롭게 작성해주세요:", placeholder="예: 신혼부부이고 맞벌이입니다.")
    
    if requirement1 and requirement1.strip():
        with st.spinner('요구사항 분석 중...'):
            # Fake filtering
            num_to_keep = random.randint(20,30)
            filtered = random.sample(st.session_state.filtered_services, min(num_to_keep, len(st.session_state.filtered_services)))
            st.session_state.filtered_services = filtered
            time.sleep(6)
            
        st.success(f"{len(filtered)}개의 관련 서비스를 찾았습니다.")
        st.session_state.stage = 3
        st.rerun()

# 네 번째 단계: 두 번째 자연어 요구사항
elif st.session_state.stage == 3:
    st.info(f"{len(st.session_state.filtered_services)}개의 문서가 검토 대상입니다.")
    requirement2 = st.text_area("더 구체적인 요구사항을 작성해주세요:", placeholder="예: 월소득 500만원 이하이고 자녀가 없습니다.")
    
    if requirement2 and requirement2.strip():
        with st.spinner('최종 분석 중...'):
            # Get random 5 services for final results
            final_services = random.sample(st.session_state.filtered_services, min(5, len(st.session_state.filtered_services)))
            st.session_state.filtered_services = final_services
            time.sleep(7)
            
        st.success("최종적으로 가장 적합한 5개의 서비스를 찾았습니다!")
        st.session_state.stage = 4
        st.rerun()

# 다섯 번째 단계: 최종 결과 표시
elif st.session_state.stage == 4:
    st.subheader("🎉 추천 서비스 목록")
    
    for idx, service in enumerate(st.session_state.filtered_services, 1):
        with st.container():
            col1, col2 = st.columns([4,1])
            with col1:
                st.markdown(f"### {idx}. {service['service_title']}")
                st.write(f"**서비스 설명:** {service['service_description']}")
                
                with st.expander("상세 정보 보기"):
                    st.markdown("**지원대상**")
                    st.write(service['target_content'])
                    
                    st.markdown("**지원내용**")
                    st.write(service['support_content'])
                    
                    st.markdown("**신청방법**")
                    st.write(service['apply_content'])
                    
                    st.markdown("**문의처**")
                    st.write(service['contact_content'])
                    
            with col2:
                match_score = random.randint(85, 99)
                st.metric("매칭률", f"{match_score}%")
            st.divider()
    
    if st.button("처음부터 다시 시작"):
        st.session_state.stage = 0
        st.session_state.filtered_services = services_db # Reset to all services
        st.session_state.search_query = ""
        st.session_state.user_age = 0
        st.rerun()