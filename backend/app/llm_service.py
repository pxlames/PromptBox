import requests
from typing import Dict, Optional, Iterator
import json
from . import config


class LLMService:
    """大模型调用服务"""
    
    def __init__(self):
        self.config = config.get_siliconflow_config()
        self.api_key = self.config.get("api_key")
        self.base_url = self.config.get("base_url")
        self.model = self.config.get("model")
    
    def breakdown_jd(
        self, 
        jd_content: str, 
        system_prompt: Optional[str] = None
    ) -> str:
        """
        拆解JD（岗位要求）
        
        Args:
            jd_content: JD内容（文字描述）
            system_prompt: 系统提示词，如果为None则使用默认提示词
            
        Returns:
            拆解后的内容（Markdown格式）
        """
        # 默认系统提示词
        default_system_prompt = """你是一个专业的JD（岗位要求）分析专家。你的任务是对JD中的每一句话进行详细解释和分析。

请按照以下要求输出拆解结果（使用Markdown格式）：

## 逐句解释
**这是核心部分，必须逐句解释JD中的每一句话：**

将JD的内容按照段落和句子进行拆分，对每一句话（或每一条要求）进行详细解释：

### 格式示例：
```
### 第X段：岗位职责

**原句**：[粘贴JD中的原句]

**详细解释**：
- 这句话的具体含义是什么？
- 这句话要求候选人具备什么能力？
- 这句话在实际工作中意味着需要做什么？
- 这句话可能包含的隐式要求有哪些？
```

### 解释要求：
1. **逐句拆分**：将JD按句子或要点拆分开，不要遗漏任何一句
2. **详细解释**：对每一句话都要详细解释其含义、要求、隐含意思
3. **通俗易懂**：用通俗易懂的语言解释，避免只是重复原话
4. **深入分析**：不仅要说明字面意思，还要分析其背后的深层要求
5. **能力映射**：说明这句话对应需要什么技能、经验、能力

## 总结归纳
在逐句解释完成后，简要总结：
- JD中提到的核心技能要求
- JD中强调的关键能力
- JD中可能隐含的额外要求

请确保不遗漏JD中的任何一句话，每句话都要有详细解释。
"""
        
        # 如果没有提供自定义系统提示词，使用默认的
        system_prompt = system_prompt or default_system_prompt
        
        # 构建消息
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"请分析以下JD：\n\n{jd_content}"}
        ]
        
        # 调用API
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": 0.7,
            "max_tokens": 8000
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=payload,
                timeout=60
            )
            
            # 检查响应状态
            if response.status_code == 403:
                error_msg = "API访问被拒绝 (403 Forbidden)"
                try:
                    error_detail = response.json()
                    # SiliconFlow API返回格式：{"code": 30001, "message": "...", "data": null}
                    if isinstance(error_detail, dict):
                        if 'message' in error_detail:
                            error_msg = f"{error_msg}: {error_detail['message']}"
                        elif 'error' in error_detail:
                            if isinstance(error_detail['error'], dict) and 'message' in error_detail['error']:
                                error_msg = f"{error_msg}: {error_detail['error']['message']}"
                            else:
                                error_msg = f"{error_msg}: {error_detail['error']}"
                except:
                    # 如果无法解析JSON，尝试读取文本
                    try:
                        error_text = response.text[:200]
                        if error_text:
                            error_msg = f"{error_msg}: {error_text}"
                    except:
                        pass
                raise Exception(error_msg)
            
            response.raise_for_status()
            
            result = response.json()
            
            # 提取回复内容
            if "choices" in result and len(result["choices"]) > 0:
                content = result["choices"][0]["message"]["content"]
                return content
            else:
                raise Exception("API返回的数据格式异常")
                
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 403:
                error_msg = "API访问被拒绝 (403 Forbidden)"
                try:
                    error_detail = e.response.json()
                    # SiliconFlow API返回格式：{"code": 30001, "message": "...", "data": null}
                    if isinstance(error_detail, dict):
                        if 'message' in error_detail:
                            error_msg = f"{error_msg}: {error_detail['message']}"
                        elif 'error' in error_detail:
                            if isinstance(error_detail['error'], dict) and 'message' in error_detail['error']:
                                error_msg = f"{error_msg}: {error_detail['error']['message']}"
                            else:
                                error_msg = f"{error_msg}: {error_detail['error']}"
                except:
                    # 如果无法解析JSON，尝试读取文本
                    try:
                        error_text = e.response.text[:200]
                        if error_text:
                            error_msg = f"{error_msg}: {error_text}"
                    except:
                        pass
                if error_msg == "API访问被拒绝 (403 Forbidden)":
                    error_msg = 'API访问被拒绝 (403)，请检查API密钥是否有效、账户是否有余额、以及是否有权限访问该模型'
                raise Exception(error_msg)
            raise Exception(f"调用大模型API失败 (HTTP {e.response.status_code}): {str(e)}")
        except requests.exceptions.RequestException as e:
            raise Exception(f"调用大模型API失败: {str(e)}")
        except Exception as e:
            raise Exception(f"解析响应失败: {str(e)}")
    
    def breakdown_jd_stream(
        self,
        jd_content: str,
        system_prompt: Optional[str] = None
    ) -> Iterator[str]:
        """
        流式拆解JD（岗位要求）
        
        Args:
            jd_content: JD内容（文字描述）
            system_prompt: 系统提示词，如果为None则使用默认提示词
            
        Yields:
            拆解内容的增量片段
        """
        # 默认系统提示词（与基础API保持一致）
        default_system_prompt = """你是一个专业的JD（岗位要求）分析专家。你的任务是对JD中的每一句话进行详细解释和分析。

请按照以下要求输出拆解结果（使用Markdown格式）：

## 逐句解释
**这是核心部分，必须逐句解释JD中的每一句话：**

将JD的内容按照段落和句子进行拆分，对每一句话（或每一条要求）进行详细解释：

### 格式示例：
```
### 第X段：岗位职责

**原句**：[粘贴JD中的原句]

**详细解释**：
- 这句话的具体含义是什么？
- 这句话要求候选人具备什么能力？
- 这句话在实际工作中意味着需要做什么？
- 这句话可能包含的隐式要求有哪些？
```

### 解释要求：
1. **逐句拆分**：将JD按句子或要点拆分开，不要遗漏任何一句
2. **详细解释**：对每一句话都要详细解释其含义、要求、隐含意思
3. **通俗易懂**：用通俗易懂的语言解释，避免只是重复原话
4. **深入分析**：不仅要说明字面意思，还要分析其背后的深层要求
5. **能力映射**：说明这句话对应需要什么技能、经验、能力

## 总结归纳
在逐句解释完成后，简要总结：
- JD中提到的核心技能要求
- JD中强调的关键能力
- JD中可能隐含的额外要求

请确保不遗漏JD中的任何一句话，每句话都要有详细解释。
"""
        
        # 如果没有提供自定义系统提示词，使用默认的
        system_prompt = system_prompt or default_system_prompt
        
        # 构建消息
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"请分析以下JD：\n\n{jd_content}"}
        ]
        
        # 调用API
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": 0.7,
            "max_tokens": 8000,
            "stream": True
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=payload,
                stream=True,
                timeout=120
            )
            
            # 检查响应状态
            if response.status_code == 403:
                error_msg = "API访问被拒绝 (403 Forbidden)"
                try:
                    error_detail = response.json()
                    # SiliconFlow API返回格式：{"code": 30001, "message": "...", "data": null}
                    if isinstance(error_detail, dict):
                        if 'message' in error_detail:
                            error_msg = f"{error_msg}: {error_detail['message']}"
                        elif 'error' in error_detail:
                            if isinstance(error_detail['error'], dict) and 'message' in error_detail['error']:
                                error_msg = f"{error_msg}: {error_detail['error']['message']}"
                            else:
                                error_msg = f"{error_msg}: {error_detail['error']}"
                except:
                    # 如果无法解析JSON，尝试读取文本
                    try:
                        error_text = response.text[:200]
                        if error_text:
                            error_msg = f"{error_msg}: {error_text}"
                    except:
                        pass
                raise Exception(error_msg)
            
            response.raise_for_status()
            
            # 处理流式响应
            for line in response.iter_lines():
                if line:
                    line_text = line.decode('utf-8')
                    # 跳过以 "data: " 开头的行
                    if line_text.startswith('data: '):
                        data_str = line_text[6:]  # 移除 "data: " 前缀
                        
                        # 检查是否是结束标记
                        if data_str.strip() == '[DONE]':
                            break
                        
                        try:
                            data = json.loads(data_str)
                            # 提取增量内容
                            if "choices" in data and len(data["choices"]) > 0:
                                delta = data["choices"][0].get("delta", {})
                                content = delta.get("content", "")
                                if content:
                                    yield content
                        except json.JSONDecodeError:
                            # 忽略无法解析的行
                            continue
                            
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 403:
                error_msg = "API访问被拒绝 (403 Forbidden)"
                try:
                    error_detail = e.response.json()
                    # SiliconFlow API返回格式：{"code": 30001, "message": "...", "data": null}
                    if isinstance(error_detail, dict):
                        if 'message' in error_detail:
                            error_msg = f"{error_msg}: {error_detail['message']}"
                        elif 'error' in error_detail:
                            if isinstance(error_detail['error'], dict) and 'message' in error_detail['error']:
                                error_msg = f"{error_msg}: {error_detail['error']['message']}"
                            else:
                                error_msg = f"{error_msg}: {error_detail['error']}"
                except:
                    # 如果无法解析JSON，尝试读取文本
                    try:
                        error_text = e.response.text[:200]
                        if error_text:
                            error_msg = f"{error_msg}: {error_text}"
                    except:
                        pass
                if error_msg == "API访问被拒绝 (403 Forbidden)":
                    error_msg = 'API访问被拒绝 (403)，请检查API密钥是否有效、账户是否有余额、以及是否有权限访问该模型'
                raise Exception(error_msg)
            raise Exception(f"调用大模型API失败 (HTTP {e.response.status_code}): {str(e)}")
        except requests.exceptions.RequestException as e:
            raise Exception(f"调用大模型API失败: {str(e)}")
        except Exception as e:
            raise Exception(f"解析响应失败: {str(e)}")


# 全局实例
_llm_service = None


def get_llm_service() -> LLMService:
    """获取LLM服务实例"""
    global _llm_service
    if _llm_service is None:
        _llm_service = LLMService()
    return _llm_service
