# 🏆 CodeForge — Online Judge Platform

CodeForge is a **full-stack online judge platform** built with **traditional Django**, a **custom HTML/CSS/JS frontend**, and a **microservice-based compiler engine**.  
It allows users to solve problems, run code in multiple languages, participate in contests, track leaderboards, and receive AI-assisted code reviews.

---

## 📌 Features

- **User Authentication**

  - Custom login, signup, and logout flows
  - Profile view with badges, streak tracking, and stats

- **Problem Management**

  - Problem listing and detail views
  - Tag-based filtering
  - Score and difficulty system

- **Code Execution**

  - Support for Python, C++, and Java
  - Run code with custom inputs
  - Submission evaluation against multiple test cases
  - Plagiarism detection (basic similarity check)

- **Contest System**

  - Create, register, and participate in contests
  - Contest-only problem visibility
  - Real-time leaderboard

- **AI Code Review**

  - Generate code review feedback using AI

- **Microservice Compiler**

  - Standalone compiler service (`compiler_service`) deployed on AWS
  - Handles secure, resource-limited code execution
  - Supports compilation and execution with time & memory limits

- **Dockerized Deployment**
  - Separate Dockerfiles for main app and compiler microservice
  - Main app hosted on **Render**
  - Compiler microservice hosted on **AWS**

---

## 🛠 Tech Stack

**Backend:**

- Django (Traditional, no DRF)
- SQLite (development) / PostgreSQL (production)
- Python 3.10

**Frontend:**

- HTML, CSS, JavaScript
- Custom dark theme with glassmorphism
- Responsive UI

**Compiler Microservice:**

- Python subprocess for running code
- C++, Java, and Python execution
- CPU and memory limits via `resource` module
- Runs inside a Docker container for isolation

**Deployment:**

- **Main App** → Render
- **Compiler Service** → AWS (EC2 or container service)
- **Dockerized** for reproducibility

---

## 📂 Project Structure

```

OJ-Project/
│
├── oj/                      # Main Django project settings
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
│
├── core/                    # Core functionality (problems, submissions, profiles)
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── templates/core/
│
├── contests/                # Contest management
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── templates/contests/
│
├── compiler/                # Local compiler app (API bridge to compiler\_service)
│   ├── execution.py
│   ├── evaluation.py
│   ├── utils.py
│   ├── views.py
│   └── urls.py
│
├── compiler\_service/        # Standalone compiler microservice
│   ├── compiler/            # Code execution logic
│   ├── compiler\_service/    # Django project files
│   ├── Dockerfile
│   └── manage.py
│
├── user\_auth/               # Authentication
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── templates/user\_auth/
│
├── templates/               # Shared templates
│
├── static/                  # CSS, JS, Images
│
├── Dockerfile               # Main app Dockerfile
├── requirements.txt
└── manage.py

```

---

## ⚙️ Architecture Overview

```

\[ User Browser ]
│
▼
\[ Django Main App (Render) ]
core/views.py
│
├── Local compiler app → calls compiler\_service API
│
▼
\[ Compiler Microservice (AWS) ]
Executes code securely (Docker sandbox)
│
▼
\[ Returns Output / Verdict ]

```

**Flow Example:**

1. User writes code in editor → clicks **Run** or **Submit**.
2. Django `compiler` app sends request to **compiler_service** API.
3. Compiler service compiles/runs code inside Docker, applies resource limits.
4. Output/verdict returned → displayed on frontend.

---

## 🚀 Deployment

### 1️⃣ Main App (Render)

```bash
# Build & deploy
docker build -t codeforge-main .
docker run -p 8000:8000 codeforge-main
```

Render automatically detects `Dockerfile` and deploys.

### 2️⃣ Compiler Service (AWS)

```bash
# Inside compiler_service/
docker build -t compiler-service .
docker run -p 8000:8000 compiler-service
```

Expose via AWS security group & load balancer.

---

## 🔒 Security & Limitations

- Execution runs in **isolated temp directories**.
- CPU limit: **2 seconds** per run.
- Memory limit: **64 MB**.
- Only whitelisted languages supported.
- Basic plagiarism detection using code similarity checks.

---

## 🧑‍💻 Development Setup

```bash
# Clone repository
git clone https://github.com/<username>/OJ-Project.git
cd OJ-Project

# Install dependencies
pip install -r requirements.txt

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run server
python manage.py runserver
```

---

## 📝 Environment Variables

For production, set:

```env
DJANGO_SECRET_KEY=your_secret_key
DEBUG=False
ALLOWED_HOSTS=your_domain
COMPILER_SERVICE_URL=https://<aws-compiler-service-url>
```

---

## 📊 Future Improvements

- Real-time WebSocket-based leaderboard
- Advanced plagiarism detection (MOSS integration)
- Support for more languages (Go, Rust)
- Submission replay and visualization
- Test case randomization

---

## 📜 License

This project is licensed under the MIT License.

---

**Author:** Vaibhav Kumar
**GitHub:** [Vaibhav-Kumar10](https://github.com/Vaibhav-Kumar10)

---

# Images

## Home

<img width="1920" height="1080" alt="Screenshot 2025-08-10 011027" src="https://github.com/user-attachments/assets/2fb36cad-afce-4273-b470-80b836ebb02c" />
<img width="1920" height="1080" alt="Screenshot 2025-08-10 011032" src="https://github.com/user-attachments/assets/a6c8e5af-9cd4-4336-aad4-9a65f09de189" />
<img width="1920" height="1080" alt="Screenshot 2025-08-10 011038" src="https://github.com/user-attachments/assets/a78eeb5d-db4c-4b40-bec5-b67cdd596e5c" />
<img width="1920" height="1080" alt="Screenshot 2025-08-10 011123" src="https://github.com/user-attachments/assets/cf6d1047-85c9-4473-be90-5542f74b9449" />
<img width="1920" height="1080" alt="Screenshot 2025-08-10 011127" src="https://github.com/user-attachments/assets/86412612-e5f7-4b37-a8f8-c8026d13d57f" />

## All Problems

<img width="1920" height="1080" alt="Screenshot 2025-08-10 011049" src="https://github.com/user-attachments/assets/4314076d-a66a-4b27-a9bd-1dc985fbef5f" />

## Leaderboard

<img width="1920" height="1080" alt="Screenshot 2025-08-10 011107" src="https://github.com/user-attachments/assets/e44cf128-10a0-4441-b600-d7c5950f39ab" />
<img width="1920" height="1080" alt="Screenshot 2025-08-10 011113" src="https://github.com/user-attachments/assets/0c1cda58-d50f-4617-887d-c4080772ae6f" />

## Contests

<img width="1920" height="1080" alt="Screenshot 2025-08-10 011057" src="https://github.com/user-attachments/assets/d16e9bd3-f0d1-4235-9892-510d9ad8a53f" />

## Problem

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/618a1de3-1aaa-442e-a984-242660454c9e" />

## Signup

<img width="1920" height="1080" alt="Screenshot 2025-08-10 011233" src="https://github.com/user-attachments/assets/311f7eda-be49-464f-9251-75831f7305ea" />

## Login

<img width="1920" height="1080" alt="Screenshot 2025-08-10 011201" src="https://github.com/user-attachments/assets/3e7aff36-c503-4c3b-aa89-fc9f6dd02e27" />

## Profile

<img width="1920" height="1080" alt="Screenshot 2025-08-10 011213" src="https://github.com/user-attachments/assets/80c1dc25-f67d-4641-a4bc-e50b5c31d4ba" />
<img width="1920" height="1080" alt="Screenshot 2025-08-10 011217" src="https://github.com/user-attachments/assets/3bb3b2a5-686b-4644-adff-a0740e7edb33" />
<img width="1920" height="1080" alt="Screenshot 2025-08-10 011222" src="https://github.com/user-attachments/assets/e52648ef-b42f-45f4-ad10-efc5b8fe8b13" />
