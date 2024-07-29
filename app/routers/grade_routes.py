from fastapi import APIRouter
from fastapi import Request
from sqlalchemy import select, desc
from starlette import status
from starlette.responses import JSONResponse

from app.models.models import GradeResponse, APIResponse, GradeBase, SubjectStats, StudentStats
from app.schemas.grade_schemas import Grade

router = APIRouter(prefix='/grades', tags=["Grade"])


@router.post("/", response_model=APIResponse[GradeResponse],
             status_code=status.HTTP_201_CREATED,
             responses={422: {"model": APIResponse[None], "description": "Validation Error"}})
async def submit_grade(request: Request, grade: GradeBase):
    db = request.scope['session']
    new_grade = Grade(student_id=grade.student_id, subject_id=grade.subject_id, grade=grade.grade)
    db.add(new_grade)
    await db.flush()
    await db.commit()
    await db.refresh(new_grade)
    return APIResponse[GradeResponse](data=new_grade)


@router.get("/subject/{subject_id}/",
            response_model=APIResponse[SubjectStats],
            status_code=status.HTTP_200_OK, summary='Get Subject Stats',
            responses={404: {"model": APIResponse[None], "description": "Subject not found"},
                       422: {"model": APIResponse[None], "description": "Validation Error"}})
async def get_grades_by_subject(request: Request, subject_id: int):
    if subject_id < 1:
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=APIResponse(error='Subject ID must be greater than 0').model_dump()
        )

    db = request.scope['session']
    query = (
        select(Grade.grade, Grade.student_id)
        .where(Grade.subject_id == subject_id)
        .order_by(Grade.student_id, desc(Grade.created_at))
    ).distinct(Grade.student_id)
    result = await db.execute(query)
    grades = result.fetchall()

    if not grades:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=APIResponse(error='No grades found for this subject').model_dump()
        )

    grades_numeric = [grade[0] for grade in grades]
    stats = SubjectStats.calculate_stats(grades_numeric)
    return APIResponse[SubjectStats](data=stats)


@router.get("/student/{student_id}",
            response_model=APIResponse[StudentStats],
            status_code=status.HTTP_200_OK,
            responses={404: {"model": APIResponse[None], "description": "Student not found"},
                       422: {"model": APIResponse[None], "description": "Validation Error"}})
async def get_grades_by_student(request: Request, student_id: int):
    if student_id < 1:
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=APIResponse(error='Student ID must be greater than 0').model_dump()
        )

    db = request.scope['session']
    query = (
        select(Grade)
        .where(Grade.student_id == student_id)
        .order_by(Grade.subject_id, desc(Grade.created_at))
    ).distinct(Grade.subject_id)
    result = await db.execute(query)
    grades = result.scalars().all()

    if not grades:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=APIResponse(error='No grades found for this student').model_dump()
        )

    stats = StudentStats.get_student_stats(grades)

    return APIResponse[StudentStats](
        data=stats
    )
