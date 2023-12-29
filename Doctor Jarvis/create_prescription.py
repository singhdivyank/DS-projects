import os


class Prescription:
    def __init__(self, age: int, gender: str):
        self.age = age,
        self.gender = gender
        self.prescription_file = os.path.join(
            os.getcwd(), 
            os.getenv(key='FILE_NAME')
        )
        self.delete_file()
    
    def delete_file(self):
        """
        delete txt file
        """
        
        if os.path.exists(path=self.prescription_file):
            os.remove(path=self.prescription_file)
    
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
        if not os.path.exists(self.prescription_file):
            content = f"AGE: {self.age}\nGENDER: {self.gender}\n\n"
            with open(file=self.prescription_file, mode='w', encoding='utf8') as f:
                f.write(content)
                f.close()
        
        with open(file=self.prescription_file, mode='a', encoding='utf8') as f:
            f.write(dialog)
            f.close()
    