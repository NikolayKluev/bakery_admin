-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Хост: 127.0.0.1
-- Время создания: Окт 26 2026 г., 18:40
-- Версия сервера: 10.4.32-MariaDB
-- Версия PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- База данных: `bakery_admin`
--

-- --------------------------------------------------------

--
-- Структура таблицы `admin_setting`
--

CREATE TABLE `admin_setting` (
  `id` int(11) NOT NULL,
  `skey` varchar(100) NOT NULL,
  `svalue` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Дамп данных таблицы `admin_setting`
--

INSERT INTO `admin_setting` (`id`, `skey`, `svalue`) VALUES
(2, 'security.password_policy', '{\"min_length\": 6, \"require_digits\": false, \"require_upper\": false, \"lock_threshold\": 5}'),
(3, 'backup.config', '{\"enabled\": false, \"retention_days\": 14}');

-- --------------------------------------------------------

--
-- Структура таблицы `auth_log`
--

CREATE TABLE `auth_log` (
  `id` int(11) NOT NULL,
  `attempted_login` varchar(50) DEFAULT NULL,
  `ip` varchar(45) DEFAULT NULL,
  `user_agent` varchar(255) DEFAULT NULL,
  `is_success` tinyint(1) DEFAULT NULL,
  `reason` varchar(100) DEFAULT NULL,
  `created_at` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Дамп данных таблицы `auth_log`
--

INSERT INTO `auth_log` (`id`, `attempted_login`, `ip`, `user_agent`, `is_success`, `reason`, `created_at`) VALUES
(7, 'tipovv', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 YaBrowser/26.8.0.0 Safari/537.36', 1, 'success', '2026-10-22 17:36:29'),
(8, 'sam', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 YaBrowser/26.8.0.0 Safari/537.36', 1, 'success', '2026-10-22 17:37:17'),
(9, 'sam', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 YaBrowser/26.10.0.0 Safari/537.36', 1, 'success', '2026-10-22 19:02:04'),
(10, 'sam', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 YaBrowser/26.10.0.0 Safari/537.36', 1, 'success', '2026-10-25 21:40:45'),
(11, 'sammuel', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 YaBrowser/26.10.0.0 Safari/537.36', 1, 'success', '2026-10-25 21:55:03'),
(12, 'tipovv', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 YaBrowser/26.10.0.0 Safari/537.36', 1, 'success', '2026-10-26 19:45:15'),
(13, 'sam', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 YaBrowser/26.10.0.0 Safari/537.36', 1, 'success', '2026-10-26 19:45:25'),
(14, 'sam', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 YaBrowser/26.10.0.0 Safari/537.36', 0, 'bad_credentials', '2026-10-26 20:05:05'),
(15, 'sam', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 YaBrowser/26.10.0.0 Safari/537.36', 1, 'success', '2026-10-26 20:05:16'),
(16, 'tipovv', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 YaBrowser/26.10.0.0 Safari/537.36', 0, 'bad_credentials', '2026-10-26 20:08:37'),
(17, 'tipovv', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 YaBrowser/26.10.0.0 Safari/537.36', 0, 'bad_credentials', '2026-10-26 20:08:47'),
(18, 'tipovv', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 YaBrowser/26.10.0.0 Safari/537.36', 1, 'success', '2026-10-26 20:09:01'),
(19, 'sammuel', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 YaBrowser/26.10.0.0 Safari/537.36', 1, 'success', '2026-10-26 20:10:16');

-- --------------------------------------------------------

--
-- Структура таблицы `backup_log`
--

CREATE TABLE `backup_log` (
  `id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `started_at` datetime NOT NULL,
  `finished_at` datetime DEFAULT NULL,
  `status` enum('pending','running','success','failed') NOT NULL DEFAULT 'pending',
  `file_path` varchar(255) DEFAULT NULL,
  `message` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Дамп данных таблицы `backup_log`
--

INSERT INTO `backup_log` (`id`, `user_id`, `started_at`, `finished_at`, `status`, `file_path`, `message`) VALUES
(1, 1, '2026-10-11 17:56:11', NULL, 'running', NULL, NULL),
(2, 1, '2026-10-11 17:56:30', NULL, 'running', NULL, NULL),
(3, 1, '2026-10-11 18:07:22', '2026-10-11 18:07:24', 'success', '/backups/backup-2026-10-11.sql.gz', 'Резервная копия создана успешно.'),
(4, 1, '2026-10-11 18:12:55', '2026-10-11 18:12:57', 'success', '/backups/backup-2026-10-11.sql.gz', 'Резервная копия создана успешно.'),
(5, 1, '2026-10-11 18:13:33', '2026-10-11 18:13:35', 'success', '/backups/backup-2026-10-11.sql.gz', 'Резервная копия создана успешно.'),
(6, 1, '2026-10-11 18:35:45', '2026-10-11 18:35:47', 'success', '/backups/backup-2026-10-11.sql.gz', 'Резервная копия создана успешно.'),
(7, 1, '2026-10-11 18:37:22', '2026-10-11 18:37:24', 'success', '/backups/backup-2026-10-11.sql.gz', 'Резервная копия создана успешно.'),
(8, 1, '2026-10-17 17:23:25', '2026-10-17 17:23:27', 'success', '/backups/backup-2026-10-17.sql.gz', 'Резервная копия создана успешно.'),
(9, 1, '2026-10-17 17:24:53', '2026-10-17 17:24:55', 'success', '/backups/backup-2026-10-17.sql.gz', 'Резервная копия создана успешно.');

-- --------------------------------------------------------

--
-- Структура таблицы `integration`
--

CREATE TABLE `integration` (
  `id` int(11) NOT NULL,
  `name` varchar(100) DEFAULT NULL,
  `type` varchar(50) DEFAULT NULL,
  `config` text DEFAULT NULL,
  `is_active` tinyint(1) DEFAULT NULL,
  `created_at` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Дамп данных таблицы `integration`
--

INSERT INTO `integration` (`id`, `name`, `type`, `config`, `is_active`, `created_at`) VALUES
(1, 'number one', 'payment', '{\"host\":\"smtp.example.com\",\"port\":587,\"user\":\"...\",\"pass\":\"...\"}', 0, '2026-10-11 13:59:53'),
(2, '[object Object]', 'marketing', '{}\r\n        ', 0, '2026-10-17 19:51:46');

-- --------------------------------------------------------

--
-- Структура таблицы `permissions`
--

CREATE TABLE `permissions` (
  `id` int(11) NOT NULL,
  `code` varchar(50) NOT NULL COMMENT 'Уникальный код права',
  `description` text NOT NULL COMMENT 'Описание того, что это право даёт пользователю'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Дамп данных таблицы `permissions`
--

INSERT INTO `permissions` (`id`, `code`, `description`) VALUES
(1, 'bakeries.create', 'Создание новых пекарен'),
(2, 'recipes.manage', 'Управление рецептами блюд'),
(3, 'orders.view', 'Просмотр заказов клиентов'),
(4, 'reports.generate', 'Генерация отчётов о продажах'),
(5, 'users.edit', 'Редактирование профилей пользователей');

-- --------------------------------------------------------

--
-- Структура таблицы `products`
--

CREATE TABLE `products` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL COMMENT 'Название изделия',
  `category` varchar(100) DEFAULT NULL COMMENT 'Категория (может быть null)',
  `unit_price` float NOT NULL DEFAULT 0 COMMENT 'Цена за единицу'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Дамп данных таблицы `products`
--

INSERT INTO `products` (`id`, `name`, `category`, `unit_price`) VALUES
(1, 'Пирог яблочный', 'Пироги', 1000),
(2, 'Пирог клубничный', 'Пироги', 1200);

-- --------------------------------------------------------

--
-- Структура таблицы `roles`
--

CREATE TABLE `roles` (
  `id` int(11) NOT NULL,
  `name` varchar(50) NOT NULL COMMENT 'Название роли: admin, cashier, user'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Дамп данных таблицы `roles`
--

INSERT INTO `roles` (`id`, `name`) VALUES
(1, 'Admin'),
(3, 'Backer'),
(2, 'Cashier');

-- --------------------------------------------------------

--
-- Структура таблицы `role_permissions`
--

CREATE TABLE `role_permissions` (
  `role_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Дамп данных таблицы `role_permissions`
--

INSERT INTO `role_permissions` (`role_id`, `permission_id`) VALUES
(1, 2),
(1, 3),
(1, 4),
(1, 5),
(2, 3),
(3, 1),
(3, 3);

-- --------------------------------------------------------

--
-- Структура таблицы `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `login` varchar(50) NOT NULL,
  `full_name` varchar(150) DEFAULT NULL,
  `email` varchar(150) DEFAULT NULL,
  `role` enum('Admin','Cashier','Backer') NOT NULL DEFAULT 'Cashier',
  `is_active` tinyint(1) DEFAULT NULL,
  `password_hash` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Дамп данных таблицы `users`
--

INSERT INTO `users` (`id`, `login`, `full_name`, `email`, `role`, `is_active`, `password_hash`) VALUES
(1, 'sam', 'Sammov Sam', 'sam@mail.ru', 'Admin', 1, 'scrypt:32768:8:1$rWGVKklEaxieYdTO$ec578dfbfe568c4f581da268b056eddf4b057f40d56af3b034f9efecab244b6525bb7bab2cda929200241b7d49996bea2538b9b22b352365132724e730111507'),
(6, 'sammuel', 'sammuel', 'sammuel@mail.ru', 'Cashier', 1, 'scrypt:32768:8:1$XxP7GMJZARF32F49$34965c4e6501451c8e5c5eabfd1eee04f24cde1016e31498ea68902f68b46803bdf2b0ef354c48be96ed52e58dca99423164838e1d7a1cb5b2c11336260475a9'),
(7, 'tipovv', 'Tipov Tipti', 'tip@mail.ru', 'Admin', 1, 'scrypt:32768:8:1$AwztFRHXaIw6oG7I$b89f76c978244b27760c3ee8a4e014d2696825171851678b6eb7e8d48f0a8750e3467bff3c56f01ed8415de98af40756a27c1c8abe9f28f0e7c03033faf89c3a');

--
-- Индексы сохранённых таблиц
--

--
-- Индексы таблицы `admin_setting`
--
ALTER TABLE `admin_setting`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `skey` (`skey`);

--
-- Индексы таблицы `auth_log`
--
ALTER TABLE `auth_log`
  ADD PRIMARY KEY (`id`);

--
-- Индексы таблицы `backup_log`
--
ALTER TABLE `backup_log`
  ADD PRIMARY KEY (`id`),
  ADD KEY `ix_backup_log_user_id` (`user_id`);

--
-- Индексы таблицы `integration`
--
ALTER TABLE `integration`
  ADD PRIMARY KEY (`id`);

--
-- Индексы таблицы `permissions`
--
ALTER TABLE `permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `code` (`code`);

--
-- Индексы таблицы `products`
--
ALTER TABLE `products`
  ADD PRIMARY KEY (`id`);

--
-- Индексы таблицы `roles`
--
ALTER TABLE `roles`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Индексы таблицы `role_permissions`
--
ALTER TABLE `role_permissions`
  ADD PRIMARY KEY (`role_id`,`permission_id`),
  ADD KEY `permission_id` (`permission_id`);

--
-- Индексы таблицы `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `login` (`login`);

--
-- AUTO_INCREMENT для сохранённых таблиц
--

--
-- AUTO_INCREMENT для таблицы `admin_setting`
--
ALTER TABLE `admin_setting`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT для таблицы `auth_log`
--
ALTER TABLE `auth_log`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=20;

--
-- AUTO_INCREMENT для таблицы `backup_log`
--
ALTER TABLE `backup_log`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT для таблицы `integration`
--
ALTER TABLE `integration`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT для таблицы `permissions`
--
ALTER TABLE `permissions`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT для таблицы `products`
--
ALTER TABLE `products`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT для таблицы `roles`
--
ALTER TABLE `roles`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT для таблицы `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
