import os

from consts import PRESCRIPTION_NAME


class Prescription:
    def __init__(self, age: int, gender: str):
        self.age = age,
        self.gender = gender
        self.prescription_file = os.path.join(os.getcwd(), PRESCRIPTION_NAME)
        self.delete_file()
    
    def delete_file(self):
        """
        delete txt file
        """
        
        if os.path.exists(path=self.prescription_file):
            os.remove(path=self.prescription_file)
    
    def create_prescription(self, inital_msg: str, conversation: list, medication: str):
        """
        create a txt file summarizing patient's visit

        Params:
            initial_msg (str): message given by user at the start
            conversation (list): conversation between patient and doctor
            medication (str): medication prescribed by doctor
        """

        dialog = f"YOU: {inital_msg}\n"
        for _, conv in enumerate(conversation):
            # create the conversation
            dialog += f"JARVIS: {conv[0]}\nYOU: {conv[1]}\n"
        dialog += f"JARVIS: {medication}"

        # write to txt file
        if not os.path.exists(self.prescription_file):
            content = f"AGE: {self.age}\nGENDER: {self.gender}\n\n{dialog}"
            with open(file=self.prescription_file, mode='w', encoding='utf8') as f:
                f.write(content)
                f.close()
    