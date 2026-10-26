# Bakery Admin — Flask + MySQL стартовый шаблон

## Запуск
```bash
python -m venv .venv && . .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
export DATABASE_URL="mysql+pymysql://user:pass@localhost/bakery_admin?charset=utf8mb4"  # Windows: set
export SECRET_KEY="123"
python app.py
# откройте http://127.0.0.1:5000/admin
```

## Учётные данные
Используйте существующих пользователей из вашей БД `bakery_admin`. Для простоты
в коде допускается сравнение `password_hash == введённый_пароль` или хеширование через Werkzeug.

## Структура
- `app.py` — точка входа
- `config.py` — конфигурация
- `blueprints/admin` — блюпринт, модели, роуты, формы
- `templates/admin` — шаблоны панели
- `static/css/styles.css` — ваши стили

## Пароли и аутентификация (важно)
Для тестирования или первого входа есть два пользователя с правами администратора:

login: sam
passwoed: qazwsx

login: tipovv
password: qazwsx

И пользователь без прав администратора:

login: sammuel
password: qwerasdf
