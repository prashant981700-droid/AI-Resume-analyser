"""
Course Suggester
Maps missing skills to recommended online courses with platform, duration, and level.
"""
from typing import List, Dict

# Comprehensive skill → course mapping
COURSE_DB: Dict[str, dict] = {
    # Python & Programming
    "python":           {"title": "Python Bootcamp: Zero to Hero", "platform": "Udemy", "url": "https://www.udemy.com/course/complete-python-bootcamp/", "duration": "22h", "level": "Beginner"},
    "javascript":       {"title": "The Complete JavaScript Course", "platform": "Udemy", "url": "https://www.udemy.com/course/the-complete-javascript-course/", "duration": "69h", "level": "Beginner"},
    "typescript":       {"title": "Understanding TypeScript", "platform": "Udemy", "url": "https://www.udemy.com/course/understanding-typescript/", "duration": "22h", "level": "Intermediate"},
    "java":             {"title": "Java Programming Masterclass", "platform": "Udemy", "url": "https://www.udemy.com/course/java-the-complete-java-developer-course/", "duration": "80h", "level": "Beginner"},
    "go":               {"title": "Learn How to Code: Google's Go", "platform": "Udemy", "url": "https://www.udemy.com/course/learn-how-to-code/", "duration": "46h", "level": "Intermediate"},
    "rust":             {"title": "Ultimate Rust Crash Course", "platform": "Udemy", "url": "https://www.udemy.com/course/ultimate-rust-crash-course/", "duration": "6h", "level": "Intermediate"},
    # Web Frameworks
    "react":            {"title": "React - The Complete Guide", "platform": "Udemy", "url": "https://www.udemy.com/course/react-the-complete-guide-incl-redux/", "duration": "68h", "level": "Beginner"},
    "vue":              {"title": "Vue - The Complete Guide", "platform": "Udemy", "url": "https://www.udemy.com/course/vuejs-2-the-complete-guide/", "duration": "32h", "level": "Beginner"},
    "angular":          {"title": "Angular - The Complete Guide", "platform": "Udemy", "url": "https://www.udemy.com/course/the-complete-guide-to-angular-2/", "duration": "36h", "level": "Intermediate"},
    "django":           {"title": "Django for Everybody", "platform": "Coursera", "url": "https://www.coursera.org/specializations/django", "duration": "20h", "level": "Intermediate"},
    "flask":            {"title": "REST APIs with Flask and Python", "platform": "Udemy", "url": "https://www.udemy.com/course/rest-api-flask-and-python/", "duration": "18h", "level": "Intermediate"},
    "fastapi":          {"title": "FastAPI - The Complete Course", "platform": "Udemy", "url": "https://www.udemy.com/course/fastapi-the-complete-course/", "duration": "10h", "level": "Intermediate"},
    "node.js":          {"title": "The Complete Node.js Developer Course", "platform": "Udemy", "url": "https://www.udemy.com/course/the-complete-nodejs-developer-course-2/", "duration": "35h", "level": "Beginner"},
    # Cloud & DevOps
    "aws":              {"title": "AWS Certified Solutions Architect", "platform": "Udemy", "url": "https://www.udemy.com/course/aws-certified-solutions-architect-associate-saa-c03/", "duration": "27h", "level": "Intermediate"},
    "azure":            {"title": "AZ-900: Microsoft Azure Fundamentals", "platform": "Udemy", "url": "https://www.udemy.com/course/az900-azure/", "duration": "9h", "level": "Beginner"},
    "gcp":              {"title": "Google Cloud Professional Architect", "platform": "Coursera", "url": "https://www.coursera.org/professional-certificates/gcp-cloud-architect", "duration": "30h", "level": "Advanced"},
    "docker":           {"title": "Docker & Kubernetes: The Practical Guide", "platform": "Udemy", "url": "https://www.udemy.com/course/docker-kubernetes-the-practical-guide/", "duration": "24h", "level": "Intermediate"},
    "kubernetes":       {"title": "Kubernetes Mastery", "platform": "Udemy", "url": "https://www.udemy.com/course/kubernetesmastery/", "duration": "9h", "level": "Advanced"},
    "terraform":        {"title": "HashiCorp Terraform Associate", "platform": "Udemy", "url": "https://www.udemy.com/course/terraform-beginner-to-advanced/", "duration": "20h", "level": "Intermediate"},
    # Data & ML
    "machine learning": {"title": "Machine Learning Specialization", "platform": "Coursera", "url": "https://www.coursera.org/specializations/machine-learning-introduction", "duration": "95h", "level": "Intermediate"},
    "deep learning":    {"title": "Deep Learning Specialization", "platform": "Coursera", "url": "https://www.coursera.org/specializations/deep-learning", "duration": "100h", "level": "Advanced"},
    "tensorflow":       {"title": "TensorFlow Developer Certificate", "platform": "Coursera", "url": "https://www.coursera.org/professional-certificates/tensorflow-in-practice", "duration": "60h", "level": "Intermediate"},
    "pytorch":          {"title": "PyTorch for Deep Learning Bootcamp", "platform": "Udemy", "url": "https://www.udemy.com/course/pytorch-for-deep-learning-and-computer-vision/", "duration": "17h", "level": "Intermediate"},
    "scikit-learn":     {"title": "Scikit-learn Machine Learning", "platform": "Udemy", "url": "https://www.udemy.com/course/machinelearning/", "duration": "44h", "level": "Intermediate"},
    "sql":              {"title": "The Complete SQL Bootcamp", "platform": "Udemy", "url": "https://www.udemy.com/course/the-complete-sql-bootcamp/", "duration": "9h", "level": "Beginner"},
    "postgresql":       {"title": "SQL and PostgreSQL: The Complete Developer's Guide", "platform": "Udemy", "url": "https://www.udemy.com/course/sql-and-postgresql/", "duration": "24h", "level": "Intermediate"},
    "mongodb":          {"title": "MongoDB - The Complete Developer's Guide", "platform": "Udemy", "url": "https://www.udemy.com/course/mongodb-the-complete-developers-guide/", "duration": "17h", "level": "Beginner"},
    "pandas":           {"title": "Data Analysis with Pandas and Python", "platform": "Udemy", "url": "https://www.udemy.com/course/data-analysis-with-pandas/", "duration": "19h", "level": "Beginner"},
    "nlp":              {"title": "Natural Language Processing Specialization", "platform": "Coursera", "url": "https://www.coursera.org/specializations/natural-language-processing", "duration": "120h", "level": "Advanced"},
    "tableau":          {"title": "Tableau 2024 A-Z", "platform": "Udemy", "url": "https://www.udemy.com/course/tableau10/", "duration": "9h", "level": "Beginner"},
    "power bi":         {"title": "Microsoft Power BI - The Practical Guide", "platform": "Udemy", "url": "https://www.udemy.com/course/microsoft-power-bi-up-running-with-power-bi-desktop/", "duration": "20h", "level": "Beginner"},
    # Security
    "penetration testing": {"title": "Complete Ethical Hacking Bootcamp", "platform": "Udemy", "url": "https://www.udemy.com/course/complete-ethical-hacking-bootcamp-zero-to-mastery/", "duration": "29h", "level": "Intermediate"},
    # Misc
    "git":              {"title": "Git & GitHub Bootcamp", "platform": "Udemy", "url": "https://www.udemy.com/course/git-and-github-bootcamp/", "duration": "17h", "level": "Beginner"},
    "linux":            {"title": "Linux Command Line Basics", "platform": "Udemy", "url": "https://www.udemy.com/course/linux-command-line-volume1/", "duration": "6h", "level": "Beginner"},
    "statistics":       {"title": "Statistics for Data Science and Business Analysis", "platform": "Udemy", "url": "https://www.udemy.com/course/statistics-for-data-science-and-business-analysis/", "duration": "7h", "level": "Beginner"},
}

PLATFORM_ICONS = {
    "Udemy":    "U",
    "Coursera": "C",
    "edX":      "E",
    "YouTube":  "Y",
    "LinkedIn": "L",
}

def suggest_courses(missing_skills: List[str]) -> List[dict]:
    """Return ranked course suggestions for missing skills."""
    suggestions = []
    seen_titles = set()

    for skill in missing_skills:
        skill_lower = skill.lower()
        course = COURSE_DB.get(skill_lower)
        if course and course["title"] not in seen_titles:
            suggestions.append({
                "skill":    skill,
                "title":    course["title"],
                "platform": course["platform"],
                "url":      course["url"],
                "duration": course["duration"],
                "level":    course["level"],
                "icon":     PLATFORM_ICONS.get(course["platform"], "?"),
            })
            seen_titles.add(course["title"])

    # Sort: Beginner first, then Intermediate, Advanced
    level_order = {"Beginner": 0, "Intermediate": 1, "Advanced": 2}
    suggestions.sort(key=lambda c: level_order.get(c["level"], 99))

    return suggestions[:12]  # Return top 12
