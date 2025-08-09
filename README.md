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


## My File Structure

OJ-PROJECT/   
│    
├── user_auth/   
│ ├── models.py # User Date, Profile    
│ ├── views.py # login, signup, logout     
│ ├── urls.py        
│          
├── core/        
│ ├── models.py # Problems, submissions, testcases   
│ ├── views.py # home  
│ ├── urls.py    
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
├── templates/      
|     |---login      
|     |---logout       
|     |---signup       
|     |---dashboard   
|     |---home    
|     |---allproblems 
|     |---problem_detail
|     |---contest     
|     |---leaderboard      
|
├── contests/         
│ ├── models.py # Contest, Participation.       
│ ├── views.py      
│ ├── urls.py       
|
├── manage.py
├── Dockerfile
├── requirements.txt


### ARCHITECTURE OVERVIEW

User hits frontend (core/views.py)        
   → calls compiler views via path("compiler/...") [local]       
       → uses compiler/evaluation.py or compiler/execution.py      
           → which makes API call to compiler_service microservice        
               → compiles / evaluates and returns output     
           ← returns result to compiler app     
       ← compiler view returns to core view context     
← core view shows result to user    
