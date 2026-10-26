from flask import render_template, request, redirect, url_for, flash, current_app
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from . import admin_bp, db
from .models import RoleEnum, User, Integration, BackupLog, AdminSetting, AuthLog, BackupLog, BackupStatus, Product, Role, Permission
from .forms import LoginForm, IntegrationForm, RegistrationForm, ProductForm, AssignPermissionForm, FilterLogs
from werkzeug.security import check_password_hash, generate_password_hash
import json, datetime
from flask_wtf.csrf import validate_csrf, generate_csrf as _unused_generate_csrf
from datetime import timedelta


login_manager = LoginManager()

def verify_password(stored: str, provided: str) -> bool:
    
    if not stored:
        return False
    is_werkzeug_hash = stored.startswith("pbkdf2:") or stored.count("$") >= 2
    if is_werkzeug_hash:
        try:
            return check_password_hash(stored, provided)
        except Exception:
            return False
    return stored == provided


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def admin_required(func):
    from functools import wraps
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for("admin.login"))
        # простая проверка роли: роль 1 считаем админгой
        if current_user.role != RoleEnum.Admin:            
            flash("Недостаточно прав", "error")
            return redirect(url_for("admin.dashboard"))
        return func(*args, **kwargs)
    return wrapper


def log_failed_attempt(attempted_login):

    log = AuthLog(
        attempted_login=attempted_login,
        ip=request.remote_addr,
        user_agent=request.headers.get("User-Agent"),
        is_success=False,
        reason="no_such_user"
    )
    db.session.add(log)
    db.session.commit()  


@admin_bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    
    # Это нужно для отображения формы при GET-запросе.
    if not form.validate_on_submit():
        return render_template("admin/login.html", form=form)

    # На этом этапе мы точно знаем, что данные валидны.
    user = User.query.filter_by(login=form.login.data).first()

    # Создаём объект лога ДО проверки результата.
    log_entry = AuthLog(
        attempted_login=form.login.data,
        ip=request.remote_addr,
        user_agent=request.headers.get("User-Agent"),
        created_at=datetime.datetime.now(),  
        is_success=False,                
        reason=None                      
    )

    # Теперь проверяем результат.
    if user and verify_password(user.password_hash, form.password.data):
        # Вход успешен.
        log_entry.is_success = True
        log_entry.reason = "success"
        
        login_user(user)
        
        # Сообщение пользователю.
        flash(f"Добро пожаловать, {user.full_name or user.login}!", "success")
        
        # Сохраняем запись об УСПЕШНОМ входе.
        db.session.add(log_entry)
        try:
            db.session.commit()
        except Exception as e:
            # Мы можем проигнорировать эту ошибку, так как главное — это вход пользователя.
            print(f"WARNING: Failed to save successful auth log: {e}")
        
        # Перенаправляем на панель администратора.
        return redirect(url_for("admin.dashboard"))
    else:
        # Вход НЕ успешен.
        log_entry.reason = "bad_credentials"
        
        # Сохраняем запись об НЕУДАЧНОМ входе.
        db.session.add(log_entry)
        try:
            db.session.commit()
        except Exception as e:
            # Логируем ошибку, чтобы админ мог разобраться.
            print(f"ERROR: Failed to save failed auth log: {e}")
            # Не делаем rollback, так как он необязателен для продолжения.
        
        # Сообщаем пользователю.
        flash("Ошибка авторизации.", "error")

    # Возвращаемся к форме.
    return render_template("admin/login.html", form=form)


@admin_bp.route("/logout", methods=["GET"])
@login_required
def logout():
    logout_user()
    flash("Вы вышли из системы", "success")
    return redirect(url_for("admin.login"))

@admin_bp.route("/", methods=["GET"])
@login_required
def dashboard():           
    return render_template("admin/index.html")


@admin_bp.route("/integration/add", methods=["POST"])
@admin_bp.route("/integration/edit/<int:int_id>", methods=["POST"])
@login_required
@admin_required
def manage_integration(int_id=None):
    
    if request.method != "POST":
        return redirect(url_for('admin.dashboard'))

    # 1. Собираем данные
    form_type = request.form.get("type")
    form_name = request.form.get("name")
    form_config = request.form.get("config")
    is_active = 'is_active' in request.form

    # 2. Валидация JSON 
    try:
        json.loads(form_config)
    except json.JSONDecodeError:
        flash("Ошибка: Поле 'Конфигурация' должно быть валидным JSON.", "error")
        return redirect(request.referrer) # Возвращаем на страницу, где была форма

    # 3. Логика сохранения (UPSERT)
    if int_id:
        # --- РЕЖИМ РЕДАКТИРОВАНИЯ ---
        integration = Integration.query.get_or_404(int_id)
        integration.type = form_type
        integration.name = form_name
        integration.config = form_config
        integration.is_active = is_active
        flash("Интеграция успешно обновлена!", "success")
    else:
        # --- РЕЖИМ ДОБАВЛЕНИЯ ---
        new_int = Integration(
            type=form_type,
            name=form_name,
            config=form_config,
            is_active=is_active
        )
        db.session.add(new_int)
        flash("Интеграция успешно добавлена!", "success")

    # 4. Сохранение и редирект
    db.session.commit()
    return redirect(url_for('admin.integrity_page'))



@admin_bp.route("/user/<int:id>/edit", methods=["GET", "POST"])
@login_required 
@admin_required
def edit_user(id):
    user = User.query.get_or_404(id)
    
    if request.method == 'POST':
        # === ОБРАБОТКА ДАННЫХ ===        
        # Логин обязателен
        new_login = request.form.get("login")
        if not new_login or len(new_login) < 2:
            flash("Ошибка: логин должен быть минимум 6 символов.", "error")
            return redirect(url_for('admin.edit_user', id=user.id))

        # Роль должна быть корректна
        role_id_from_form = request.form.get('role_id')
        ROLE_MAP = {'1': RoleEnum.Admin, '2': RoleEnum.Cashier, '3': RoleEnum.Backer}
        if role_id_from_form not in ROLE_MAP:
            flash("Ошибка: недопустимая роль.", "error")
            return redirect(url_for('admin.edit_user', id=user.id))

        # Сохранение
        user.login = new_login
        user.full_name = request.form.get("full_name") or ""
        user.email = request.form.get("email") or ""  # Почта может быть пустой?
        user.is_active = bool(request.form.get("is_active"))
        user.role = ROLE_MAP[role_id_from_form]
        user.password_hash = generate_password_hash(request.form.get("password")) or ""

        try:
            db.session.commit()
            flash(f"Пользователь {user.login} успешно обновлён.", "success")
            return redirect(url_for('admin.edit_user', id=user.id))
        except Exception as e:
            db.session.rollback()
            flash(f"Ошибка сохранения: {str(e)}", "danger")
            return redirect(url_for('admin.edit_user', id=user.id))
    
    else:
        return render_template("admin/edit_user.html", user=user)


@admin_bp.route("/security-page")
@login_required
@admin_required
def security_page():
    return render_template("admin/security.html")

@admin_bp.route("/integrity-page")
@login_required
@admin_required
def integrity_page():
    integrations = Integration.query.order_by(Integration.id.desc()).limit(10).all()
    return render_template("admin/integrity.htm", integrations=integrations)

@admin_bp.route("/backup-page")
@login_required
@admin_required
def backup_page():
    backups = BackupLog.query.order_by(BackupLog.started_at.desc()).limit(10).all()
    return render_template("admin/backup-page.html", backups=backups)

@admin_bp.route("/users&role_page")
@login_required
@admin_required
def users_role_page():
    users = User.query.order_by(User.id.asc()).limit(50).all()
    return render_template("admin/users&role-page.html", users=users)

@admin_bp.route("/logs-page")
@login_required
@admin_required
def logs_page():
    form = FilterLogs(request.args)
    authlogs = AuthLog.query.order_by(AuthLog.created_at.desc())
    query = AuthLog.query.order_by(AuthLog.created_at.desc())

    if form.login.data: 
        query = query.filter(AuthLog.attempted_login.ilike(f"%{form.login.data}%"))

    from_date = form.date_from.data 
    to_date = form.date_to.data or (from_date + timedelta(days=31)) if from_date else None 
    if from_date and to_date: query = query.filter(AuthLog.created_at.between(from_date, to_date)) 
    
    authlogs = query.limit(100).all()
    return render_template("admin/logs-page.html", authlogs=authlogs, form=form)

@admin_bp.route("/security", methods=["POST"])
@login_required
@admin_required
def security_save():
    # 1. Собираем данные из формы
    min_length = request.form.get('min_length')
    require_digits = 'require_digits' in request.form
    require_upper = 'require_upper' in request.form
    lock_threshold = request.form.get('lock_threshold')

    # 2. Формируем словарь с политикой
    policy_data = {
        "min_length": int(min_length),
        "require_digits": require_digits,
        "require_upper": require_upper,
        "lock_threshold": int(lock_threshold)
    }

    # 3. Ищем существующую запись в БД
    setting = AdminSetting.query.filter_by(skey='security.password_policy').first()

    if setting:
        # Если запись есть — обновляем значение
        setting.svalue = json.dumps(policy_data)
    else:
        # Если записи нет — создаем новую
        setting = AdminSetting(
            skey='security.password_policy',
            svalue=json.dumps(policy_data)
        )
        db.session.add(setting)

    # 4. Сохраняем в БД (ВАЖНО: ВНЕ блока if/else!)
    db.session.commit() 
    
    flash('Политика безопасности успешно обновлена!', 'success')
    
    # 5. Возвращаем пользователя на главную страницу админки, 
    # где находится форма. Редирект убирает проблему повторной отправки формы.
    return redirect(url_for('admin.security_page'))       

# --- СТРАНИЦА НАСТРОЕК И ЖУРНАЛА ---
@admin_bp.route("/backup", methods=["GET"])
@login_required
@admin_required
def backup_settings():
    # 1. Получаем настройки из таблицы admin_setting
    setting = AdminSetting.query.filter_by(skey='backup.config').first()
    config = {}
    if setting and setting.svalue:
        try:
            config = json.loads(setting.svalue)
        except Exception:
            config = {}
            
    # 2. Получаем журнал (последние 50 записей)
    # logs = BackupLog.query.order_by(BackupLog.started_at.desc()).limit(50).all()
    
    return redirect(url_for('admin.backup_page'))


# --- ОБРАБОТЧИК СОХРАНЕНИЯ НАСТРОЕК ---
@admin_bp.route("/backup/settings", methods=["POST"])
@login_required
@admin_required
def save_backup_settings():
    enabled = 'backup_enabled' in request.form
    retention = request.form.get('retention_days', 14)
    
    # Валидация числа
    try:
        retention = int(retention)
        if retention < 1 or retention > 365:
            raise ValueError
    except ValueError:
        flash("Ошибка: количество дней хранения должно быть от 1 до 365.", "error")
        return redirect(url_for('admin.backup_settings'))

    # Формируем JSON
    config_data = {
        "enabled": enabled,
        "retention_days": retention
    }

    # Сохраняем в БД (UPSERT)
    setting = AdminSetting.query.filter_by(skey='backup.config').first()
    if setting:
        setting.svalue = json.dumps(config_data)
    else:
        setting = AdminSetting(skey='backup.config', svalue=json.dumps(config_data))
        db.session.add(setting)
        
    db.session.commit()
    flash("Настройки резервного копирования сохранены.", "success")
    return redirect(url_for('admin.backup_settings'))


@admin_bp.route("/backup/run", methods=["POST"])
@login_required
@admin_required
def run_backup():
    # 1. Создаем запись в журнале
    log_entry = BackupLog(
        user_id=current_user.id,
        status=BackupStatus.running
    )
    db.session.add(log_entry)
    db.session.commit() # Важно зафиксировать ID сразу
    
   
    try:
        # --- НАЧАЛО ИМИТАЦИИ ---
        import time
        time.sleep(2) # Имитируем долгую работу
        file_name = f"backup-{datetime.now().strftime('%Y-%m-%d')}.sql.gz"
        file_path = f"/backups/{file_name}"
        
        # Здесь ваша реальная логика архивации БД        
        # --- КОНЕЦ ИМИТАЦИИ ---
        
        log_entry.status = BackupStatus.success
        log_entry.file_path = file_path
        log_entry.message = "Резервная копия создана успешно."
        
    except Exception as e:
        log_entry.status = BackupStatus.failed
        log_entry.message = str(e)
        
    finally:
        log_entry.finished_at = datetime.utcnow()
        db.session.commit()
        
    flash(f"Бэкап завершен. Статус: {log_entry.status}", "info")
    return redirect(url_for('admin.backup_settings'))


@admin_bp.route('/register', methods=['GET', 'POST'])
@login_required
@admin_required
def register():
    form = RegistrationForm()

    if form.validate_on_submit():  # Проверка валидности полей
        existing_user_login = User.query.filter_by(login=form.login.data).first()
        existing_user_email = User.query.filter_by(email=form.email.data).first()
        
        if existing_user_login or existing_user_email:
            error_message = (
                f"Пользователь с таким {'логином' if existing_user_login else 'адресом электронной почты'} уже существует."
            )
            flash(error_message, category="danger")
            return render_template('admin/register.html', title='Регистрация', form=form)

        # Хешируем пароль
        hashed_password = generate_password_hash(form.password.data)

        new_user = User(
            login=form.login.data,
            full_name=form.full_name.data,
            email=form.email.data,
            role=RoleEnum.Cashier,  # Роль задаётся жёстко
            is_active=form.is_active.data,
            password_hash=hashed_password
        )

        try:
            db.session.add(new_user)
            db.session.commit()  # Сохраняем в БД
            
            flash(f"Аккаунт {new_user.login} успешно создан!", category="success")
            return redirect(url_for('auth.login'))  # Перенаправляем на страницу входа
        except Exception as e:
            db.session.rollback()
            flash("Ошибка при создании аккаунта.", category="danger")

    return render_template('admin/register.html', title='Регистрация', form=form)


@admin_bp.route('/products')
@login_required
def all_products():  
    all_products = Product.query.all()     
    return render_template('products-page.html', products=all_products)

@admin_bp.route('/product/new', methods=['GET', 'POST'])
@login_required
def new_product():
    
    form = ProductForm()

    if form.validate_on_submit():
        # Создаём новый объект из данных формы
        new_product = Product(name=form.name.data,
                             category=form.category.data,
                             unit_price=form.unit_price.data)
        
        db.session.add(new_product)
        db.session.commit()
        flash(f'Изделие "{new_product.name}" создано.', 'success')
        return redirect(url_for('.all_products'))  # Перенаправляем на список

    return render_template('edit_product.html', title='Добавление изделия', form=form)

@admin_bp.route('/product/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_product(id):
    """
    Редактирование существующего изделия.
    """
    product = Product.query.get_or_404(id)

    # Передаём экземпляр объекта в форму для заполнения полей
    form = ProductForm(obj=product)

    if form.validate_on_submit():
        # Обновляем поля объекта данными из формы
        form.populate_obj(product)
        db.session.commit()
        flash(f'Изменения для изделия "{product.name}" сохранены.', 'success')
        return redirect(url_for('.all_products'))

    return render_template('edit_product.html', title=f'Редактирование: {product.name}', form=form)

@admin_bp.route('/product/<int:id>/delete', methods=['POST'])
@login_required
def delete_product(id):
    
    product = Product.query.get_or_404(id)
    
    # Каскадное удаление сработает автоматически благодаря настройкам модели
    db.session.delete(product)
    db.session.commit()
    flash(f'Изделие "{product.name}" было удалено.', 'info')
    return redirect(url_for('.all_products'))


@admin_bp.route('/roles/assign', methods=['GET', 'POST'])
@login_required
@admin_required
def assign_permission():    
    all_roles = Role.query.all()
    form = AssignPermissionForm()
    # Заполняем выпадающие списки перед рендером или проверкой валидности.
    form.populate_choices()
    if form.validate_on_submit():
        role = Role.query.get(form.r_role.data)
        permission = Permission.query.get(form.r_perm.data)
        
        # Проверка на дублирование не нужна, т.к. это отношение многие-ко-многим.
        role.permissions.append(permission)
        db.session.commit()
        flash(f'Право "{permission.code}" успешно назначено роли "{role.name}".', category='success')
        return redirect(url_for('.assign_permission'))

    return render_template('roles.html', form=form, roles=all_roles)


@admin_bp.route("/debug-urls") 
def debug_urls(): 
    return str(current_app.url_map)
