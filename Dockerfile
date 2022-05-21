FROM fnndsc/ubuntu-python3

RUN ["pip","install","--upgrade","pip"]

RUN ["pip3","install","django","djangorestframework","pandas","numpy","scikit-learn==1.0.2","lightgbm","django-cors-headers"]

RUN ["apt","-y","update"]

RUN ["apt","-y","upgrade"]

ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Asia/Seoul

RUN apt-get install -y tzdata

COPY . .

#RUN ["git","clone","https://github.com/FeelSoftwareConvergence/FeelSoftwareDjango.git"]

# WORKDIR ./FeelSoftwareDjango

ENTRYPOINT ["python", "manage.py", "runserver", "0:8000"]
EXPOSE 8000