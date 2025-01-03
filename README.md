💼 TalentScout Hiring Assistant
===============================

**TalentScout Hiring Assistant** is an interactive Streamlit application designed to streamline the hiring process by collecting candidate information and generating tailored technical interview questions based on their tech stack using the GPT-2 Medium language model.

🚀 Features
-----------

-   **Interactive Chat Interface:** Engage with candidates through a user-friendly conversational UI.
-   **Automated Information Gathering:** Collect essential details such as name, email, phone number, experience, desired position, location, and tech stack.
-   **Dynamic Technical Question Generation:** Generate customized interview questions based on the candidate's specified technologies.
-   **Input Validation:** Ensure data integrity with email and phone number validations.
-   **Session Management:** Maintain conversation state across interactions for a seamless user experience.

🛠️ Installation
----------------

### 1\. Clone the Repository

```
git clone https://github.com/yourusername/talentscout-hiring-assistant.git
cd talentscout-hiring-assistant

```

### 2\. Create a Virtual Environment

It's recommended to use a virtual environment to manage dependencies.

```
python3 -m venv venv

```

Activate the virtual environment:

-   **On Windows:**

    ```
    venv\Scripts\activate

    ```

-   **On macOS and Linux:**

    ```
    source venv/bin/activate

    ```

### 3\. Install Dependencies

Install the required packages:

```
pip install -r requirements.txt

```

### 4\. Run the Application

```
streamlit run app.py

```


📋 Usage
--------

1.  **Start the Application:** Launch the app using the command above. It will open in your default web browser.
2.  **Interact with the Assistant:** Follow the prompts to provide your information.
3.  **Receive Technical Questions:** After submitting your tech stack, the assistant will generate relevant interview questions.
4.  **Conclude the Session:** End the conversation gracefully by typing keywords like "bye", "exit", or "thanks".

📂 Project Structure
--------------------

```
talentscout-hiring-assistant/
├── app.py
├── requirements.txt
└── README.md 

```

-   **`app.py`**: Main application script.
-   **`requirements.txt`**: Lists all Python dependencies.
-   **`README.md`**: Project documentation.
-   **`.gitignore`**: Specifies files and directories to ignore in Git.
-   **`assets/`**: Contains images and other static assets.

📄 Requirements
---------------

Ensure you have the following packages installed (as listed in `requirements.txt`):

```
streamlit==1.25.0
transformers==4.30.0
torch==2.0.0

```
