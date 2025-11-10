"""
为 timeline_entries 表添加 image_paths 列的迁移脚本
"""
import sys
import io
from pathlib import Path

# 设置输出编码为 UTF-8（Windows 兼容）
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent))

from app.db import engine
from sqlalchemy import text


def migrate():
    """执行迁移：为 timeline_entries 表添加 image_paths 列"""
    try:
        with engine.begin() as conn:  # 使用 begin() 自动提交事务
            # 检查列是否已存在
            check_sql = """
                SELECT COUNT(*) as count
                FROM information_schema.COLUMNS
                WHERE TABLE_SCHEMA = DATABASE()
                AND TABLE_NAME = 'timeline_entries'
                AND COLUMN_NAME = 'image_paths'
            """
            result = conn.execute(text(check_sql))
            count = result.scalar()
            
            if count > 0:
                print("[OK] image_paths 列已存在，无需迁移")
                return
            
            # 添加列（使用 IF NOT EXISTS 的方式，如果 MySQL 版本支持）
            # 如果不支持，会抛出异常，我们捕获并提示手动执行
            alter_sql = """
                ALTER TABLE timeline_entries 
                ADD COLUMN image_paths TEXT NULL COMMENT '图片路径，用逗号分隔' 
                AFTER content
            """
            conn.execute(text(alter_sql))
            print("[OK] 成功为 timeline_entries 表添加 image_paths 列")
            
    except Exception as e:
        error_msg = str(e)
        # 检查是否是"列已存在"的错误
        if 'Duplicate column name' in error_msg or 'already exists' in error_msg.lower():
            print("[OK] image_paths 列已存在，无需迁移")
            return
        
        print(f"[ERROR] 迁移失败: {e}")
        print("\n请手动执行以下 SQL 语句:")
        print("ALTER TABLE timeline_entries ADD COLUMN image_paths TEXT NULL AFTER content;")
        print("\n或者如果列已存在，可以忽略此错误")
        sys.exit(1)


if __name__ == "__main__":
    print("开始执行数据库迁移...")
    migrate()
    print("迁移完成！")

