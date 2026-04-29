-- 敦煌洞窟信息系统 - 数据库初始化脚本

CREATE DATABASE IF NOT EXISTS dunhuang_grottoes CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE dunhuang_grottoes;

CREATE TABLE IF NOT EXISTS users (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE COMMENT '用户名',
    password VARCHAR(255) NOT NULL COMMENT '密码（明文）',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    is_deleted TINYINT(1) DEFAULT 0 COMMENT '是否删除（0-否 1-是）'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户表';

CREATE TABLE IF NOT EXISTS caves (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    location VARCHAR(100) NOT NULL COMMENT '所在（莫高窟、榆林窟、千佛洞）',
    number VARCHAR(50) NOT NULL COMMENT '洞窟编号',
    build_period VARCHAR(50) COMMENT '建造时代',
    status VARCHAR(50) DEFAULT '普窟' COMMENT '开发状态（特窟、普窟、未开放）',
    description TEXT COMMENT '洞窟描述',
    features TEXT COMMENT '洞窟特色',
    remarks TEXT COMMENT '备注',
    official_link VARCHAR(500) COMMENT '官网链接',
    has_video TINYINT(1) DEFAULT 0 COMMENT '是否有视频（0-否 1-是）',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    is_deleted TINYINT(1) DEFAULT 0 COMMENT '是否删除（0-否 1-是）'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='洞窟主表';

CREATE INDEX idx_caves_location ON caves(location);
CREATE INDEX idx_caves_status ON caves(status);
CREATE INDEX idx_caves_is_deleted ON caves(is_deleted);

CREATE TABLE IF NOT EXISTS cave_shapes (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    cave_id BIGINT NOT NULL COMMENT '洞窟ID',
    shape_name VARCHAR(100) NOT NULL COMMENT '形制名称',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    CONSTRAINT fk_cave_shapes_cave FOREIGN KEY (cave_id) REFERENCES caves(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='洞窟-形制关联表';

CREATE INDEX idx_cave_shapes_cave_id ON cave_shapes(cave_id);
CREATE INDEX idx_cave_shapes_shape_name ON cave_shapes(shape_name);

CREATE TABLE IF NOT EXISTS cave_repair_eras (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    cave_id BIGINT NOT NULL COMMENT '洞窟ID',
    repair_era VARCHAR(100) NOT NULL COMMENT '修复时代',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    CONSTRAINT fk_cave_repair_eras_cave FOREIGN KEY (cave_id) REFERENCES caves(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='洞窟-修复时代关联表';

CREATE INDEX idx_cave_repair_eras_cave_id ON cave_repair_eras(cave_id);
CREATE INDEX idx_cave_repair_eras_era ON cave_repair_eras(repair_era);

CREATE TABLE IF NOT EXISTS cave_images (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    cave_id BIGINT NOT NULL COMMENT '洞窟ID',
    image_url VARCHAR(500) NOT NULL COMMENT '图片URL',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    CONSTRAINT fk_cave_images_cave FOREIGN KEY (cave_id) REFERENCES caves(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='洞窟图片表';

CREATE INDEX idx_cave_images_cave_id ON cave_images(cave_id);

CREATE TABLE IF NOT EXISTS cave_videos (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    cave_id BIGINT NOT NULL COMMENT '洞窟ID',
    video_url VARCHAR(500) NOT NULL COMMENT '视频URL',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    CONSTRAINT fk_cave_videos_cave FOREIGN KEY (cave_id) REFERENCES caves(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='洞窟视频表';

CREATE INDEX idx_cave_videos_cave_id ON cave_videos(cave_id);

INSERT INTO users (username, password) VALUES ('admin', 'admin123');