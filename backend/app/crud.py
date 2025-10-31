from sqlalchemy.orm import Session
from sqlalchemy import select, func
from typing import List, Optional
from datetime import datetime, timezone

from . import models, schemas


def create_prompt(db: Session, data: schemas.PromptCreate) -> models.Prompt:
    prompt = models.Prompt(title=data.title, content=data.content, tags=data.tags or "")
    db.add(prompt)
    db.commit()
    db.refresh(prompt)
    return prompt


def get_prompt(db: Session, prompt_id: int) -> Optional[models.Prompt]:
    return db.get(models.Prompt, prompt_id)


def list_prompts(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    q: Optional[str] = None,
    sort: Optional[str] = None,
) -> List[models.Prompt]:
    stmt = select(models.Prompt)
    if q:
        like = f"%{q}%"
        stmt = stmt.where(
            (models.Prompt.title.ilike(like)) | (models.Prompt.content.ilike(like)) | (models.Prompt.tags.ilike(like))
        )
    # sort pattern: field:dir, default created_at:desc
    field = "created_at"
    direction = "desc"
    if sort:
        try:
            f, d = sort.split(":", 1)
            if f in {"created_at", "updated_at", "title", "id"}:
                field = f
            if d.lower() in {"asc", "desc"}:
                direction = d.lower()
        except Exception:
            pass
    col = getattr(models.Prompt, field)
    stmt = stmt.order_by(col.asc() if direction == "asc" else col.desc())
    stmt = stmt.offset(skip).limit(limit)
    return list(db.execute(stmt).scalars().all())


def count_prompts(db: Session, q: Optional[str] = None) -> int:
    stmt = select(func.count(models.Prompt.id))
    if q:
        like = f"%{q}%"
        stmt = stmt.where(
            (models.Prompt.title.ilike(like)) | (models.Prompt.content.ilike(like)) | (models.Prompt.tags.ilike(like))
        )
    return int(db.execute(stmt).scalar_one())


def update_prompt(db: Session, prompt_id: int, data: schemas.PromptUpdate) -> Optional[models.Prompt]:
    prompt = db.get(models.Prompt, prompt_id)
    if not prompt:
        return None
    if data.title is not None:
        prompt.title = data.title
    if data.content is not None:
        prompt.content = data.content
    if data.tags is not None:
        prompt.tags = data.tags
    db.add(prompt)
    db.commit()
    db.refresh(prompt)
    return prompt


def delete_prompt(db: Session, prompt_id: int) -> bool:
    prompt = db.get(models.Prompt, prompt_id)
    if not prompt:
        return False
    db.delete(prompt)
    db.commit()
    return True


# 实习经历CRUD操作
def create_internship(db: Session, data: schemas.InternshipCreate) -> models.Internship:
    internship = models.Internship(
        group_title=data.group_title,
        company=data.company,
        position=data.position,
        start_date=data.start_date,
        end_date=data.end_date,
        description=data.description,
        skills=data.skills
    )
    db.add(internship)
    db.commit()
    db.refresh(internship)
    return internship


def get_internship(db: Session, internship_id: int) -> Optional[models.Internship]:
    return db.get(models.Internship, internship_id)


def list_internships(db: Session, skip: int = 0, limit: int = 100) -> List[models.Internship]:
    stmt = select(models.Internship).order_by(models.Internship.start_date.desc()).offset(skip).limit(limit)
    return list(db.execute(stmt).scalars().all())


def update_internship(db: Session, internship_id: int, data: schemas.InternshipUpdate) -> Optional[models.Internship]:
    internship = db.get(models.Internship, internship_id)
    if not internship:
        return None
    if data.group_title is not None:
        internship.group_title = data.group_title
    if data.company is not None:
        internship.company = data.company
    if data.position is not None:
        internship.position = data.position
    if data.start_date is not None:
        internship.start_date = data.start_date
    if data.end_date is not None:
        internship.end_date = data.end_date
    if data.description is not None:
        internship.description = data.description
    if data.skills is not None:
        internship.skills = data.skills
    db.add(internship)
    db.commit()
    db.refresh(internship)
    return internship


def delete_internship(db: Session, internship_id: int) -> bool:
    internship = db.get(models.Internship, internship_id)
    if not internship:
        return False
    db.delete(internship)
    db.commit()
    return True


# 项目经历CRUD操作
def create_project(db: Session, data: schemas.ProjectCreate) -> models.Project:
    project = models.Project(
        name=data.name,
        description=data.description,
        tech_stack=data.tech_stack,
        start_date=data.start_date,
        end_date=data.end_date,
        url=data.url
    )
    db.add(project)
    db.commit()
    db.refresh(project)
    return project


def get_project(db: Session, project_id: int) -> Optional[models.Project]:
    return db.get(models.Project, project_id)


def list_projects(db: Session, skip: int = 0, limit: int = 100) -> List[models.Project]:
    stmt = select(models.Project).order_by(models.Project.created_at.desc()).offset(skip).limit(limit)
    return list(db.execute(stmt).scalars().all())


def update_project(db: Session, project_id: int, data: schemas.ProjectUpdate) -> Optional[models.Project]:
    project = db.get(models.Project, project_id)
    if not project:
        return None
    if data.name is not None:
        project.name = data.name
    if data.description is not None:
        project.description = data.description
    if data.tech_stack is not None:
        project.tech_stack = data.tech_stack
    if data.start_date is not None:
        project.start_date = data.start_date
    if data.end_date is not None:
        project.end_date = data.end_date
    if data.url is not None:
        project.url = data.url
    db.add(project)
    db.commit()
    db.refresh(project)
    return project


def delete_project(db: Session, project_id: int) -> bool:
    project = db.get(models.Project, project_id)
    if not project:
        return False
    db.delete(project)
    db.commit()
    return True


# 技术栈CRUD操作
def create_tech_stack(db: Session, data: schemas.TechStackCreate) -> models.TechStack:
    tech_stack = models.TechStack(
        category=data.category,
        name=data.name,
        level=data.level,
        description=data.description
    )
    db.add(tech_stack)
    db.commit()
    db.refresh(tech_stack)
    return tech_stack


def get_tech_stack(db: Session, tech_stack_id: int) -> Optional[models.TechStack]:
    return db.get(models.TechStack, tech_stack_id)


def list_tech_stacks(db: Session, skip: int = 0, limit: int = 100) -> List[models.TechStack]:
    stmt = select(models.TechStack).order_by(models.TechStack.category.asc(), models.TechStack.name.asc()).offset(skip).limit(limit)
    return list(db.execute(stmt).scalars().all())


def update_tech_stack(db: Session, tech_stack_id: int, data: schemas.TechStackUpdate) -> Optional[models.TechStack]:
    tech_stack = db.get(models.TechStack, tech_stack_id)
    if not tech_stack:
        return None
    if data.category is not None:
        tech_stack.category = data.category
    if data.name is not None:
        tech_stack.name = data.name
    if data.level is not None:
        tech_stack.level = data.level
    if data.description is not None:
        tech_stack.description = data.description
    db.add(tech_stack)
    db.commit()
    db.refresh(tech_stack)
    return tech_stack


def delete_tech_stack(db: Session, tech_stack_id: int) -> bool:
    tech_stack = db.get(models.TechStack, tech_stack_id)
    if not tech_stack:
        return False
    db.delete(tech_stack)
    db.commit()
    return True


# 简历照片CRUD操作
def create_resume_photo(db: Session, data: schemas.ResumePhotoCreate) -> models.ResumePhoto:
    resume_photo = models.ResumePhoto(
        title=data.title,
        image_path=data.image_path
    )
    db.add(resume_photo)
    db.commit()
    db.refresh(resume_photo)
    return resume_photo


def get_resume_photo(db: Session, photo_id: int) -> Optional[models.ResumePhoto]:
    return db.get(models.ResumePhoto, photo_id)


def list_resume_photos(db: Session, skip: int = 0, limit: int = 100) -> List[models.ResumePhoto]:
    stmt = select(models.ResumePhoto).order_by(models.ResumePhoto.created_at.desc()).offset(skip).limit(limit)
    return list(db.execute(stmt).scalars().all())


def update_resume_photo(db: Session, photo_id: int, data: schemas.ResumePhotoUpdate) -> Optional[models.ResumePhoto]:
    resume_photo = db.get(models.ResumePhoto, photo_id)
    if not resume_photo:
        return None
    if data.title is not None:
        resume_photo.title = data.title
    if data.image_path is not None:
        resume_photo.image_path = data.image_path
    db.add(resume_photo)
    db.commit()
    db.refresh(resume_photo)
    return resume_photo


def delete_resume_photo(db: Session, photo_id: int) -> bool:
    resume_photo = db.get(models.ResumePhoto, photo_id)
    if not resume_photo:
        return False
    db.delete(resume_photo)
    db.commit()
    return True


# 岗位要求（JD）CRUD操作
def create_job_description(db: Session, data: schemas.JobDescriptionCreate) -> models.JobDescription:
    jd = models.JobDescription(
        company=data.company,
        position=data.position,
        image_paths=data.image_paths,
        description=data.description
    )
    db.add(jd)
    db.commit()
    db.refresh(jd)
    return jd


def get_job_description(db: Session, jd_id: int) -> Optional[models.JobDescription]:
    return db.get(models.JobDescription, jd_id)


def list_job_descriptions(db: Session, skip: int = 0, limit: int = 100) -> List[models.JobDescription]:
    stmt = select(models.JobDescription).order_by(models.JobDescription.created_at.desc()).offset(skip).limit(limit)
    return list(db.execute(stmt).scalars().all())


def update_job_description(db: Session, jd_id: int, data: schemas.JobDescriptionUpdate) -> Optional[models.JobDescription]:
    jd = db.get(models.JobDescription, jd_id)
    if not jd:
        return None
    if data.company is not None:
        jd.company = data.company
    if data.position is not None:
        jd.position = data.position
    if data.image_paths is not None:
        jd.image_paths = data.image_paths
    if data.description is not None:
        jd.description = data.description
    db.add(jd)
    db.commit()
    db.refresh(jd)
    return jd


def delete_job_description(db: Session, jd_id: int) -> bool:
    jd = db.get(models.JobDescription, jd_id)
    if not jd:
        return False
    db.delete(jd)
    db.commit()
    return True


# JD拆解CRUD操作
def create_jd_breakdown(db: Session, data: schemas.JdBreakdownCreate) -> models.JdBreakdown:
    breakdown = models.JdBreakdown(
        jd_id=data.jd_id,
        company=data.company,
        position=data.position,
        breakdown_content=data.breakdown_content
    )
    db.add(breakdown)
    db.commit()
    db.refresh(breakdown)
    return breakdown


def get_jd_breakdown(db: Session, breakdown_id: int) -> Optional[models.JdBreakdown]:
    return db.get(models.JdBreakdown, breakdown_id)


def list_jd_breakdowns(db: Session, skip: int = 0, limit: int = 100) -> List[models.JdBreakdown]:
    stmt = select(models.JdBreakdown).order_by(models.JdBreakdown.created_at.desc()).offset(skip).limit(limit)
    return list(db.execute(stmt).scalars().all())


def list_jd_breakdowns_by_jd(db: Session, jd_id: int) -> List[models.JdBreakdown]:
    stmt = select(models.JdBreakdown).where(models.JdBreakdown.jd_id == jd_id).order_by(models.JdBreakdown.created_at.desc())
    return list(db.execute(stmt).scalars().all())


def update_jd_breakdown(db: Session, breakdown_id: int, data: schemas.JdBreakdownUpdate) -> Optional[models.JdBreakdown]:
    breakdown = db.get(models.JdBreakdown, breakdown_id)
    if not breakdown:
        return None
    if data.company is not None:
        breakdown.company = data.company
    if data.position is not None:
        breakdown.position = data.position
    if data.breakdown_content is not None:
        breakdown.breakdown_content = data.breakdown_content
    db.add(breakdown)
    db.commit()
    db.refresh(breakdown)
    return breakdown


def delete_jd_breakdown(db: Session, breakdown_id: int) -> bool:
    breakdown = db.get(models.JdBreakdown, breakdown_id)
    if not breakdown:
        return False
    db.delete(breakdown)
    db.commit()
    return True


# OKR CRUD操作
def create_okr(db: Session, data: schemas.OKRCreate) -> models.OKR:
    okr = models.OKR(
        objective=data.objective,
        due_date=data.due_date
    )
    db.add(okr)
    db.commit()
    db.refresh(okr)
    return okr


def get_okr(db: Session, okr_id: int) -> Optional[models.OKR]:
    return db.get(models.OKR, okr_id)


def list_okrs(db: Session, skip: int = 0, limit: int = 100) -> List[models.OKR]:
    stmt = select(models.OKR).order_by(models.OKR.created_at.desc()).offset(skip).limit(limit)
    return list(db.execute(stmt).scalars().all())


def update_okr(db: Session, okr_id: int, data: schemas.OKRUpdate) -> Optional[models.OKR]:
    okr = db.get(models.OKR, okr_id)
    if not okr:
        return None
    if data.objective is not None:
        okr.objective = data.objective
    if data.completed is not None:
        okr.completed = data.completed
    if data.due_date is not None:
        okr.due_date = data.due_date
    db.add(okr)
    db.commit()
    db.refresh(okr)
    return okr


def delete_okr(db: Session, okr_id: int) -> bool:
    okr = db.get(models.OKR, okr_id)
    if not okr:
        return False
    db.delete(okr)
    db.commit()
    return True


def toggle_okr_completion(db: Session, okr_id: int, completed: bool) -> Optional[models.OKR]:
    okr = db.get(models.OKR, okr_id)
    if not okr:
        return None
    okr.completed = completed
    db.add(okr)
    db.commit()
    db.refresh(okr)
    return okr


# Task CRUD操作
def create_task(db: Session, data: schemas.TaskCreate) -> models.Task:
    task = models.Task(
        okr_id=data.okr_id,
        title=data.title,
        description=data.description
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


def get_task(db: Session, task_id: int) -> Optional[models.Task]:
    return db.get(models.Task, task_id)


def list_tasks_by_okr(db: Session, okr_id: int, skip: int = 0, limit: int = 100) -> List[models.Task]:
    stmt = select(models.Task).where(models.Task.okr_id == okr_id).order_by(models.Task.created_at.desc()).offset(skip).limit(limit)
    return list(db.execute(stmt).scalars().all())


def update_task(db: Session, task_id: int, data: schemas.TaskUpdate) -> Optional[models.Task]:
    task = db.get(models.Task, task_id)
    if not task:
        return None
    if data.title is not None:
        task.title = data.title
    if data.description is not None:
        task.description = data.description
    if data.completed is not None:
        task.completed = data.completed
    if data.okr_id is not None:
        task.okr_id = data.okr_id
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


def delete_task(db: Session, task_id: int) -> bool:
    task = db.get(models.Task, task_id)
    if not task:
        return False
    db.delete(task)
    db.commit()
    return True


def toggle_task_completion(db: Session, task_id: int, completed: bool) -> Optional[models.Task]:
    task = db.get(models.Task, task_id)
    if not task:
        return None
    task.completed = completed
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


# ==================== 面试题库 CRUD操作 ====================

# InterviewCategory CRUD
def create_interview_category(db: Session, data: schemas.InterviewCategoryCreate) -> models.InterviewCategory:
    category = models.InterviewCategory(
        name=data.name,
        order=data.order
    )
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


def get_interview_category(db: Session, category_id: int) -> Optional[models.InterviewCategory]:
    return db.get(models.InterviewCategory, category_id)


def list_interview_categories(db: Session, skip: int = 0, limit: int = 1000) -> List[models.InterviewCategory]:
    stmt = select(models.InterviewCategory).order_by(models.InterviewCategory.order.asc(), models.InterviewCategory.id.asc()).offset(skip).limit(limit)
    return list(db.execute(stmt).scalars().all())


def update_interview_category(db: Session, category_id: int, data: schemas.InterviewCategoryUpdate) -> Optional[models.InterviewCategory]:
    category = db.get(models.InterviewCategory, category_id)
    if not category:
        return None
    if data.name is not None:
        category.name = data.name
    if data.order is not None:
        category.order = data.order
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


def delete_interview_category(db: Session, category_id: int) -> bool:
    category = db.get(models.InterviewCategory, category_id)
    if not category:
        return False
    # 删除分类时，将关联的问题的 category_id 设为 None
    stmt = select(models.InterviewQuestion).where(models.InterviewQuestion.category_id == category_id)
    questions = db.execute(stmt).scalars().all()
    for question in questions:
        question.category_id = None
    db.delete(category)
    db.commit()
    return True


# InterviewQuestion CRUD
def create_interview_question(db: Session, data: schemas.InterviewQuestionCreate) -> models.InterviewQuestion:
    question = models.InterviewQuestion(
        description=data.description,
        category_id=data.category_id,
        company=data.company or "",
        tags=data.tags or "",
        difficulty=data.difficulty,
        round=data.round or ""
    )
    db.add(question)
    db.commit()
    db.refresh(question)
    return question


def get_interview_question(db: Session, question_id: int) -> Optional[models.InterviewQuestion]:
    return db.get(models.InterviewQuestion, question_id)


def list_interview_questions(
    db: Session, 
    skip: int = 0, 
    limit: int = 1000,
    category_id: Optional[int] = None
) -> List[models.InterviewQuestion]:
    stmt = select(models.InterviewQuestion)
    if category_id is not None:
        stmt = stmt.where(models.InterviewQuestion.category_id == category_id)
    stmt = stmt.order_by(models.InterviewQuestion.updated_at.desc()).offset(skip).limit(limit)
    return list(db.execute(stmt).scalars().all())


def update_interview_question(db: Session, question_id: int, data: schemas.InterviewQuestionUpdate) -> Optional[models.InterviewQuestion]:
    question = db.get(models.InterviewQuestion, question_id)
    if not question:
        return None
    if data.description is not None:
        question.description = data.description
    if data.category_id is not None:
        question.category_id = data.category_id
    if data.company is not None:
        question.company = data.company
    if data.tags is not None:
        question.tags = data.tags
    if data.difficulty is not None:
        question.difficulty = data.difficulty
    if data.round is not None:
        question.round = data.round
    db.add(question)
    db.commit()
    db.refresh(question)
    return question


def delete_interview_question(db: Session, question_id: int) -> bool:
    question = db.get(models.InterviewQuestion, question_id)
    if not question:
        return False
    # 删除问题时，同时删除关联的所有答案
    stmt = select(models.InterviewAnswer).where(models.InterviewAnswer.question_id == question_id)
    answers = db.execute(stmt).scalars().all()
    for answer in answers:
        db.delete(answer)
    db.delete(question)
    db.commit()
    return True


# InterviewAnswer CRUD
def create_interview_answer(db: Session, data: schemas.InterviewAnswerCreate) -> Optional[models.InterviewAnswer]:
    # 验证问题是否存在
    question = db.get(models.InterviewQuestion, data.question_id)
    if not question:
        return None
    answer = models.InterviewAnswer(
        question_id=data.question_id,
        content=data.content
    )
    db.add(answer)
    # 更新问题的 updated_at
    question.updated_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(answer)
    return answer


def get_interview_answer(db: Session, answer_id: int) -> Optional[models.InterviewAnswer]:
    return db.get(models.InterviewAnswer, answer_id)


def list_interview_answers_by_question(db: Session, question_id: int) -> List[models.InterviewAnswer]:
    stmt = select(models.InterviewAnswer).where(models.InterviewAnswer.question_id == question_id).order_by(models.InterviewAnswer.created_at.asc())
    return list(db.execute(stmt).scalars().all())


def update_interview_answer(db: Session, answer_id: int, data: schemas.InterviewAnswerUpdate) -> Optional[models.InterviewAnswer]:
    answer = db.get(models.InterviewAnswer, answer_id)
    if not answer:
        return None
    if data.content is not None:
        answer.content = data.content
        # 更新关联问题的 updated_at
        question = db.get(models.InterviewQuestion, answer.question_id)
        if question:
            question.updated_at = datetime.now(timezone.utc)
    db.add(answer)
    db.commit()
    db.refresh(answer)
    return answer


def delete_interview_answer(db: Session, answer_id: int) -> bool:
    answer = db.get(models.InterviewAnswer, answer_id)
    if not answer:
        return False
    question_id = answer.question_id
    db.delete(answer)
    # 更新关联问题的 updated_at
    question = db.get(models.InterviewQuestion, question_id)
    if question:
        question.updated_at = datetime.now(timezone.utc)
    db.commit()
    return True


# ==================== 观点记录 CRUD操作 ====================

# OpinionCategory CRUD
def create_opinion_category(db: Session, data: schemas.OpinionCategoryCreate) -> models.OpinionCategory:
    category = models.OpinionCategory(
        name=data.name,
        order=data.order
    )
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


def get_opinion_category(db: Session, category_id: int) -> Optional[models.OpinionCategory]:
    return db.get(models.OpinionCategory, category_id)


def list_opinion_categories(db: Session, skip: int = 0, limit: int = 1000) -> List[models.OpinionCategory]:
    stmt = select(models.OpinionCategory).order_by(models.OpinionCategory.order.asc(), models.OpinionCategory.id.asc()).offset(skip).limit(limit)
    return list(db.execute(stmt).scalars().all())


def update_opinion_category(db: Session, category_id: int, data: schemas.OpinionCategoryUpdate) -> Optional[models.OpinionCategory]:
    category = db.get(models.OpinionCategory, category_id)
    if not category:
        return None
    if data.name is not None:
        category.name = data.name
    if data.order is not None:
        category.order = data.order
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


def delete_opinion_category(db: Session, category_id: int) -> bool:
    category = db.get(models.OpinionCategory, category_id)
    if not category:
        return False
    # 删除分类时，将关联的观点 category_id 设为 None
    stmt = select(models.Opinion).where(models.Opinion.category_id == category_id)
    opinions = db.execute(stmt).scalars().all()
    for opinion in opinions:
        opinion.category_id = None
    db.delete(category)
    db.commit()
    return True


# Opinion CRUD
def create_opinion(db: Session, data: schemas.OpinionCreate) -> models.Opinion:
    opinion = models.Opinion(
        description=data.description,
        category_id=data.category_id
    )
    db.add(opinion)
    db.commit()
    db.refresh(opinion)
    return opinion


def get_opinion(db: Session, opinion_id: int) -> Optional[models.Opinion]:
    return db.get(models.Opinion, opinion_id)


def list_opinions(
    db: Session, 
    skip: int = 0, 
    limit: int = 1000,
    category_id: Optional[int] = None
) -> List[models.Opinion]:
    stmt = select(models.Opinion)
    if category_id is not None:
        stmt = stmt.where(models.Opinion.category_id == category_id)
    stmt = stmt.order_by(models.Opinion.updated_at.desc()).offset(skip).limit(limit)
    return list(db.execute(stmt).scalars().all())


def update_opinion(db: Session, opinion_id: int, data: schemas.OpinionUpdate) -> Optional[models.Opinion]:
    opinion = db.get(models.Opinion, opinion_id)
    if not opinion:
        return None
    if data.description is not None:
        opinion.description = data.description
    if data.category_id is not None:
        opinion.category_id = data.category_id
    db.add(opinion)
    db.commit()
    db.refresh(opinion)
    return opinion


def delete_opinion(db: Session, opinion_id: int) -> bool:
    opinion = db.get(models.Opinion, opinion_id)
    if not opinion:
        return False
    db.delete(opinion)
    db.commit()
    return True


