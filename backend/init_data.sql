-- 创建book表（如果不存在）
CREATE TABLE IF NOT EXISTS book (
  id int NOT NULL AUTO_INCREMENT,
  title varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  author varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  isbn varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  publisher varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  publish_date date NULL DEFAULT NULL,
  status varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT '可借',
  PRIMARY KEY (id) USING BTREE
);

-- 创建lend表（如果不存在）
CREATE TABLE IF NOT EXISTS lend (
  id int NOT NULL AUTO_INCREMENT,
  reader_id int NULL DEFAULT NULL,
  book_id int NULL DEFAULT NULL,
  lend_date date NULL DEFAULT NULL,
  due_date date NULL DEFAULT NULL,
  return_date date NULL DEFAULT NULL,
  PRIMARY KEY (id) USING BTREE,
  INDEX reader_id(reader_id) USING BTREE,
  INDEX book_id(book_id) USING BTREE
);

-- 插入测试数据
INSERT INTO staff (username, password, name, contact) VALUES 
('staff1', '123456', '张三', '13800138000'),
('staff2', '123456', '李四', '13800138001');

INSERT INTO reader (username, password, name, contact, level) VALUES 
('reader1', '123456', '王五', '13900139000', '普通会员'),
('reader2', '123456', '赵六', '13900139001', 'VIP会员');

INSERT INTO book (title, author, isbn, publisher, publish_date, status) VALUES 
('三国演义', '罗贯中', '9787020008728', '人民文学出版社', '1998-01-01', '可借'),
('水浒传', '施耐庵', '9787020008735', '人民文学出版社', '1997-01-01', '可借'),
('西游记', '吴承恩', '9787020008742', '人民文学出版社', '1999-01-01', '可借'),
('红楼梦', '曹雪芹', '9787020008759', '人民文学出版社', '1996-01-01', '可借'),
('Java编程思想', 'Bruce Eckel', '9787111213826', '机械工业出版社', '2007-01-01', '可借');

INSERT INTO reservation (reader_id, book_id, date, status) VALUES 
(1, 1, '2024-01-15', '待处理'),
(1, 2, '2024-01-16', '已处理'),
(2, 3, '2024-01-17', '待处理'),
(2, 4, '2024-01-18', '已取消');

INSERT INTO lend (reader_id, book_id, lend_date, due_date, return_date) VALUES 
(1, 1, '2024-01-10', '2024-02-10', '2024-01-25'),
(1, 2, '2024-01-15', '2024-02-15', NULL),
(2, 3, '2024-01-05', '2024-02-05', NULL),
(2, 4, '2023-12-01', '2024-01-01', '2023-12-20'); 