"""
批量导入算法题目到数据库
"""
import os
import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional

# 修复Windows控制台编码问题
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 添加backend目录到路径
sys.path.insert(0, str(Path(__file__).parent / 'backend'))

from sqlalchemy.orm import Session
from app.db import SessionLocal, engine
from app.models import AlgoCategory, AlgoProblem
from app.db import Base

# 确保数据库表存在
Base.metadata.create_all(bind=engine)


def extract_from_ipynb(file_path: Path) -> Optional[str]:
    """从Jupyter notebook中提取代码"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            notebook = json.load(f)
        
        code_cells = []
        for cell in notebook.get('cells', []):
            if cell.get('cell_type') == 'code':
                source = cell.get('source', [])
                if isinstance(source, list):
                    code = ''.join(source)
                else:
                    code = source
                if code.strip():
                    code_cells.append(code)
        
        return '\n\n'.join(code_cells)
    except Exception as e:
        print(f"  读取ipynb文件失败: {e}")
        return None


def extract_problem_info(file_path: Path) -> Optional[Dict]:
    """从文件中提取题目信息"""
    # 处理ipynb文件
    if file_path.suffix == '.ipynb':
        content = extract_from_ipynb(file_path)
        if not content:
            return None
    else:
        try:
            content = file_path.read_text(encoding='utf-8')
        except Exception as e:
            print(f"  读取文件失败: {e}")
            return None
    
    # 从文件名提取题目标题
    name = file_path.stem
    
    # 清理文件名：移除日期前缀、扩展名等
    title = name
    # 移除 dateXX- 前缀
    title = re.sub(r'^date\d+-', '', title)
    # 移除数字前缀（如 554-砖墙）
    title = re.sub(r'^\d+-', '', title)
    # 移除 copy 后缀
    title = re.sub(r'\s+copy$', '', title, flags=re.IGNORECASE)
    # 移除括号内容（如 "数组的相对排序(数组)"）
    title = re.sub(r'\([^)]*\)', '', title)
    title = title.strip()
    
    # 从代码中提取信息
    description_parts = []
    solution = content
    
    # 尝试提取注释中的描述
    lines = content.split('\n')
    comment_lines = []
    for line in lines[:30]:  # 查看前30行
        line = line.strip()
        if line.startswith('#') and len(line) > 1:
            comment = line[1:].strip()
            if comment and not comment.startswith('!'):  # 忽略 shebang
                if not comment.startswith('coding') and not comment.startswith('utf'):
                    comment_lines.append(comment)
    
    if comment_lines:
        description_parts.extend(comment_lines)
    
    # 从docstring提取描述
    docstring_match = re.search(r'"""(.*?)"""', content, re.DOTALL)
    if docstring_match:
        doc = docstring_match.group(1).strip()
        if doc and len(doc) > 10:  # 忽略太短的docstring
            description_parts.append(doc)
    
    # 如果描述为空，使用标题作为描述
    if not description_parts:
        description = f"算法题目：{title}"
    else:
        description = '\n'.join(description_parts[:5])  # 只取前5个描述
    
    # 推断分类（根据文件名和内容）
    title_lower = title.lower()
    content_lower = content.lower()
    
    category_name = None
    
    # 链表相关
    if '链表' in title or 'linked' in content_lower or 'list' in content_lower and '链表' in content:
        category_name = '链表'
    # 数组相关
    elif '数组' in title or any(kw in title for kw in ['轮转', '两数之和', '删除重复', '相对排序', '第K个最大']):
        category_name = '数组'
    # 字符串相关
    elif '字符串' in title or any(kw in title for kw in ['回文', '子串', '子序列', '重排序', '无重复']):
        category_name = '字符串'
    # 动态规划相关
    elif any(kw in title for kw in ['公共子', '最长', '不相交']) or 'dp' in content_lower or '动态规划' in content:
        category_name = '动态规划'
    # 二叉树相关
    elif '二叉树' in title or 'tree' in content_lower or '二叉搜索树' in title or '中序遍历' in title:
        category_name = '二叉树'
    # 栈相关
    elif '栈' in title or 'stack' in content_lower or '接雨水' in title:
        category_name = '栈'
    # 哈希表相关
    elif any(kw in title for kw in ['哈希', 'LRU', '缓存', '异位', '两数之和']):
        category_name = '哈希表'
    # 图论相关
    elif any(kw in title for kw in ['岛屿', '矩阵']) or 'graph' in content_lower:
        category_name = '图论'
    
    # 推断标签
    tags_set = set()
    
    # 根据文件名和内容添加标签
    if '链表' in title or 'linked' in content_lower:
        tags_set.add('链表')
    if '数组' in title or 'array' in content_lower:
        tags_set.add('数组')
    if '字符串' in title or 'string' in content_lower:
        tags_set.add('字符串')
    if '二叉树' in title or 'tree' in content_lower or 'binary' in content_lower:
        tags_set.add('二叉树')
    if '动态规划' in content or 'dp' in content_lower:
        tags_set.add('动态规划')
    if '递归' in content or 'recursion' in content_lower:
        tags_set.add('递归')
    if '双指针' in content or 'two pointer' in content_lower or 'two-pointer' in content_lower:
        tags_set.add('双指针')
    if '哈希' in content or 'hash' in content_lower or 'dict' in content_lower:
        tags_set.add('哈希表')
    if '栈' in content or 'stack' in content_lower:
        tags_set.add('栈')
    if '队列' in content or 'queue' in content_lower:
        tags_set.add('队列')
    if '二分' in content or 'binary search' in content_lower:
        tags_set.add('二分查找')
    if '滑动窗口' in content or 'sliding window' in content_lower:
        tags_set.add('滑动窗口')
    
    tags = ','.join(sorted(list(tags_set))) if tags_set else ''
    
    # 推断难度（简单启发式）
    difficulty = '中等'  # 默认中等
    if any(kw in title for kw in ['两数之和', '最小栈', '反转链表']):
        difficulty = '简单'
    elif any(kw in title for kw in ['合并k个', '最长公共子序列', '接雨水', 'LRU']):
        difficulty = '困难'
    
    return {
        'title': title,
        'description': description,
        'solution': solution[:5000] if len(solution) > 5000 else solution,  # 限制长度
        'difficulty': difficulty,
        'tags': tags,
        'category_name': category_name,  # 用于后续匹配分类ID
        'status': '未开始',
        'link': '',
        'companies': ''
    }


def create_category_if_not_exists(db: Session, name: str) -> Optional[int]:
    """创建分类（如果不存在）"""
    try:
        # 查找现有分类
        existing = db.query(AlgoCategory).filter(AlgoCategory.name == name).first()
        if existing:
            return existing.id
        
        # 获取最大order值
        max_order = db.query(AlgoCategory).count()
        
        # 创建新分类
        category = AlgoCategory(name=name, order=max_order + 1)
        db.add(category)
        db.commit()
        db.refresh(category)
        return category.id
    except Exception as e:
        print(f"  创建分类失败 {name}: {e}")
        db.rollback()
        return None


def import_problem(db: Session, problem_data: Dict) -> bool:
    """导入单个题目"""
    try:
        # 检查是否已存在（通过标题）
        existing = db.query(AlgoProblem).filter(AlgoProblem.title == problem_data['title']).first()
        if existing:
            print(f"  [!] 题目已存在，跳过: {problem_data['title']}")
            return False
        
        # 创建新题目
        problem = AlgoProblem(
            title=problem_data['title'],
            category_id=problem_data.get('category_id'),
            difficulty=problem_data.get('difficulty', '中等'),
            companies=problem_data.get('companies', ''),
            tags=problem_data.get('tags', ''),
            status=problem_data.get('status', '未开始'),
            link=problem_data.get('link', ''),
            description=problem_data.get('description', ''),
            solution=problem_data.get('solution', '')
        )
        db.add(problem)
        db.commit()
        db.refresh(problem)
        print(f"  [+] 成功导入: {problem_data['title']}")
        return True
    except Exception as e:
        print(f"  [-] 导入失败 {problem_data['title']}: {e}")
        db.rollback()
        return False


def main():
    """主函数"""
    # 创建数据库会话
    db = SessionLocal()
    
    try:
        # 题目目录
        problems_dir = Path(r"D:\project\Improve-Algorithm\常考题目")
        
        if not problems_dir.exists():
            print(f"目录不存在: {problems_dir}")
            return
        
        # 获取所有Python文件和ipynb文件（排除图片和测试文件）
        py_files = list(problems_dir.glob("*.py"))
        ipynb_files = [f for f in problems_dir.glob("*.ipynb") if 'image' not in f.name.lower() and 'test' not in f.name.lower()]
        all_files = py_files + ipynb_files
        
        # 排除测试文件和图片
        all_files = [f for f in all_files if 'test' not in f.name.lower() and 'image' not in f.name.lower() and 'snipaste' not in f.name.lower()]
        
        print(f"找到 {len(py_files)} 个Python文件和 {len(ipynb_files)} 个Jupyter文件，共 {len(all_files)} 个文件")
        
        # 创建默认分类（如果不存在）
        default_categories = ['数组', '链表', '字符串', '动态规划', '二叉树', '栈', '哈希表', '图论']
        category_map = {}
        for cat_name in default_categories:
            cat_id = create_category_if_not_exists(db, cat_name)
            if cat_id:
                category_map[cat_name] = cat_id
                print(f"[+] 分类已就绪: {cat_name} (ID: {cat_id})")
        
        # 提取并导入题目
        imported_count = 0
        failed_count = 0
        skipped_count = 0
        
        for file in all_files:
            print(f"\n处理文件: {file.name}")
            problem_info = extract_problem_info(file)
            
            if problem_info:
                # 设置分类ID
                category_name = problem_info.pop('category_name')
                if category_name and category_name in category_map:
                    problem_info['category_id'] = category_map[category_name]
                else:
                    problem_info['category_id'] = None
                
                if import_problem(db, problem_info):
                    imported_count += 1
                else:
                    failed_count += 1
            else:
                print(f"  [-] 无法提取题目信息，跳过")
                skipped_count += 1
        
        print(f"\n{'='*50}")
        print(f"导入完成!")
        print(f"成功: {imported_count}")
        print(f"失败: {failed_count}")
        print(f"跳过: {skipped_count}")
        print(f"{'='*50}")
    
    finally:
        db.close()


if __name__ == "__main__":
    main()

