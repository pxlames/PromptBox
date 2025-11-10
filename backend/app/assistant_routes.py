from fastapi import APIRouter, HTTPException, File, UploadFile, Depends, Query
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import List, Optional
import json
import uuid
from pathlib import Path
from sqlalchemy.orm import Session
from .doubao_service import get_doubao_service
from .db import get_db
from . import crud, schemas

assistant_router = APIRouter(prefix="/assistant", tags=["assistant"])


class ChatMessage(BaseModel):
    """聊天消息"""
    role: str  # "user" or "assistant" or "system"
    content: str  # 文本内容
    image_urls: Optional[List[str]] = None  # 图片URL列表


class ChatRequest(BaseModel):
    """聊天请求"""
    messages: List[ChatMessage]  # 消息历史
    stream: bool = False  # 是否流式返回
    reasoning_effort: str = "medium"  # 推理努力程度
    temperature: float = 0.7
    max_tokens: Optional[int] = None


class ChatStreamRequest(BaseModel):
    """流式聊天请求"""
    messages: List[ChatMessage]
    reasoning_effort: str = "medium"
    temperature: float = 0.7
    max_tokens: Optional[int] = None


def convert_messages(messages: List[ChatMessage]) -> List[dict]:
    """
    转换消息格式为豆包API需要的格式
    - 如果只有文本：content 为字符串
    - 如果有图片：content 为对象数组
    """
    result = []
    for msg in messages:
        # 如果有图片，必须使用数组格式
        if msg.image_urls and len(msg.image_urls) > 0:
            content_items = []
            
            # 添加图片
            for img_url in msg.image_urls:
                # 如果是相对路径，保持原样（豆包API需要可访问的完整URL）
                full_url = img_url if img_url.startswith('http') else img_url
                
                content_items.append({
                    "type": "image_url",
                    "image_url": {"url": full_url}
                })
            
            # 添加文本内容（如果有）
            if msg.content and msg.content.strip():
                content_items.append({
                    "type": "text",
                    "text": msg.content
                })
            
            result.append({
                "role": msg.role,
                "content": content_items
            })
        else:
            # 只有文本内容，直接使用字符串格式
            result.append({
                "role": msg.role,
                "content": msg.content or ""
            })
    
    return result


@assistant_router.post("/chat")
async def chat(request: ChatRequest):
    """
    发送聊天请求（非流式）
    """
    try:
        doubao_service = get_doubao_service()
        
        # 转换消息格式
        messages = convert_messages(request.messages)
        
        # 调用豆包服务
        result = doubao_service.chat_complete(
            messages=messages,
            reasoning_effort=request.reasoning_effort,
            temperature=request.temperature,
            max_tokens=request.max_tokens
        )
        
        return {
            "content": result["content"],
            "reasoning_content": result["reasoning_content"]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI聊天失败: {str(e)}")


@assistant_router.post("/chat/stream")
async def chat_stream(request: ChatStreamRequest):
    """
    发送聊天请求（流式）
    """
    try:
        doubao_service = get_doubao_service()
        
        # 转换消息格式
        messages = convert_messages(request.messages)
        
        # 流式响应生成器
        def generate():
            try:
                for chunk in doubao_service.chat_stream(
                    messages=messages,
                    reasoning_effort=request.reasoning_effort,
                    temperature=request.temperature,
                    max_tokens=request.max_tokens
                ):
                    # 发送SSE格式的数据
                    data = json.dumps({"content": chunk}, ensure_ascii=False)
                    yield f"data: {data}\n\n"
                
                # 发送完成标记
                final_data = json.dumps({"done": True}, ensure_ascii=False)
                yield f"data: {final_data}\n\n"
                
            except Exception as e:
                error_data = json.dumps({
                    "error": f"流式响应失败: {str(e)}"
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
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI聊天失败: {str(e)}")


@assistant_router.post("/upload-image")
async def upload_image(file: UploadFile = File(...)):
    """
    上传图片用于AI助手
    """
    try:
        # 创建uploads目录
        upload_dir = Path("uploads")
        upload_dir.mkdir(exist_ok=True)
        
        # 生成唯一文件名
        file_ext = file.filename.split('.')[-1] if '.' in file.filename else 'jpg'
        filename = f"{uuid.uuid4()}.{file_ext}"
        file_path = upload_dir / filename
        
        # 保存文件
        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())
        
        # 返回文件URL（前端可以通过 /uploads/ 访问，不需要 /api 前缀）
        # 因为后端已经挂载了 /uploads 静态文件服务
        return {
            "filename": filename,
            "url": f"/uploads/{filename}"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"图片上传失败: {str(e)}")


# ==================== 聊天历史 API ====================

class SaveChatHistoryRequest(BaseModel):
    """保存聊天历史请求"""
    title: Optional[str] = None
    messages: List[ChatMessage]  # 消息列表


class ChatHistoryListItem(BaseModel):
    """聊天历史列表项"""
    id: int
    title: Optional[str]
    created_at: str
    updated_at: str


@assistant_router.post("/history")
def save_chat_history(request: SaveChatHistoryRequest, db: Session = Depends(get_db)):
    """
    保存聊天历史
    """
    try:
        # 如果没有提供标题，自动生成（使用第一条用户消息的前30个字符）
        title = request.title
        if not title:
            for msg in request.messages:
                if msg.role == "user" and msg.content:
                    title = msg.content[:30]
                    if len(msg.content) > 30:
                        title += "..."
                    break
        
        # 将消息列表转换为JSON字符串
        messages_json = json.dumps([
            {
                "role": msg.role,
                "content": msg.content,
                "image_urls": msg.image_urls or []
            }
            for msg in request.messages
        ], ensure_ascii=False)
        
        # 创建聊天历史
        history_data = schemas.ChatHistoryCreate(
            title=title or "新对话",
            messages=messages_json
        )
        
        history = crud.create_chat_history(db, history_data)
        
        return {
            "id": history.id,
            "title": history.title,
            "created_at": history.created_at.isoformat(),
            "updated_at": history.updated_at.isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"保存聊天历史失败: {str(e)}")


@assistant_router.get("/history")
def list_chat_histories(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    q: Optional[str] = Query(None, description="搜索标题或内容"),
    db: Session = Depends(get_db)
):
    """
    获取聊天历史列表
    """
    try:
        histories = crud.list_chat_histories(db, skip=skip, limit=limit, q=q)
        
        return [
            {
                "id": h.id,
                "title": h.title,
                "created_at": h.created_at.isoformat(),
                "updated_at": h.updated_at.isoformat()
            }
            for h in histories
        ]
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取聊天历史列表失败: {str(e)}")


@assistant_router.get("/history/{history_id}")
def get_chat_history(history_id: int, db: Session = Depends(get_db)):
    """
    获取指定聊天历史详情
    """
    try:
        history = crud.get_chat_history(db, history_id)
        if not history:
            raise HTTPException(status_code=404, detail="聊天历史不存在")
        
        # 解析消息列表
        try:
            messages_data = json.loads(history.messages)
            messages = [
                ChatMessage(
                    role=msg.get("role", "user"),
                    content=msg.get("content", ""),
                    image_urls=msg.get("image_urls", [])
                )
                for msg in messages_data
            ]
        except json.JSONDecodeError:
            messages = []
        
        return {
            "id": history.id,
            "title": history.title,
            "messages": [{"role": m.role, "content": m.content, "image_urls": m.image_urls} for m in messages],
            "created_at": history.created_at.isoformat(),
            "updated_at": history.updated_at.isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取聊天历史失败: {str(e)}")


@assistant_router.put("/history/{history_id}")
def update_chat_history(
    history_id: int,
    request: SaveChatHistoryRequest,
    db: Session = Depends(get_db)
):
    """
    更新聊天历史
    """
    try:
        # 将消息列表转换为JSON字符串
        messages_json = json.dumps([
            {
                "role": msg.role,
                "content": msg.content,
                "image_urls": msg.image_urls or []
            }
            for msg in request.messages
        ], ensure_ascii=False)
        
        # 更新聊天历史
        history_data = schemas.ChatHistoryUpdate(
            title=request.title,
            messages=messages_json
        )
        
        history = crud.update_chat_history(db, history_id, history_data)
        if not history:
            raise HTTPException(status_code=404, detail="聊天历史不存在")
        
        return {
            "id": history.id,
            "title": history.title,
            "created_at": history.created_at.isoformat(),
            "updated_at": history.updated_at.isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"更新聊天历史失败: {str(e)}")


@assistant_router.delete("/history/{history_id}")
def delete_chat_history(history_id: int, db: Session = Depends(get_db)):
    """
    删除聊天历史
    """
    try:
        ok = crud.delete_chat_history(db, history_id)
        if not ok:
            raise HTTPException(status_code=404, detail="聊天历史不存在")
        return {"success": True}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"删除聊天历史失败: {str(e)}")


# ==================== 随机观点功能 ====================

@assistant_router.get("/random-opinion")
def get_random_opinion(
    category_id: Optional[int] = Query(None, description="按分类筛选"),
    db: Session = Depends(get_db)
):
    """
    随机获取一个观点（筛子功能）
    """
    try:
        opinion = crud.get_random_opinion(db, category_id)
        if not opinion:
            raise HTTPException(status_code=404, detail="没有找到观点")
        
        return {
            "id": opinion.id,
            "description": opinion.description,
            "category_id": opinion.category_id
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取随机观点失败: {str(e)}")


# ==================== 点赞记录功能 ====================

class LikeRecordCreate(BaseModel):
    """创建点赞记录请求"""
    question: str
    answer: str


@assistant_router.post("/likes/", response_model=schemas.LikeRecordOut, status_code=201)
def create_like_record(
    data: LikeRecordCreate,
    db: Session = Depends(get_db)
):
    """
    创建点赞记录
    """
    try:
        like_record = crud.create_like_record(db, schemas.LikeRecordCreate(
            question=data.question,
            answer=data.answer
        ))
        return like_record
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"创建点赞记录失败: {str(e)}")


@assistant_router.get("/likes/", response_model=List[schemas.LikeRecordOut])
def list_like_records(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """
    列表点赞记录
    """
    try:
        return crud.list_like_records(db, skip=skip, limit=limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取点赞记录列表失败: {str(e)}")


@assistant_router.get("/likes/{like_id}", response_model=schemas.LikeRecordOut)
def get_like_record(
    like_id: int,
    db: Session = Depends(get_db)
):
    """
    获取点赞记录详情
    """
    try:
        like_record = crud.get_like_record(db, like_id)
        if not like_record:
            raise HTTPException(status_code=404, detail="点赞记录不存在")
        return like_record
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取点赞记录失败: {str(e)}")


@assistant_router.delete("/likes/{like_id}", status_code=204)
def delete_like_record(
    like_id: int,
    db: Session = Depends(get_db)
):
    """
    删除点赞记录
    """
    try:
        ok = crud.delete_like_record(db, like_id)
        if not ok:
            raise HTTPException(status_code=404, detail="点赞记录不存在")
        return None
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"删除点赞记录失败: {str(e)}")
