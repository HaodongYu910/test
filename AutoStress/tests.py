from django.test import TestCase

# Create your tests here.
import datetime
a = datetime.datetime.now() + datetime.timedelta(minutes=int(1))
while True:
    b= datetime.datetime.now()
    if  b> a:
        print("大于")
        break
    else:
        print(b)