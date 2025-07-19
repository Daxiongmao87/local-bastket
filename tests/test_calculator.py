import pytest
from src.calculator import Calculator

def test_add():
    calc = Calculator()
    assert calc.add(1, 2) == 3
    assert calc.add(-1, 1) == 0
    assert calc.add(-1, -1) == -2

def test_subtract():
    calc = Calculator()
    assert calc.subtract(2, 1) == 1
    assert calc.subtract(-1, 1) == -2
    assert calc.subtract(-1, -1) == 0

def test_multiply():
    calc = Calculator()
    assert calc.multiply(2, 3) == 6
    assert calc.multiply(-1, 1) == -1
    assert calc.multiply(-1, -1) == 1

def test_divide():
    calc = Calculator()
    assert calc.divide(4, 2) == 2
    with pytest.raises(ValueError):
        calc.divide(1, 0)