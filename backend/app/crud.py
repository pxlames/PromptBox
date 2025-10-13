from sqlalchemy.orm import Session
from sqlalchemy import select, func
from typing import List, Optional

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


