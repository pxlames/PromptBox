-- 为 timeline_entries 表添加 image_paths 列
-- 如果列已存在，会报错但不会影响数据

ALTER TABLE timeline_entries 
ADD COLUMN image_paths TEXT NULL COMMENT '图片路径，用逗号分隔' 
AFTER content;

