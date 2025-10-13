from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List

from .db import get_db
from . import schemas, crud


router = APIRouter(prefix="/prompts", tags=["prompts"])


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


