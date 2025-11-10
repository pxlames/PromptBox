from fastapi import APIRouter, Depends, HTTPException, Query, File, UploadFile
from sqlalchemy.orm import Session
from typing import List
import uuid
from pathlib import Path

from .db import get_db
from . import schemas, crud

story_router = APIRouter(prefix="/story", tags=["story"])


# StoryCategory API
@story_router.get("/categories/", response_model=List[schemas.StoryCategoryOut])
def list_story_categories(skip: int = Query(0, ge=0), limit: int = Query(1000, ge=1, le=1000), db: Session = Depends(get_db)):
    return crud.list_story_categories(db, skip=skip, limit=limit)


@story_router.get("/categories/{category_id}", response_model=schemas.StoryCategoryOut)
def get_story_category(category_id: int, db: Session = Depends(get_db)):
    category = crud.get_story_category(db, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Story category not found")
    return category


@story_router.post("/categories/", response_model=schemas.StoryCategoryOut, status_code=201)
def create_story_category(data: schemas.StoryCategoryCreate, db: Session = Depends(get_db)):
    return crud.create_story_category(db, data)


@story_router.put("/categories/{category_id}", response_model=schemas.StoryCategoryOut)
def update_story_category(category_id: int, data: schemas.StoryCategoryUpdate, db: Session = Depends(get_db)):
    category = crud.update_story_category(db, category_id, data)
    if not category:
        raise HTTPException(status_code=404, detail="Story category not found")
    return category


@story_router.delete("/categories/{category_id}", status_code=204)
def delete_story_category(category_id: int, db: Session = Depends(get_db)):
    ok = crud.delete_story_category(db, category_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Story category not found")
    return None


# Story API
@story_router.get("/stories/", response_model=List[schemas.StoryOut])
def list_stories(
    skip: int = Query(0, ge=0),
    limit: int = Query(1000, ge=1, le=1000),
    category_id: int | None = Query(None, description="Filter by category ID"),
    db: Session = Depends(get_db),
):
    return crud.list_stories(db, skip=skip, limit=limit, category_id=category_id)


@story_router.get("/stories/{story_id}", response_model=schemas.StoryOut)
def get_story(story_id: int, db: Session = Depends(get_db)):
    story = crud.get_story(db, story_id)
    if not story:
        raise HTTPException(status_code=404, detail="Story not found")
    return story


@story_router.post("/stories/", response_model=schemas.StoryOut, status_code=201)
def create_story(data: schemas.StoryCreate, db: Session = Depends(get_db)):
    return crud.create_story(db, data)


@story_router.put("/stories/{story_id}", response_model=schemas.StoryOut)
def update_story(story_id: int, data: schemas.StoryUpdate, db: Session = Depends(get_db)):
    story = crud.update_story(db, story_id, data)
    if not story:
        raise HTTPException(status_code=404, detail="Story not found")
    return story


@story_router.delete("/stories/{story_id}", status_code=204)
def delete_story(story_id: int, db: Session = Depends(get_db)):
    ok = crud.delete_story(db, story_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Story not found")
    return None


# 图片上传API
@story_router.post("/upload-images")
async def upload_story_images(files: list[UploadFile] = File(...)):
    """
    上传故事图片
    """
    # 创建uploads目录
    upload_dir = Path("uploads")
    upload_dir.mkdir(exist_ok=True)
    
    uploaded_files = []
    for file in files:
        # 生成唯一文件名，添加story前缀
        file_ext = file.filename.split('.')[-1] if '.' in file.filename else 'jpg'
        filename = f"story_{uuid.uuid4()}.{file_ext}"
        file_path = upload_dir / filename
        
        # 保存文件
        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())
        
        uploaded_files.append(filename)
    
    return {"filenames": uploaded_files}

