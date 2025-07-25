/*
 Navicat Premium Data Transfer

 Source Server         : localhost
 Source Server Type    : MySQL
 Source Server Version : 80100
 Source Host           : localhost:3306
 Source Schema         : library-all

 Target Server Type    : MySQL
 Target Server Version : 80100
 File Encoding         : 65001

 Date: 15/07/2025 16:16:20
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for book
-- ----------------------------
DROP TABLE IF EXISTS `book`;
CREATE TABLE `book`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `author` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `publisher` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `isbn` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `stock` int NULL DEFAULT 0,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 4 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of book
-- ----------------------------
INSERT INTO `book` VALUES (1, '111', '111', '111', '111', 6);
INSERT INTO `book` VALUES (2, '222', '222', '222', '222', 2);
INSERT INTO `book` VALUES (3, '1111', '1111', '1111', '1111', 4);
INSERT INTO `book` VALUES (4, '図書館管理システム', '図書館', 'システム', '1111', 2);
INSERT INTO `book` VALUES (5, '666', '666', '666', '666', 1);

-- ----------------------------
-- Table structure for comment
-- ----------------------------
DROP TABLE IF EXISTS `comment`;
CREATE TABLE `comment`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `reader_id` int NULL DEFAULT NULL,
  `content` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `comment_date` datetime NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `reader_id`(`reader_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 6 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of comment
-- ----------------------------
INSERT INTO `comment` VALUES (1, 1, '111', '2025-07-07 00:00:00');
INSERT INTO `comment` VALUES (2, 2, '棒极了！', '2025-07-07 00:00:00');
INSERT INTO `comment` VALUES (3, 1, '我爱你', '2025-07-09 00:00:00');
INSERT INTO `comment` VALUES (4, 1, 'qwq', '2025-07-09 00:00:00');
INSERT INTO `comment` VALUES (5, 1, '6666666666', '2025-07-14 00:00:00');
INSERT INTO `comment` VALUES (6, 1, 'AAA的士速递第三方第三方代发算法的', '2025-07-15 00:00:00');
INSERT INTO `comment` VALUES (7, 1, '所发生的烦都烦死懂法守法沙发上', '2025-07-15 00:00:00');
INSERT INTO `comment` VALUES (8, 1, '666666666666666', '2025-07-15 14:41:50');

-- ----------------------------
-- Table structure for lend
-- ----------------------------
DROP TABLE IF EXISTS `lend`;
CREATE TABLE `lend`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `reader_id` int NULL DEFAULT NULL,
  `book_id` int NULL DEFAULT NULL,
  `lend_date` date NULL DEFAULT NULL,
  `due_date` date NULL DEFAULT NULL,
  `return_date` date NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `reader_id`(`reader_id`) USING BTREE,
  INDEX `book_id`(`book_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 10 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of lend
-- ----------------------------
INSERT INTO `lend` VALUES (1, 2, 1, '2025-07-07', '2025-08-06', NULL);
INSERT INTO `lend` VALUES (2, 1, 1, '2025-07-07', '2025-08-06', '2025-07-09');
INSERT INTO `lend` VALUES (3, 1, 1, '2025-07-09', '2025-08-08', '2025-07-09');
INSERT INTO `lend` VALUES (4, 1, 1, '2025-07-09', '2025-08-08', '2025-07-09');
INSERT INTO `lend` VALUES (5, 1, 1, '2025-07-09', '2025-08-08', '2025-07-09');
INSERT INTO `lend` VALUES (6, 1, 1, '2025-07-09', '2025-08-08', '2025-07-09');
INSERT INTO `lend` VALUES (7, 1, 1, '2025-07-09', '2025-08-08', NULL);
INSERT INTO `lend` VALUES (8, 1, 1, '2025-07-09', '2025-08-08', NULL);
INSERT INTO `lend` VALUES (9, 1, 1, '2025-07-09', '2025-08-08', '2025-07-14');
INSERT INTO `lend` VALUES (10, 1, 4, '2025-07-15', '2025-07-29', NULL);

-- ----------------------------
-- Table structure for notice
-- ----------------------------
DROP TABLE IF EXISTS `notice`;
CREATE TABLE `notice`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `staff_id` int NULL DEFAULT NULL,
  `reader_id` int NULL DEFAULT NULL,
  `content` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `send_date` datetime NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `staff_id`(`staff_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 9 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of notice
-- ----------------------------
INSERT INTO `notice` VALUES (1, 1, 1, '1234', '2025-07-07 13:49:18');
INSERT INTO `notice` VALUES (2, 1, 2, '111', '2025-07-09 05:33:03');
INSERT INTO `notice` VALUES (3, 1, 1, '1111', '2025-07-15 11:05:58');

-- ----------------------------
-- Table structure for reader
-- ----------------------------
DROP TABLE IF EXISTS `reader`;
CREATE TABLE `reader`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `password` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `contact` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `level` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT '普通会员',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `username`(`username`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 3 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of reader
-- ----------------------------
INSERT INTO `reader` VALUES (1, '1111', '1111', '读者1', NULL, '普通会员');
INSERT INTO `reader` VALUES (2, '1234', '1234', '读者2', NULL, '普通会员');

-- ----------------------------
-- Table structure for refund
-- ----------------------------
DROP TABLE IF EXISTS `refund`;
CREATE TABLE `refund`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `lend_id` int NULL DEFAULT NULL,
  `refund_date` date NULL DEFAULT NULL,
  `reason` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `lend_id`(`lend_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of refund
-- ----------------------------

-- ----------------------------
-- Table structure for reservation
-- ----------------------------
DROP TABLE IF EXISTS `reservation`;
CREATE TABLE `reservation`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `reader_id` int NULL DEFAULT NULL,
  `book_id` int NULL DEFAULT NULL,
  `date` date NULL DEFAULT NULL,
  `status` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `reader_id`(`reader_id`) USING BTREE,
  INDEX `book_id`(`book_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 4 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of reservation
-- ----------------------------
INSERT INTO `reservation` VALUES (1, 1, 5, '2025-07-15', '処理待ち');
INSERT INTO `reservation` VALUES (2, 1, 4, '2025-07-15', '処理済み');
INSERT INTO `reservation` VALUES (3, 1, 4, '2025-07-16', 'キャンセル済み');

-- ----------------------------
-- Table structure for return
-- ----------------------------
DROP TABLE IF EXISTS `return`;
CREATE TABLE `return`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `lend_id` int NULL DEFAULT NULL,
  `return_date` date NULL DEFAULT NULL,
  `status` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `lend_id`(`lend_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 6 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of return
-- ----------------------------
INSERT INTO `return` VALUES (1, 2, '2025-07-09', '已归还');
INSERT INTO `return` VALUES (2, 3, '2025-07-09', '已归还');
INSERT INTO `return` VALUES (3, 4, '2025-07-09', '已归还');
INSERT INTO `return` VALUES (4, 5, '2025-07-09', '已归还');
INSERT INTO `return` VALUES (5, 6, '2025-07-09', '已归还');

-- ----------------------------
-- Table structure for staff
-- ----------------------------
DROP TABLE IF EXISTS `staff`;
CREATE TABLE `staff`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `password` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `contact` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of staff
-- ----------------------------
INSERT INTO `staff` VALUES (1, '1111', '1111', '职员1', NULL);

SET FOREIGN_KEY_CHECKS = 1;
