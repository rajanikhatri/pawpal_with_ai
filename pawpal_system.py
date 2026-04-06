"""Core class skeletons for the PawPal+ project.

This module defines the basic OOP structure for a beginner-friendly
pet care management system. The classes are intentionally lightweight,
and most methods are left as stubs for later implementation.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime, time, timedelta
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
        start_datetime = datetime.combine(self.date, self.start_time)
        end_datetime = start_datetime + timedelta(minutes=self.duration_minutes)
        return end_datetime.time()

    def occurs_on(self, check_date: date) -> bool:
        """Return whether the task occurs on the given date."""
        repeat_type = self.repeat.strip().lower()

        if repeat_type not in {"none", "daily", "weekly"}:
            repeat_type = "none"

        if repeat_type == "none":
            return self.date == check_date

        if repeat_type == "daily":
            return check_date >= self.date

        if repeat_type == "weekly":
            days_apart = (check_date - self.date).days
            return days_apart >= 0 and days_apart % 7 == 0

        return False

    def conflicts_with(self, other_task: "Task") -> bool:
        """Return whether this task overlaps with another task."""
        self_repeat = self.repeat.strip().lower()
        other_repeat = other_task.repeat.strip().lower()

        if self_repeat not in {"none", "daily", "weekly"}:
            self_repeat = "none"

        if other_repeat not in {"none", "daily", "weekly"}:
            other_repeat = "none"

        self_start = datetime.combine(date.min, self.start_time)
        self_end = self_start + timedelta(minutes=self.duration_minutes)

        other_start = datetime.combine(date.min, other_task.start_time)
        other_end = other_start + timedelta(minutes=other_task.duration_minutes)

        times_overlap = self_start < other_end and other_start < self_end

        if not times_overlap:
            return False

        if self_repeat == "none" and other_repeat == "none":
            return self.date == other_task.date

        if self_repeat == "none":
            return other_task.occurs_on(self.date)

        if other_repeat == "none":
            return self.occurs_on(other_task.date)

        if self_repeat == "daily" or other_repeat == "daily":
            return True

        return self.date.weekday() == other_task.date.weekday()

    def mark_complete(self) -> None:
        """Mark the task as completed."""
        self.completed = True


@dataclass
class Pet:
    """Represents a pet and the tasks assigned to it."""

    name: str
    species: str
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a task to this pet."""
        self.tasks.append(task)

    def remove_task(self, task_title: str) -> None:
        """Remove a task by its title."""
        for task in self.tasks:
            if task.title == task_title:
                self.tasks.remove(task)
                break

    def get_tasks(self) -> list[Task]:
        """Return the list of tasks for this pet."""
        return self.tasks


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
