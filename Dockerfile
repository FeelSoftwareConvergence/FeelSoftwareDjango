FROM fnndsc/ubuntu-python3

RUN ["pip","install","--upgrade","pip"]

RUN ["pip3","install","django","djangorestframework","pandas","numpy","scikit-learn","lightgbm","django-cors-headers"]

COPY . .

ENTRYPOINT ["python", "manage.py", "runserver", "0:8000"]
EXPOSE 8000