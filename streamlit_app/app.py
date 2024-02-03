import os
import warnings
import sys
import streamlit as st
import unidecode


warnings.filterwarnings("ignore")
# Get the directory of the current file
current_dir = os.path.dirname(os.path.abspath(__file__))

# Define the path relative to the current file
# For example, if the directory to add is the parent directory of the current file
parent_dir = os.path.join(current_dir, "..")

# Add the parent directory to sys.path
sys.path.insert(0, parent_dir)

from sql_agent.agent import create_agent
from streamlit_app.gen_final_output import display_text_with_images

st.set_page_config(page_title="Rappel conso")


def generate_response(input_text):
    """
    Generates a response based on the given input text using the agent.

    Args:
        input_text (str): The input text to generate a response for.

    Returns:
        str: The generated response.
    """
    prompt = unidecode.unidecode(input_text)
    return st.session_state.agent.run(prompt)


def reset_conversation():
    st.session_state.messages = []
    st.session_state.agent = create_agent()


# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

if "agent" not in st.session_state:
    st.session_state.agent = create_agent()


st.title("Rappel conso QA :rotating_light: :health_worker: :flag-fr:")
col1, col2 = st.columns([3, 1])
with col2:
    st.button("Reset Chat", on_click=reset_conversation)

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message["role"] == "assistant":
            display_text_with_images(message["content"])
        else:
            st.markdown(message["content"])


# Accept user input
if prompt := st.chat_input("Please ask your question / Posez votre question:"):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    response = generate_response(prompt)
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        display_text_with_images(response)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})
