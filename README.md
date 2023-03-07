# TFTracker
<p align="center">
  <img src="https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB" alt="React.js">
  <img src="https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=green" alt="Django">
  <img src="https://img.shields.io/badge/django%20rest-ff1709?style=for-the-badge&logo=django&logoColor=white" alt="Django Rest Framework">
  <img src="https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white" alt="PostgreSQL">
  <img src="https://img.shields.io/badge/Material%20UI-007FFF?style=for-the-badge&logo=mui&logoColor=white" alt="MaterialUI">
</p>

 

TFTracker is a full-stack transformer (toy) collection tracking website with a
React.js frontend and a Django backend (via the Django REST Framework).

# Features

- [x] Session Authentication
- [x] User Accounts
- [x] Registration
- [x] Login
- [x] Redux State Management
- [x] Database Search Interface
    - [x] Trigram Similarity Searching
    - [x] Sorting
    - [x] Filtering
- [ ] Saved Collections (implemented in backend)
- [ ] User Preferences (model implemented in backend)
- [ ] User Settings (model implemented in backend)
- [ ] Docker Image

# Getting Started

Currently, TFTracker can only be run in a development environment

### System Requirements

:bulb: Before you begin, make sure you have the following installed:

- [Node.js v16 or above](https://nodejs.org/en/download/)
- [Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git/)
- [Python](https://www.python.org/downloads/)

### Getting Started With Local Development

Follow these simple instructions to set up a local development environment.

1. Clone the repository:

```bash
git clone https://github.com/dagleaves/tftracker.git
cd tftracker
```

2. (optional) Create a Python virtual environment:

```bash
python -m venv env
source env/Scripts/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
cd frontend/client
npm i
```

4. TODO: Run Docker image

4. Apply database migrations:

```bash
python backend/django-app/manage.py migrate
```

5. Start development servers:

```bash
# Backend server - open localhost:8000 to manage
python backend/django-app/manage.py runserver

# Frontend sever - open localhost:3000 to manage
cd frontend/client
npm start
```

# Notes

There are API keys (S3, Firebase) in the git history from before I made this
repository public. These were all regenerated.

## Motivation

I plan on putting this website into production when it reaches a usable state.
However, this project has consumed a significant enough amount of time and has
reached a size that I have to include it in my portfolio.
