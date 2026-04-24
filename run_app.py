import os
import sys

if __name__ == "__main__":
    print("Launching Touchless Control Web App...")
    # Add virtual_mouse to Python path if necessary
    sys.path.append(os.path.join(os.path.dirname(__file__), 'virtual_mouse'))
    
    # Run the streamlit application
    os.system("streamlit run virtual_mouse/streamlit_app.py")
