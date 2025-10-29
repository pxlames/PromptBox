from sqlalchemy import Column, Integer, String, Text, DateTime, func, Boolean, ForeignKey
from .db import Base


class Prompt(Base):
    __tablename__ = "prompts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False, index=True)
    content = Column(Text, nullable=False)
    tags = Column(String(255), nullable=True, default="")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)


class Internship(Base):
    __tablename__ = "internships"

    id = Column(Integer, primary_key=True, index=True)
    group_title = Column(String(500), nullable=True, default='')  # 分组标题，同一标题下可以有多个描述
    company = Column(String(500), nullable=True, default='')  # 公司名称可以为空
    position = Column(String(500), nullable=True, default='')  # 子标题可以为空
    start_date = Column(String(50), nullable=True, default='')  # 开始时间可以为空
    end_date = Column(String(50), nullable=True, default='')
    description = Column(Text, nullable=True)
    skills = Column(String(500), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(500), nullable=True, default='')
    description = Column(Text, nullable=True)
    tech_stack = Column(String(500), nullable=True)
    start_date = Column(String(50), nullable=True)
    end_date = Column(String(50), nullable=True)
    url = Column(String(500), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)


class TechStack(Base):
    __tablename__ = "tech_stacks"

    id = Column(Integer, primary_key=True, index=True)
    category = Column(String(500), nullable=True, default='')  # 技术分类
    name = Column(String(500), nullable=True, default='')  # 技术名称
    level = Column(String(100), nullable=True, default='')  # 熟练程度
    description = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)


class ResumePhoto(Base):
    __tablename__ = "resume_photos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(500), nullable=False)
    image_path = Column(Text, nullable=True)  # 存储多个图片路径，用逗号分隔
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)


class JobDescription(Base):
    __tablename__ = "job_descriptions"

    id = Column(Integer, primary_key=True, index=True)
    company = Column(String(500), nullable=False)  # 公司名称
    position = Column(String(500), nullable=False)  # 岗位名称
    image_paths = Column(Text, nullable=True)  # JD图片路径，用逗号分隔
    description = Column(Text, nullable=True)  # 文字描述
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)


class JdBreakdown(Base):
    __tablename__ = "jd_breakdowns"

    id = Column(Integer, primary_key=True, index=True)
    jd_id = Column(Integer, nullable=False)  # 关联的 JD ID
    company = Column(String(500), nullable=False)  # 公司名称
    position = Column(String(500), nullable=False)  # 岗位名称
    breakdown_content = Column(Text, nullable=False)  # 拆解内容（Markdown格式）
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)


class OKR(Base):
    __tablename__ = "okrs"

    id = Column(Integer, primary_key=True, index=True)
    objective = Column(String(500), nullable=False)  # 目标
    completed = Column(Boolean, default=False, nullable=False)  # 是否完成
    due_date = Column(DateTime(timezone=True), nullable=True)  # 截止日期
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    okr_id = Column(Integer, ForeignKey("okrs.id"), nullable=False, index=True)  # 关联的OKR ID
    title = Column(String(500), nullable=False)  # 任务标题
    description = Column(Text, nullable=True)  # 任务描述
    completed = Column(Boolean, default=False, nullable=False)  # 是否完成
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)


