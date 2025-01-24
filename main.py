import streamlit as st
from langchain_core.messages.chat import ChatMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import load_prompt

# 사용자의 입력
st.title("나의 Chat GPT")


if "messages" not in st.session_state:

    # 대화기록 저장
    st.session_state["messages"] = []

# 사이드바 생성
with st.sidebar:
# 대화 초기화 버튼
    clear_button = st.button("대화 초기화")
    if clear_button:
        st.write("대화 초기화 완료")


# 이전 대화 출력
def print_messages():
    for chat_message in st.session_state["messages"]:
        st.chat_message(chat_message.role).write(chat_message.content)


print_messages()


# 새로운 메세지 추가
def add_message(role, message):
    st.session_state["messages"].append(ChatMessage(role=role, content=message))

# 체인 생성
def create_chain():
    # 프롬프트(기본모드)
    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            "당신은 친절한 AI 어시스턴트입니다. 다음의 질문에 건설하게 답변해 주세요.",
        ),
        ("user", "{question}"),
    ])

    # GPT
    llm = ChatOpenAI(model="gpt-4", temperature=0.8)
    # 출력 파서
    output_parser = StrOutputParser()
    # 체인 생성
    chain = prompt | llm | output_parser
    return chain



# 초기화 버튼 클릭 시
if clear_button:
    st.session_state["messages"] = []
    st.rerun()
    
# 사용자 입력
user_input = st.chat_input("뭐든물어 보세요")

# 만약에 사용자 입력이 들어오면
if user_input:
    # 사용자의 입력
    st.chat_message("user").write(user_input)
    # 체인 생성 (기본모드만 사용)
    chain = create_chain()
    response = chain.invoke({"question": user_input})
    
    # AI 응답 출력 (스트리밍)
    with st.chat_message("AI"):
        container = st.empty()
        answer = ""
        for token in response:
            answer += token
            container.markdown(answer)

    # 대화기록 저장
    add_message("user", user_input)
    add_message("AI", answer)
