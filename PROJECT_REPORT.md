
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

5. **Database Integration**
   - MongoDB integration with transaction support (sessions)
   - Custom JSON serialization to handle MongoDB-specific data types (ObjectId, dates)

6. **Input Validation & Error Handling**
   - Request data validation using webargs and marshmallow schemas
   - Consistent error responses with appropriate HTTP status codes
   - Proper exception handling throughout the application

## API Endpoints

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





