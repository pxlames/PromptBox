import os
from openai import OpenAI
from typing import List, Iterator, Optional, Dict, Any
import base64
from pathlib import Path
from . import config


class DoubaoService:
    """豆包AI服务（ByteDance）"""
    
    def __init__(self):
        cfg = config.get_doubao_config()
        self.api_key = cfg.get("api_key") or os.environ.get("ARK_API_KEY")
        self.base_url = cfg.get("base_url", "https://ark.cn-beijing.volces.com/api/v3")
        self.model = cfg.get("model", "doubao-seed-1-6-251015")
        
        if not self.api_key:
            raise ValueError("ARK_API_KEY not found in config or environment variables")
        
        self.client = OpenAI(
            base_url=self.base_url,
            api_key=self.api_key,
        )
    
    def _prepare_image_url(self, image_path: str, is_url: bool = False) -> str:
        """准备图片URL
        
        Args:
            image_path: 图片路径（本地文件路径或URL）
            is_url: 是否为URL
            
        Returns:
            图片URL（如果是本地文件，需要转换为可访问的URL）
        """
        if is_url:
            return image_path
        
        # 如果是本地文件，需要检查是否为相对路径（uploads目录下的文件）
        # 在实际应用中，这些文件应该通过静态文件服务提供访问
        if image_path.startswith('/'):
            # 假设是通过静态服务访问的路径
            return image_path
        else:
            # 返回相对路径，前端会通过 /api/uploads/ 访问
            return f"/api/uploads/{image_path}"
    
    def chat(
        self,
        messages: List[Dict[str, Any]],
        stream: bool = False,
        reasoning_effort: str = "medium",
        temperature: float = 0.7,
        max_tokens: Optional[int] = None
    ) -> Any:
        """
        发送聊天请求（非流式）
        
        Args:
            messages: 消息列表，格式如：
                [
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "image_url",
                                "image_url": {"url": "..."}
                            },
                            {"type": "text", "text": "..."}
                        ]
                    }
                ]
            stream: 是否流式返回
            reasoning_effort: 推理努力程度 ("low", "medium", "high")
            temperature: 温度参数
            max_tokens: 最大token数
            
        Returns:
            如果是非流式，返回完整的响应对象
            如果是流式，返回流式迭代器
        """
        params = {
            "model": self.model,
            "messages": messages,
            "stream": stream,
            "reasoning_effort": reasoning_effort,
            "temperature": temperature,
        }
        
        if max_tokens:
            params["max_tokens"] = max_tokens
        
        if stream:
            return self.client.chat.completions.create(**params)
        else:
            return self.client.chat.completions.create(**params)
    
    def chat_stream(
        self,
        messages: List[Dict[str, Any]],
        reasoning_effort: str = "medium",
        temperature: float = 0.7,
        max_tokens: Optional[int] = None
    ) -> Iterator[str]:
        """
        发送聊天请求（流式）
        
        Args:
            messages: 消息列表
            reasoning_effort: 推理努力程度
            temperature: 温度参数
            max_tokens: 最大token数
            
        Yields:
            响应内容的增量片段
        """
        stream = self.chat(
            messages=messages,
            stream=True,
            reasoning_effort=reasoning_effort,
            temperature=temperature,
            max_tokens=max_tokens
        )
        
        reasoning_content = ""
        content = ""
        
        try:
            for chunk in stream:
                # 处理推理内容（如果有）
                if hasattr(chunk.choices[0].delta, 'reasoning_content') and chunk.choices[0].delta.reasoning_content:
                    reasoning_content += chunk.choices[0].delta.reasoning_content
                
                # 处理实际内容
                delta_content = chunk.choices[0].delta.content
                if delta_content is not None:
                    content += delta_content
                    yield delta_content
        except Exception as e:
            raise Exception(f"流式响应处理失败: {str(e)}")
    
    def chat_complete(
        self,
        messages: List[Dict[str, Any]],
        reasoning_effort: str = "medium",
        temperature: float = 0.7,
        max_tokens: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        发送聊天请求（非流式，返回完整内容）
        
        Args:
            messages: 消息列表
            reasoning_effort: 推理努力程度
            temperature: 温度参数
            max_tokens: 最大token数
            
        Returns:
            包含content和reasoning_content的字典
        """
        completion = self.chat(
            messages=messages,
            stream=False,
            reasoning_effort=reasoning_effort,
            temperature=temperature,
            max_tokens=max_tokens
        )
        
        message = completion.choices[0].message
        result = {
            "content": message.content or "",
            "reasoning_content": ""
        }
        
        if hasattr(message, 'reasoning_content'):
            result["reasoning_content"] = message.reasoning_content or ""
        
        return result


# 全局实例
_doubao_service = None


def get_doubao_service() -> DoubaoService:
    """获取豆包服务实例"""
    global _doubao_service
    if _doubao_service is None:
        _doubao_service = DoubaoService()
    return _doubao_service

