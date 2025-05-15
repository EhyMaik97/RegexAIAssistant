import streamlit as st
from chains import Chain


def create_streamlit_app(llm):
    """
    Create a Streamlit app that allows the user to input a sample text and a value, and then generate a regex pattern that matches the value exactly.
    """
    st.title("🤖 Regex AI Assistant")
    st.markdown("Enter a sample text and a value you want to extract. The AI will generate a regex that matches the value exactly.")
    
    if 'string_input' not in st.session_state:
        st.session_state.string_input = ""
    if 'value_input' not in st.session_state:
        st.session_state.value_input = ""

    string_input = st.text_area("Enter the sample text:", value=st.session_state.string_input, height=150)
    value_input = st.text_input("Enter the value you want to retrieve:", value=st.session_state.value_input)
    submit_button = st.button("🔍 Generate Regex")

    st.session_state.string_input = string_input
    st.session_state.value_input = value_input

    if submit_button and string_input and value_input:
        try:
            regex_pattern = llm.write_regex(string_input, value_input)
            
            # Show the generated regex
            st.subheader("✅ Generated Regex:")
            st.code(regex_pattern, language="regex")
            
        except Exception as e:
            st.error(f"An Error Occurred: {e}")


if __name__ == "__main__":
    st.set_page_config(layout="wide", page_title="Regex AI Assistant", page_icon="🤖")
    chain = Chain()
    create_streamlit_app(chain)
