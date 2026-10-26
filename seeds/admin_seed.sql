-- Создание пользователя-админа для входа в админ-панель.
-- Вариант A (рекомендуется): хешированный пароль через Werkzeug (pbkdf2)
-- Замените ХЕШ_ЗДЕСЬ на результат generate_password_hash('Admin123!')

-- UPDATE users SET password_hash='ХЕШ_ЗДЕСЬ', role_id=1, is_active=1 WHERE login='admin';

-- Вариант B (учебный, небезопасно): простой текстовый пароль.
-- Работает из-за verify_password() в routes.py, не используйте в продакшене.

-- UPDATE users SET password_hash='Admin123!', role_id=1, is_active=1 WHERE login='admin';

-- Если пользователя admin нет — создадим.
-- Для MySQL 8+ обратите внимание на возможные ограничения NOT NULL/UNIQUE и нужные поля.

INSERT INTO users (login, full_name, email, role_id, is_active, password_hash)
VALUES ('admin', 'Администратор', 'admin@example.com', 1, 1, 'Admin123!')
ON DUPLICATE KEY UPDATE
  role_id=VALUES(role_id),
  is_active=VALUES(is_active),
  password_hash=VALUES(password_hash);
