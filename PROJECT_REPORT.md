
# School Management System (SMS) - Project Report

## Project Overview

The School Management System (SMS) is a comprehensive web-based application built with Flask that manages various aspects of educational institutions. The system provides complete functionality for managing students, teachers, courses, enrollments, and a sophisticated quiz/assessment system with automated grading capabilities.

## Architecture

The application follows a layered architecture pattern with clear separation of concerns:

1. **API Layer** (`app/api/`): Handles HTTP requests/responses, input validation, and routing
2. **Business Logic Layer** (`app/blc/`): Contains the business logic and rules
3. **Repository Layer** (`app/repository/`): Responsible for database operations
4. **Schema Layer** (`app/schema/`): Defines data models and validation rules
5. **Configuration** (`app/config.py`): Manages environment variables and application configuration

## Key Features Implemented

1. **Student Management**
   - Complete CRUD operations for student records
   - Data validation for student attributes (e.g., grade must be between 1-12)
   - Automatic deletion of related enrollments when a student is deleted

2. **Teacher Management**
   - Complete CRUD operations for teacher records
   - Storage of teacher qualifications and contact information

3. **Course Management**
   - Creation and management of courses with assigned teachers
   - Support for course descriptions, credit values, and student capacity limits

4. **Enrollment System**
   - Track which students are enrolled in which courses
   - Maintain enrollment status and student grades
   - View enrollments by student or by course

5. **Quiz Management System**
   - Complete quiz creation and management for teachers
   - Multiple question types support (multiple choice, text, etc.)
   - Quiz scheduling with start and end dates
   - Student quiz submission and grading system
   - Automatic grade calculation and results tracking
   - Quiz results and analytics for teachers

6. **User Authentication System**
   - User registration (signup) functionality
   - Login with JWT token-based authentication
   - Secure password hashing
   - Token expiration management

7. **Database Integration**
   - SQLite database integration with SQLAlchemy ORM
   - Proper relationship mapping between entities
   - Transaction support for data consistency

8. **Input Validation & Error Handling**
   - Request data validation using webargs and marshmallow schemas
   - Consistent error responses with appropriate HTTP status codes
   - Proper exception handling throughout the application

## API Endpoints

### Root API
- `GET /` - Welcome message and API status

### User Authentication APIs
- `POST /signup` - Register a new user account
- `POST /login` - Login and receive JWT authentication token

### Student APIs
- `GET /students/list` - Retrieve all students
- `GET /students/detail/<id>` - Get a specific student by ID
- `POST /students/create` - Create a new student
- `PUT /students/update/<id>` - Update a student's information
- `DELETE /students/delete/<id>` - Delete a student and their enrollments

### Teacher APIs
- `GET /teachers/list` - Retrieve all teachers
- `GET /teachers/detail/<id>` - Get a specific teacher by ID
- `POST /teachers/create` - Create a new teacher
- `PUT /teachers/update/<id>` - Update a teacher's information
- `DELETE /teachers/delete/<id>` - Delete a teacher

### Course APIs
- `GET /courses/list` - Retrieve all courses
- `GET /courses/detail/<id>` - Get a specific course by ID
- `POST /courses/create` - Create a new course
- `PUT /courses/update/<id>` - Update a course
- `DELETE /courses/delete/<id>` - Delete a course

### Enrollment APIs
- `GET /enrollments/list` - Retrieve all enrollments
- `GET /enrollments/by-student/<student_id>` - Get all enrollments for a specific student
- `GET /enrollments/by-course/<course_id>` - Get all enrollments for a specific course
- `POST /enrollments/create` - Create a new enrollment
- `PUT /enrollments/update/<id>` - Update an enrollment (status, grade)
- `DELETE /enrollments/delete/<id>` - Delete an enrollment

### Quiz Management APIs (Teacher)
- `POST /quizzes/create` - Create a new quiz
- `GET /quizzes/<quiz_id>` - Get quiz details with questions
- `GET /quizzes/course/<course_id>` - Get all quizzes for a specific course
- `PUT /quizzes/<quiz_id>` - Update quiz information
- `DELETE /quizzes/<quiz_id>` - Delete a quiz

### Quiz Question APIs (Teacher)
- `POST /quizzes/<quiz_id>/questions` - Add questions to a quiz
- `GET /quizzes/<quiz_id>/questions` - Get all questions for a quiz
- `PUT /quizzes/questions/<question_id>` - Update a specific question
- `DELETE /quizzes/questions/<question_id>` - Delete a specific question

### Quiz Student APIs (Student)
- `GET /quizzes/student/<student_id>/course/<course_id>/available` - Get available quizzes for a student in a course
- `GET /quizzes/student/<student_id>/quiz/<quiz_id>/preview` - Preview quiz before starting
- `POST /quizzes/student/<student_id>/submit/<quiz_id>` - Submit quiz answers

### Quiz Grading APIs (Teacher)
- `GET /quizzes/<quiz_id>/submissions` - Get all submissions for a quiz
- `GET /quizzes/submissions/<submission_id>/answers` - View detailed submission answers
- `POST /quizzes/submissions/<submission_id>/grade` - Grade a quiz submission

### Quiz Results APIs
- `GET /quizzes/<quiz_id>/results` - Get all results for a quiz
- `GET /quizzes/submissions/<submission_id>/result` - Get result for a specific submission
- `GET /quizzes/student/<student_id>/course/<course_id>/results` - Get all quiz results for a student in a course






