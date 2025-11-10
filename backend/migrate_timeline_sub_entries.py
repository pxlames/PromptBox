"""
为 timeline_sub_entries 表创建迁移脚本
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
    """执行迁移：创建 timeline_sub_entries 表"""
    try:
        with engine.begin() as conn:  # 使用 begin() 自动提交事务
            # 检查表是否已存在
            check_sql = """
                SELECT COUNT(*) as count
                FROM information_schema.TABLES
                WHERE TABLE_SCHEMA = DATABASE()
                AND TABLE_NAME = 'timeline_sub_entries'
            """
            result = conn.execute(text(check_sql))
            count = result.scalar()
            
            if count > 0:
                print("[OK] timeline_sub_entries 表已存在，无需迁移")
                return
            
            # 创建表
            create_table_sql = """
                CREATE TABLE timeline_sub_entries (
                    id INT NOT NULL AUTO_INCREMENT,
                    entry_id INT NOT NULL,
                    subtitle VARCHAR(500) NOT NULL,
                    conclusion TEXT NULL,
                    content TEXT NULL,
                    image_paths TEXT NULL COMMENT '图片路径，用逗号分隔',
                    `order` INT NOT NULL DEFAULT 0,
                    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    PRIMARY KEY (id),
                    INDEX ix_timeline_sub_entries_id (id),
                    INDEX ix_timeline_sub_entries_entry_id (entry_id),
                    CONSTRAINT fk_timeline_sub_entries_entry_id 
                        FOREIGN KEY (entry_id) 
                        REFERENCES timeline_entries (id) 
                        ON DELETE CASCADE
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """
            conn.execute(text(create_table_sql))
            print("[OK] 成功创建 timeline_sub_entries 表")
            
    except Exception as e:
        error_msg = str(e)
        # 检查是否是"表已存在"的错误
        if 'already exists' in error_msg.lower() or 'Duplicate table name' in error_msg:
            print("[OK] timeline_sub_entries 表已存在，无需迁移")
            return
        
        print(f"[ERROR] 迁移失败: {e}")
        print("\n请手动执行以下 SQL 语句:")
        print("""
CREATE TABLE timeline_sub_entries (
    id INT NOT NULL AUTO_INCREMENT,
    entry_id INT NOT NULL,
    subtitle VARCHAR(500) NOT NULL,
    conclusion TEXT NULL,
    content TEXT NULL,
    image_paths TEXT NULL COMMENT '图片路径，用逗号分隔',
    `order` INT NOT NULL DEFAULT 0,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    INDEX ix_timeline_sub_entries_id (id),
    INDEX ix_timeline_sub_entries_entry_id (entry_id),
    CONSTRAINT fk_timeline_sub_entries_entry_id 
        FOREIGN KEY (entry_id) 
        REFERENCES timeline_entries (id) 
        ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
        """)
        sys.exit(1)


if __name__ == "__main__":
    print("开始执行数据库迁移...")
    migrate()
    print("迁移完成！")

