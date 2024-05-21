import replicate.prediction
from PyPDF2 import PdfReader
from transformers import AutoTokenizer
import replicate
from concurrent.futures import ThreadPoolExecutor
from threading import current_thread
import streamlit as st
from streamlit.delta_generator import DeltaGenerator
import functools
from streamlit.runtime.scriptrunner.script_run_context import (
    add_script_run_ctx,
    get_script_run_ctx,
)

def initialization() -> None:
    # Initialize the Streamlit page configuration and header
    st.set_page_config("Cover Letter with Artic", page_icon=":snowflake:", layout="wide")
    st.header(":snowflake: Generate your cover letter with Artic!", divider="blue")

def sidebar() -> None:
    # Setup the sidebar for parameter input and Replicate API token validation
    with st.sidebar:
        st.header('Parameters', divider=True)
        if 'REPLICATE_API_TOKEN' in st.secrets:
            replicate_api = st.secrets['REPLICATE_API_TOKEN']
            st.caption("Replicate API Token found :white_check_mark:")
        else:
            replicate_api = st.text_input('Enter Replicate API token:', type='password')
            if not (replicate_api.startswith('r8_') and len(replicate_api) == 40):
                st.warning('Please enter your Replicate API token.', icon='⚠️')
                st.markdown(
                    "**Don't have an API token?** Head over to [Replicate](https://replicate.com) to sign up for one."
                )
            else:
                st.caption("Replicate API Token :white_check_mark:")

def input_form() -> None:
    # Create the input form for uploading CV and pasting the job offer
    with st.form("input", border=True):
        st.subheader(":card_index: Upload your CV", divider="blue")
        st.file_uploader("CV", ["pdf"], label_visibility="collapsed",key="file",accept_multiple_files=False)
        if st.session_state.file:
            pdf_reader = PdfReader( st.session_state.file)
            st.session_state.cv = ""
            for page in pdf_reader.pages:
                st.session_state.cv += page.extract_text()
            st.caption("CV uploaded :white_check_mark:")
        else:
            st.caption("You can extract a CV from your LinkedIn account!")

        st.subheader(":page_with_curl: Copy / Paste the offer", divider="blue")
        st.text_area("Offer", "", height=300, placeholder="Paste the offer here", label_visibility="collapsed", key="offer")

        if st.form_submit_button("Confirm", use_container_width=True):
            st.rerun()

@st.cache_resource(show_spinner=False)
def get_tokenizer() -> None:
    # Get a tokenizer to ensure text length constraints for the model
    return AutoTokenizer.from_pretrained("huggyllama/llama-7b")

def get_num_tokens(prompt:str) -> int:
    # Get the number of tokens in a given prompt
    tokenizer = get_tokenizer()
    tokens = tokenizer.tokenize(prompt)
    return len(tokens)

def generate_cover_letter() -> None:
    # Generate the cover letter based on CV and job offer
    prompt = [
        "user\n",
        f"Here is my CV : {st.session_state.cv}. Write the cover letter for this offer : {st.session_state.offer}",
        "Create a compelling cover letter for a data scientist position, highlighting relevant experience, technical skills, and enthusiasm for the role, tailored to the specific company and job description. Use paragraphs.",
        "",
        "assistant",
        ""
    ]
    prompt_str = "\n".join(prompt)
    
    if get_num_tokens(prompt_str) >= 3072:
        st.error("Conversation length too long. Please keep it under 3072 tokens.")

    for event in replicate.stream(
        "snowflake/snowflake-arctic-instruct",
        input={
            "prompt": prompt_str,
            "prompt_template": r"{prompt}",
            "temperature": 0.3,
            "top_p": 0.9,
        }
    ):
        yield str(event)

def generate_links() -> None:
    # Generate key links between CV and job offer requirements
    prompt = [
        "user\n",
        f"Here is my CV : {st.session_state.cv}. Here is an offer : {st.session_state.offer}",
        "",
        "user\n",
        "Please write in markdown a formatted and indented 2-levels Numbered list. Each number describe a link between the offer's requirements and the CV",
        "Each number is the name of the link in bold (3-4 words) and has indented 2 sub-bullets: one that contains the exact extract that state the requirements and the other the exact extract from the CV that is relevant to that requirements.",
        """Example : 1. **Fine-Tuning an NLP Model**  
        * **Offer :** Develop and/or fine-tune language models and build downstream NLP capabilities for a variety of textual datasets to enable document summarization, entity extraction and relationship identification, and information retrieval.
        * **CV:** Integrated a finetuned flauBERT model that unlocked 50% more matches compared to the base model""",
        "assistant",
        ""
    ]
    prompt_str = "\n".join(prompt)
    
    if get_num_tokens(prompt_str) >= 3072:
        st.error("Conversation length too long. Please keep it under 3072 tokens.")

    for event in replicate.stream(
        "snowflake/snowflake-arctic-instruct",
        input={
            "prompt": prompt_str,
            "prompt_template": r"{prompt}",
            "temperature": 0.3,
            "top_p": 0.9,
        }
    ):
        yield str(event)

def stream_data_in_column(function: callable, container: DeltaGenerator, ctx: any) -> None:
    # Populate columns simultaneously with streamed data
    add_script_run_ctx(current_thread(), ctx)
    with container:
        st.write_stream(function)

def main() -> None:
    # Main function to setup the layout and start streaming data
    left_col, right_col = st.columns(2)

    keypoints_container = left_col.container(border=True)
    letter_container = right_col.container(border=True)

    letter_container.subheader(":envelope: Cover Letter Example", divider="blue")
    keypoints_container.subheader(":dart: Key points", divider="blue")
    
    parameters = zip([keypoints_container, letter_container], [generate_links, generate_cover_letter])
    with ThreadPoolExecutor(max_workers=2) as executor:
        ctx = get_script_run_ctx()
        futures = [
            executor.submit(functools.partial(stream_data_in_column, function, container, ctx)) for container, function in parameters
        ]

if __name__ == "__main__":
    initialization()
    sidebar()
    with st.sidebar:
        input_form()
    if st.session_state.file and len(st.session_state.offer) > 100:
        main()
    else:
        st.info("First upload your CV and paste the target job offer in the fields on the sidebar!")
