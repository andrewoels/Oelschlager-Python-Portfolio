import spacy
from spacy.cli import download

try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

import streamlit as st
from spacy import displacy
import random

st.set_page_config(page_title="Custom NER App", layout="wide")
st.title("🧠 Custom Named Entity Recognition (NER)")

st.markdown("""
### **Welcome to the Custom Named Entity Recognition (NER) App!**
This app lets you explore and customize Named Entity Recognition (NER) by adding your own labels and patterns to text. You can input or upload your own text and define custom entity labels (like "Brand", "Sport", "Product") alongside spaCy’s existing labels such as "PERSON", "ORG", or "GPE". The app will then highlight both the entities you define and those recognized by spaCy’s built-in model, allowing you to see how your custom labels interact with the pre-existing ones. Whether you’re analyzing a document or experimenting with different patterns, this app helps you customize and expand the power of NER to fit your unique needs.
""")

# Load spaCy's built-in English model
#nlp = spacy.load("en_core_web_sm")

# Initialize session state for dynamic entity labels
if "label_count" not in st.session_state:
    st.session_state.label_count = 2  # Start with 2 sets

st.sidebar.header("Step 1: Input Text")
input_method = st.sidebar.radio("Choose how to enter text:", ["Type text", "Upload .txt file"])

sample_texts = {
    "— Choose a sample —": "",
    "Tech Brands": "Apple and Microsoft released their quarterly earnings while OpenAI announced a new model.",
    "Athletes": "LeBron James (Los Angeles Lakers) and Lionel Messi (Inter Miami) are among the highest-paid athletes in the world.",
    "Products & Retail": "Customers love shopping at Target for brands like Nike, Xbox, and Samsung."
}

user_text = ""

if input_method == "Type text":
    st.markdown("**Or choose a sample to auto-fill:**")
    sample_choice = st.selectbox("Sample Texts", list(sample_texts.keys()), index=0)
    
    if sample_texts[sample_choice]:
        user_text = sample_texts[sample_choice]
    
    # Allow user to edit or enter text after autofill
    user_text = st.text_area("Enter your text below:", value=user_text, height=200)
else:
    uploaded_file = st.file_uploader("Upload a .txt file", type=["txt"])
    if uploaded_file:
        user_text = uploaded_file.read().decode("utf-8")
    else:
        user_text = ""

st.sidebar.header("Step 2: Define Custom Entities")

with st.sidebar.form(key="entity_form"):
    label_inputs = []
    for i in range(st.session_state.label_count):
        label = st.text_input(f"Label {i+1}", key=f"label_{i}", 
                             placeholder=f"Example: TEAM")
        phrases = st.text_area(f"Phrases for Label {i+1} (one per line)", key=f"phrases_{i}",
                               placeholder="Example:\nLos Angeles Lakers\nChicago Blackhawks\nDenver Broncos")
        label_inputs.append((label, phrases))

    add_more = st.form_submit_button("➕ Add Another Entity")
    submitted = st.form_submit_button("✅ Apply Entity Rules")

if add_more:
    st.session_state.label_count += 1
    st.experimental_rerun()

if submitted and user_text:
    if "entity_ruler" in nlp.pipe_names:
        nlp.remove_pipe("entity_ruler")

    ruler = nlp.add_pipe("entity_ruler", before="ner")

    def build_patterns(label, phrases):
        return [{"label": label.upper(), "pattern": phrase.strip()}
                for phrase in phrases.splitlines() if phrase.strip()]

    patterns = []
    for label, phrases in label_inputs:
        if label and phrases:
            patterns += build_patterns(label, phrases)

    ruler.add_patterns(patterns)
    doc = nlp(user_text)

    # Generate a unique color for each custom label
    label_colors = {label: f"rgb({random.randint(50, 255)}, {random.randint(50, 255)}, {random.randint(50, 255)})"
                    for label, _ in label_inputs}

    # Create a color mapping for the entity labels
    def custom_render_ents(doc):
        rendered = displacy.render(doc, style="ent", page=False)
        for label, color in label_colors.items():
            # Replace the label in the rendered HTML with a span tag containing the color
            rendered = rendered.replace(f'entity-{label.upper()}',
                                        f'span class="entity-{label.upper()}" style="color: {color};"')
        return rendered

    st.subheader("🔍 Highlighted Entities")
    html = custom_render_ents(doc)
    st.markdown(html, unsafe_allow_html=True)

    st.subheader("📋 Extracted Entities")
    if doc.ents:
        #explanation = spacy.explain(ent) or "No explanation available"
        st.table([{"Text": ent.text, "Label": ent.label_, "Explanation": spacy.explain(ent.label_) or "Custom entry. No explanation available"} for ent in doc.ents])
    else:
        st.info("No entities detected with the current rules or model.")
elif submitted:
    st.warning("Please enter some text to analyze.")
