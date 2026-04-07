from datetime import date, time
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from pawpal_system import Owner, Pet, Scheduler, Task


def test_mark_complete_sets_task_to_completed() -> None:
    task = Task(
        title="Morning Walk",
        category="Exercise",
        date=date(2026, 4, 6),
        start_time=time(9, 0),
        duration_minutes=30,
    )

    task.mark_complete()

    assert task.completed is True


def test_recurring_task_completion_is_tracked_per_date() -> None:
    task = Task(
        title="Daily Medication",
        category="Medicine",
        date=date(2026, 4, 7),
        start_time=time(8, 0),
        duration_minutes=10,
        repeat="daily",
    )

    task.mark_complete(date(2026, 4, 7))

    assert task.is_completed_on(date(2026, 4, 7)) is True
    assert task.is_completed_on(date(2026, 4, 8)) is False


def test_add_task_increases_pet_task_count() -> None:
    pet = Pet(name="Mochi", species="Dog")
    task = Task(
        title="Breakfast",
        category="Feeding",
        date=date(2026, 4, 6),
        start_time=time(8, 0),
        duration_minutes=15,
    )

    pet.add_task(task)

    assert len(pet.get_tasks()) == 1


def test_sort_by_time_returns_tasks_in_chronological_order() -> None:
    owner = Owner(name="Jordan")
    scheduler = Scheduler(owner=owner)

    early_task = Task(
        title="Breakfast",
        category="Feeding",
        date=date(2026, 4, 6),
        start_time=time(8, 0),
        duration_minutes=15,
    )
    late_task = Task(
        title="Walk",
        category="Exercise",
        date=date(2026, 4, 6),
        start_time=time(10, 0),
        duration_minutes=30,
    )
    middle_task = Task(
        title="Brush Fur",
        category="Grooming",
        date=date(2026, 4, 6),
        start_time=time(9, 0),
        duration_minutes=10,
    )

    sorted_tasks = scheduler.sort_by_time([late_task, middle_task, early_task])

    assert sorted_tasks == [early_task, middle_task, late_task]


def test_find_conflicts_detects_overlapping_tasks() -> None:
    owner = Owner(name="Jordan")
    pet = Pet(name="Mochi", species="Dog")
    owner.add_pet(pet)
    scheduler = Scheduler(owner=owner)

    first_task = Task(
        title="Morning Walk",
        category="Exercise",
        date=date(2026, 4, 6),
        start_time=time(9, 0),
        duration_minutes=30,
    )
    second_task = Task(
        title="Breakfast",
        category="Feeding",
        date=date(2026, 4, 6),
        start_time=time(9, 15),
        duration_minutes=20,
    )

    pet.add_task(first_task)
    pet.add_task(second_task)

    conflicts = scheduler.find_conflicts([first_task, second_task])

    assert len(conflicts) == 1
    assert conflicts[0] == (first_task, second_task)
