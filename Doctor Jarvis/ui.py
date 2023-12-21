import gradio as gr

from googletrans import Translator

from typing import List

from create_prescription import Prescription
from speechOps import (
    Transcribe, 
    Translate
)

# introduction message
MAIN_MSG = "send message from microphone. To stop, say 'thank you'"
# define all supported language codes
LANGUAGES = {
    "bengali": "bn",
    "bhojpuri": "bh",
    "english": "en",
    "gujrati": "gu",
    "hindi": "hi",
    "kannada": "kn",
    "malayalam": "ml",
    "marathi": "mr",
    "punjabi": "pa",
    "sindhi": "sd",
    "tamil": "ta",
    "telugu": "te",
    "urdu": "ur"
}

def translation(for_usr: str, lan_code: str) -> str:
    """
    translate from one language to another using
    Google Translate
    
    Params:
        for_usr (str): input text
        lan_code (str): desired language
    
    Returns:
        translation (str): translated text
    """

    translation = Translator.translate(for_usr, dest=lan_code)
    return translation

def run_diagnosis():
    return "Hello"

def call_doctor(user_profile: List) -> str:
    """
    using the voice assistant for diagnosis

    Params:
        user_profile (List): user details
    
    Returns:
        str: prescription file path
    """
    
    language = user_profile[0]
    lan_code = LANGUAGES.get(language)
    print(lan_code)
    # send message to user
    message = translation(for_usr=MAIN_MSG, lan_code=lan_code) if not lan_code == 'en' else MAIN_MSG
    gr.Textbox(value=message, lines=1, 
               label='welcome message', show_label=True
               )
    # get user message
    user_text = Transcribe(language=lan_code).get_text()
    print(user_text)
    # get translated message
    user_text = translation(for_usr=user_text, lan_code='en') if not lan_code == 'en' else user_text
    # iterative process
    while not user_text.lower() == 'thank you':
        # render user message
        gr.Textbox(value=user_text, 
                   lines=5, 
                   label='user message', 
                   show_label=True
                   )
        # TODO- LangChain implementation
        doc_notes = run_diagnosis()
        # get translated diagnosis results
        doc_notes = translation(for_usr=doc_notes, lan_code=lan_code) if not lan_code == 'en' else doc_notes
        # generate audio
        Translate(
            txt_msg=doc_notes,
            language=lan_code
        ).text_to_speech()
        # render diagnosis results
        gr.Textbox(value=doc_notes, 
                   lines=10, 
                   label='doctor message', 
                   show_label=True
                   )
        # create prescription
        prescription_ob = Prescription(patient_notes=user_text, 
                                       doc_notes=doc_notes,
                                       age=user_profile[-1],
                                       gender=user_profile[1]
                                       )
    # TODO- render the file
    return prescription_ob.prescription_name

def create_dashboard(server: str, port: int):
    """
    user profile/dashboard

    Params:
        server (str): server for inteface
        port (int): dedicated server port
    """

    inputs = [
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
    ]

    # create gradio UI
    ui = gr.Interface(
        fn=call_doctor,
        inputs=inputs,
        outputs=gr.Textbox(lines=1, 
                           label="prescription file",
                           show_label=True
                           )
    )
    ui.launch(server_name=server, server_port=port)
