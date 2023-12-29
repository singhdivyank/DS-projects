import os

import gradio as gr

from dotenv import (
    load_dotenv, 
    find_dotenv
)
from typing import List

from create_prescription import Prescription
from speechOps import (
    Transcribe, 
    ToAudio
)
from perform_translation import Translate
from diagnosis import perform_diagnosis

load_dotenv(dotenv_path=find_dotenv())

# define all supported language codes
LANGUAGES = {
    "english": "en",
    "bengali": "bn",
    "gujrati": "gu",
    "hindi": "hi",
    "kannada": "kn",
    "malayalam": "ml",
    "marathi": "mr",
    "tamil": "ta",
    "telugu": "te",
    "urdu": "ur"
}

def main(language: str, gender: List, age: str):
    """
    user profile/dashboard
    """
    
    # get language code
    lan_code = LANGUAGES.get(language, 'en')
    print(lan_code)

    # create class objects
    translate_ob = Translate(lan_code=lan_code)
    audio_ob = ToAudio(language=lan_code)
    prescription_ob = Prescription(
        age=age,
        gender=gender[0] if gender[0] in ["Male", "Female"] else "Others"
    )
    transcribe_ob = Transcribe(language=lan_code)
    
    # get all static messages
    all_msgs = translate_ob.get_msgs()

    # send introduction message to user
    audio_ob.text_to_speech(txt_msg=all_msgs[0])
    # send instruction message to user
    audio_ob.text_to_speech(txt_msg=all_msgs[1])

    # get user message
    user_text = transcribe_ob.get_text()
    if user_text == "NO INTERNET CONNECTION":
        return "please connect to the internet"
    # translate to English for LLM model
    for_doc = translate_ob.translation(
        for_usr=user_text, 
        llm_flag=True
    ) if not lan_code == 'en' else user_text

    # call LLM and find medication
    doc_notes = perform_diagnosis(usr_msg=for_doc)
    print("doc notes:: ", doc_notes)
    # translate results to user language
    doc_notes = translate_ob.translation(
        for_usr=doc_notes, 
        llm_flag=False
    ) if not lan_code == 'en' else doc_notes
    # generate audio message
    audio_ob.text_to_speech(txt_msg=doc_notes)
    
    # create prescription
    prescription_ob.create_prescription(
        patient_notes=user_text, 
        doc_notes=doc_notes
    )
    print("created prescription...")
    return prescription_ob.prescription_file


if __name__ == '__main__':

    ui=gr.Interface(
        fn=main,
        inputs=[
            gr.Dropdown(
                choices=list(LANGUAGES.keys()),
                multiselect=False,
                label="language selection",
                show_label=True,
                interactive=True
            ),
            gr.CheckboxGroup(
                choices=["Male", "Female", "Prefer not to disclose"],
                label="gender selection",
                show_label=True,
                interactive=True,
            ),
            gr.Slider(
                minimum=10,
                maximum=50,
                step=2,
                label="age selection",
                show_label=True,
                interactive=True
            )
        ],
        outputs=["text"]
    )
    # launch the UI
    ui.launch(
        server_name=os.getenv(key='GRADIO_SERVER_NAME'), 
        server_port=int(os.getenv(key='GRADIO_SERVER_PORT')), 
        share=False
    )
