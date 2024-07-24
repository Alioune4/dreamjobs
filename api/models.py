from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from api.connection import db
from sqlalchemy import Enum
import enum


class RoleEnum(enum.Enum):
    ADMIN = 'Admin'
    RECRUITER = 'Recruiter'
    JOB_SEEKER = 'Job seeker'

    def __str__(self):
        return self.value


class CategoryEnum(enum.Enum):
    ENGINEERING = "Engineering"
    MARKETING = "Marketing"
    SALES = "Sales"
    HR = "HR"
    FINANCE = "Finance"
    ADMINISTRATION = "Administration"
    DESIGN = "Design"
    OTHER = "Other"

    def __str__(self):
        return self.value


class EmploymentTypeEnum(enum.Enum):
    FULL_TIME = "Full-time"
    PART_TIME = "Part-time"
    INTERN = "Intern"

    def __str__(self):
        return self.value

class User(db.Model):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)

    role: Mapped[RoleEnum] = mapped_column(Enum(RoleEnum), nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'

    def to_dict(self):
        return row_to_dict(self)


class JobPost(db.Model):
    __tablename__ = 'job_posts'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    salary: Mapped[int] = mapped_column(nullable=True)
    location: Mapped[str] = mapped_column(nullable=True)

    employment_type: Mapped[EmploymentTypeEnum] = mapped_column(Enum(EmploymentTypeEnum), nullable=False)

    category: Mapped[CategoryEnum] = mapped_column(Enum(CategoryEnum), nullable=False)

    updated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Job {self.title}'

    def to_dict(self):
        return row_to_dict(self)


def row_to_dict(row):
    output_dict = {}
    for column in row.__table__.columns:
        if isinstance(getattr(row, column.name), enum.Enum):
            output_dict[column.name] = str(getattr(row, column.name))
        else:
            output_dict[column.name] = getattr(row, column.name)

    return output_dict