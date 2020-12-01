# BankID-Test
Test application for Swedish bankID Integration with django

**Run using docker**
```
docker pull saipranavk/bankid_test
```
**or**
```
pip install requirements.txt
python manage.py runserver
```

**IMPORTANT**: This project requires a Swedish BankID test account and app on your mobile device. Also, the test certificate used for this project might be outdated at the time of access. Please download the latest version of mobile application and test certificate from Swedish BankID API documentation https://www.bankid.com/utvecklare/rp-info. Please follow the instructions on the website to create a test account. 