import streamlit as st
import openai

# Load OpenAI client
@st.cache_resource
def create_openai_client(apikey):
    return openai.Client(api_key=apikey)

@st.cache_data
def generate_text(input_text, num_words, temperature):
    
    client = create_openai_client(st.secrets["my_secrets"]["openai_key"])

    prompt = input_text
    #top_tokens_list = []
    response_list=[]
    generated_text = prompt

    for _ in range(num_words):
        
        response = client.completions.create(
            model="gpt-3.5-turbo-instruct",
            prompt=generated_text,
            max_tokens=1,
            temperature=temperature,
            logprobs=5,
        )
        token = response.choices[0].text.strip()
        generated_text += " " + token

        #logprobs = response.choices[0].logprobs.top_logprobs[0].items()
        #top_tokens = [token for token, prob in logprobs]
        #top_tokens_list.append(top_tokens)
        response_list.append(generated_text)

    return response_list


# Streamlit app
def main():
    
    #client = create_openai_client(st.secrets["my_secrets"]["openai_key"])

    st.title("Predicting the Next Word")
    st.subheader("Autoregression Demonstration")

    st.write("""
    This application demonstrates the autoregressive mechanism of a foundational LLM by predicting the next word(s) based on input text.
    """)
    st.write('Source code and ⭐ at [GitHub](https://github.com/jismartin/nextw)','  Author: jisantos')
    st.divider()

    # Number of words to predict
    num_words = st.slider("Number of words to predict:", 1, 20, 5)

    # Temperature setting
    temperature = st.slider("Model Temperature:", 0.0, 1.0, 0.7, 0.1)

    # Session state to hold the input text
    if "current_input" not in st.session_state:
        st.session_state.current_input = "The best thing of AI is its ability to"
    # Input text
    input_text = st.text_area("Enter your text below:", st.session_state.current_input) #"The best thing of AI is its ability to")

    if st.button("Generate Next Words"):
        if input_text.strip():
            with st.spinner("Generating..."):
                response_list = generate_text(input_text, num_words, temperature)
#            st.success("Generated Text:")
            for r in response_list:
                st.write(r)
        else:
            st.error("Please enter some input text to generate predictions.")


if __name__ == "__main__":
    main()
