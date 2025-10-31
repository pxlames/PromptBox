from fastapi import APIRouter, Depends, HTTPException, Query, File, UploadFile
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel
import json

from .db import get_db
from . import schemas, crud
from .llm_service import get_llm_service


router = APIRouter(prefix="/prompts", tags=["prompts"])
resume_router = APIRouter(prefix="/resume", tags=["resume"])


@router.post("/", response_model=schemas.PromptOut)
def create_prompt(data: schemas.PromptCreate, db: Session = Depends(get_db)):
    return crud.create_prompt(db, data)


@router.get("/", response_model=List[schemas.PromptOut])
def get_prompts(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=1000),
    q: str | None = Query(None, description="fuzzy search in title/content/tags"),
    sort: str | None = Query("created_at:desc", description="field:dir e.g., created_at:desc"),
    db: Session = Depends(get_db),
):
    return crud.list_prompts(db, skip=skip, limit=limit, q=q, sort=sort)


@router.get("/count")
def get_prompts_count(
    q: str | None = Query(None, description="fuzzy search in title/content/tags"),
    db: Session = Depends(get_db),
):
    return {"total": crud.count_prompts(db, q=q)}


@router.get("/{prompt_id}", response_model=schemas.PromptOut)
def get_prompt(prompt_id: int, db: Session = Depends(get_db)):
    prompt = crud.get_prompt(db, prompt_id)
    if not prompt:
        raise HTTPException(status_code=404, detail="Prompt not found")
    return prompt


@router.put("/{prompt_id}", response_model=schemas.PromptOut)
def update_prompt(prompt_id: int, data: schemas.PromptUpdate, db: Session = Depends(get_db)):
    prompt = crud.update_prompt(db, prompt_id, data)
    if not prompt:
        raise HTTPException(status_code=404, detail="Prompt not found")
    return prompt


@router.delete("/{prompt_id}", status_code=204)
def delete_prompt(prompt_id: int, db: Session = Depends(get_db)):
    ok = crud.delete_prompt(db, prompt_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Prompt not found")
    return None


# 实习经历API
@resume_router.post("/internships/", response_model=schemas.InternshipOut)
def create_internship(data: schemas.InternshipCreate, db: Session = Depends(get_db)):
    return crud.create_internship(db, data)


@resume_router.get("/internships/", response_model=List[schemas.InternshipOut])
def get_internships(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
):
    return crud.list_internships(db, skip=skip, limit=limit)


@resume_router.get("/internships/{internship_id}", response_model=schemas.InternshipOut)
def get_internship(internship_id: int, db: Session = Depends(get_db)):
    internship = crud.get_internship(db, internship_id)
    if not internship:
        raise HTTPException(status_code=404, detail="Internship not found")
    return internship


@resume_router.put("/internships/{internship_id}", response_model=schemas.InternshipOut)
def update_internship(internship_id: int, data: schemas.InternshipUpdate, db: Session = Depends(get_db)):
    internship = crud.update_internship(db, internship_id, data)
    if not internship:
        raise HTTPException(status_code=404, detail="Internship not found")
    return internship


@resume_router.delete("/internships/{internship_id}", status_code=204)
def delete_internship(internship_id: int, db: Session = Depends(get_db)):
    ok = crud.delete_internship(db, internship_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Internship not found")
    return None


# 项目经历API
@resume_router.post("/projects/", response_model=schemas.ProjectOut)
def create_project(data: schemas.ProjectCreate, db: Session = Depends(get_db)):
    return crud.create_project(db, data)


@resume_router.get("/projects/", response_model=List[schemas.ProjectOut])
def get_projects(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
):
    return crud.list_projects(db, skip=skip, limit=limit)


@resume_router.get("/projects/{project_id}", response_model=schemas.ProjectOut)
def get_project(project_id: int, db: Session = Depends(get_db)):
    project = crud.get_project(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@resume_router.put("/projects/{project_id}", response_model=schemas.ProjectOut)
def update_project(project_id: int, data: schemas.ProjectUpdate, db: Session = Depends(get_db)):
    project = crud.update_project(db, project_id, data)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@resume_router.delete("/projects/{project_id}", status_code=204)
def delete_project(project_id: int, db: Session = Depends(get_db)):
    ok = crud.delete_project(db, project_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Project not found")
    return None


# 技术栈API
@resume_router.post("/tech-stacks/", response_model=schemas.TechStackOut)
def create_tech_stack(data: schemas.TechStackCreate, db: Session = Depends(get_db)):
    return crud.create_tech_stack(db, data)


@resume_router.get("/tech-stacks/", response_model=List[schemas.TechStackOut])
def get_tech_stacks(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
):
    return crud.list_tech_stacks(db, skip=skip, limit=limit)


@resume_router.get("/tech-stacks/{tech_stack_id}", response_model=schemas.TechStackOut)
def get_tech_stack(tech_stack_id: int, db: Session = Depends(get_db)):
    tech_stack = crud.get_tech_stack(db, tech_stack_id)
    if not tech_stack:
        raise HTTPException(status_code=404, detail="Tech stack not found")
    return tech_stack


@resume_router.put("/tech-stacks/{tech_stack_id}", response_model=schemas.TechStackOut)
def update_tech_stack(tech_stack_id: int, data: schemas.TechStackUpdate, db: Session = Depends(get_db)):
    tech_stack = crud.update_tech_stack(db, tech_stack_id, data)
    if not tech_stack:
        raise HTTPException(status_code=404, detail="Tech stack not found")
    return tech_stack


@resume_router.delete("/tech-stacks/{tech_stack_id}", status_code=204)
def delete_tech_stack(tech_stack_id: int, db: Session = Depends(get_db)):
    ok = crud.delete_tech_stack(db, tech_stack_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Tech stack not found")
    return None


# 简历照片API
@resume_router.get("/photos/", response_model=list[schemas.ResumePhotoOut])
def list_resume_photos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.list_resume_photos(db, skip, limit)


@resume_router.get("/photos/{photo_id}", response_model=schemas.ResumePhotoOut)
def get_resume_photo(photo_id: int, db: Session = Depends(get_db)):
    photo = crud.get_resume_photo(db, photo_id)
    if not photo:
        raise HTTPException(status_code=404, detail="Resume photo not found")
    return photo


@resume_router.post("/photos/", response_model=schemas.ResumePhotoOut, status_code=201)
def create_resume_photo(data: schemas.ResumePhotoCreate, db: Session = Depends(get_db)):
    return crud.create_resume_photo(db, data)


@resume_router.put("/photos/{photo_id}", response_model=schemas.ResumePhotoOut)
def update_resume_photo(photo_id: int, data: schemas.ResumePhotoUpdate, db: Session = Depends(get_db)):
    photo = crud.update_resume_photo(db, photo_id, data)
    if not photo:
        raise HTTPException(status_code=404, detail="Resume photo not found")
    return photo


@resume_router.delete("/photos/{photo_id}", status_code=204)
def delete_resume_photo(photo_id: int, db: Session = Depends(get_db)):
    ok = crud.delete_resume_photo(db, photo_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Resume photo not found")
    return None


@resume_router.post("/photos/upload")
async def upload_photo(files: list[UploadFile] = File(...)):
    import uuid
    from pathlib import Path
    
    # 创建uploads目录
    upload_dir = Path("uploads")
    upload_dir.mkdir(exist_ok=True)
    
    uploaded_files = []
    for file in files:
        # 生成唯一文件名
        file_ext = file.filename.split('.')[-1] if '.' in file.filename else 'jpg'
        filename = f"{uuid.uuid4()}.{file_ext}"
        file_path = upload_dir / filename
        
        # 保存文件
        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())
        
        uploaded_files.append(filename)
    
    return {"filenames": uploaded_files}


# 岗位要求（JD）API
@resume_router.get("/job-descriptions/", response_model=list[schemas.JobDescriptionOut])
def list_job_descriptions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.list_job_descriptions(db, skip, limit)


@resume_router.get("/job-descriptions/{jd_id}", response_model=schemas.JobDescriptionOut)
def get_job_description(jd_id: int, db: Session = Depends(get_db)):
    jd = crud.get_job_description(db, jd_id)
    if not jd:
        raise HTTPException(status_code=404, detail="Job description not found")
    return jd


@resume_router.post("/job-descriptions/", response_model=schemas.JobDescriptionOut, status_code=201)
def create_job_description(data: schemas.JobDescriptionCreate, db: Session = Depends(get_db)):
    return crud.create_job_description(db, data)


@resume_router.put("/job-descriptions/{jd_id}", response_model=schemas.JobDescriptionOut)
def update_job_description(jd_id: int, data: schemas.JobDescriptionUpdate, db: Session = Depends(get_db)):
    jd = crud.update_job_description(db, jd_id, data)
    if not jd:
        raise HTTPException(status_code=404, detail="Job description not found")
    return jd


@resume_router.delete("/job-descriptions/{jd_id}", status_code=204)
def delete_job_description(jd_id: int, db: Session = Depends(get_db)):
    ok = crud.delete_job_description(db, jd_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Job description not found")
    return None


@resume_router.post("/job-descriptions/upload")
async def upload_jd_image(files: list[UploadFile] = File(...)):
    import uuid
    from pathlib import Path
    
    # 创建uploads目录
    upload_dir = Path("uploads")
    upload_dir.mkdir(exist_ok=True)
    
    uploaded_files = []
    for file in files:
        # 生成唯一文件名
        file_ext = file.filename.split('.')[-1] if '.' in file.filename else 'jpg'
        filename = f"{uuid.uuid4()}.{file_ext}"
        file_path = upload_dir / filename
        
        # 保存文件
        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())
        
        uploaded_files.append(filename)
    
    return {"filenames": uploaded_files}


# JD拆解API
@resume_router.get("/jd-breakdowns/", response_model=list[schemas.JdBreakdownOut])
def list_jd_breakdowns(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.list_jd_breakdowns(db, skip, limit)


@resume_router.get("/jd-breakdowns/jd/{jd_id}", response_model=list[schemas.JdBreakdownOut])
def list_jd_breakdowns_by_jd(jd_id: int, db: Session = Depends(get_db)):
    return crud.list_jd_breakdowns_by_jd(db, jd_id)


@resume_router.get("/jd-breakdowns/{breakdown_id}", response_model=schemas.JdBreakdownOut)
def get_jd_breakdown(breakdown_id: int, db: Session = Depends(get_db)):
    breakdown = crud.get_jd_breakdown(db, breakdown_id)
    if not breakdown:
        raise HTTPException(status_code=404, detail="JD breakdown not found")
    return breakdown


@resume_router.post("/jd-breakdowns/", response_model=schemas.JdBreakdownOut, status_code=201)
def create_jd_breakdown(data: schemas.JdBreakdownCreate, db: Session = Depends(get_db)):
    return crud.create_jd_breakdown(db, data)


@resume_router.put("/jd-breakdowns/{breakdown_id}", response_model=schemas.JdBreakdownOut)
def update_jd_breakdown(breakdown_id: int, data: schemas.JdBreakdownUpdate, db: Session = Depends(get_db)):
    breakdown = crud.update_jd_breakdown(db, breakdown_id, data)
    if not breakdown:
        raise HTTPException(status_code=404, detail="JD breakdown not found")
    return breakdown


@resume_router.delete("/jd-breakdowns/{breakdown_id}", status_code=204)
def delete_jd_breakdown(breakdown_id: int, db: Session = Depends(get_db)):
    ok = crud.delete_jd_breakdown(db, breakdown_id)
    if not ok:
        raise HTTPException(status_code=404, detail="JD breakdown not found")
    return None


# JD解析相关schemas
class JdBreakdownRequest(BaseModel):
    jd_id: int
    system_prompt: str | None = None


@resume_router.post("/jd-breakdowns/analyze")
def analyze_jd(request: JdBreakdownRequest, db: Session = Depends(get_db)):
    """
    使用大模型分析并拆解JD
    """
    try:
        # 获取JD信息
        jd = crud.get_job_description(db, request.jd_id)
        if not jd:
            raise HTTPException(status_code=404, detail="Job description not found")
        
        # 获取JD内容（描述）
        jd_content = jd.description or ""
        if not jd_content:
            raise HTTPException(status_code=400, detail="JD description is empty")
        
        # 调用大模型进行拆解
        llm_service = get_llm_service()
        breakdown_content = llm_service.breakdown_jd(
            jd_content=jd_content,
            system_prompt=request.system_prompt
        )
        
        # 创建拆解记录
        breakdown_data = schemas.JdBreakdownCreate(
            jd_id=request.jd_id,
            company=jd.company,
            position=jd.position,
            breakdown_content=breakdown_content
        )
        
        breakdown = crud.create_jd_breakdown(db, breakdown_data)
        
        return breakdown
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to analyze JD: {str(e)}")


@resume_router.post("/jd-breakdowns/analyze-stream")
async def analyze_jd_stream(request: JdBreakdownRequest, db: Session = Depends(get_db)):
    """
    使用大模型流式分析并拆解JD
    """
    # 获取JD信息
    jd = crud.get_job_description(db, request.jd_id)
    if not jd:
        raise HTTPException(status_code=404, detail="Job description not found")
    
    # 获取JD内容（描述）
    jd_content = jd.description or ""
    if not jd_content:
        raise HTTPException(status_code=400, detail="JD description is empty")
    
    # 流式响应生成器
    def generate():
        try:
            llm_service = get_llm_service()
            full_content = ""
            
            # 流式获取内容
            for chunk in llm_service.breakdown_jd_stream(
                jd_content=jd_content,
                system_prompt=request.system_prompt
            ):
                full_content += chunk
                # 发送SSE格式的数据
                data = json.dumps({"content": chunk}, ensure_ascii=False)
                yield f"data: {data}\n\n"
            
            # 流式传输完成后，保存到数据库
            try:
                breakdown_data = schemas.JdBreakdownCreate(
                    jd_id=request.jd_id,
                    company=jd.company,
                    position=jd.position,
                    breakdown_content=full_content
                )
                breakdown = crud.create_jd_breakdown(db, breakdown_data)
                # 发送完成信号和最终的breakdown ID
                final_data = json.dumps({
                    "done": True,
                    "breakdown_id": breakdown.id
                }, ensure_ascii=False)
                yield f"data: {final_data}\n\n"
            except Exception as e:
                # 如果保存失败，发送错误信息
                error_data = json.dumps({
                    "error": f"保存拆解结果失败: {str(e)}"
                }, ensure_ascii=False)
                yield f"data: {error_data}\n\n"
                
        except Exception as e:
            error_data = json.dumps({
                "error": f"AI拆解失败: {str(e)}"
            }, ensure_ascii=False)
            yield f"data: {error_data}\n\n"
    
    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"
        }
    )


# ==================== OKR API ====================

okr_router = APIRouter(prefix="/okr", tags=["okr"])


@okr_router.get("/okrs/", response_model=List[schemas.OKROut])
def list_okrs(skip: int = Query(0, ge=0), limit: int = Query(100, ge=1, le=1000), db: Session = Depends(get_db)):
    return crud.list_okrs(db, skip=skip, limit=limit)


@okr_router.get("/okrs/{okr_id}", response_model=schemas.OKROut)
def get_okr(okr_id: int, db: Session = Depends(get_db)):
    okr = crud.get_okr(db, okr_id)
    if not okr:
        raise HTTPException(status_code=404, detail="OKR not found")
    return okr


@okr_router.post("/okrs/", response_model=schemas.OKROut, status_code=201)
def create_okr(data: schemas.OKRCreate, db: Session = Depends(get_db)):
    return crud.create_okr(db, data)


@okr_router.put("/okrs/{okr_id}", response_model=schemas.OKROut)
def update_okr(okr_id: int, data: schemas.OKRUpdate, db: Session = Depends(get_db)):
    okr = crud.update_okr(db, okr_id, data)
    if not okr:
        raise HTTPException(status_code=404, detail="OKR not found")
    return okr


@okr_router.post("/okrs/{okr_id}/toggle", response_model=schemas.OKROut)
def toggle_okr_completion(okr_id: int, data: dict, db: Session = Depends(get_db)):
    completed = data.get('completed', False)
    okr = crud.toggle_okr_completion(db, okr_id, completed)
    if not okr:
        raise HTTPException(status_code=404, detail="OKR not found")
    return okr


@okr_router.delete("/okrs/{okr_id}", status_code=204)
def delete_okr(okr_id: int, db: Session = Depends(get_db)):
    ok = crud.delete_okr(db, okr_id)
    if not ok:
        raise HTTPException(status_code=404, detail="OKR not found")
    return None


# ==================== Task API ====================

@okr_router.get("/okrs/{okr_id}/tasks/", response_model=List[schemas.TaskOut])
def list_tasks_by_okr(okr_id: int, skip: int = Query(0, ge=0), limit: int = Query(100, ge=1, le=1000), db: Session = Depends(get_db)):
    return crud.list_tasks_by_okr(db, okr_id, skip=skip, limit=limit)


@okr_router.get("/tasks/{task_id}", response_model=schemas.TaskOut)
def get_task(task_id: int, db: Session = Depends(get_db)):
    task = crud.get_task(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@okr_router.post("/tasks/", response_model=schemas.TaskOut, status_code=201)
def create_task(data: schemas.TaskCreate, db: Session = Depends(get_db)):
    # 验证OKR是否存在
    okr = crud.get_okr(db, data.okr_id)
    if not okr:
        raise HTTPException(status_code=404, detail="OKR not found")
    return crud.create_task(db, data)


@okr_router.put("/tasks/{task_id}", response_model=schemas.TaskOut)
def update_task(task_id: int, data: schemas.TaskUpdate, db: Session = Depends(get_db)):
    task = crud.update_task(db, task_id, data)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@okr_router.post("/tasks/{task_id}/toggle", response_model=schemas.TaskOut)
def toggle_task_completion(task_id: int, data: dict, db: Session = Depends(get_db)):
    completed = data.get('completed', False)
    task = crud.toggle_task_completion(db, task_id, completed)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@okr_router.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    ok = crud.delete_task(db, task_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Task not found")
    return None


# ==================== 面试题库 API ====================

interview_router = APIRouter(prefix="/interview", tags=["interview"])


# InterviewCategory API
@interview_router.get("/categories/", response_model=List[schemas.InterviewCategoryOut])
def list_interview_categories(skip: int = Query(0, ge=0), limit: int = Query(1000, ge=1, le=1000), db: Session = Depends(get_db)):
    return crud.list_interview_categories(db, skip=skip, limit=limit)


@interview_router.get("/categories/{category_id}", response_model=schemas.InterviewCategoryOut)
def get_interview_category(category_id: int, db: Session = Depends(get_db)):
    category = crud.get_interview_category(db, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Interview category not found")
    return category


@interview_router.post("/categories/", response_model=schemas.InterviewCategoryOut, status_code=201)
def create_interview_category(data: schemas.InterviewCategoryCreate, db: Session = Depends(get_db)):
    return crud.create_interview_category(db, data)


@interview_router.put("/categories/{category_id}", response_model=schemas.InterviewCategoryOut)
def update_interview_category(category_id: int, data: schemas.InterviewCategoryUpdate, db: Session = Depends(get_db)):
    category = crud.update_interview_category(db, category_id, data)
    if not category:
        raise HTTPException(status_code=404, detail="Interview category not found")
    return category


@interview_router.delete("/categories/{category_id}", status_code=204)
def delete_interview_category(category_id: int, db: Session = Depends(get_db)):
    ok = crud.delete_interview_category(db, category_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Interview category not found")
    return None


# InterviewQuestion API
@interview_router.get("/questions/", response_model=List[schemas.InterviewQuestionOut])
def list_interview_questions(
    skip: int = Query(0, ge=0),
    limit: int = Query(1000, ge=1, le=1000),
    category_id: int | None = Query(None, description="Filter by category ID"),
    db: Session = Depends(get_db),
):
    questions = crud.list_interview_questions(db, skip=skip, limit=limit, category_id=category_id)
    # 加载每个问题的答案
    result = []
    for q in questions:
        answers = crud.list_interview_answers_by_question(db, q.id)
        # 构建返回对象
        q_out = schemas.InterviewQuestionOut(
            id=q.id,
            description=q.description,
            category_id=q.category_id,
            company=q.company or "",
            tags=q.tags or "",
            difficulty=q.difficulty,
            round=q.round or "",
            created_at=q.created_at,
            updated_at=q.updated_at,
            answers=[schemas.InterviewAnswerOut(
                id=a.id,
                question_id=a.question_id,
                content=a.content,
                created_at=a.created_at,
                updated_at=a.updated_at
            ) for a in answers]
        )
        result.append(q_out)
    return result


@interview_router.get("/questions/{question_id}", response_model=schemas.InterviewQuestionOut)
def get_interview_question(question_id: int, db: Session = Depends(get_db)):
    question = crud.get_interview_question(db, question_id)
    if not question:
        raise HTTPException(status_code=404, detail="Interview question not found")
    answers = crud.list_interview_answers_by_question(db, question_id)
    return schemas.InterviewQuestionOut(
        id=question.id,
        description=question.description,
        category_id=question.category_id,
        company=question.company or "",
        tags=question.tags or "",
        difficulty=question.difficulty,
        round=question.round or "",
        created_at=question.created_at,
        updated_at=question.updated_at,
        answers=[schemas.InterviewAnswerOut(
            id=a.id,
            question_id=a.question_id,
            content=a.content,
            created_at=a.created_at,
            updated_at=a.updated_at
        ) for a in answers]
    )


@interview_router.post("/questions/", response_model=schemas.InterviewQuestionOut, status_code=201)
def create_interview_question(data: schemas.InterviewQuestionCreate, db: Session = Depends(get_db)):
    question = crud.create_interview_question(db, data)
    return schemas.InterviewQuestionOut(
        id=question.id,
        description=question.description,
        category_id=question.category_id,
        company=question.company or "",
        tags=question.tags or "",
        difficulty=question.difficulty,
        round=question.round or "",
        created_at=question.created_at,
        updated_at=question.updated_at,
        answers=[]
    )


@interview_router.put("/questions/{question_id}", response_model=schemas.InterviewQuestionOut)
def update_interview_question(question_id: int, data: schemas.InterviewQuestionUpdate, db: Session = Depends(get_db)):
    question = crud.update_interview_question(db, question_id, data)
    if not question:
        raise HTTPException(status_code=404, detail="Interview question not found")
    answers = crud.list_interview_answers_by_question(db, question_id)
    return schemas.InterviewQuestionOut(
        id=question.id,
        description=question.description,
        category_id=question.category_id,
        company=question.company or "",
        tags=question.tags or "",
        difficulty=question.difficulty,
        round=question.round or "",
        created_at=question.created_at,
        updated_at=question.updated_at,
        answers=[schemas.InterviewAnswerOut(
            id=a.id,
            question_id=a.question_id,
            content=a.content,
            created_at=a.created_at,
            updated_at=a.updated_at
        ) for a in answers]
    )


@interview_router.delete("/questions/{question_id}", status_code=204)
def delete_interview_question(question_id: int, db: Session = Depends(get_db)):
    ok = crud.delete_interview_question(db, question_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Interview question not found")
    return None


# InterviewAnswer API
@interview_router.get("/questions/{question_id}/answers/", response_model=List[schemas.InterviewAnswerOut])
def list_interview_answers_by_question(question_id: int, db: Session = Depends(get_db)):
    return crud.list_interview_answers_by_question(db, question_id)


@interview_router.get("/answers/{answer_id}", response_model=schemas.InterviewAnswerOut)
def get_interview_answer(answer_id: int, db: Session = Depends(get_db)):
    answer = crud.get_interview_answer(db, answer_id)
    if not answer:
        raise HTTPException(status_code=404, detail="Interview answer not found")
    return answer


@interview_router.post("/answers/", response_model=schemas.InterviewAnswerOut, status_code=201)
def create_interview_answer(data: schemas.InterviewAnswerCreate, db: Session = Depends(get_db)):
    answer = crud.create_interview_answer(db, data)
    if not answer:
        raise HTTPException(status_code=404, detail="Interview question not found")
    return answer


@interview_router.put("/answers/{answer_id}", response_model=schemas.InterviewAnswerOut)
def update_interview_answer(answer_id: int, data: schemas.InterviewAnswerUpdate, db: Session = Depends(get_db)):
    answer = crud.update_interview_answer(db, answer_id, data)
    if not answer:
        raise HTTPException(status_code=404, detail="Interview answer not found")
    return answer


@interview_router.delete("/answers/{answer_id}", status_code=204)
def delete_interview_answer(answer_id: int, db: Session = Depends(get_db)):
    ok = crud.delete_interview_answer(db, answer_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Interview answer not found")
    return None


# ==================== 观点记录 API ====================

opinion_router = APIRouter(prefix="/opinion", tags=["opinion"])


# OpinionCategory API
@opinion_router.get("/categories/", response_model=List[schemas.OpinionCategoryOut])
def list_opinion_categories(skip: int = Query(0, ge=0), limit: int = Query(1000, ge=1, le=1000), db: Session = Depends(get_db)):
    return crud.list_opinion_categories(db, skip=skip, limit=limit)


@opinion_router.get("/categories/{category_id}", response_model=schemas.OpinionCategoryOut)
def get_opinion_category(category_id: int, db: Session = Depends(get_db)):
    category = crud.get_opinion_category(db, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Opinion category not found")
    return category


@opinion_router.post("/categories/", response_model=schemas.OpinionCategoryOut, status_code=201)
def create_opinion_category(data: schemas.OpinionCategoryCreate, db: Session = Depends(get_db)):
    return crud.create_opinion_category(db, data)


@opinion_router.put("/categories/{category_id}", response_model=schemas.OpinionCategoryOut)
def update_opinion_category(category_id: int, data: schemas.OpinionCategoryUpdate, db: Session = Depends(get_db)):
    category = crud.update_opinion_category(db, category_id, data)
    if not category:
        raise HTTPException(status_code=404, detail="Opinion category not found")
    return category


@opinion_router.delete("/categories/{category_id}", status_code=204)
def delete_opinion_category(category_id: int, db: Session = Depends(get_db)):
    ok = crud.delete_opinion_category(db, category_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Opinion category not found")
    return None


# Opinion API
@opinion_router.get("/opinions/", response_model=List[schemas.OpinionOut])
def list_opinions(
    skip: int = Query(0, ge=0),
    limit: int = Query(1000, ge=1, le=1000),
    category_id: int | None = Query(None, description="Filter by category ID"),
    db: Session = Depends(get_db),
):
    return crud.list_opinions(db, skip=skip, limit=limit, category_id=category_id)


@opinion_router.get("/opinions/{opinion_id}", response_model=schemas.OpinionOut)
def get_opinion(opinion_id: int, db: Session = Depends(get_db)):
    opinion = crud.get_opinion(db, opinion_id)
    if not opinion:
        raise HTTPException(status_code=404, detail="Opinion not found")
    return opinion


@opinion_router.post("/opinions/", response_model=schemas.OpinionOut, status_code=201)
def create_opinion(data: schemas.OpinionCreate, db: Session = Depends(get_db)):
    return crud.create_opinion(db, data)


@opinion_router.put("/opinions/{opinion_id}", response_model=schemas.OpinionOut)
def update_opinion(opinion_id: int, data: schemas.OpinionUpdate, db: Session = Depends(get_db)):
    opinion = crud.update_opinion(db, opinion_id, data)
    if not opinion:
        raise HTTPException(status_code=404, detail="Opinion not found")
    return opinion


@opinion_router.delete("/opinions/{opinion_id}", status_code=204)
def delete_opinion(opinion_id: int, db: Session = Depends(get_db)):
    ok = crud.delete_opinion(db, opinion_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Opinion not found")
    return None


