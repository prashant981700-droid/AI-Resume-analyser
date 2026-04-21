from flask import Flask, render_template, request, jsonify
import os, json
from utils.parser import parse_resume
from utils.analyser import analyse_skills, compute_score
from utils.matcher import match_jd
from utils.suggester import suggest_courses

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5 MB

ALLOWED_EXT = {'pdf', 'docx', 'txt'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXT

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyse', methods=['POST'])
def analyse():
    resume_text = ""

    # Handle file upload
    if 'resume_file' in request.files:
        f = request.files['resume_file']
        if f and f.filename and allowed_file(f.filename):
            ext = f.filename.rsplit('.', 1)[1].lower()
            data = f.read()
            resume_text = parse_resume(data, ext)

    # Fallback to pasted text
    if not resume_text:
        resume_text = request.form.get('resume_text', '').strip()

    if not resume_text:
        return jsonify({'error': 'No resume content provided.'}), 400

    job_desc   = request.form.get('job_description', '').strip()
    target_role = request.form.get('target_role', 'Software Engineer').strip()

    # AI pipeline
    skill_data  = analyse_skills(resume_text, target_role)
    jd_data     = match_jd(resume_text, job_desc) if job_desc else {}
    score       = compute_score(skill_data, jd_data)
    courses     = suggest_courses(skill_data.get('missing_skills', []))

    return jsonify({
        'score':          score,
        'present_skills': skill_data.get('present_skills', []),
        'missing_skills': skill_data.get('missing_skills', []),
        'categories':     skill_data.get('categories', {}),
        'jd_match':       jd_data,
        'courses':        courses,
        'resume_preview': resume_text[:600] + ('...' if len(resume_text) > 600 else '')
    })

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
