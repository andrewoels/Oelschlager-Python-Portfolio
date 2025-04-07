# 🧠 Custom Named Entity Recognition (NER) App

Welcome to the Custom NER App — a Streamlit-based web application that lets users explore and extend the power of **Named Entity Recognition (NER)** using [spaCy](https://spacy.io). This app allows you to define your own custom entity labels and patterns while preserving the functionality of spaCy’s built-in NER pipeline, creating a hybrid model that recognizes both standard and user-defined entities.

---

## 📌 Project Overview

Named Entity Recognition is a Natural Language Processing (NLP) technique used to locate and classify entities like people, organizations, products, and locations in text. This app leverages **spaCy's EntityRuler**, a rule-based component that can be inserted into spaCy’s pipeline to recognize custom patterns.

The app allows users to:
- Input or upload custom text
- Define new entity labels and associated phrases
- See both custom and spaCy-detected entities highlighted in real-time
- Explore example texts and patterns to better understand how NER works

---

## 🚀 Setup Instructions

### 🔧 Running Locally

1. **Clone the repository:**

   ```bash
   git clone https://github.com/your-username/custom-ner-app.git
   cd custom-ner-app
   ```

2. **Create and activate a virtual environment (optional but recommended):**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install the required libraries:**

   ```bash
   pip install -r requirements.txt
   ```

   Or manually install:

   ```bash
   pip install streamlit spacy
   python -m spacy download en_core_web_sm
   ```

4. **Run the app:**

   ```bash
   streamlit run app.py
   ```

### 🌐 Access the Deployed Version

Visit the live version on [Streamlit Community Cloud](https://your-deployment-url.streamlit.app) (replace with your actual URL).

---

## ✨ App Features

- **📄 Text Input Options**: Type text manually or upload a `.txt` file.
- **🏷️ Custom Entity Labels**: Define multiple entity labels and phrases using the sidebar form.
- **🔍 Visual Output**: See entities highlighted in color-coded spans. Each label has a unique color.
- **📋 Entity Table**: View a structured table of extracted entities and their corresponding labels.
- **📚 Examples & Suggestions**:
  - Choose from predefined text examples like:
    - Tech Brands
    - Athletes
    - Products & Retail
  - When no text is provided, suggestions appear in the sidebar to help guide users.

### 🛠 Example Usage

Label: `BRAND`  
Phrases:
```
Nike
Apple
Target
```

Label: `SPORT`  
Phrases:
```
basketball
soccer
tennis
```

---

## 📚 References & Resources

- [spaCy Documentation](https://spacy.io/usage)
- [EntityRuler in spaCy](https://spacy.io/api/entityruler)
- [spaCy Visualizer (displacy)](https://spacy.io/usage/visualizers)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [NER Explained (Stanford NLP)](https://nlp.stanford.edu/software/CRF-NER.html)

---

## 👨‍💻 Author

**Andrew Oelschlager**  
Senior Design Student @ University of Notre Dame  
Creative Technologist | Designer | Developer
