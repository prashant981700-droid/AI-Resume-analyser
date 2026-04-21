/* ──────────────────────────────────────────────
   ResumeAI – Frontend Logic
   ────────────────────────────────────────────── */

// File drop zone
const dropZone = document.getElementById('drop-zone');
const fileInput = document.getElementById('resume_file');

dropZone.addEventListener('dragover',  e => { e.preventDefault(); dropZone.classList.add('drag-over'); });
dropZone.addEventListener('dragleave', () => dropZone.classList.remove('drag-over'));
dropZone.addEventListener('drop', e => {
  e.preventDefault();
  dropZone.classList.remove('drag-over');
  const file = e.dataTransfer.files[0];
  if (file) handleFileSelect(file);
});
fileInput.addEventListener('change', () => {
  if (fileInput.files[0]) handleFileSelect(fileInput.files[0]);
});

function handleFileSelect(file) {
  const hint = dropZone.querySelector('.upload-hint');
  const text = dropZone.querySelector('.upload-text');
  text.textContent = `📄 ${file.name}`;
  hint.textContent = `${(file.size / 1024).toFixed(1)} KB`;
}

// Tab switching
function switchTab(name, btn) {
  document.querySelectorAll('.tab-pane').forEach(p => p.classList.add('hidden'));
  document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
  document.getElementById('tab-' + name).classList.remove('hidden');
  btn.classList.add('active');
}

// Main analysis
async function runAnalysis() {
  const btn     = document.getElementById('analyse-btn');
  const btnText = document.getElementById('btn-text');
  const spinner = document.getElementById('btn-spinner');

  const resumeText = document.getElementById('resume_text').value.trim();
  const hasFile    = fileInput.files.length > 0;

  if (!resumeText && !hasFile) {
    alert('Please upload a resume file or paste your resume text.');
    return;
  }

  // Loading state
  btn.disabled = true;
  btnText.classList.add('hidden');
  spinner.classList.remove('hidden');
  document.getElementById('results').classList.add('hidden');

  const fd = new FormData();
  if (hasFile) fd.append('resume_file', fileInput.files[0]);
  if (resumeText) fd.append('resume_text', resumeText);
  fd.append('job_description', document.getElementById('job_description').value);
  fd.append('target_role',     document.getElementById('target_role').value);

  try {
    const res  = await fetch('/analyse', { method: 'POST', body: fd });
    const data = await res.json();

    if (data.error) { alert('Error: ' + data.error); return; }

    renderResults(data);
    document.getElementById('results').classList.remove('hidden');
    document.getElementById('results').scrollIntoView({ behavior: 'smooth', block: 'start' });

  } catch (err) {
    alert('Network error. Make sure the Flask server is running.');
    console.error(err);
  } finally {
    btn.disabled = false;
    btnText.classList.remove('hidden');
    spinner.classList.add('hidden');
  }
}

function renderResults(data) {
  renderScore(data.score);
  renderSkills(data.present_skills, data.missing_skills, data.categories);
  renderJD(data.jd_match);
  renderCourses(data.courses);
  renderPreview(data.resume_preview);
}

/* Score ring */
function renderScore(score) {
  const pct     = score.overall;
  const circle  = document.getElementById('ring-circle');
  const radius  = 50;
  const circumference = 2 * Math.PI * radius;

  circle.style.strokeDasharray  = circumference;
  circle.style.strokeDashoffset = circumference;

  // Animate number
  let current = 0;
  const step  = pct / 60;
  const timer = setInterval(() => {
    current = Math.min(current + step, pct);
    document.getElementById('score-number').textContent = Math.round(current);
    if (current >= pct) clearInterval(timer);
  }, 16);

  // Animate ring
  setTimeout(() => {
    const offset = circumference - (pct / 100) * circumference;
    circle.style.strokeDashoffset = offset;
    circle.className = 'ring-fill ring-grade-' + score.grade;
  }, 50);

  document.getElementById('score-grade').textContent   = score.grade;
  document.getElementById('score-message').textContent = score.message;
  document.getElementById('pill-skill').textContent    = score.skill_pct + '%';
  document.getElementById('pill-jd').textContent       = score.jd_pct + '%';
  document.getElementById('pill-present').textContent  = score.present_count;
  document.getElementById('pill-missing').textContent  = score.missing_count;
}

/* Skills */
function renderSkills(present, missing, categories) {
  const pEl = document.getElementById('present-skills');
  const mEl = document.getElementById('missing-skills');

  pEl.innerHTML = present.length
    ? present.map(s => `<span class="skill-tag">${s}</span>`).join('')
    : '<span style="color:var(--text3);font-size:13px">No skills detected</span>';

  mEl.innerHTML = missing.length
    ? missing.slice(0, 30).map(s => `<span class="skill-tag">${s}</span>`).join('')
    : '<span style="color:var(--text3);font-size:13px">No gaps found — great!</span>';

  // Category bars
  const barsEl = document.getElementById('category-bars');
  barsEl.innerHTML = '';
  for (const [cat, catData] of Object.entries(categories)) {
    const row = document.createElement('div');
    row.className = 'cat-row';
    row.innerHTML = `
      <div class="cat-header">
        <span class="cat-name">${cat}</span>
        <span class="cat-pct">${catData.pct}% (${catData.present.length}/${catData.present.length + catData.missing.length})</span>
      </div>
      <div class="bar-track">
        <div class="bar-fill" data-pct="${catData.pct}" style="width:0%"></div>
      </div>`;
    barsEl.appendChild(row);
  }
  // Animate bars after render
  setTimeout(() => {
    document.querySelectorAll('.bar-fill').forEach(bar => {
      bar.style.width = bar.dataset.pct + '%';
    });
  }, 200);
}

/* JD Match */
function renderJD(jd) {
  const statsEl   = document.getElementById('jd-stats');
  const emptyEl   = document.getElementById('jd-empty');
  const matchedEl = document.getElementById('matched-kw');
  const missingEl = document.getElementById('missing-kw');

  if (!jd || !jd.match_percent) {
    statsEl.classList.add('hidden');
    emptyEl.classList.remove('hidden');
    matchedEl.innerHTML = '<span style="color:var(--text3);font-size:13px">No JD provided</span>';
    missingEl.innerHTML = '<span style="color:var(--text3);font-size:13px">No JD provided</span>';
    return;
  }

  statsEl.classList.remove('hidden');
  emptyEl.classList.add('hidden');

  document.getElementById('jd-match-pct').textContent    = jd.match_percent + '%';
  document.getElementById('jd-density').textContent      = jd.keyword_density + '%';
  document.getElementById('jd-matched-count').textContent = jd.matched_count;
  document.getElementById('jd-total-kw').textContent     = jd.total_jd_keywords;

  matchedEl.innerHTML = (jd.matched_keywords || []).length
    ? jd.matched_keywords.map(k => `<span class="skill-tag">${k}</span>`).join('')
    : '<span style="color:var(--text3);font-size:13px">None</span>';

  missingEl.innerHTML = (jd.missing_keywords || []).length
    ? jd.missing_keywords.map(k => `<span class="skill-tag">${k}</span>`).join('')
    : '<span style="color:var(--text3);font-size:13px">None — great match!</span>';
}

/* Courses */
function renderCourses(courses) {
  const gridEl  = document.getElementById('courses-grid');
  const emptyEl = document.getElementById('courses-empty');

  if (!courses || courses.length === 0) {
    gridEl.innerHTML = '';
    emptyEl.classList.remove('hidden');
    return;
  }
  emptyEl.classList.add('hidden');

  const levelColor = { Beginner: '#34d399', Intermediate: '#fbbf24', Advanced: '#fb7185' };

  gridEl.innerHTML = courses.map(c => `
    <div class="course-card">
      <div class="course-header">
        <div class="course-platform-badge">${c.icon}</div>
        <div class="course-title">${c.title}</div>
      </div>
      <div class="course-skill-tag">Missing skill: ${c.skill}</div>
      <div class="course-meta">
        <span>${c.platform}</span>
        <span>⏱ ${c.duration}</span>
        <span style="color:${levelColor[c.level] || '#9a9bb8'}">${c.level}</span>
      </div>
      <a href="${c.url}" target="_blank" rel="noopener" class="course-link">
        View Course
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M5 12h14M12 5l7 7-7 7"/>
        </svg>
      </a>
    </div>`).join('');
}

/* Preview */
function renderPreview(text) {
  document.getElementById('resume-preview').textContent = text || 'No text extracted.';
}
