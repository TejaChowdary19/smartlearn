# Python Programming Examples and Patterns

## Basic Data Structures

### List Comprehensions
# Traditional way
squares = []
for i in range(10):
    squares.append(i**2)

# List comprehension
squares = [i**2 for i in range(10)]
even_squares = [i**2 for i in range(10) if i % 2 == 0]

### Dictionary Comprehensions
# Create dictionary from lists
names = ['Alice', 'Bob', 'Charlie']
ages = [25, 30, 35]
people = {name: age for name, age in zip(names, ages)}

# Filter dictionary
adults = {name: age for name, age in people.items() if age >= 18}

## Object-Oriented Programming

### Class with Properties
class Student:
    def __init__(self, name, age):
        self._name = name
        self._age = age
    
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise ValueError("Name must be a string")
        self._name = value
    
    @property
    def age(self):
        return self._age
    
    @age.setter
    def age(self, value):
        if not isinstance(value, int) or value < 0:
            raise ValueError("Age must be a positive integer")
        self._age = value

### Singleton Pattern
class DatabaseConnection:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.connection = None
        return cls._instance
    
    def connect(self):
        if not self.connection:
            self.connection = "Connected to database"
        return self.connection

## Functional Programming

### Higher-Order Functions
def apply_operation(func, numbers):
    return [func(num) for num in numbers]

def square(x):
    return x ** 2

def cube(x):
    return x ** 3

# Usage
numbers = [1, 2, 3, 4, 5]
squared = apply_operation(square, numbers)
cubed = apply_operation(cube, numbers)

### Lambda Functions
# Simple lambda
add = lambda x, y: x + y

# Lambda with map
numbers = [1, 2, 3, 4, 5]
doubled = list(map(lambda x: x * 2, numbers))

# Lambda with filter
evens = list(filter(lambda x: x % 2 == 0, numbers))

## Error Handling

### Context Managers
class FileManager:
    def __init__(self, filename, mode):
        self.filename = filename
        self.mode = mode
        self.file = None
    
    def __enter__(self):
        self.file = open(self.filename, self.mode)
        return self.file
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.file:
            self.file.close()

# Usage
with FileManager('test.txt', 'w') as f:
    f.write('Hello, World!')

### Custom Exceptions
class ValidationError(Exception):
    def __init__(self, message, field=None):
        self.message = message
        self.field = field
        super().__init__(self.message)

def validate_email(email):
    if '@' not in email:
        raise ValidationError("Invalid email format", "email")
    if '.' not in email.split('@')[1]:
        raise ValidationError("Invalid domain", "email")
    return True

## Data Processing

### CSV Processing
import csv

def read_csv_data(filename):
    data = []
    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.append(row)
    return data

def write_csv_data(filename, data, fieldnames):
    with open(filename, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

### JSON Processing
import json

def load_json_config(filename):
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        return {}

def save_json_config(filename, data):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=2)

## Algorithm Implementations

### Binary Search
def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return -1

### Quick Sort
def quicksort(arr):
    if len(arr) <= 1:
        return arr
    
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    
    return quicksort(left) + middle + quicksort(right)

## Web Development

### Flask Route Example
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/api/users', methods=['GET'])
def get_users():
    users = [
        {'id': 1, 'name': 'Alice', 'email': 'alice@example.com'},
        {'id': 2, 'name': 'Bob', 'email': 'bob@example.com'}
    ]
    return jsonify(users)

@app.route('/api/users', methods=['POST'])
def create_user():
    data = request.get_json()
    
    if not data or 'name' not in data or 'email' not in data:
        return jsonify({'error': 'Missing required fields'}), 400
    
    # Process user creation
    new_user = {
        'id': 3,  # In real app, generate unique ID
        'name': data['name'],
        'email': data['email']
    }
    
    return jsonify(new_user), 201

## Testing

### Unit Test Example
import unittest

class Calculator:
    def add(self, a, b):
        return a + b
    
    def subtract(self, a, b):
        return a - b
    
    def multiply(self, a, b):
        return a * b
    
    def divide(self, a, b):
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b

class TestCalculator(unittest.TestCase):
    def setUp(self):
        self.calc = Calculator()
    
    def test_add(self):
        self.assertEqual(self.calc.add(3, 5), 8)
        self.assertEqual(self.calc.add(-1, 1), 0)
    
    def test_divide_by_zero(self):
        with self.assertRaises(ValueError):
            self.calc.divide(10, 0)

if __name__ == '__main__':
    unittest.main()
