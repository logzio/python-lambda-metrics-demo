FROM amazon/aws-lambda-python:3.8
ADD requirements.txt requirements.txt
ADD app.py ./
RUN yum update -y
RUN yum install -y snappy-devel
RUN pip install -r requirements.txt

CMD ["app.handler"]

