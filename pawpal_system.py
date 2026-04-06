"""Core class skeletons for the PawPal+ project.

This module defines the basic OOP structure for a beginner-friendly
pet care management system. The classes are intentionally lightweight,
and most methods are left as stubs for later implementation.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, time
from typing import Optional


@dataclass
class Task:
    """Represents a single pet care task."""

    title: str
    category: str
    date: date
    start_time: time
    duration_minutes: int
    repeat: str = "none"
    completed: bool = False

    def get_end_time(self) -> time:
        """Return the task's calculated end time."""
        pass

    def occurs_on(self, check_date: date) -> bool:
        """Return whether the task occurs on the given date."""
        pass

    def conflicts_with(self, other_task: "Task") -> bool:
        """Return whether this task overlaps with another task."""
        pass

    def mark_complete(self) -> None:
        """Mark the task as completed."""
        pass


@dataclass
class Pet:
    """Represents a pet and the tasks assigned to it."""

    name: str
    species: str
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a task to this pet."""
        pass

    def remove_task(self, task_title: str) -> None:
        """Remove a task by its title."""
        pass

    def get_tasks(self) -> list[Task]:
        """Return the list of tasks for this pet."""
        pass


@dataclass
class Owner:
    """Represents the pet owner and their pets."""

    name: str
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner."""
        pass

    def remove_pet(self, pet_name: str) -> None:
        """Remove a pet by name."""
        pass

    def get_pets(self) -> list[Pet]:
        """Return the list of pets owned."""
        pass


@dataclass
class Scheduler:
    """Handles task lookup, sorting, filtering, and conflict checks."""

    owner: Owner

    def get_todays_tasks(self, check_date: date) -> list[Task]:
        """Return all tasks that occur on the given date."""
        pass

    def sort_by_time(self, tasks: list[Task]) -> list[Task]:
        """Return tasks sorted by start time."""
        pass

    def filter_tasks(
        self,
        tasks: list[Task],
        category: Optional[str] = None,
        pet_name: Optional[str] = None,
    ) -> list[Task]:
        """Return tasks filtered by category and/or pet name."""
        pass

    def find_conflicts(self, tasks: list[Task]) -> list[tuple[Task, Task]]:
        """Return pairs of tasks that conflict with each other."""
        pass
