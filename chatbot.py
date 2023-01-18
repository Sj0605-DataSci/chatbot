import openai
import streamlit as st
from streamlit_chat import message
from gtts import gTTS
from io import BytesIO
# import os
# from dotenv import load_dotenv
#
# # Load environment variables from a .env file in the same directory as this file
# load_dotenv()
#
# # Get the OpenAI API key
# openai_api_key = os.getenv("OPENAI_API_KEY")
#
# # Use the API key to authenticate with OpenAI
# openai.api_key = openai_api_key
openai.api_key = "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"

def generate_text(prompt):
    completions = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.7,
    )
    message = completions.choices[0].text
    return message

def text_to_speech(text):
    tts = gTTS(text)
    f = BytesIO()
    tts.write_to_fp(f)
    f.seek(0)
    return f.read()

st.title("Chatbot using Open AI")

#
# def set_bg_hack_url():
#
#     st.markdown(
#         f"""
#          <style>
#          .stApp {{
#              background: url("https://png.pngtree.com/background/20210714/original/pngtree-template-for-science-and-technology-presentation-connected-cells-with-links-picture-image_1250440.jpg");
#              background-size: cover
#          }}
#          </style>
#          """,
#         unsafe_allow_html=True
#     )
#
# set_bg_hack_url()
#
# theme_options = ["default", "dark"]
# theme_select = st.selectbox("Select the theme", theme_options)
# if theme_select == "dark":
#     st.markdown("""
#         <style>
#             body {
#                 background-color: #2c3e50;
#                 color: white;
#             }
#             .title {
#                 color: white;
#                 text-align: center;
#                 padding-top: 20px;
#             }
#             .input {
#                 width: 60%;
#                 margin-left: 20%;
#                 margin-right: 20%;
#                 padding: 12px 20px;
#                 margin: 8px 0;
#                 box-sizing: border-box;
#                 border: 2px solid #ccc;
#                 border-radius: 4px;
#             }
#             .output {
#                 background-color: rgba(255, 255, 255, 0.7);
#                 border-radius: 10px;
#                 padding: 20px;
#                 margin-left: 20%;
#                 margin-right: 20%;
#                 margin-top: 20px;
#             }
#             audio {
#                 display: block;
#                 margin: auto;
#                 margin-left: 20%;
#                 margin-right: 20%;
#             }
#         </style>
#     """, unsafe_allow_html=True)

if 'generated' not in st.session_state:
    st.session_state['generated'] = []
if 'past' not in st.session_state:
    st.session_state['past'] = []

def get_text():
    input_text = st.text_input("You:","Hello How are you?",key="input")
    return input_text

user_input = get_text()

if user_input:
    output = generate_text(user_input)
    st.session_state.past.append(user_input)
    st.session_state.generated.append(output)
    audio_bytes = text_to_speech(output)
    audio_element = st.audio(audio_bytes, format='audio/mp3')

if st.session_state['generated']:

    for i in range(len(st.session_state['generated'])-1,-1,-1):
        message(st.session_state['generated'][i],key=str(i))
        message(st.session_state['past'][i],is_user=True ,key=str(i)+'_user')
