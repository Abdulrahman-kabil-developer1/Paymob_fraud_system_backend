# Paymob_fraud_system_backend
this repo contains backend project of Paymob fraud system with docker files and ex (.env) file

## Run Project 
fill .env file (found example in project dir)
- ## docker run
  install docker disktop 
  open CMD in project dir 

      docker-compose up

  project run in localhost:8000

  pg Admin run in localhost:8080
- ## local run
  install python3
  
  change DB settings in (paymob/settings)
  
  open CMD in project dir
  
          pip install -r requirements.txt
          
          python manage.py makemigrations
          
          python manage.py migrate
          
          python manage.py runserver 0.0.0.0:8000
          
  project run in localhost:8000

# If you find any difficulties or problems, do not hesitate to contact me

- email: abdulrahman.ragab.kabil@gmail.com
- phone: (+20) 1149312512
- linkedin: https://www.linkedin.com/in/abdulrahman-kabil-5729621a2/
# System review
login

![login](https://github.com/Abdulrahman-Kabil-developer/Paymob_fraud_system_backend/blob/main/screenshots/Screenshot%202022-10-08%20224712.png)

admin panel view

![adminPanelView](https://github.com/Abdulrahman-Kabil-developer/Paymob_fraud_system_backend/blob/main/screenshots/Screenshot%202022-10-08%20224905.png)

list of actions 

![actions](https://github.com/Abdulrahman-Kabil-developer/Paymob_fraud_system_backend/blob/main/screenshots/Screenshot%202022-10-12%20213725.png)

black list view

![blackList](https://github.com/Abdulrahman-Kabil-developer/Paymob_fraud_system_backend/blob/main/screenshots/Screenshot%202022-10-08%20225227.png)

