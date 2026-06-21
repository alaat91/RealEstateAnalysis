from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.repositories import property_goal_repository
from app.schemas.property_goal import (
    PropertyGoalCreate,
    PropertyGoalRead,
    PropertyGoalUpdate,
)

router = APIRouter(prefix="/property-goals", tags=["property goal"])


@router.post("", response_model=PropertyGoalRead, status_code=status.HTTP_201_CREATED)
def create_property_goal(payload: PropertyGoalCreate, db: Session = Depends(get_db)):
    return property_goal_repository.create_property_goal(db, payload)


@router.get("", response_model=list[PropertyGoalRead])
def list_property_goals(city: str | None = None, limit: int = Query(default=50, ge=1, le=100), offset: int = Query(default=0, ge=0), db: Session = Depends(get_db)):
    return property_goal_repository.list_property_goals(db=db, city=city, limit=limit, offset=offset)


@router.get("/{goal_id}", response_model=PropertyGoalRead)
def get_property_goal(goal_id: UUID, db: Session = Depends(get_db)):
    goal = property_goal_repository.get_property_goal(db, goal_id)

    if goal is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Property goal not found",
        )

    return goal


@router.patch("/{goal_id}", response_model=PropertyGoalRead)
def update_property_goal(goal_id: UUID, payload: PropertyGoalUpdate, db: Session = Depends(get_db),):
    goal = property_goal_repository.get_property_goal(db, goal_id)

    if goal is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Property goal not found",
        )
    return property_goal_repository.update_property_goal(db, goal, payload)


@router.delete("/{goal_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_property_goal(goal_id: UUID, db: Session = Depends(get_db)):
    goal = property_goal_repository.get_property_goal(db, goal_id)

    if goal is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Property goal not found",
        )

    property_goal_repository.delete_property_goal(db, goal)
