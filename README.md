This is a personal back-end project created using django version 4.2.6 
To run this project locally you would need the following (Python version 3.11) and you would need to follow the following instructions:

create a virtual environment and name it whatever you would like:
mkvirtualenv the-chosen-name-for-your-virtual-environment
 next steps...
    
  installing django run : pip install Django==4.2.6

  installing the dependencies required to run the project run in the terminal:
  1 - cors headers (Cross-Origins_Resource-Sharing aka cors in django):  pip install django-cors-headers
  2 - djangrestframework (for buildiing web APIs):  pip install django-cors-headers
  3 - pip install djangorestframework-simplejwt (Provides Json web token for authentication for django): pip install djangorestframework-simplejwt

  4- alternatively just run the following command to install these dependencies all at once: pip install Django==4.2.6 django-cors-headers djangorestframework djangorestframework-simplejwt

  if the following de[pendencies installed without issue then running the project should not be a problem, just run the last command: python manage.py runserver and after a few minutes the project should run..
  since this project is an api the user there is no way to effectively manipulate of communicate with the project without he django admin panel so preferably to run this project we would need to also run the react front end created personally for this project located in my profile at the file Hireme-front-end


    
