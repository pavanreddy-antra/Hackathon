import streamlit as st
from hackathon.csp import GCPCSP

MESSAGE_HISTORY_LENGTH = 10



class Server():
    def __init__(self):
        self.csp = GCPCSP(embeddings='gcp', chat='gcp', stt='gcp')

    def main(self):
        st.set_page_config(page_title="Chat-ESG", page_icon=":teacher:", layout="wide")
        st.image("tw.png", width=150)
        st.title("Techwish - Challenge 1 - ESG Evaluation Chatbot")
        st.header("Chat with your ESG expert :teacher:")

        if 'conversation' not in st.session_state:
            st.session_state.conversation = []
        if 'history' not in st.session_state:
            st.session_state.history = []
        if 'state' not in st.session_state:
            st.session_state.state = "started"

        if 'reset_input' in st.session_state and st.session_state.reset_input:
            st.session_state.question = ""
            st.session_state.reset_input = False

        user_question = st.text_input("Type your question and press enter:", key="question")

        if st.button("Send"):
            if user_question:
                st.session_state.conversation.append(f"You: {user_question}")

                if len(st.session_state.history) >= MESSAGE_HISTORY_LENGTH:
                    active_history = st.session_state.history[-MESSAGE_HISTORY_LENGTH:]
                    st.session_state.history = st.session_state.history[:-MESSAGE_HISTORY_LENGTH]
                else:
                    active_history = st.session_state.history.copy()
                    st.session_state.history = []

                response, updated_history, updated_state = self.csp.start_conversation(user_question, active_history, st.session_state.state)
                st.session_state.conversation.append(f"Bot: {response}")

                st.session_state.history = st.session_state.history + updated_history
                st.session_state.state = updated_state

        for message in st.session_state.conversation:
            st.write(message)

if __name__ == '__main__':
    Server().main()
