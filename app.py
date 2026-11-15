import streamlit as st
import requests

# Page configuration
st.set_page_config(
    page_title="AI Language Translator",
    page_icon="🌍",
    layout="centered"
)

# Initialize translation history
if "history" not in st.session_state:
    st.session_state.history = []

# Application title
st.title("🌍 AI Language Translation Tool")
st.write("Break language barriers with easy translation.")

st.divider()

# Supported languages
languages = {
    "English": "en",
    "Telugu": "te",
    "Hindi": "hi",
    "Tamil": "ta",
    "Kannada": "kn",
    "Malayalam": "ml",
    "Bengali": "bn",
    "French": "fr",
    "Spanish": "es",
    "German": "de",
    "Japanese": "ja",
    "Chinese": "zh",
    "Arabic": "ar",
    "Korean": "ko"
}

# Language selection
col1, col2 = st.columns(2)

with col1:
    source_language = st.selectbox(
        "From Language",
        list(languages.keys())
    )

with col2:
    target_language = st.selectbox(
        "To Language",
        list(languages.keys()),
        index=1
    )

# Input text
input_text = st.text_area(
    "Enter text to translate:",
    height=150,
    placeholder="Type your text here..."
)

# Translation function
def translate_text(text, source, target):

    url = "https://api.mymemory.translated.net/get"

    params = {
        "q": text,
        "langpair": f"{source}|{target}"
    }

    response = requests.get(
        url,
        params=params,
        timeout=20
    )

    response.raise_for_status()

    data = response.json()

    if data.get("responseStatus") != 200:
        raise ValueError(
            data.get("responseDetails", "Translation unavailable.")
        )

    return data["responseData"]["translatedText"]


# Translation button
if st.button("Translate", type="primary", use_container_width=True):

    if not input_text.strip():
        st.warning("Please enter some text to translate.")

    elif source_language == target_language:
        st.warning("Please select two different languages.")

    else:
        try:
            result = translate_text(
                input_text,
                languages[source_language],
                languages[target_language]
            )

            st.success("Translation completed!")

            st.subheader("Translated Text")

            st.code(result)

            # Save successful translation to history
            st.session_state.history.append({
                "source": source_language,
                "target": target_language,
                "input": input_text,
                "output": result
            })

        except requests.exceptions.RequestException:
            st.error(
                "Network error. Please check your internet connection and try again."
            )

        except (ValueError, KeyError) as error:
            st.error(f"Translation failed: {error}")

        except Exception as error:
            st.error(f"An unexpected error occurred: {error}")


# Translation History
st.divider()

st.subheader("📚 Translation History")

if st.session_state.history:

    for item in reversed(st.session_state.history):

        with st.expander(
            f"{item['source']} ➜ {item['target']}"
        ):
            st.write("**Original Text:**")
            st.write(item["input"])

            st.write("**Translated Text:**")
            st.write(item["output"])

    if st.button("Clear History"):
        st.session_state.history = []
        st.rerun()

else:
    st.info("No translation history available yet.")

# Footer
st.divider()

st.caption("Developed as part of a CodeAlpha AI Internship.")