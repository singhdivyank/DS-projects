import os

from dotenv import load_dotenv

from ui import create_dashboard

load_dotenv()

if __name__ == '__main__':
    create_dashboard(server=os.getenv("GRADIO_SERVER_NAME"), 
                     port=int(os.getenv("GRADIO_SERVER_PORT"))
                     )
