from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.property_goal import PropertyGoal
from app.schemas.property_goal import PropertyGoalCreate, PropertyGoalUpdate


def create_property_goal(db: Session, payload: PropertyGoalCreate) -> PropertyGoal:
    goal = PropertyGoal(**payload.model_dump())

    db.add(goal)
    db.commit()
    db.refresh(goal)

    return goal


def list_property_goals(db: Session, city: str | None = None, limit: int = 50, offset: int = 0) -> list[PropertyGoal]:
    stmt = select(PropertyGoal)

    if city is not None:
        stmt = stmt.where(PropertyGoal.city == city)

    stmt = stmt.order_by(PropertyGoal.created_at.desc()
                         ).limit(limit).offset(offset)

    return list(db.execute(stmt).scalars().all())


def get_property_goal(db: Session, goal_id: UUID) -> PropertyGoal:
    stmt = select(PropertyGoal).where(PropertyGoal.id == goal_id)
    return db.execute(stmt).scalar_one_or_none()


def update_property_goal(db: Session, goal: PropertyGoal, payload: PropertyGoalUpdate) -> PropertyGoal:
    update_data = payload.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(goal, field, value)

    db.commit()
    db.refresh(goal)

    return goal


def delete_property_goal(db: Session, goal: PropertyGoal) -> None:
    db.delete(goal)
    db.commit()
