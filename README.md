## Home 

## All Problems

## Leaderboard 

## Contests

## Problem


### Submissions added


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
