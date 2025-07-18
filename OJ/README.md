My File Structure

OJ-PROJECT/
│
├── auth/
│ ├── models.py # User Date, Profile
│ ├── views.py # login, signup, logout
│ ├── urls.py
│ ├── templates/
|       |---login
|       |---logout
|       |---signup
|       |---dashboard
│
│(vesrion2)
├── contests/
│ ├── models.py # Contest, Participation
│ ├── views.py
│ ├── urls.py
│ ├── templates/
|       |---contest
|       |---leaderboard
│
├── core/
│ ├── models.py # Problems, submissions, testcases
│ ├── views.py # home
│ ├── urls.py
│ ├── templates/
|       |---home
|       |---allproblems
│
├── compiler/
│ ├── models.py  
│ ├── views.py  
│ ├── urls.py
│
├── oj/
│ ├── settings.py
│ ├── urls.py # includes all app urls
│
├── manage.py
