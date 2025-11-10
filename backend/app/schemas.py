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


# ==================== 点赞记录相关 ====================

class LikeRecordBase(BaseModel):
    question: str
    answer: str


class LikeRecordCreate(LikeRecordBase):
    pass


class LikeRecordOut(LikeRecordBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


# ==================== 刷题相关 schemas ====================

class AlgoCategoryBase(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    order: Optional[int] = Field(default=0)


class AlgoCategoryCreate(AlgoCategoryBase):
    pass


class AlgoCategoryUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1, max_length=200)
    order: Optional[int] = None


class AlgoCategoryOut(AlgoCategoryBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class AlgoProblemBase(BaseModel):
    title: str = Field(min_length=1, max_length=500)
    category_id: Optional[int] = None
    difficulty: str = Field(default="中等")  # 简单/中等/困难
    companies: Optional[str] = Field(default="", max_length=500)
    tags: Optional[str] = Field(default="", max_length=500)
    status: str = Field(default="未开始")  # 未开始/已掌握/再复习
    link: Optional[str] = Field(default="", max_length=1000)
    description: Optional[str] = None
    solution: Optional[str] = None


class AlgoProblemCreate(AlgoProblemBase):
    pass


class AlgoProblemUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=500)
    category_id: Optional[int] = None
    difficulty: Optional[str] = None
    companies: Optional[str] = Field(default=None, max_length=500)
    tags: Optional[str] = Field(default=None, max_length=500)
    status: Optional[str] = None
    link: Optional[str] = Field(default=None, max_length=1000)
    description: Optional[str] = None
    solution: Optional[str] = None


class AlgoProblemOut(AlgoProblemBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


# ==================== 题解相关 schemas ====================

class AlgoSolutionBase(BaseModel):
    title: Optional[str] = Field(default="", max_length=200)
    content: str = Field(min_length=1)  # 题解内容必填
    language: Optional[str] = Field(default="", max_length=50)
    complexity_time: Optional[str] = Field(default="", max_length=50)
    complexity_space: Optional[str] = Field(default="", max_length=50)
    order: Optional[int] = Field(default=0)


class AlgoSolutionCreate(AlgoSolutionBase):
    problem_id: int  # 关联的题目ID


class AlgoSolutionUpdate(BaseModel):
    title: Optional[str] = Field(default=None, max_length=200)
    content: Optional[str] = Field(default=None, min_length=1)
    language: Optional[str] = Field(default=None, max_length=50)
    complexity_time: Optional[str] = Field(default=None, max_length=50)
    complexity_space: Optional[str] = Field(default=None, max_length=50)
    order: Optional[int] = None


class AlgoSolutionOut(AlgoSolutionBase):
    id: int
    problem_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


# ==================== 故事会相关 schemas ====================

class StoryCategoryBase(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    order: int = Field(default=0, ge=0)


class StoryCategoryCreate(StoryCategoryBase):
    pass


class StoryCategoryUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1, max_length=200)
    order: Optional[int] = Field(default=None, ge=0)


class StoryCategoryOut(StoryCategoryBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class StoryBase(BaseModel):
    title: str = Field(min_length=1, max_length=500)
    content: str = Field(min_length=1)
    category_id: Optional[int] = None
    image_paths: Optional[str] = None  # 图片路径，用逗号分隔
    essence: Optional[str] = None  # 透过故事看到的本质


class StoryCreate(StoryBase):
    pass


class StoryUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=500)
    content: Optional[str] = Field(default=None, min_length=1)
    category_id: Optional[int] = None
    image_paths: Optional[str] = None
    essence: Optional[str] = None


class StoryOut(StoryBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


# ==================== 时间线记录相关 schemas ====================

class TimelineTopicBase(BaseModel):
    title: str = Field(min_length=1, max_length=500)
    order: int = Field(default=0, ge=0)


class TimelineTopicCreate(TimelineTopicBase):
    pass


class TimelineTopicUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=500)
    order: Optional[int] = Field(default=None, ge=0)


class TimelineTopicOut(TimelineTopicBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class TimelineTopicOutWithEntries(TimelineTopicOut):
    entries: List['TimelineEntryOut'] = []


class TimelineEntryBase(BaseModel):
    subtitle: str = Field(min_length=1, max_length=500)
    conclusion: Optional[str] = None
    content: Optional[str] = None
    image_paths: Optional[str] = None  # 图片路径，用逗号分隔
    order: int = Field(default=0, ge=0)


class TimelineEntryCreate(TimelineEntryBase):
    topic_id: int


class TimelineEntryUpdate(BaseModel):
    subtitle: Optional[str] = Field(default=None, min_length=1, max_length=500)
    conclusion: Optional[str] = None
    content: Optional[str] = None
    image_paths: Optional[str] = None
    order: Optional[int] = Field(default=None, ge=0)


class TimelineEntryOut(TimelineEntryBase):
    id: int
    topic_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class TimelineSubEntryBase(BaseModel):
    subtitle: str = Field(min_length=1, max_length=500)
    conclusion: Optional[str] = None
    content: Optional[str] = None
    image_paths: Optional[str] = None  # 图片路径，用逗号分隔
    order: int = Field(default=0, ge=0)


class TimelineSubEntryCreate(TimelineSubEntryBase):
    entry_id: int


class TimelineSubEntryUpdate(BaseModel):
    subtitle: Optional[str] = Field(default=None, min_length=1, max_length=500)
    conclusion: Optional[str] = None
    content: Optional[str] = None
    image_paths: Optional[str] = None
    order: Optional[int] = Field(default=None, ge=0)


class TimelineSubEntryOut(TimelineSubEntryBase):
    id: int
    entry_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


