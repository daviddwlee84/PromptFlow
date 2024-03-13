import streamlit as st
from typing import Literal, Tuple, Dict, List
import os
import openai
import requests


def generate_api_and_language_model_selection() -> Literal["OpenAI", "Azure OpenAI"]:
    openai_selection = st.selectbox("OpenAI Version", ["OpenAI", "Azure OpenAI"])

    if openai_selection == "OpenAI":
        st.session_state.openai_api_key = st.text_input(
            "OpenAI API Key",
            value=st.session_state.get("openai_api_key", os.getenv("OPENAI_API_KEY")),
            type="password",
        )
    elif openai_selection == "Azure OpenAI":
        st.session_state.azure_openai_api_key = st.text_input(
            "Azure OpenAI API Key",
            value=st.session_state.get(
                "azure_openai_api_key", os.getenv("AZURE_OPENAI_KEY")
            ),
            type="password",
        )
        st.session_state.azure_openai_endpoint = st.text_input(
            "Azure OpenAI Endpoint",
            value=st.session_state.get(
                "azure_openai_endpoint", os.getenv("AZURE_OPENAI_ENDPOINT")
            ),
            type="default",
        )
        st.session_state.azure_openai_deployment_name = st.text_input(
            "Azure OpenAI Deployment Name",
            value=st.session_state.get(
                "azure_openai_deployment_name",
                os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
            ),
            type="default",
        )
        st.session_state.azure_openai_version = st.text_input(
            "Azure OpenAI Version",
            value=st.session_state.get(
                "azure_openai_version", os.getenv("AZURE_OPENAI_VERSION")
            ),
            type="default",
        )

    st.divider()

    st.session_state.model = st.text_input(
        "Model Name",
        value=st.session_state.get("model", "gpt-3.5-turbo"),
        type="default",
    )
    st.session_state.temperature = st.number_input(
        "Temperature",
        min_value=0.0,
        max_value=2.0,
        step=0.1,
        value=st.session_state.get("temperature", 0.0),
    )

    return openai_selection


def extract_error_from_openai_BadRequestError(
    error: openai.BadRequestError,
) -> Tuple[str, dict]:
    """
    openai.InvalidRequestError (openai < 1.0) -> openai.BadRequestError (openai >= 1.0)
    https://github.com/openai/openai-python/discussions/742
    """
    error = error.response.json()
    error_message = error["error"]["message"]
    error_reason = {}
    for reason, result in error["error"]["innererror"]["content_filter_result"].items():
        if result["filtered"]:
            error_reason[reason] = result["severity"]
    return error_message, error_reason

def construct_prompt_flow_chat_history_from_openai(openai_format_chat_history: List[Dict[str, str]]):
    """
    TODO:

    Convert

    [
        {
            "role": "user",
            "content": "What is DRI?"
        },
        {
            "role": "assistant",
            "content": "DRI stands for Directly Responsible Individual. In the context of DRI Responsibilities, the DRI is the primary person responsible for specific tasks and responsibilities outlined in the document. (Source: DRI Responsibilities.md)"
        },
        {
            "role": "user",
            "content": "What is IcM?"
        },
        {
            "role": "assistant",
            "content": "IcM stands for Incident and Change Management. It is a system or process used to manage and track incidents and changes within an organization. (Source: DRI Responsibilities.md)"
        }
    ]

    To

    {
        "chat_history": [
            {
                "id": "45fee55b-42d4-4588-9b3d-86eaca859e8a",
                "inputs": {"question": "I'm David"},
                "outputs": {
                    "answer": "Hello David! How can I assist you today?"
                },
                "duration": 2.9924000000059605,
                "navId": "37a4ba7e-55e8-43cc-a65e-dd2bc55bd2eb",
            },
            {
                "id": "ed82197c-a77b-45e6-9046-48001674e869",
                "inputs": {"question": "Who am I?"},
                "outputs": {
                    "output": "You are David, as you mentioned earlier. Is there anything specific you would like assistance with, David?"
                },
                "duration": 2.1015,
                "navId": "37a4ba7e-55e8-43cc-a65e-dd2bc55bd2eb",
            },
        ]
    }

    NOTE: Prompt Flow history is inputs-outputs pair, while openai is assistant and human individual
    """

class PromptFlowScoring:
    def __init__(self, endpoint: str, key: str = None) -> None:
        """
        Using local endpoint can run without key
        """
        self.endpoint = endpoint
        self.key = key
        # https://stackoverflow.com/questions/29931671/making-an-api-call-in-python-with-an-api-that-requires-a-bearer-token
        # TODO: https://requests.readthedocs.io/en/latest/user/authentication/#new-forms-of-authentication
        self.headers = {
            "Content-Type": "application/json",
        }
        if key:
            self.headers["Authorization"] = f"Bearer {key}"

    def call(self, data: dict) -> requests.Response:
        return requests.post(self.endpoint, headers=self.headers, json=data)

    def query(self, data: dict) -> dict:
        # BUG: requests.exceptions.InvalidJSONError: Circular reference detected
        response = self.call(data)
        if response.status_code != 200:
            return {"error": response.text}
        return response.json()


if __name__ == "__main__":
    from dotenv import load_dotenv

    load_dotenv()
    scoring = PromptFlowScoring(
        os.getenv("PROMPT_FLOW_SCORING_ENDPOINT"), os.getenv("PROMPT_FLOW_KEY")
    )
    print(response := scoring.call({"question": "What is DRI?"}))
    print(answer := scoring.query({"question": "What do you know?"}))

    local_scoring = PromptFlowScoring("http://localhost:28080/score")
    print(local_response := local_scoring.call({"question": "How is your day?"}))

    import ipdb

    ipdb.set_trace()
