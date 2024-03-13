import streamlit as st
from dotenv import load_dotenv
import os
import openai
import datetime
import json
import utils

curr_dir = os.path.dirname(os.path.abspath(__file__))

load_dotenv(os.path.join(curr_dir, "../.env"))

st.set_page_config(
    page_title="Prompt Flow Scoring",
)

st.title("Prompt Flow Scoring")

st.caption(
    """
NOTE:
Currently we will use {"question": "your prompt"} as input and expect {"output": "LLM response"}.
Make sure your scoring API interface is working like this.
"""
)


with st.sidebar:
    st.session_state.prompt_flow_scoring_endpoint = st.text_input(
        "Prompt Flow Scoring Endpoint",
        value=st.session_state.get(
            "prompt_flow_scoring_endpoint", os.getenv("PROMPT_FLOW_SCORING_ENDPOINT")
        ),
        type="default",
    )
    st.session_state.prompt_flow_scoring_key = st.text_input(
        "Prompt Flow Scoring Key",
        value=st.session_state.get(
            "prompt_flow_scoring_key", os.getenv("PROMPT_FLOW_KEY")
        ),
        type="password",
    )

download_button = st.empty()


if "prompt_flow_scoring_history" not in st.session_state:
    st.session_state["prompt_flow_scoring_history"] = []

# Render history messages
for msg in st.session_state.prompt_flow_scoring_history:
    role = msg["role"]
    if msg["role"] == "error":
        role = "assistant"
    with st.chat_message(role):
        if msg["role"] != "error":
            st.write(msg["content"])
        else:
            st.error(msg["content"])

# https://streamlit.io/generative-ai
# TODO: make response streaming https://docs.streamlit.io/knowledge-base/tutorials/build-conversational-apps#build-a-simple-chatbot-gui-with-streaming
if prompt := st.chat_input():
    if (
        not st.session_state.prompt_flow_scoring_endpoint
        or not st.session_state.prompt_flow_scoring_key
    ):
        st.warning("🥸 Please add your Prompt Flow Endpoint and Key to continue.")
        st.stop()

    client = utils.PromptFlowScoring(
        st.session_state.prompt_flow_scoring_endpoint,
        st.session_state.prompt_flow_scoring_key,
    )

    st.session_state.prompt_flow_scoring_history.append(
        {"role": "user", "content": prompt}
    )
    st.chat_message("user").write(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        try:
            response = client.query({"question": prompt})
            st.session_state.prompt_flow_scoring_history.append(
                {"role": "assistant", "content": response["output"]}
            )
            message_placeholder.write(response["output"])
        except:
            message_placeholder.error(response["error"])

            st.session_state.prompt_flow_scoring_history.append(
                {
                    "role": "error",
                    "content": response["error"],
                }
            )


# TODO: maybe summarize content for the file name
download_button.download_button(
    "Download current chat history",
    json.dumps(
        st.session_state.prompt_flow_scoring_history, indent=4, ensure_ascii=False
    ),
    f"history_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.json",
    mime="text/plain",
    disabled=not st.session_state.prompt_flow_scoring_history,
)
