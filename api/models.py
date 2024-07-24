from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from api.connection import db


class Role(db.Model):
    __tablename__ = 'roles'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True, nullable=False)

    def __repr__(self):
        return f'<Role {self.name}>'


class User(db.Model):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)

    role_id: Mapped[int] = mapped_column(db.ForeignKey('roles.id'), nullable=False)
    role = db.relationship('Role', backref='users')

    def __repr__(self):
        return f'<User {self.username}>'


class EmploymentType(db.Model):
    __tablename__ = 'employment_types'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True, nullable=False)

    def __repr__(self):
        return f'<EmploymentType {self.name}>'


class Category(db.Model):
    __tablename__ = 'categories'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True, nullable=False)

    def __repr__(self):
        return f'<Category {self.name}>'


class JobPost(db.Model):
    __tablename__ = 'job_posts'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    salary: Mapped[int] = mapped_column(nullable=False)
    location: Mapped[str] = mapped_column(nullable=False)

    employment_type_id: Mapped[int] = mapped_column(db.ForeignKey('employment_types.id'), nullable=False)
    employment_type = db.relationship('EmploymentType', backref='job_posts')

    posted_by: Mapped[int] = mapped_column(db.ForeignKey('users.id'), nullable=False)
    posted_by_user = db.relationship('User', backref='job_posts')

    category_id: Mapped[int] = mapped_column(db.ForeignKey('categories.id'), nullable=False)
    category = db.relationship('Category', backref='job_posts')

    updated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Job {self.title}'


def row_to_dict(row):
    return {column.name: getattr(row, column.name) for column in row.__table__.columns}
