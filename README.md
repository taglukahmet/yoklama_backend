# yoklama_backend


here is a dependecies list, these are the critical ones that you should make sure that you downloaded them

# dependencies list:

1. *beautifulsoup4=4.13.4=py312haa95532_0*
2. *django=5.2=py312haa95532_0*
3. *django-cors-headers=4.7.0=pyhd8ed1ab_0*
4. *django-phonenumber-field=8.1.0=pyhd8ed1ab_0*
5. *djangorestframework=3.16.0=pyhd8ed1ab_1*
6. *environs=14.2.0=pyhd8ed1ab_0*
7. *marshmallow=4.0.0=py312haa95532_0*
8. *phonenumbers=8.13.49=py312haa95532_0*
9. *pillow=11.3.0=py312hb328d1f_0*
10. *python=3.12.11=h716150d_0*

also note that postgreSQL 17 is required due to some spesific lines in the codebase

please download it from the official website, you can learn how to create a database from here https://youtu.be/KuQUNHCeKCk
also make sure that you edited the variables in accordance with your PostgreSQL information in settings.py

# how to run and use:

1. open your terminal (whichever you use for python, I use anaconda prompt)
2. if its conda, activate your environment dedicated to the project
3. open the folder in the terminal
4. always make sure that you run these commands beforehand, because I may be making changes on some fileds:
   a. python manage.py makemigrations
   b. python manage.py migrate
5. then run "python manage.py runserver" and you are goood to go.
6. it will show you the localhost address, you will be using it for the frontend for local tests
