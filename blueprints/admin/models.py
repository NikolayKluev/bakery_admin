from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from enum import Enum as PyEnum
from sqlalchemy import Enum
import json
from datetime import datetime
import enum


class RoleEnum(PyEnum): 
    Admin = 'Admin' 
    Cashier = 'Cashier' 
    Backer = 'Backer'

class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(50), unique=True, nullable=False)
    full_name = db.Column(db.String(150))
    email = db.Column(db.String(150))
    role = db.Column(Enum(RoleEnum), nullable=False, default=RoleEnum.Cashier)
    is_active = db.Column(db.Boolean, default=True)
    password_hash = db.Column(db.String(255))

    def get_id(self):
        return str(self.id)

class AdminSetting(db.Model):
    __tablename__ = "admin_setting"
    id = db.Column(db.Integer, primary_key=True)
    skey = db.Column(db.String(100), unique=True, nullable=False)
    svalue = db.Column(db.Text)

class Integration(db.Model):
    __tablename__ = "integration"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    type = db.Column(db.String(50))
    config = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, server_default=func.now())


class AuthLog(db.Model):
    __tablename__ = "auth_log"
    id = db.Column(db.Integer, primary_key=True)
    attempted_login = db.Column(db.String(50))
    ip = db.Column(db.String(45))
    user_agent = db.Column(db.String(255))
    is_success = db.Column(db.Boolean)
    reason = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, server_default=func.now())

class BackupStatus(str, enum.Enum):
    pending = 'pending'
    running = 'running'
    success = 'success'
    failed = 'failed'

class BackupLog(db.Model):
    __tablename__ = 'backup_log'

    id = db.Column(db.Integer, primary_key=True)
    
    # Ссылка на пользователя (кто запустил), может быть NULL если сработал cron
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    
    started_at = db.Column(db.DateTime, default=datetime.utcnow)
    finished_at = db.Column(db.DateTime, nullable=True)
    
    status = db.Column(db.Enum(BackupStatus), default=BackupStatus.pending)
    file_path = db.Column(db.String(255), nullable=True) # Путь к файлу бэкапа
    message = db.Column(db.Text, nullable=True) # Сообщение об ошибке или успехе

    def __repr__(self):
        return f"<BackupLog {self.id} | {self.status}>"


class Product(db.Model):
    __tablename__ = 'products'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)          # Название изделия
    category = db.Column(db.String(100))                     # Категория (может быть null)
    unit_price = db.Column(db.Float, default=0.0, nullable=False)  # Цена за единицу
    
    def __repr__(self):
        return f'<Product {self.name}>'


# Таблица связи между ролями и правами (многие ко многим)
role_permissions = db.Table('role_permissions',
    db.Column('role_id', db.Integer, db.ForeignKey('roles.id'), primary_key=True),
    db.Column('permission_id', db.Integer, db.ForeignKey('permissions.id'), primary_key=True)
)

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False) # admin, cashier, user
    
    permissions = db.relationship(
        "Permission", secondary=role_permissions,
        backref="roles"
    )

class Permission(db.Model):
    __tablename__ = 'permissions'
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(50), unique=True, nullable=False) # bakeries.create
    description = db.Column(db.Text, nullable=False) # Создание новой пекарни

def seed_data():
    
    # Назначаем права администраторам.
    admin_role = Role.query.filter_by(name='admin').first()
    all_perms = Permission.query.all()
    admin_role.permissions.extend(all_perms)

    db.session.commit()
