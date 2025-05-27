import streamlit as st
import asyncio
from dotenv import load_dotenv
import os
gemini_api_key = os.getenv("GEMINI_API_KEY")
import streamlit as st
gemini_api_key = st.secrets["GEMINI_API_KEY"]


from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, RunConfig


load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")

if not gemini_api_key:
    st.error(" GEMINI_API_KEY is not set in your .env file.")
    st.stop()


external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

# Model setup
model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client
)

config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True
)

# Translator agent definition
translator_agent = Agent(
    name="Translator Agent",
    instructions="""
        You are a translation expert. You translate text from one language to another.
        Support translation between Urdu, English, Hindi, Arabic, and French.
        Just return the translated version without explanation.
    """
)


async def translate_text(input_text):
    return await Runner.run(
        translator_agent,
        input=input_text,
        run_config=config
    )


st.set_page_config(page_title="AI Translator", page_icon="🌍")

st.title("🌍 AI Translator")
st.markdown("Translate text between Urdu, English, Hindi, Arabic, and French using Gemini AI.")

# Input area
input_text = st.text_area("✍️ Enter your text to translate:", height=150)

if st.button("Translate"):
    if not input_text.strip():
        st.warning("⚠️ Please enter some text first.")
    else:
        with st.spinner("🔄 Translating..."):
            try:
                result = asyncio.run(translate_text(input_text))
                st.success("✅ Translation complete!")
                st.markdown("### 📝 Translated Text")
                st.code(result.final_output.strip(), language="text")
            except Exception as e:
                st.error(f"❌ An error occurred:\n\n{e}")


