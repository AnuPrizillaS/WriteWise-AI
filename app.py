
import os
import time
import textwrap
import streamlit as st
from dotenv import load_dotenv
from google import genai
from google.genai import types


# ==========================================
# 1. PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="WriteWise AI",
    page_icon="✍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")


# ==========================================
# 2. CUSTOM CSS
# ==========================================

st.markdown("""
<style>

.stApp {
    background-color: #f7f8fc !important;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1250px;
}

.hero-title {
    font-size: 40px;
    font-weight: 800;
    color: #172554 !important;
    margin-bottom: 5px;
}

.hero-subtitle {
    font-size: 16px;
    color: #64748b !important;
    margin-bottom: 25px;
}

.section-heading {
    color: #172554 !important;
    font-size: 22px;
    font-weight: 750;
    margin-top: 12px;
    margin-bottom: 15px;
}

/* Sidebar */

[data-testid="stSidebar"] {
    background-color: #111827 !important;
}

[data-testid="stSidebar"] * {
    color: #f9fafb !important;
}

/* Feature cards */

.feature-card {
    background-color: #ffffff;
    padding: 20px;
    border-radius: 14px;
    border: 1px solid #e2e8f0;
    min-height: 130px;
}

.feature-icon {
    font-size: 27px;
}

.feature-name {
    color: #172554 !important;
    font-weight: 700;
    font-size: 16px;
    margin-top: 8px;
}

.feature-description {
    color: #64748b !important;
    font-size: 13px;
    margin-top: 5px;
}

/* Input area */

[data-testid="stTextArea"] textarea {
    background-color: #ffffff !important;
    color: #1f2937 !important;
    border: 1px solid #cbd5e1 !important;
    border-radius: 10px !important;
}

[data-testid="stTextArea"] textarea::placeholder {
    color: #94a3b8 !important;
}

/* Select boxes */

[data-testid="stSelectbox"] div[data-baseweb="select"] {
    background-color: #ffffff !important;
}

/* Buttons */

.stButton > button,
.stDownloadButton > button {
    border-radius: 9px !important;
    min-height: 44px;
    font-weight: 600;
}

/* Main text */

[data-testid="stMain"] {
    color: #1f2937 !important;
}

[data-testid="stMain"] [data-testid="stMarkdownContainer"],
[data-testid="stMain"] [data-testid="stMarkdownContainer"] p,
[data-testid="stMain"] [data-testid="stMarkdownContainer"] li,
[data-testid="stMain"] [data-testid="stMarkdownContainer"] h1,
[data-testid="stMain"] [data-testid="stMarkdownContainer"] h2,
[data-testid="stMain"] [data-testid="stMarkdownContainer"] h3,
[data-testid="stMain"] label,
[data-testid="stMain"] .stCaption {
    color: #1f2937 !important;
}

/* Generated result: black text on white */

.st-key-generated_output {
    background-color: #ffffff !important;
    color: #000000 !important;
    border: 1px solid #e2e8f0 !important;
    border-radius: 12px !important;
}

.st-key-generated_output,
.st-key-generated_output * {
    color: #000000 !important;
}

.st-key-generated_output h1,
.st-key-generated_output h2,
.st-key-generated_output h3,
.st-key-generated_output h4 {
    color: #000000 !important;
    font-weight: 700 !important;
}

/* Footer */

.footer {
    text-align: center;
    color: #64748b !important;
    font-size: 13px;
    padding-top: 20px;
}

</style>
""", unsafe_allow_html=True)


# ==========================================
# 3. GEMINI CLIENT
# ==========================================

if not API_KEY:
    st.error("Gemini API key not found. Please check your .env file.")
    st.stop()

client = genai.Client(api_key=API_KEY)


# ==========================================
# 4. SUPPORTED LANGUAGES
# ==========================================

LANGUAGES = [
    "English",
    "Tamil (தமிழ்)",
    "Hindi (हिन्दी)",
    "Telugu (తెలుగు)",
    "Kannada (ಕನ್ನಡ)",
    "Malayalam (മലയാളം)",
    "Bengali (বাংলা)",
    "Marathi (मराठी)",
    "Gujarati (ગુજરાતી)",
    "Punjabi (ਪੰਜਾਬੀ)",
    "Urdu (اردو)",
    "Odia (ଓଡ଼ିଆ)",
    "Assamese (অসমীয়া)",
    "Spanish (Español)",
    "French (Français)",
    "German (Deutsch)",
    "Portuguese (Português)",
    "Arabic (العربية)",
    "Chinese (中文)",
    "Japanese (日本語)",
    "Korean (한국어)",
    "Other / Specify in instructions"
]


# ==========================================
# 5. PROMPT TEMPLATES
# ==========================================

PROMPT_TEMPLATES = {

    "Social Media Post": """
Act as a creative social media content writer.

Create an engaging and attractive social media post.
Include suitable hashtags where appropriate.
Use an appropriate tone for the requested platform.

User request:
""",

    "Email Drafting": """
Act as a professional email writing assistant.

Write a polite, clear and professional email.
Include a suitable subject and email body.

User request:
""",

    "Blog Writing": """
Act as a professional blog writer.

Write an engaging, informative and beginner-friendly blog.
Include a suitable title, introduction, headings,
examples and conclusion.

User request:
""",

    "Code Explanation": """
Act as an experienced programming instructor.

Explain the given code in simple beginner-friendly language.
Explain its purpose, important lines, logic and output.
Include an example where useful.

User request:
""",

    "Song Lyrics": """
Act as a creative and professional songwriter.

Write completely ORIGINAL song lyrics based on the user's idea.

Structure the song with:
1. A suitable song title
2. Verse 1
3. Pre-Chorus (if appropriate)
4. Chorus
5. Verse 2
6. Bridge
7. Final Chorus

Pay attention to:
- The requested language
- Song genre and musical mood
- Emotional expression
- Meaningful and memorable lines
- Natural rhythm and lyrical flow
- A catchy chorus

Do not copy existing copyrighted song lyrics.
Do not imitate the distinctive style of a specific artist.

User request:
""",

    "Poem Writing": """
Act as a creative and professional poet.

Write a completely ORIGINAL poem based on the user's idea.

Include:
1. A meaningful poem title
2. Beautiful and expressive verses
3. Creative imagery and descriptions
4. Appropriate rhythm and flow
5. A memorable ending

Consider:
- The requested language
- The theme and emotions
- The requested poetic style
- The intended audience
- The requested length

Use meaningful words and original expressions.
Do not reproduce existing copyrighted poems.

User request:
"""
}


# ==========================================
# 6. FEATURE DETAILS
# ==========================================

FEATURE_DETAILS = {

    "Social Media Post": (
        "📱",
        "Create engaging posts for social media platforms."
    ),

    "Email Drafting": (
        "✉️",
        "Write clear and professional emails."
    ),

    "Blog Writing": (
        "📝",
        "Generate informative blogs with structured headings."
    ),

    "Code Explanation": (
        "💻",
        "Understand programming code with simple explanations."
    ),

    "Song Lyrics": (
        "🎵",
        "Create original song lyrics in different languages."
    ),

    "Poem Writing": (
        "📖",
        "Create beautiful and expressive original poems."
    )
}


# ==========================================
# 7. DISCOVER AVAILABLE GEMINI MODELS
# ==========================================

@st.cache_resource(ttl=300)
def get_available_models():

    models = []

    try:

        for model in client.models.list():

            name = getattr(model, "name", None)

            actions = (
                getattr(model, "supported_actions", []) or []
            )

            if name and "generateContent" in actions:
                models.append(name)

        models.sort(
            key=lambda name: (
                "flash" not in name.lower(),
                name
            )
        )

        return models

    except Exception:

        # Fallback used if model discovery fails.
        return ["gemini-3.8-flash"]


# ==========================================
# 8. GENERATE CONTENT
# ==========================================

def generate_content(prompt, temperature):

    available_models = get_available_models()

    if not available_models:

        raise Exception(
            "No text generation models were found for your API key."
        )

    errors = []

    for model_name in available_models:

        for attempt in range(2):

            try:

                response = client.models.generate_content(

                    model=model_name,

                    contents=prompt,

                    config=types.GenerateContentConfig(

                        temperature=temperature,

                        max_output_tokens=2048
                    )
                )

                if response and response.text:

                    return response.text, model_name

                errors.append(
                    f"{model_name}: No text was returned."
                )

                break

            except Exception as error:

                message = str(error)
                upper_message = message.upper()

                if (
                    "503" in upper_message
                    or "UNAVAILABLE" in upper_message
                ):

                    if attempt == 0:
                        time.sleep(3)
                        continue

                    errors.append(
                        f"{model_name}: Server temporarily unavailable."
                    )

                    break

                elif any(
                    code in upper_message
                    for code in ["400", "401", "403"]
                ):

                    raise Exception(
                        f"API request or permission error: {message}"
                    )

                elif "429" in upper_message:

                    errors.append(
                        f"{model_name}: API rate limit reached."
                    )

                    break

                else:

                    errors.append(
                        f"{model_name}: {message}"
                    )

                    break

    raise Exception(
        "All available models failed.\n\n"
        + "\n".join(errors)
    )


# ==========================================
# 9. SESSION STATE
# ==========================================

if "generated_text" not in st.session_state:
    st.session_state.generated_text = ""

if "selected_model" not in st.session_state:
    st.session_state.selected_model = ""

if "last_feature" not in st.session_state:
    st.session_state.last_feature = ""

if "user_input" not in st.session_state:
    st.session_state.user_input = ""


def clear_workspace():

    st.session_state.generated_text = ""
    st.session_state.selected_model = ""
    st.session_state.last_feature = ""
    st.session_state.user_input = ""


# ==========================================
# 10. SIDEBAR
# ==========================================

with st.sidebar:

    st.markdown("# ✍️ WriteWise AI")

    st.caption("YOUR SMART WRITING COMPANION")

    st.divider()

    st.markdown("### Navigation")

    feature = st.radio(

        "Choose a writing tool",

        list(PROMPT_TEMPLATES.keys()),

        format_func=lambda x:
            FEATURE_DETAILS[x][0] + "  " + x,

        label_visibility="collapsed"
    )

    st.divider()

    st.markdown("### About")

    st.write(
        "WriteWise AI helps you create professional "
        "content, write original lyrics and poems, "
        "and understand programming code using AI."
    )

    st.divider()

    st.caption("Powered by Google Gemini")

    st.caption("Built with Python and Streamlit")


# ==========================================
# 11. MAIN HEADER
# ==========================================

st.markdown(
    '<div class="hero-title">'
    'Create something amazing.'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="hero-subtitle">'
    'Your intelligent AI writing workspace. '
    'Write smarter, create faster and learn better.'
    '</div>',
    unsafe_allow_html=True
)

st.divider()


# ==========================================
# 12. FEATURE CARDS
# ==========================================

st.markdown(
    '<div class="section-heading">'
    'What would you like to create?'
    '</div>',
    unsafe_allow_html=True
)

feature_items = list(FEATURE_DETAILS.items())

# Three cards per row, six cards in total.

for start in range(0, len(feature_items), 3):

    columns = st.columns(3)

    for column, (name, details) in zip(
        columns,
        feature_items[start:start + 3]
    ):

        icon, description = details

        with column:

            selected_style = (
                "border: 2px solid #6366ff;"
                if feature == name
                else "border: 1px solid #e2e8f0;"
            )

            card_html = f"""
<div class="feature-card" style="{selected_style}">
    <div class="feature-icon">{icon}</div>
    <div class="feature-name">{name}</div>
    <div class="feature-description">{description}</div>
</div>
"""

            st.markdown(
                textwrap.dedent(card_html),
                unsafe_allow_html=True
            )

    st.write("")


# ==========================================
# 13. WRITING WORKSPACE
# ==========================================

left, right = st.columns(
    [1.15, 0.85],
    gap="large"
)


with left:

    st.markdown(
        '<div class="section-heading">'
        '✏️ Writing Workspace'
        '</div>',
        unsafe_allow_html=True
    )

    st.caption(f"Selected tool: {feature}")

    # Example prompts for each feature

    placeholders = {

        "Social Media Post":
        "Example: Write a LinkedIn post about completing a Python course...",

        "Email Drafting":
        "Example: Draft an email requesting an internship opportunity...",

        "Blog Writing":
        "Example: Write a blog about the future of Artificial Intelligence...",

        "Code Explanation":
        "Paste your Python, C++, Java or other programming code here...",

        "Song Lyrics":
        "Example: Write an emotional Tamil melody song about friendship...",

        "Poem Writing":
        "Example: Write a beautiful poem about nature, friendship and dreams..."
    }

    # Language selection for lyrics and poems

    selected_language = "English"

    if feature in ["Song Lyrics", "Poem Writing"]:

        st.markdown("#### 🌐 Choose Your Language")

        selected_language = st.selectbox(

            "Select the language for your creation",

            LANGUAGES,

            index=0,

            help=(
                "Your song lyrics or poem will be generated "
                "in the language you select."
            )
        )

    # User input

    user_input = st.text_area(

        "Enter your instructions or content",

        height=230,

        placeholder=placeholders[feature],

        key="user_input"
    )

    with st.expander("⚙️ Advanced Settings"):

        temperature = st.slider(

            "Creativity level",

            min_value=0.0,

            max_value=1.0,

            value=0.7,

            step=0.1
        )

        st.caption(
            "Lower values produce focused responses. "
            "Higher values allow more creative responses."
        )

    generate_button = st.button(

        "✨ Generate Content",

        type="primary",

        use_container_width=True
    )

    st.button(

        "Clear Workspace",

        use_container_width=True,

        on_click=clear_workspace
    )


# ==========================================
# 14. GENERATION LOGIC
# ==========================================

if generate_button:

    if not user_input.strip():

        st.warning(
            "Please enter your instructions first."
        )

    else:

        prompt = PROMPT_TEMPLATES[feature]

        # Add language instructions for lyrics and poems.

        if feature in ["Song Lyrics", "Poem Writing"]:

            if selected_language == "Other / Specify in instructions":

                language_instruction = """
                LANGUAGE REQUIREMENT:
                Use the language explicitly specified by the user
                in their instructions. If no language is specified,
                ask the user to specify one.
                Write naturally using the appropriate writing system.
                """

            else:

                language_instruction = f"""
                LANGUAGE REQUIREMENT:
                Write the entire {feature.lower()} in
                {selected_language}.

                Use the appropriate native writing script.
                Use natural vocabulary, grammar and expressions.
                Do not unnecessarily mix English with the selected language.
                Keep the meaning and emotions natural in that language.
                """

            prompt += "\n" + language_instruction

        prompt += "\nUSER'S REQUEST:\n" + user_input

        try:

            with st.spinner(
                "✨ WriteWise AI is creating your content..."
            ):

                generated_text, selected_model = generate_content(

                    prompt,

                    temperature
                )

            st.session_state.generated_text = generated_text

            st.session_state.selected_model = selected_model

            st.session_state.last_feature = feature

            st.toast(
                "Your content has been generated!"
            )

        except Exception as error:

            st.error(str(error))

            st.warning(
                "Please try again after a few minutes. "
                "Also check your Gemini API quota and model availability."
            )


# ==========================================
# 15. GENERATED OUTPUT
# ==========================================

with right:

    st.markdown(
        '<div class="section-heading">'
        '✨ Generated Result'
        '</div>',
        unsafe_allow_html=True
    )

    if st.session_state.generated_text:

        st.caption(
            f"Generated using: {st.session_state.last_feature}"
        )

        st.success(
            "Content generated successfully!"
        )

        # White background with black text.

        with st.container(
            border=True,
            key="generated_output"
        ):

            st.markdown(
                st.session_state.generated_text
            )

        st.write("")

        st.download_button(

            label="⬇️ Download Content",

            data=st.session_state.generated_text,

            file_name="writewise_generated_content.txt",

            mime="text/plain",

            use_container_width=True
        )

        if st.button(
            "🗑️ Remove Generated Result",
            use_container_width=True
        ):

            st.session_state.generated_text = ""
            st.session_state.selected_model = ""
            st.session_state.last_feature = ""

            st.rerun()

    else:

        with st.container(border=True):

            st.markdown(
                "### Your result will appear here"
            )

            st.write(
                "Select a writing tool, enter your instructions "
                "and click Generate Content."
            )

            st.write("")

            st.markdown("💡 **Tips for better results**")

            st.markdown("""
            - Be clear about your topic.
            - Mention your preferred tone.
            - Include important details.
            - Specify the expected output.
            """)


# ==========================================
# 16. FOOTER
# ==========================================

st.divider()

st.markdown(
    """
    <div class="footer">

        ✍️ WriteWise AI | Powered by Google Gemini

        <br>

        Your ideas, powered by Artificial Intelligence.

    </div>
    """,
    unsafe_allow_html=True
)
