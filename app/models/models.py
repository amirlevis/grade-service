from datetime import datetime
from typing import TypeVar, Generic, Optional, List

from pydantic import BaseModel, Field, field_validator
from pydantic_core.core_schema import ValidationInfo

DataT = TypeVar("DataT")


class APIResponse(BaseModel, Generic[DataT]):
    data: Optional[DataT] = Field(None)
    error: Optional[str] = Field(None, description="Error message if an error occurred")


class GradeBase(BaseModel):
    student_id: int
    subject_id: int
    grade: int

    @field_validator('student_id', 'subject_id')
    def check_greater_than_zero(cls, v: int, info: ValidationInfo) -> int:
        if v <= 0:
            raise ValueError(f'{info.field_name} must be greater than zero')
        return v

    @field_validator('grade')
    def grade_range(cls, v: int, info: ValidationInfo) -> int:
        if 0 <= v <= 100:
            return v
        else:
            raise ValueError(f"{ValidationInfo.field_name} must be a value between 0 and 100.")


class SubjectStats(BaseModel):
    num_students: int
    average_grade: float
    median_grade: float

    @staticmethod
    def calculate_stats(grades: List[int]) -> 'SubjectStats':
        if not grades:
            return SubjectStats(num_students=0, average_grade=0.0, median_grade=0.0, grades=grades)

        num_students = len(grades)
        average_grade = sum(grades) / num_students

        sorted_grades = sorted(grades)
        if num_students % 2 == 0:
            median_grade = sum(sorted_grades[num_students // 2 - 1: num_students // 2 + 1]) / 2
        else:
            median_grade = sorted_grades[num_students // 2]

        return SubjectStats(num_students=num_students, average_grade=average_grade, median_grade=median_grade)


class StudentStats(BaseModel):
    average_grade: float
    student_grades: List['StudentGrade'] = Field(..., description="Statistics for each subject")

    @staticmethod
    def get_student_stats(grades: List[GradeBase]) -> 'StudentStats':
        students_grades = [StudentGrade(subject_id=grade.subject_id, grade=grade.grade) for grade in grades]
        average_grade = sum(map(lambda student: student.grade, students_grades)) / len(students_grades)

        return StudentStats(average_grade=average_grade, student_grades=students_grades)


class StudentGrade(BaseModel):
    subject_id: int
    grade: int


class GradeResponse(BaseModel):
    id: int
    student_id: int
    subject_id: int
    grade: int
    created_at: datetime

    class Config:
        from_attributes = True
