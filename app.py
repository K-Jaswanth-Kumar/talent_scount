import streamlit as st
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import warnings
import re

# -------------------------------
# Suppress Specific Warnings
# -------------------------------
warnings.filterwarnings("ignore", category=UserWarning, module='torch')
warnings.filterwarnings("ignore", category=UserWarning, module='transformers')

# -------------------------------
# Set Page Configuration
# -------------------------------
st.set_page_config(
    page_title="TalentScout Hiring Assistant",
    page_icon="💼",
    layout="centered",
    initial_sidebar_state="expanded",
)

# -------------------------------
# Helper Functions
# -------------------------------

def is_valid_email(email):
    """
    Validates the email format using regex.
    """
    regex = r'^\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    return re.match(regex, email)

def is_valid_phone(phone):
    """
    Validates the phone number format using regex.
    """
    regex = r'^\+?\d{10,15}$'
    return re.match(regex, phone)

def is_conversation_end(user_input):
    """
    Check if the user input contains a conversation-ending keyword.
    """
    end_keywords = ["bye", "exit", "quit", "thank you", "thanks"]
    return any(keyword in user_input.lower() for keyword in end_keywords)

# -------------------------------
# Model Loading and Initialization
# -------------------------------

@st.cache_resource
def load_model():
    """
    Load the GPT-2 Medium tokenizer and model.
    Cached to prevent reloading on every interaction.
    """
    tokenizer = AutoTokenizer.from_pretrained("gpt2-medium")
    
    # Assign eos_token as pad_token
    tokenizer.pad_token = tokenizer.eos_token
    
    model = AutoModelForCausalLM.from_pretrained(
        "gpt2-medium",
        device_map="auto",  # Automatically maps model to available device (GPU)
        torch_dtype=torch.float32,
        pad_token_id=tokenizer.eos_token_id  # Set pad_token_id
    )
    return tokenizer, model

tokenizer, model = load_model()


# -------------------------------
# Session State Initialization
# -------------------------------

if 'messages' not in st.session_state:
    st.session_state['messages'] = [
        {"role": "system", "content": "You are TalentScout's Hiring Assistant. Your task is to gather candidate information and ask relevant technical questions based on their tech stack."}
    ]
    st.session_state['stage'] = 'greeting'
    st.session_state['candidate_info'] = {}

# -------------------------------
# Helper Functions
# -------------------------------

def generate_response(conversation):
    """
    Generate a response from the model based on the conversation history.
    """
    prompt = ""
    for msg in conversation:
        if msg['role'] == 'system':
            continue  # Skip system messages in prompt
        elif msg['role'] == 'user':
            prompt += f"Candidate: {msg['content']}\n"
        else:
            prompt += f"Assistant: {msg['content']}\n"
    prompt += "Assistant:"

    inputs = tokenizer.encode(prompt, return_tensors='pt').to(model.device)
    attention_mask = torch.ones_like(inputs).to(model.device)

    with torch.no_grad():
        outputs = model.generate(
            inputs,
            attention_mask=attention_mask,  # Pass attention_mask explicitly
            max_length=inputs.shape[1] + 150,  # Limit response length
            temperature=0.7,
            top_p=0.9,
            do_sample=True,
            eos_token_id=tokenizer.eos_token_id,
            pad_token_id=tokenizer.pad_token_id
        )
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    response = response[len(prompt):].strip()

    # Fallback if response is empty
    if not response:
        response = "I'm sorry, I didn't understand that. Could you please rephrase?"

    return response

def generate_technical_questions(tech_stack):
    """
    Generate technical questions based on the candidate's tech stack using the language model.
    """
    prompt = (
        f"Based on the following tech stack: {tech_stack}\n"
        "Generate 3-5 technical interview questions to assess the candidate's proficiency in each listed technology.\n\n"
        "Examples:\n"
        "Technology: Python\n"
        "1. How would you handle exceptions in Python?\n"
        "2. Explain the difference between a list and a dictionary in Python.\n"
        "3. What is a decorator in Python and how is it used?\n\n"
    )

    # Prepend system message to guide the model
    conversation = [
        {"role": "system", "content": "You are an expert interviewer. Generate diverse and relevant technical questions based on the candidate's tech stack."},
        {"role": "user", "content": prompt}
    ]

    response = generate_response(conversation)
    return response

# -------------------------------
# Streamlit User Interface
# -------------------------------

st.title("💼 TalentScout Hiring Assistant")

# -------------------------------
# Process User Input
# -------------------------------
with st.form(key='input_form', clear_on_submit=True):
    user_input = st.text_input("You:", placeholder="Type your message here...")
    submit_button = st.form_submit_button(label='Send')

if submit_button and user_input:
    st.session_state['messages'].append({"role": "user", "content": user_input})

    # Check for conversation-ending keywords
    if is_conversation_end(user_input):
        end_message = "Thank you for your time. We will contact you about the next steps."
        st.session_state['messages'].append({"role": "assistant", "content": end_message})
    else:
        stage = st.session_state['stage']

        if stage == 'greeting':
            st.session_state['stage'] = 'name'
            bot_reply = "Hello! I'm TalentScout's Hiring Assistant. I'll ask you a few questions to understand your background and skills. Let's get started! What is your full name?"
            st.session_state['messages'].append({"role": "assistant", "content": bot_reply})

        elif stage == 'name':
            name = user_input
            st.session_state['candidate_info']['Full Name'] = name
            st.session_state['stage'] = 'email'
            bot_reply = f"Nice to meet you, {name}! Could you please provide your email address?"
            st.session_state['messages'].append({"role": "assistant", "content": bot_reply})

        elif stage == 'email':
            email = user_input
            if is_valid_email(email):
                st.session_state['candidate_info']['Email Address'] = email
                st.session_state['stage'] = 'phone'
                bot_reply = "Thank you! What's your phone number?"
            else:
                bot_reply = "The email address you entered seems invalid. Please enter a valid email address."
            st.session_state['messages'].append({"role": "assistant", "content": bot_reply})

        elif stage == 'phone':
            phone = user_input
            if is_valid_phone(phone):
                st.session_state['candidate_info']['Phone Number'] = phone
                st.session_state['stage'] = 'experience'
                bot_reply = "How many years of experience do you have in the tech industry?"
            else:
                bot_reply = "The phone number you entered seems invalid. Please enter a valid phone number."
            st.session_state['messages'].append({"role": "assistant", "content": bot_reply})

        elif stage == 'experience':
            experience = user_input
            st.session_state['candidate_info']['Years of Experience'] = experience
            st.session_state['stage'] = 'position'
            bot_reply = "What position(s) are you interested in?"
            st.session_state['messages'].append({"role": "assistant", "content": bot_reply})

        elif stage == 'position':
            position = user_input
            st.session_state['candidate_info']['Desired Position'] = position
            st.session_state['stage'] = 'location'
            bot_reply = "Where are you currently located?"
            st.session_state['messages'].append({"role": "assistant", "content": bot_reply})

        elif stage == 'location':
            location = user_input
            st.session_state['candidate_info']['Current Location'] = location
            st.session_state['stage'] = 'tech_stack'
            bot_reply = "Please specify your tech stack, including programming languages, frameworks, databases, and tools you are proficient in."
            st.session_state['messages'].append({"role": "assistant", "content": bot_reply})

        elif stage == 'tech_stack':
            tech_stack = user_input
            st.session_state['candidate_info']['Tech Stack'] = tech_stack
            st.session_state['stage'] = 'questions'

            # Generate technical questions with a loading spinner
            with st.spinner("Generating technical questions..."):
                questions = generate_technical_questions(tech_stack)
            st.session_state['messages'].append({"role": "assistant", "content": questions})

        elif stage == 'questions':
            # After technical questions, conclude the conversation
            st.session_state['stage'] = 'end'
            end_message = "Thank you for providing your information and answering the technical questions. We will review your application and get back to you soon."
            st.session_state['messages'].append({"role": "assistant", "content": end_message})

        else:
            # Fallback using the language model with a loading spinner
            with st.spinner("Generating response..."):
                bot_reply = generate_response(st.session_state['messages'])
            st.session_state['messages'].append({"role": "assistant", "content": bot_reply})

# -------------------------------
# Display Chat History
# -------------------------------
st.markdown("### Chat History")
for msg in st.session_state['messages']:
    if msg['role'] == 'user':
        st.markdown(f"**You:** {msg['content']}")
    elif msg['role'] == 'assistant':
        st.markdown(f"**Bot:** {msg['content']}")
    # Skip system messages
