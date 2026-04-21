"""
Skill Analyser
Extracts present skills, identifies missing skills for target role, and scores resume.
"""
import re
from typing import Dict, List

# ──────────────────────────────────────────────
# Master skill database (role → skill categories)
# ──────────────────────────────────────────────
ROLE_SKILLS: Dict[str, Dict[str, List[str]]] = {
    "Software Engineer": {
        "Programming Languages": ["python", "java", "javascript", "typescript", "c++", "c#", "go", "rust", "kotlin", "swift", "ruby", "php", "scala"],
        "Web Frameworks":        ["django", "flask", "fastapi", "react", "angular", "vue", "node.js", "express", "spring boot", "laravel", "rails"],
        "Databases":             ["mysql", "postgresql", "mongodb", "redis", "elasticsearch", "sqlite", "cassandra", "dynamodb", "oracle"],
        "DevOps & Cloud":        ["docker", "kubernetes", "aws", "azure", "gcp", "ci/cd", "jenkins", "github actions", "terraform", "ansible"],
        "Tools & Practices":     ["git", "agile", "scrum", "rest api", "graphql", "microservices", "tdd", "unit testing", "linux", "bash"],
    },
    "Data Scientist": {
        "Programming":           ["python", "r", "sql", "scala", "julia"],
        "ML & AI":               ["machine learning", "deep learning", "tensorflow", "pytorch", "scikit-learn", "keras", "xgboost", "nlp", "computer vision"],
        "Data Tools":            ["pandas", "numpy", "matplotlib", "seaborn", "plotly", "jupyter", "spark", "hadoop", "airflow"],
        "Statistics":            ["statistics", "hypothesis testing", "regression", "classification", "clustering", "time series", "a/b testing", "bayesian"],
        "Cloud & MLOps":         ["aws sagemaker", "gcp vertex ai", "mlflow", "kubeflow", "docker", "kubernetes", "git", "dvc"],
    },
    "Data Analyst": {
        "Analytics Tools":       ["excel", "sql", "tableau", "power bi", "google analytics", "looker", "metabase"],
        "Programming":           ["python", "r", "vba"],
        "Data Skills":           ["data cleaning", "data visualization", "etl", "data modeling", "reporting", "dashboard", "kpi"],
        "Statistics":            ["statistics", "regression", "forecasting", "a/b testing", "pivot tables", "vlookup"],
        "Databases":             ["mysql", "postgresql", "bigquery", "redshift", "snowflake"],
    },
    "Frontend Developer": {
        "Core Web":              ["html", "css", "javascript", "typescript"],
        "Frameworks":            ["react", "angular", "vue", "next.js", "nuxt", "svelte"],
        "Styling":               ["tailwind css", "sass", "styled-components", "bootstrap", "material ui", "chakra ui"],
        "Tools":                 ["webpack", "vite", "npm", "yarn", "git", "figma", "storybook", "jest", "cypress"],
        "Performance":           ["web performance", "seo", "accessibility", "pwa", "responsive design", "web vitals"],
    },
    "Backend Developer": {
        "Languages":             ["python", "java", "node.js", "go", "rust", "php", "ruby", "c#"],
        "Frameworks":            ["django", "flask", "fastapi", "spring boot", "express", "laravel", "rails", "asp.net"],
        "Databases":             ["mysql", "postgresql", "mongodb", "redis", "elasticsearch", "dynamodb"],
        "APIs & Architecture":   ["rest api", "graphql", "grpc", "microservices", "message queue", "rabbitmq", "kafka"],
        "DevOps":                ["docker", "kubernetes", "aws", "azure", "gcp", "linux", "nginx", "ci/cd", "terraform"],
    },
    "DevOps Engineer": {
        "Cloud Platforms":       ["aws", "azure", "gcp", "digitalocean", "heroku"],
        "Containerisation":      ["docker", "kubernetes", "helm", "podman", "openshift"],
        "IaC & Config":          ["terraform", "ansible", "chef", "puppet", "cloudformation", "pulumi"],
        "CI/CD":                 ["jenkins", "github actions", "gitlab ci", "circleci", "travis ci", "argocd"],
        "Monitoring":            ["prometheus", "grafana", "elk stack", "datadog", "splunk", "pagerduty", "nagios"],
    },
    "Machine Learning Engineer": {
        "ML Frameworks":         ["tensorflow", "pytorch", "scikit-learn", "keras", "jax", "hugging face"],
        "MLOps":                 ["mlflow", "kubeflow", "dvc", "bentoml", "seldon", "feast", "great expectations"],
        "Cloud ML":              ["aws sagemaker", "gcp vertex ai", "azure ml", "databricks"],
        "Data Engineering":      ["spark", "airflow", "kafka", "dbt", "feast", "delta lake"],
        "Programming":           ["python", "scala", "java", "sql", "bash", "go"],
    },
    "Full Stack Developer": {
        "Frontend":              ["html", "css", "javascript", "typescript", "react", "vue", "angular", "next.js"],
        "Backend":               ["node.js", "python", "java", "php", "ruby", "django", "flask", "express", "spring"],
        "Databases":             ["mysql", "postgresql", "mongodb", "redis", "firebase"],
        "DevOps":                ["docker", "git", "aws", "linux", "nginx", "ci/cd"],
        "Tools":                 ["rest api", "graphql", "agile", "scrum", "jest", "webpack"],
    },
    "Cybersecurity Analyst": {
        "Security Domains":      ["penetration testing", "vulnerability assessment", "siem", "soc", "incident response", "threat hunting"],
        "Tools":                 ["kali linux", "metasploit", "burp suite", "wireshark", "nmap", "nessus", "splunk"],
        "Standards & Certs":     ["iso 27001", "nist", "owasp", "gdpr", "pci dss", "cissp", "ceh", "oscp"],
        "Networking":            ["tcp/ip", "firewall", "vpn", "ids/ips", "dns", "http/https", "ssl/tls"],
        "Cloud Security":        ["aws security", "azure security", "iam", "zero trust", "devsecops"],
    },
    "Product Manager": {
        "Strategy & Planning":   ["product roadmap", "product strategy", "market research", "competitive analysis", "okrs", "kpis"],
        "Agile & Tools":         ["agile", "scrum", "jira", "confluence", "trello", "asana", "notion", "figma"],
        "Analytics":             ["google analytics", "mixpanel", "amplitude", "sql", "data analysis", "a/b testing"],
        "Soft Skills":           ["stakeholder management", "user interviews", "user stories", "prioritisation", "go-to-market"],
        "Technical":             ["api understanding", "sql", "wireframing", "mvp", "technical writing"],
    },
}

# Normalise role name
def _normalise_role(role: str) -> str:
    role_lower = role.lower()
    for key in ROLE_SKILLS:
        if key.lower() in role_lower or role_lower in key.lower():
            return key
    return "Software Engineer"  # default

def analyse_skills(resume_text: str, target_role: str) -> dict:
    role_key  = _normalise_role(target_role)
    skill_map = ROLE_SKILLS.get(role_key, ROLE_SKILLS["Software Engineer"])
    text_lower = resume_text.lower()

    present, missing, categories = [], [], {}

    for category, skills in skill_map.items():
        cat_present, cat_missing = [], []
        for skill in skills:
            # Match whole-word skill mentions
            pattern = r'\b' + re.escape(skill) + r'\b'
            if re.search(pattern, text_lower):
                cat_present.append(skill)
                if skill not in present:
                    present.append(skill)
            else:
                cat_missing.append(skill)
                if skill not in missing:
                    missing.append(skill)
        categories[category] = {
            "present": cat_present,
            "missing": cat_missing,
            "pct": round(len(cat_present) / len(skills) * 100) if skills else 0
        }

    return {
        "present_skills": present,
        "missing_skills": missing,
        "categories":     categories,
        "role":           role_key,
    }

def compute_score(skill_data: dict, jd_data: dict) -> dict:
    present = len(skill_data.get("present_skills", []))
    missing = len(skill_data.get("missing_skills", []))
    total   = present + missing

    skill_pct = round((present / total * 100) if total > 0 else 0)

    # Bonus if JD match is available
    jd_pct = jd_data.get("match_percent", 50) if jd_data else 50
    overall = round(skill_pct * 0.65 + jd_pct * 0.35)

    # Grade
    if overall >= 80:  grade, msg = "A", "Excellent match! Minor gaps only."
    elif overall >= 65: grade, msg = "B", "Good profile. Focus on missing skills."
    elif overall >= 50: grade, msg = "C", "Decent base — upskilling recommended."
    elif overall >= 35: grade, msg = "D", "Significant skill gaps detected."
    else:               grade, msg = "F", "Major reskilling needed for this role."

    return {
        "overall":    overall,
        "skill_pct":  skill_pct,
        "jd_pct":     jd_pct,
        "grade":      grade,
        "message":    msg,
        "present_count": present,
        "missing_count": missing,
    }
