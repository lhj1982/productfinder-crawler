-- launch.products definition

CREATE TABLE `products` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `stylecolor` varchar(100) NOT NULL,
  `name` varchar(100) NOT NULL,
  `description` varchar(100) DEFAULT NULL,
  `price` double DEFAULT NULL,
  `url` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT NULL,
  `start_time` datetime DEFAULT NULL,
  `enabled` tinyint(4) DEFAULT '0',
  `rating` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `products_UN` (`stylecolor`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


-- launch.product_reviews definition

CREATE TABLE `product_reviews` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `product_id` bigint(20) NOT NULL,
  `source` varchar(100) NOT NULL COMMENT 'e.g. weibo',
  `text` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `timestamp` timestamp NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `account_id` varchar(100) NOT NULL,
  `account_name` varchar(100) DEFAULT NULL,
  `review_user_id` varchar(100) NOT NULL,
  `review_user_name` varchar(100) DEFAULT NULL,
  `like_count` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `product_reviews_UN` (`product_id`,`source`,`timestamp`,`account_id`,`review_user_id`,`text`(255)),
  CONSTRAINT `product_reviews_FK` FOREIGN KEY (`product_id`) REFERENCES `products` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=147 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


CREATE TABLE launch.product_prices (
	id BIGINT auto_increment NOT NULL,
	product_id BIGINT NOT NULL,
	check_date DATETIME NOT NULL,
	price DOUBLE NULL,
	CONSTRAINT product_prices_PK PRIMARY KEY (id),
	CONSTRAINT product_prices_UN UNIQUE KEY (product_id,check_date)
)
ENGINE=InnoDB
DEFAULT CHARSET=utf8mb4
COLLATE=utf8mb4_0900_ai_ci;


CREATE TABLE product_crawl_record
(
    id BIGINT auto_increment NOT NULL,
    product_id BIGINT NOT NULL,
    stylecolor varchar(64)  not null,
    platform   varchar(255) not null,
    crawl_time DATETIME DEFAULT NULL,
    CONSTRAINT product_crawl_record_PK PRIMARY KEY (id)
) ENGINE=InnoDB
DEFAULT CHARSET=utf8mb4
COLLATE=utf8mb4_0900_ai_ci;