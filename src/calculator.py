class Calculator:
    """
    A simple calculator class that performs basic arithmetic operations.
    """

    def add(self, a: float, b: float) -> float:
        """Add two numbers."""
        return a + b

    def subtract(self, a: float, b: float) -> float:
        """Subtract the second number from the first."""
        return a - b

    def multiply(self, a: float, b: float) -> float:
        """Multiply two numbers."""
        return a * b

    def divide(self, a: float, b: float) -> float:
        """
        Divide the first number by the second.
        Raises an error if the second number is zero.
        """
        if b == 0:
            raise ValueError("Cannot divide by zero.")
        return a / b