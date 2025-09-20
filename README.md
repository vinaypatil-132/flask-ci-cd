# Flask CI/CD with Blue-Green Deployment

This project demonstrates a **Flask web application** integrated with a **CI/CD pipeline using Jenkins**, featuring **Blue-Green Deployment**.

---

## 🚀 Project Overview
- A simple **Flask app** with `index.html` as the landing page.
- Automated pipeline with:
  - **Build & Test**: Python virtual environment + `pytest`
  - **CI/CD with Jenkins**: Code pushed to GitHub triggers Jenkins pipeline
  - **Blue-Green Deployment**: Zero-downtime deployments with two environments (`blue` and `green`)

---

## 🛠️ Tech Stack
- **Flask (Python 3)**
- **Jenkins (Pipeline)**  
- **GitHub (Version Control)**
- **Nginx / Gunicorn (for serving app, optional)**
- **Docker (optional for containerized deployment)**

---

## 📂 Project Structure
flask-ci-cd/
│── app.py # Main Flask app
│── requirements.txt # Python dependencies
│── templates/
│ └── index.html # HTML template
│── tests/
│ └── test_app.py # Sample unit test
│── Jenkinsfile # CI/CD pipeline config
│── .gitignore # Ignore unnecessary files
│── README.md # Project documentation


---

## ⚙️ Setup Instructions

### 1. Clone Repo
```bash
git clone https://github.com/<your-username>/flask-ci-cd.git
cd flask-ci-cd
```
### 2. Setup Python Environment
```bash
python3 -m venv venv
. venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```
### 3. Run Locally
```bash
python app.py
```
App runs at: http://127.0.0.1:5000/
### 🧪 Running Tests
```bash
pytest -q
```
### 🔄 CI/CD Pipeline (Jenkins)

- Trigger: Push to GitHub → Jenkins Webhook

- Stages:

        1. Checkout Code
        2. Install Dependencies
        3. Run Tests
        4. Build & Deploy
        5. Blue-Green Switch
### 🌍 Blue-Green Deployment Flow

1. Deploy new version to idle environment (Blue/Green).
2. Run smoke tests.
3. If successful → switch traffic to new environment.
4. Old environment stays as rollback option.

### 📌 Future Improvements
- Add Docker support for containerized deployment
- Add monitoring & alerts for deployments
- Expand test coverage

### 👨‍💻 Author
- Vinay Patil
- DevOps | Web Developer | Ethical Hacker
- Portfolio https://vinaypatil-132.github.io/Portfolio/
