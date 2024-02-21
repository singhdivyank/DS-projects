import warnings
import pickle

import gradio as gr

def diabetesApp(glucose: float, insulin: float, bmi: float, age: int) -> str:
    """
    make prediction using trained classifier model

    Params:
        glucose (float): numeric value for glucose
        insulin (float): numeric value for insulin
        bmi (float): numeric value for bmi
        age (int): numeric value for age
    
    Returns:
        prediction made by classifier model
    """

    classifier = pickle.load(file=open(file='classifier.pkl', mode='rb'))
    prediction = classifier.predict([[glucose, insulin, bmi, age]])[0]
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
        server_port=8000,
        share=False
    )
