FROM python:3.6
ENV PYTHONUNBUFFERED=1
RUN mkdir /bankid_test
WORKDIR /bankid_test
COPY requirements.txt /bankid_test/
RUN pip install -r requirements.txt
COPY . /bankid_test/

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]