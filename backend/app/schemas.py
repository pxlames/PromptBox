from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class PromptBase(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    content: str
    tags: Optional[str] = ""


class PromptCreate(PromptBase):
    pass


class PromptUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=200)
    content: Optional[str] = None
    tags: Optional[str] = None


class PromptOut(PromptBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


# 实习经历相关schemas
class InternshipBase(BaseModel):
    group_title: Optional[str] = Field(default='', max_length=500)  # 分组标题
    company: str = Field(default='', max_length=500)  # 公司名称可以为空
    position: str = Field(default='', max_length=500)  # 子标题可以为空
    start_date: str = Field(default='', max_length=50)  # 开始时间可以为空
    end_date: Optional[str] = Field(default='', max_length=50)
    description: Optional[str] = None
    skills: Optional[str] = Field(default='', max_length=500)


class InternshipCreate(InternshipBase):
    pass


class InternshipUpdate(BaseModel):
    group_title: Optional[str] = Field(default=None, max_length=500)
    company: Optional[str] = Field(default=None, max_length=500)
    position: Optional[str] = Field(default=None, max_length=500)
    start_date: Optional[str] = Field(default=None, max_length=50)
    end_date: Optional[str] = Field(default=None, max_length=50)
    description: Optional[str] = None
    skills: Optional[str] = Field(default=None, max_length=500)


class InternshipOut(InternshipBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


# 项目经历相关schemas
class ProjectBase(BaseModel):
    name: str = Field(default='', max_length=500)
    description: str = Field(default='')
    tech_stack: Optional[str] = Field(default=None, max_length=500)
    start_date: Optional[str] = Field(default=None, max_length=50)
    end_date: Optional[str] = Field(default=None, max_length=50)
    url: Optional[str] = Field(default=None, max_length=500)


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(BaseModel):
    name: Optional[str] = Field(default=None, max_length=500)
    description: Optional[str] = None
    tech_stack: Optional[str] = Field(default=None, max_length=500)
    start_date: Optional[str] = Field(default=None, max_length=50)
    end_date: Optional[str] = Field(default=None, max_length=50)
    url: Optional[str] = Field(default=None, max_length=500)


class ProjectOut(ProjectBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


# 技术栈相关schemas
class TechStackBase(BaseModel):
    category: str = Field(default='', max_length=500)
    name: str = Field(default='', max_length=500)
    level: str = Field(default='', max_length=100)
    description: Optional[str] = None


class TechStackCreate(TechStackBase):
    pass


class TechStackUpdate(BaseModel):
    category: Optional[str] = Field(default=None, max_length=500)
    name: Optional[str] = Field(default=None, max_length=500)
    level: Optional[str] = Field(default=None, max_length=100)
    description: Optional[str] = None


class TechStackOut(TechStackBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


# 简历照片相关schemas
class ResumePhotoBase(BaseModel):
    title: str = Field(min_length=1, max_length=500)
    image_path: Optional[str] = None  # 多个图片路径，用逗号分隔


class ResumePhotoCreate(ResumePhotoBase):
    pass


class ResumePhotoUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=500)
    image_path: Optional[str] = None  # 多个图片路径，用逗号分隔


class ResumePhotoOut(ResumePhotoBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


# 岗位要求（JD）相关schemas
class JobDescriptionBase(BaseModel):
    company: str = Field(min_length=1, max_length=500)
    position: str = Field(min_length=1, max_length=500)
    image_paths: Optional[str] = None  # JD图片路径，用逗号分隔
    description: Optional[str] = None  # 文字描述


class JobDescriptionCreate(JobDescriptionBase):
    pass


class JobDescriptionUpdate(BaseModel):
    company: Optional[str] = Field(default=None, min_length=1, max_length=500)
    position: Optional[str] = Field(default=None, min_length=1, max_length=500)
    image_paths: Optional[str] = None
    description: Optional[str] = None


class JobDescriptionOut(JobDescriptionBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


# JD拆解相关schemas
class JdBreakdownBase(BaseModel):
    jd_id: int
    company: str = Field(min_length=1, max_length=500)
    position: str = Field(min_length=1, max_length=500)
    breakdown_content: str = Field(min_length=1)  # 拆解内容（Markdown格式）


class JdBreakdownCreate(JdBreakdownBase):
    pass


class JdBreakdownUpdate(BaseModel):
    company: Optional[str] = Field(default=None, min_length=1, max_length=500)
    position: Optional[str] = Field(default=None, min_length=1, max_length=500)
    breakdown_content: Optional[str] = Field(default=None, min_length=1)


class JdBreakdownOut(JdBreakdownBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


# OKR相关schemas
class OKRBase(BaseModel):
    objective: str = Field(min_length=1, max_length=500)
    due_date: Optional[datetime] = None


class OKRCreate(OKRBase):
    pass


class OKRUpdate(BaseModel):
    objective: Optional[str] = Field(default=None, min_length=1, max_length=500)
    completed: Optional[bool] = None
    due_date: Optional[datetime] = None


class OKROut(OKRBase):
    id: int
    completed: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class OKROutWithTasks(OKROut):
    tasks: List['TaskOut'] = []


# Task相关schemas
class TaskBase(BaseModel):
    okr_id: int
    title: str = Field(min_length=1, max_length=500)
    description: Optional[str] = None


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    okr_id: Optional[int] = None
    title: Optional[str] = Field(default=None, min_length=1, max_length=500)
    description: Optional[str] = None
    completed: Optional[bool] = None


class TaskOut(BaseModel):
    id: int
    okr_id: int
    title: str
    description: Optional[str] = None
    completed: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


# 面试题库相关schemas
class InterviewCategoryBase(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    order: int = Field(default=0, ge=0)


class InterviewCategoryCreate(InterviewCategoryBase):
    pass


class InterviewCategoryUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1, max_length=200)
    order: Optional[int] = Field(default=None, ge=0)


class InterviewCategoryOut(InterviewCategoryBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class InterviewAnswerBase(BaseModel):
    content: str = Field(min_length=1)


class InterviewAnswerCreate(InterviewAnswerBase):
    question_id: int


class InterviewAnswerUpdate(BaseModel):
    content: Optional[str] = Field(default=None, min_length=1)


class InterviewAnswerOut(InterviewAnswerBase):
    id: int
    question_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class InterviewQuestionBase(BaseModel):
    description: str = Field(min_length=1)
    category_id: Optional[int] = None
    company: Optional[str] = Field(default="", max_length=200)
    tags: Optional[str] = Field(default="", max_length=500)
    difficulty: str = Field(default="中等", max_length=20)  # 简单/中等/困难
    round: Optional[str] = Field(default="", max_length=100)


class InterviewQuestionCreate(InterviewQuestionBase):
    pass


class InterviewQuestionUpdate(BaseModel):
    description: Optional[str] = Field(default=None, min_length=1)
    category_id: Optional[int] = None
    company: Optional[str] = Field(default=None, max_length=200)
    tags: Optional[str] = Field(default=None, max_length=500)
    difficulty: Optional[str] = Field(default=None, max_length=20)
    round: Optional[str] = Field(default=None, max_length=100)


class InterviewQuestionOut(InterviewQuestionBase):
    id: int
    created_at: datetime
    updated_at: datetime
    answers: List[InterviewAnswerOut] = []

    class Config:
        orm_mode = True


# 观点记录相关schemas
class OpinionCategoryBase(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    order: int = Field(default=0, ge=0)


class OpinionCategoryCreate(OpinionCategoryBase):
    pass


class OpinionCategoryUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1, max_length=200)
    order: Optional[int] = Field(default=None, ge=0)


class OpinionCategoryOut(OpinionCategoryBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class OpinionBase(BaseModel):
    description: str = Field(min_length=1)
    category_id: Optional[int] = None


class OpinionCreate(OpinionBase):
    pass


class OpinionUpdate(BaseModel):
    description: Optional[str] = Field(default=None, min_length=1)
    category_id: Optional[int] = None


class OpinionOut(OpinionBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


# 聊天历史相关schemas
class ChatHistoryBase(BaseModel):
    title: Optional[str] = Field(default=None, max_length=200)
    messages: str  # JSON格式的消息列表


class ChatHistoryCreate(ChatHistoryBase):
    pass


class ChatHistoryUpdate(BaseModel):
    title: Optional[str] = Field(default=None, max_length=200)
    messages: Optional[str] = None


class ChatHistoryOut(ChatHistoryBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


