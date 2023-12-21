import os


class Prescription:
    def __init__(self, patient_notes: str, doc_notes: str, age: str, gender: str):
        self.patient_str = patient_notes
        self.doc_str = doc_notes
        self.patient_details = {
            "age": age,
            "gender": gender
        }
        self.prescription_name = f"{os.path.join(os.getcwd(), os.getenv('FILE_NAME'))}.txt"
        self.create_prescription()
    
    def create_prescription(self):
        """
        write the conversation as a txt file
        """

        dialog = f"YOU: {self.patient_str}\nJARVIS: {self.doc_str}\n\n"

        # write the initial lines
        if not os.path.exists(self.prescription_name):
            content = f"AGE: {self.patient_details.get('age')}\nGENDER: \
                {self.patient_details.get('gender')}\n\n"
            with open(file=self.prescription_name, mode='w') as f:
                f.write(content)
                f.close()
        
        with open(file=self.prescription_name, mode='a') as f:
            f.write(dialog)
            f.close()
    