import os


class Prescription:
    def __init__(self, age: str, gender: str):
        self.age = age,
        self.gender = gender
        self.prescription_name = f"{os.path.join(os.getcwd(), os.getenv('FILE_NAME'))}.txt"
    
    def create_prescription(self, patient_notes: str, doc_notes: str):
        """
        write the conversation as a txt file

        Params:
            patient_notes (str): text from patient
            doc_notes (str): text from doctor
        """

        # create the conversation
        dialog = f"YOU: {patient_notes}\nJARVIS: {doc_notes}\n\n"

        # write the initial lines
        if not os.path.exists(self.prescription_name):
            content = f"AGE: {self.age}\nGENDER: {self.gender}\n\n"
            with open(file=self.prescription_name, mode='w') as f:
                f.write(content)
                f.close()
        
        with open(file=self.prescription_name, mode='a') as f:
            f.write(dialog)
            f.close()
    