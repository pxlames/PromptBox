from fastapi import APIRouter, Depends, HTTPException, Query, File, UploadFile
from sqlalchemy.orm import Session
from typing import List
import uuid
from pathlib import Path

from .db import get_db
from . import schemas, crud

timeline_router = APIRouter(prefix="/timeline", tags=["timeline"])


# TimelineTopic API
@timeline_router.get("/topics/", response_model=List[schemas.TimelineTopicOut])
def list_timeline_topics(
    skip: int = Query(0, ge=0), 
    limit: int = Query(1000, ge=1, le=1000), 
    db: Session = Depends(get_db)
):
    """列表时间线主题"""
    return crud.list_timeline_topics(db, skip=skip, limit=limit)


@timeline_router.get("/topics/{topic_id}", response_model=schemas.TimelineTopicOut)
def get_timeline_topic(topic_id: int, db: Session = Depends(get_db)):
    """获取时间线主题"""
    topic = crud.get_timeline_topic(db, topic_id)
    if not topic:
        raise HTTPException(status_code=404, detail="Timeline topic not found")
    return topic


@timeline_router.post("/topics/", response_model=schemas.TimelineTopicOut, status_code=201)
def create_timeline_topic(data: schemas.TimelineTopicCreate, db: Session = Depends(get_db)):
    """创建时间线主题"""
    return crud.create_timeline_topic(db, data)


@timeline_router.put("/topics/{topic_id}", response_model=schemas.TimelineTopicOut)
def update_timeline_topic(
    topic_id: int, 
    data: schemas.TimelineTopicUpdate, 
    db: Session = Depends(get_db)
):
    """更新时间线主题"""
    topic = crud.update_timeline_topic(db, topic_id, data)
    if not topic:
        raise HTTPException(status_code=404, detail="Timeline topic not found")
    return topic


@timeline_router.delete("/topics/{topic_id}", status_code=204)
def delete_timeline_topic(topic_id: int, db: Session = Depends(get_db)):
    """删除时间线主题"""
    ok = crud.delete_timeline_topic(db, topic_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Timeline topic not found")
    return None


# TimelineEntry API
@timeline_router.get("/entries/", response_model=List[schemas.TimelineEntryOut])
def list_timeline_entries(
    topic_id: int = Query(..., description="Filter by topic ID"),
    skip: int = Query(0, ge=0),
    limit: int = Query(1000, ge=1, le=1000),
    db: Session = Depends(get_db),
):
    """列表时间线条目"""
    return crud.list_timeline_entries(db, topic_id=topic_id, skip=skip, limit=limit)


@timeline_router.get("/entries/{entry_id}", response_model=schemas.TimelineEntryOut)
def get_timeline_entry(entry_id: int, db: Session = Depends(get_db)):
    """获取时间线条目"""
    entry = crud.get_timeline_entry(db, entry_id)
    if not entry:
        raise HTTPException(status_code=404, detail="Timeline entry not found")
    return entry


@timeline_router.post("/entries/", response_model=schemas.TimelineEntryOut, status_code=201)
def create_timeline_entry(data: schemas.TimelineEntryCreate, db: Session = Depends(get_db)):
    """创建时间线条目"""
    return crud.create_timeline_entry(db, data)


@timeline_router.put("/entries/{entry_id}", response_model=schemas.TimelineEntryOut)
def update_timeline_entry(
    entry_id: int, 
    data: schemas.TimelineEntryUpdate, 
    db: Session = Depends(get_db)
):
    """更新时间线条目"""
    entry = crud.update_timeline_entry(db, entry_id, data)
    if not entry:
        raise HTTPException(status_code=404, detail="Timeline entry not found")
    return entry


@timeline_router.delete("/entries/{entry_id}", status_code=204)
def delete_timeline_entry(entry_id: int, db: Session = Depends(get_db)):
    """删除时间线条目"""
    ok = crud.delete_timeline_entry(db, entry_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Timeline entry not found")
    return None


# TimelineSubEntry API
@timeline_router.get("/sub-entries/", response_model=List[schemas.TimelineSubEntryOut])
def list_timeline_sub_entries(
    entry_id: int = Query(..., description="Filter by entry ID"),
    skip: int = Query(0, ge=0),
    limit: int = Query(1000, ge=1, le=1000),
    db: Session = Depends(get_db),
):
    """列表时间线子条目"""
    return crud.list_timeline_sub_entries(db, entry_id=entry_id, skip=skip, limit=limit)


@timeline_router.get("/sub-entries/{sub_entry_id}", response_model=schemas.TimelineSubEntryOut)
def get_timeline_sub_entry(sub_entry_id: int, db: Session = Depends(get_db)):
    """获取时间线子条目"""
    sub_entry = crud.get_timeline_sub_entry(db, sub_entry_id)
    if not sub_entry:
        raise HTTPException(status_code=404, detail="Timeline sub entry not found")
    return sub_entry


@timeline_router.post("/sub-entries/", response_model=schemas.TimelineSubEntryOut, status_code=201)
def create_timeline_sub_entry(data: schemas.TimelineSubEntryCreate, db: Session = Depends(get_db)):
    """创建时间线子条目"""
    return crud.create_timeline_sub_entry(db, data)


@timeline_router.put("/sub-entries/{sub_entry_id}", response_model=schemas.TimelineSubEntryOut)
def update_timeline_sub_entry(
    sub_entry_id: int, 
    data: schemas.TimelineSubEntryUpdate, 
    db: Session = Depends(get_db)
):
    """更新时间线子条目"""
    sub_entry = crud.update_timeline_sub_entry(db, sub_entry_id, data)
    if not sub_entry:
        raise HTTPException(status_code=404, detail="Timeline sub entry not found")
    return sub_entry


@timeline_router.delete("/sub-entries/{sub_entry_id}", status_code=204)
def delete_timeline_sub_entry(sub_entry_id: int, db: Session = Depends(get_db)):
    """删除时间线子条目"""
    ok = crud.delete_timeline_sub_entry(db, sub_entry_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Timeline sub entry not found")
    return None


# 图片上传API
@timeline_router.post("/upload-images")
async def upload_timeline_images(files: list[UploadFile] = File(...)):
    """
    上传时间线图片
    """
    # 创建uploads目录
    upload_dir = Path("uploads")
    upload_dir.mkdir(exist_ok=True)
    
    uploaded_files = []
    for file in files:
        # 生成唯一文件名，添加timeline前缀
        file_ext = file.filename.split('.')[-1] if '.' in file.filename else 'jpg'
        filename = f"timeline_{uuid.uuid4()}.{file_ext}"
        file_path = upload_dir / filename
        
        # 保存文件
        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())
        
        uploaded_files.append(filename)
    
    return {"filenames": uploaded_files}

