import warnings
import pickle

import gradio as gr

def diabetesApp(glucose: str, insulin: str, bmi: str, age: str) -> str:
    """
    make prediction using trained classifier model

    Params:
        glucose (str): numeric value for glucose received from UI
        insulin (str): numeric value for insulin received from UI
        bmi (str): numeric value for bmi received from UI
        age (str): numeric value for age received from UI
    
    Returns:
        prediction made by classifier model
    """

    classifier = pickle.load(file=open(file='classifier.pkl', mode='rb'))
    prediction = classifier.predict([[float(glucose), float(insulin), float(bmi), int(age)]])[0]
    return "Diabetic" if prediction else "Undiabetic"


if __name__ == '__main__':
    warnings.filterwarnings(action="ignore")

    ui = gr.Interface(
        fn=diabetesApp,
        inputs=[
            gr.Textbox(
                placeholder="please enter the value for Glucose",
                label="Glucose",
                show_label=True
            ),
            gr.Textbox(
                placeholder="please enter the value for Insulin",
                label="Insulin",
                show_label=True
            ),
            gr.Textbox(
                placeholder="please enter the value for BMI",
                label="BMI",
                show_label=True
            ),
            gr.Textbox(
                placeholder="please enter your age",
                label="Age",
                show_label=True
            )
        ],
        outputs="text"
    )
    ui.launch(
        server_name='127.0.0.1',
        server_port=8001,
        share=False
    )
