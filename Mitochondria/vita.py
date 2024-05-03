import streamlit as st
from langchain.schema import HumanMessage, SystemMessage, AIMessage
from langchain_community.chat_models import ChatOpenAI

## Streamlit UI
st.set_page_config(page_title="MED Q&A Chatbot")
st.header("Hi im Vita")
# st.subheader("Please begin by sharing your full name, age, and token number. Following that, provide details about your current condition or situation")

    
openai_api_key = '''//Your API key here//'''

# Initialize the ChatOpenAI class with your API key
chat = ChatOpenAI(api_key=openai_api_key, temperature=0.5)

# Initialize session_state if not already initialized
if 'flowmessages' not in st.session_state:
    st.session_state['flowmessages'] = [
        SystemMessage(content="""Welcome to the medical AI assistant. To begin, please provide your details in given order
        name, age, and token number.
        Then, describe your medical condition for diagnosis. i will provide a comprehensive summary based on the information provided""")
    ]

## Function to get response from the OpenAI model

def get_chatmodel_response(question):
    st.session_state['flowmessages'].append(HumanMessage(content=question))
    answer = chat(st.session_state['flowmessages'])
    st.session_state['flowmessages'].append(AIMessage(content=answer.content))
    return answer.content

input_text = st.text_input("""Please begin by sharing your details order by  \n
FULL_NAME:\n
AGE:\n
\n TOKEN_NO. \n
Following that, provide details about your current condition or situation \n
is any Medical history specify """, key="input")
response = get_chatmodel_response(input_text)

submit = st.button("Diagnosis")

## If ask button is clicked

if submit:
    st.subheader("My findings")
    st.write(response)

