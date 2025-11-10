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


# 面试题库相关模型
class InterviewCategory(Base):
    __tablename__ = "interview_categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False, index=True)  # 分类名称
    order = Column(Integer, default=0, nullable=False)  # 排序顺序
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)


class InterviewQuestion(Base):
    __tablename__ = "interview_questions"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(Text, nullable=False)  # 问题描述
    category_id = Column(Integer, ForeignKey("interview_categories.id"), nullable=True, index=True)  # 分类ID
    company = Column(String(200), nullable=True, default="")  # 公司
    tags = Column(String(500), nullable=True, default="")  # 标签
    difficulty = Column(String(20), nullable=False, default="中等")  # 难度：简单/中等/困难
    round = Column(String(100), nullable=True, default="")  # 面试轮次
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)


class InterviewAnswer(Base):
    __tablename__ = "interview_answers"

    id = Column(Integer, primary_key=True, index=True)
    question_id = Column(Integer, ForeignKey("interview_questions.id"), nullable=False, index=True)  # 关联的问题ID
    content = Column(Text, nullable=False)  # 答案内容
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)


# 观点记录相关模型
class OpinionCategory(Base):
    __tablename__ = "opinion_categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False, index=True)  # 分类名称
    order = Column(Integer, default=0, nullable=False)  # 排序顺序
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)


class Opinion(Base):
    __tablename__ = "opinions"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(Text, nullable=False)  # 观点描述
    category_id = Column(Integer, ForeignKey("opinion_categories.id"), nullable=True, index=True)  # 分类ID
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)


# AI助手聊天历史相关模型
class ChatHistory(Base):
    __tablename__ = "chat_histories"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=True)  # 对话标题（可自动生成）
    messages = Column(Text, nullable=False)  # 消息列表（JSON格式）
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)


class LikeRecord(Base):
    """点赞记录"""
    __tablename__ = "chat_like_records"

    id = Column(Integer, primary_key=True, index=True)
    question = Column(Text, nullable=False)  # 用户的问题
    answer = Column(Text, nullable=False)  # AI的回复
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)


# 刷题相关模型
class AlgoCategory(Base):
    """算法题目分类"""
    __tablename__ = "algo_categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False, index=True)  # 分类名称
    order = Column(Integer, default=0, nullable=False)  # 排序顺序
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)


class AlgoProblem(Base):
    """算法题目"""
    __tablename__ = "algo_problems"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(500), nullable=False, index=True)  # 题目标题
    category_id = Column(Integer, ForeignKey("algo_categories.id"), nullable=True, index=True)  # 分类ID
    difficulty = Column(String(20), nullable=False, default="中等")  # 难度：简单/中等/困难
    companies = Column(String(500), nullable=True, default="")  # 公司（逗号分隔）
    tags = Column(String(500), nullable=True, default="")  # 标签（逗号分隔）
    status = Column(String(20), nullable=False, default="未开始")  # 状态：未开始/已掌握/再复习
    link = Column(String(1000), nullable=True, default="")  # 题目链接
    description = Column(Text, nullable=True)  # 题目描述
    solution = Column(Text, nullable=True)  # 解法思路/代码（保留原有字段，兼容旧数据）
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)


class AlgoSolution(Base):
    """算法题解"""
    __tablename__ = "algo_solutions"

    id = Column(Integer, primary_key=True, index=True)
    problem_id = Column(Integer, ForeignKey("algo_problems.id"), nullable=False, index=True)  # 关联的题目ID
    title = Column(String(200), nullable=True, default="")  # 题解标题（如：方法1、动态规划解法等）
    content = Column(Text, nullable=False)  # 题解内容（代码/思路）
    language = Column(String(50), nullable=True, default="")  # 编程语言（如：Python、Java、C++）
    complexity_time = Column(String(100), nullable=True, default="")  # 时间复杂度
    complexity_space = Column(String(100), nullable=True, default="")  # 空间复杂度
    order = Column(Integer, default=0, nullable=False)  # 排序顺序
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)


# 故事会相关模型
class StoryCategory(Base):
    """故事分类"""
    __tablename__ = "story_categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False, index=True)  # 分类名称
    order = Column(Integer, default=0, nullable=False)  # 排序顺序
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)


class Story(Base):
    """故事记录"""
    __tablename__ = "stories"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(500), nullable=False)  # 故事标题
    content = Column(Text, nullable=False)  # 故事内容
    category_id = Column(Integer, ForeignKey("story_categories.id"), nullable=True, index=True)  # 分类ID
    image_paths = Column(Text, nullable=True)  # 图片路径，用逗号分隔
    essence = Column(Text, nullable=True)  # 透过故事看到的本质
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)


# 时间线记录相关模型
class TimelineTopic(Base):
    """时间线主题"""
    __tablename__ = "timeline_topics"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(500), nullable=False, index=True)  # 主题标题
    order = Column(Integer, default=0, nullable=False)  # 排序顺序
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)


class TimelineEntry(Base):
    """时间线条目"""
    __tablename__ = "timeline_entries"

    id = Column(Integer, primary_key=True, index=True)
    topic_id = Column(Integer, ForeignKey("timeline_topics.id"), nullable=False, index=True)  # 关联的主题ID
    subtitle = Column(String(500), nullable=False)  # 小标题
    conclusion = Column(Text, nullable=True)  # 调查结论
    content = Column(Text, nullable=True)  # 内容
    image_paths = Column(Text, nullable=True)  # 图片路径，用逗号分隔
    order = Column(Integer, default=0, nullable=False)  # 排序顺序
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)


class TimelineSubEntry(Base):
    """时间线子条目"""
    __tablename__ = "timeline_sub_entries"

    id = Column(Integer, primary_key=True, index=True)
    entry_id = Column(Integer, ForeignKey("timeline_entries.id"), nullable=False, index=True)  # 关联的条目ID
    subtitle = Column(String(500), nullable=False)  # 子标题
    conclusion = Column(Text, nullable=True)  # 调查结论
    content = Column(Text, nullable=True)  # 内容
    image_paths = Column(Text, nullable=True)  # 图片路径，用逗号分隔
    order = Column(Integer, default=0, nullable=False)  # 排序顺序
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)


