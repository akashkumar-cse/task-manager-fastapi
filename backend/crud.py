from sqlalchemy.orm import Session
from sqlalchemy import func
import models
import schemas
from auth import hash_password


# ---------- User ----------
def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    db_user = models.User(
        name=user.name,
        email=user.email,
        hashed_password=hash_password(user.password),
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_by_email(db: Session, email: str) -> models.User | None:
    return db.query(models.User).filter(models.User.email == email).first()


# ---------- Project ----------
def get_projects(db: Session, user_id: int):
    return db.query(models.Project).filter(models.Project.user_id == user_id).all()


def get_project(db: Session, project_id: int, user_id: int) -> models.Project | None:
    return (
        db.query(models.Project)
        .filter(models.Project.id == project_id, models.Project.user_id == user_id)
        .first()
    )


def create_project(db: Session, project: schemas.ProjectCreate, user_id: int) -> models.Project:
    db_project = models.Project(name=project.name, description=project.description, user_id=user_id)
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project


def update_project(db: Session, db_project: models.Project, updates: schemas.ProjectUpdate) -> models.Project:
    for field, value in updates.model_dump(exclude_unset=True).items():
        setattr(db_project, field, value)
    db.commit()
    db.refresh(db_project)
    return db_project


def delete_project(db: Session, db_project: models.Project) -> None:
    db.delete(db_project)
    db.commit()


# ---------- Task ----------
def get_tasks_for_project(db: Session, project_id: int):
    return db.query(models.Task).filter(models.Task.project_id == project_id).all()


def get_task(db: Session, task_id: int, user_id: int) -> models.Task | None:
    return (
        db.query(models.Task)
        .join(models.Project)
        .filter(models.Task.id == task_id, models.Project.user_id == user_id)
        .first()
    )


def create_task(db: Session, task: schemas.TaskCreate, project_id: int) -> models.Task:
    db_task = models.Task(**task.model_dump(), project_id=project_id)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def update_task(db: Session, db_task: models.Task, updates: schemas.TaskUpdate) -> models.Task:
    for field, value in updates.model_dump(exclude_unset=True).items():
        setattr(db_task, field, value)
    db.commit()
    db.refresh(db_task)
    return db_task


def delete_task(db: Session, db_task: models.Task) -> None:
    db.delete(db_task)
    db.commit()


def filter_tasks(db: Session, user_id: int, status: str | None, priority: str | None):
    query = (
        db.query(models.Task)
        .join(models.Project)
        .filter(models.Project.user_id == user_id)
    )
    if status:
        query = query.filter(models.Task.status == status)
    if priority:
        query = query.filter(models.Task.priority == priority)
    return query.all()


# ---------- Dashboard ----------
def get_dashboard_stats(db: Session, user_id: int) -> dict:
    total_projects = db.query(models.Project).filter(models.Project.user_id == user_id).count()

    base = db.query(models.Task).join(models.Project).filter(models.Project.user_id == user_id)
    total_tasks = base.count()
    todo = base.filter(models.Task.status == models.StatusEnum.todo).count()
    in_progress = base.filter(models.Task.status == models.StatusEnum.in_progress).count()
    done = base.filter(models.Task.status == models.StatusEnum.done).count()

    return {
        "total_projects": total_projects,
        "total_tasks": total_tasks,
        "todo": todo,
        "in_progress": in_progress,
        "done": done,
    }
