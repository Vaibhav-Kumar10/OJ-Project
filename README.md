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

# Container structure

┌─────────────────────────────────────────────────┐
│          Docker Compose (docker-compose.yml)    │
├─────────────────────────────────────────────────┤
│                                                 │
│  📦 PostgreSQL (db:5432)                        │
│     └─ Stores users, problems, submissions      │
│                                                 │
│  🌐 Django Web (web:8000)                       │
│     └─ Your OJ website                          │
│     └─ Accessible at <http://localhost:8000>    │
│                                                 │
│  ⚙️  Compiler Service (compiler:8001)           │
│     └─ Runs Python/C++/Java code                │
│     └─ Called by Django when user runs code     │
│                                                 │
└─────────────────────────────────────────────────┘

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

<img width="1920" height="1080" alt="Screenshot 2026-07-29 000421" src="https://github.com/user-attachments/assets/df748973-a5dc-4185-a540-3d4977e9f34b" />
<img width="1920" height="1080" alt="Screenshot 2026-07-29 000426" src="https://github.com/user-attachments/assets/ca3a1618-a3a6-4c3f-abdb-2ddf89bfc2e9" />
<img width="1920" height="1080" alt="Screenshot 2026-07-29 000431" src="https://github.com/user-attachments/assets/e013126f-a12a-4c73-a1a6-97e72111992f" />

## All Problems

<img width="1920" height="1080" alt="Screenshot 2026-07-29 000438" src="https://github.com/user-attachments/assets/22e0137d-974b-490e-8ecb-645470d14bfc" />

## Contests

<img width="1920" height="1080" alt="Screenshot 2026-07-29 000450" src="https://github.com/user-attachments/assets/4bf50cd4-8104-4899-a4db-c3319f8e416f" />
<img width="1920" height="1080" alt="Screenshot 2026-07-29 000454" src="https://github.com/user-attachments/assets/01ced2b9-4ea1-4ee3-abf3-a785d1676038" />

## Leaderboard

<img width="1920" height="1080" alt="Screenshot 2026-07-29 000506" src="https://github.com/user-attachments/assets/54b9bba1-ae6b-4f1d-875d-9b089ddd596d" />

## Problem

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/45d6ba24-3639-4497-914a-8d6be131a8ab" />
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/a9abb3ac-cb98-40f2-aa5d-620f1801bea0" />


## Signup

<img width="1920" height="1080" alt="Screenshot 2026-07-29 000538" src="https://github.com/user-attachments/assets/ab80dc8b-3e1a-4f41-9317-de8e016e9a11" />
<img width="1920" height="1080" alt="Screenshot 2026-07-29 000543" src="https://github.com/user-attachments/assets/4790704c-889c-4264-bd4c-7af2a9582cca" />

## Login

<img width="1920" height="1080" alt="Screenshot 2026-07-29 000523" src="https://github.com/user-attachments/assets/682c5322-b657-4f2b-a64d-dce8906b731a" />

## Profile
