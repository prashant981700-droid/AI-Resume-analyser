# 🤖 AI Resume Analyser & Skill Suggestion System

A full-stack web application built with **Flask + Python** that analyses resumes using NLP, detects skill gaps, matches against job descriptions, and recommends relevant courses.

---

## ✨ Features

| Feature | Details |
|---|---|
| **Resume Parsing** | Supports PDF, DOCX, and TXT uploads |
| **Skill Gap Analysis** | Checks 10+ roles with 50–100 skills per role |
| **Resume Score** | 0–100 score with letter grade (A–F) |
| **JD Matching** | TF-IDF cosine similarity against job descriptions |
| **Keyword Analysis** | Matched vs missing JD keywords |
| **Course Suggestions** | Mapped to Udemy/Coursera with level & duration |
| **Interactive Dashboard** | Tabs, progress bars, animated score ring |

---

## 🛠 Tech Stack

- **Backend**: Python 3.10+, Flask 3.x
- **NLP**: Custom TF-IDF engine, regex-based skill extraction
- **Resume Parsing**: PyPDF2, python-docx, pdfminer.six
- **Frontend**: Vanilla HTML5, CSS3, JavaScript (no frontend framework needed)
- **Fonts**: Syne + Inter (Google Fonts)

---

## 🚀 Setup & Run

### 1. Clone / extract the project
```bash
cd ai_resume_analyser
```

### 2. Create a virtual environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac / Linux
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the app
```bash
python app.py
```

### 5. Open in browser
```
http://localhost:5000
```

---

## 📁 Project Structure

```
ai_resume_analyser/
├── app.py                  # Flask application & routes
├── requirements.txt        # Python dependencies
├── templates/
│   └── index.html          # Main UI template
├── static/
│   ├── css/style.css       # Full stylesheet
│   └── js/app.js           # Frontend logic
└── utils/
    ├── parser.py           # PDF / DOCX / TXT resume parser
    ├── analyser.py         # Skill extraction & scoring engine
    ├── matcher.py          # TF-IDF JD matcher
    └── suggester.py        # Course recommendation engine
```

---

## 🎯 Supported Roles

- Software Engineer
- Data Scientist
- Data Analyst
- Frontend Developer
- Backend Developer
- Full Stack Developer
- DevOps Engineer
- Machine Learning Engineer
- Cybersecurity Analyst
- Product Manager

---

## 🔧 Extending the Project

### Add a new role
Edit `utils/analyser.py` → `ROLE_SKILLS` dict. Add a new key with category → skill list.

### Add more courses
Edit `utils/suggester.py` → `COURSE_DB` dict. Map `"skill_name"` → course details.

### Add spaCy NER (optional upgrade)
```bash
pip install spacy
python -m spacy download en_core_web_sm
```
Then use spaCy in `parser.py` for entity extraction.

### Add AI via OpenAI API (optional upgrade)
Replace the scoring logic in `analyser.py` with a GPT call for richer, contextual feedback.

---

## 📸 Screenshot
The dashboard features:
- Animated score ring with letter grade
- Skill presence/absence tag clouds
- Category progress bars
- JD keyword match analysis
- Ranked course cards with direct links

---

## 📄 License
MIT — free to use, modify, and distribute.
