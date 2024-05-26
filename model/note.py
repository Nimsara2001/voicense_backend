from typing import Optional
from bson import ObjectId
from pydantic import BaseModel, Field


class Note(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    title: str = Field(...)
    description: str = Field(...)  # show in the note view card
    content: str = Field(...)
    created_date: str
    last_accessed: str

    class Config:
        json_schema_extra = {
            "example": {
                "_id": "60d5ec88b35866cc8fe16e6e",
                "title": "Python Programming",
                "description": "Python is a programming language that lets you work quickly and integrate systems more effectively.",
                "content": """
# Python Programming Lecture Notes

## Introduction to Python

### What is Python?
- Python is a high-level, interpreted programming language.
- It was created by Guido van Rossum and first released in 1991.

### Why Python?
- Python is easy to learn and read, making it great for beginners.
- It has a large and active community, with extensive documentation and support.
- Python is versatile, used in web development, data analysis, artificial intelligence, and more.
- It promotes code readability and encourages good programming practices.

### Getting Started with Python
- Installing Python
- Using Python IDEs (Integrated Development Environments) like PyCharm, VSCode, or Jupyter Notebook.
- Writing and running your first Python script.

## Python Basics

### Variables and Data Types
- Variables: Containers for storing data values.
- Data Types: Integers, Floats, Strings, Booleans, Lists, Tuples, Sets, Dictionaries.
- Dynamic Typing: Python automatically assigns the appropriate data type to variables.

### Operators
- Arithmetic Operators: +, -, *, /, %, ** (exponentiation).
- Comparison Operators: ==, !=, <, >, <=, >=.
- Logical Operators: and, or, not.

### Control Flow
- Conditional Statements: if, elif, else.
- Loops: for loops, while loops.
- Loop Control Statements: break, continue.

## Functions and Modules

### Functions
- Defining Functions: def keyword.
- Parameters and Arguments.
- Return Statement.

### Modules
- Importing Modules: import statement.
- Creating and using custom modules.
- Standard Library Modules: math, random, datetime, etc.

## Object-Oriented Programming (OOP) in Python

### Classes and Objects
- Defining Classes: class keyword.
- Class Attributes and Methods.
- Creating Objects (Instances) of a Class.

### Inheritance
- Extending Classes: Inheriting from a parent class.
- Overriding Methods.

### Encapsulation and Polymorphism
- Encapsulation: Hiding data within objects.
- Polymorphism: The ability of objects to take on different forms.

## Advanced Topics

### Exception Handling
- Handling Errors and Exceptions: try, except, else, finally blocks.

### File Handling
- Opening, Reading, Writing, and Closing Files.
- Using Context Managers (with statement).

### Regular Expressions (Regex)
- Pattern Matching with Regex.

### Decorators
- Modifying or Extending the Behavior of Functions or Methods.

## Conclusion
- Python is a powerful and versatile programming language with a wide range of applications.
- These lecture notes provide a foundation for further exploration into Python programming.
""",
                "created_date": "2021-06-01",
                "last_accessed": "2021-06-01",
            }
        }

