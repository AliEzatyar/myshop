from django.test import TestCase

# Create your tests here.

x = {23:"324","3432":3432}
y = x
x[23] = "3433333"
print(x,y)