from django.test import TestCase

# Create your tests here.

def add(a: int , b: int) -> int:
    return a + b
def subtract(a: int, b: int) -> int:
    return a - b
def multiply(a: int, b: int) -> int:
    return a * b
def divide(a: int, b: int) -> int:
    return a / b

class OperationTest(TestCase):
    def test_op(self):
        assert add(3,3) == 6
        assert add(5,4) == 9
        assert subtract(5,2) == 3
        assert multiply(10,10) == 100
        assert divide(100,1) == 100