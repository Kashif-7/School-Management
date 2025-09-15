from datetime import datetime, timezone
from app.extension import db


class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, onupdate=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f'<User {self.username}>'


class Student(db.Model):
    __tablename__ = 'students'
    
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    grade = db.Column(db.Integer, nullable=False)
    address = db.Column(db.String(200))
    phone = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, onupdate=lambda: datetime.now(timezone.utc))
  
    enrollments = db.relationship('Enrollment', back_populates='student', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Student {self.first_name} {self.last_name}>'


class Teacher(db.Model):
    __tablename__ = 'teachers'
    
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    subject = db.Column(db.String(100), nullable=False)
    qualification = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, onupdate=lambda: datetime.now(timezone.utc))

    courses = db.relationship('Course', back_populates='teacher')
    
    def __repr__(self):
        return f'<Teacher {self.first_name} {self.last_name}>'


class Course(db.Model):
    __tablename__ = 'courses'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    credits = db.Column(db.Integer, nullable=False)
    max_students = db.Column(db.Integer, default=30)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, onupdate=lambda: datetime.now(timezone.utc))

    teacher = db.relationship('Teacher', back_populates='courses')
    enrollments = db.relationship('Enrollment', back_populates='course', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Course {self.name}>'


class Enrollment(db.Model):
    __tablename__ = 'enrollments'
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    enrollment_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20), default='active')  # active, completed, dropped
    grade = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, onupdate=lambda: datetime.now(timezone.utc))

    student = db.relationship('Student', back_populates='enrollments')
    course = db.relationship('Course', back_populates='enrollments')
    
    def __repr__(self):
        return f'<Enrollment {self.student_id} in {self.course_id}>'






class Quiz(db.Model):
    __tablename__ = 'quizzes'
    
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    total_marks = db.Column(db.Float, nullable=False, default=10.0)
    duration_minutes = db.Column(db.Integer, default=30)  # Quiz duration in minutes
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, onupdate=lambda: datetime.now(timezone.utc))

    course = db.relationship('Course', backref='quizzes')
    questions = db.relationship('QuizQuestion', back_populates='quiz', cascade='all, delete-orphan')
    submissions = db.relationship('QuizSubmission', back_populates='quiz', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Quiz {self.title} for {self.course.name}>'


class QuizQuestion(db.Model):
    __tablename__ = 'quiz_questions'
    
    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizzes.id'), nullable=False)
    question_text = db.Column(db.Text, nullable=False)
    question_type = db.Column(db.String(20), nullable=False)  # multiple_choice, true_false, text
    option_a = db.Column(db.String(500))  # For multiple choice
    option_b = db.Column(db.String(500))
    option_c = db.Column(db.String(500))
    option_d = db.Column(db.String(500))
    correct_answer = db.Column(db.String(500), nullable=False)  # A, B, C, D for MC, True/False, or text
    marks = db.Column(db.Float, default=1.0)
    order_number = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    quiz = db.relationship('Quiz', back_populates='questions')
    answers = db.relationship('QuizAnswer', back_populates='question', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<QuizQuestion {self.order_number} for {self.quiz.title}>'


class QuizSubmission(db.Model):
    __tablename__ = 'quiz_submissions'
    
    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizzes.id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    submitted_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    time_taken_minutes = db.Column(db.Integer)  # Actual time taken
    is_completed = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    quiz = db.relationship('Quiz', back_populates='submissions')
    student = db.relationship('Student', backref='quiz_submissions')
    answers = db.relationship('QuizAnswer', back_populates='submission', cascade='all, delete-orphan')
    result = db.relationship('QuizResult', back_populates='submission', uselist=False, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<QuizSubmission {self.student_id} for {self.quiz.title}>'


class QuizAnswer(db.Model):
    __tablename__ = 'quiz_answers'
    
    id = db.Column(db.Integer, primary_key=True)
    submission_id = db.Column(db.Integer, db.ForeignKey('quiz_submissions.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('quiz_questions.id'), nullable=False)
    student_answer = db.Column(db.Text, nullable=False)  # Student's answer
    is_correct = db.Column(db.Boolean)  # Will be populated after grading
    marks_obtained = db.Column(db.Float, default=0.0)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    submission = db.relationship('QuizSubmission', back_populates='answers')
    question = db.relationship('QuizQuestion', back_populates='answers')
    
    def __repr__(self):
        return f'<QuizAnswer {self.question_id} by {self.submission.student_id}>'


class QuizResult(db.Model):
    __tablename__ = 'quiz_results'
    
    id = db.Column(db.Integer, primary_key=True)
    submission_id = db.Column(db.Integer, db.ForeignKey('quiz_submissions.id'), nullable=False)
    total_marks = db.Column(db.Float, nullable=False)
    marks_obtained = db.Column(db.Float, nullable=False)
    percentage = db.Column(db.Float, nullable=False)
    grade = db.Column(db.String(5))  # A+, A, B+, B, C+, C, D, F
    feedback = db.Column(db.Text)
    graded_by_teacher = db.Column(db.Boolean, default=False)
    graded_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, onupdate=lambda: datetime.now(timezone.utc))

    submission = db.relationship('QuizSubmission', back_populates='result')
    
    def __repr__(self):
        return f'<QuizResult {self.marks_obtained}/{self.total_marks} for submission {self.submission_id}>'
