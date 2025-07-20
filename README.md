## Home 
<img width="1912" height="967" alt="Screenshot 2025-07-20 170217" src="https://github.com/user-attachments/assets/484aa7e6-c21e-4cc9-91bf-d492de7657f2" />
<img width="1919" height="926" alt="Screenshot 2025-07-20 170229" src="https://github.com/user-attachments/assets/7a039fa0-6e8e-414a-adbb-d131a3e75ed3" />
<img width="1919" height="924" alt="Screenshot 2025-07-20 170237" src="https://github.com/user-attachments/assets/80d5341c-4977-4beb-a164-8b0b46419531" />


## All Problems
<img width="1919" height="921" alt="Screenshot 2025-07-20 170247" src="https://github.com/user-attachments/assets/c8e25840-5612-4a0a-917b-274c34502d31" />

## Problem
<img width="1918" height="980" alt="Screenshot 2025-07-20 170256" src="https://github.com/user-attachments/assets/d0c12578-514e-47a7-9208-68b30fc2f9b1" />
<img width="1919" height="925" alt="Screenshot 2025-07-20 170304" src="https://github.com/user-attachments/assets/98abb1a7-61b8-46c3-996b-056bcd1d2e59" />
<img width="1919" height="971" alt="Screenshot 2025-07-20 170309" src="https://github.com/user-attachments/assets/dacf5e98-9a6f-4755-98e1-321b43b14d7f" />




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
|
├── manage.py
├── Dockerfile
|
│(vesrion2)      
├── contests/         
│ ├── models.py # Contest, Participation   
│ ├── views.py   
│ ├── urls.py     
│ ├── templates/    
|     |---contest     
|     |---leaderboard 
