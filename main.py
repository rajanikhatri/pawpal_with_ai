"""Simple CLI demo for the PawPal+ core classes."""

from datetime import date, time, timedelta

from pawpal_system import Owner, Pet, Scheduler, Task


def find_pet_name(owner: Owner, task: Task) -> str:
    """Return the name of the pet that owns the given task."""
    for pet in owner.get_pets():
        if task in pet.get_tasks():
            return pet.name
    return "Unknown"


def print_tasks(owner: Owner, tasks: list[Task]) -> None:
    """Print tasks in a readable format."""
    if not tasks:
        print("No tasks found.")
        return

    for task in tasks:
        pet_name = find_pet_name(owner, task)
        start = task.start_time.strftime("%I:%M %p")
        end = task.get_end_time().strftime("%I:%M %p")
        print(
            f"- {start} - {end} | {task.title} ({task.category}) "
            f"for {pet_name} | repeat: {task.repeat}"
        )


def main() -> None:
    """Create sample data and show the schedule in the terminal."""
    today = date.today()

    owner = Owner("Jordan")

    mochi = Pet("Mochi", "Dog")
    luna = Pet("Luna", "Cat")

    owner.add_pet(mochi)
    owner.add_pet(luna)

    task_1 = Task(
        title="Morning Walk",
        category="Exercise",
        date=today,
        start_time=time(9, 0),
        duration_minutes=30,
        repeat="none",
    )

    task_2 = Task(
        title="Breakfast",
        category="Feeding",
        date=today - timedelta(days=2),
        start_time=time(9, 15),
        duration_minutes=20,
        repeat="daily",
    )

    task_3 = Task(
        title="Brush Fur",
        category="Grooming",
        date=today,
        start_time=time(11, 0),
        duration_minutes=15,
        repeat="none",
    )

    task_4 = Task(
        title="Medication",
        category="Health",
        date=today,
        start_time=time(11, 10),
        duration_minutes=10,
        repeat="none",
    )

    mochi.add_task(task_1)
    mochi.add_task(task_3)
    luna.add_task(task_2)
    luna.add_task(task_4)

    scheduler = Scheduler(owner)

    todays_tasks = scheduler.get_todays_tasks(today)
    sorted_tasks = scheduler.sort_by_time(todays_tasks)
    conflicts = scheduler.find_conflicts(sorted_tasks)
    luna_tasks = scheduler.filter_tasks(sorted_tasks, pet_name="Luna")

    print("PawPal+ CLI Demo")
    print("=" * 40)
    print(f"Owner: {owner.name}")
    print(f"Date: {today}")
    print()

    print("Today's Schedule")
    print("-" * 40)
    print_tasks(owner, sorted_tasks)
    print()

    print("Conflict Warnings")
    print("-" * 40)
    if conflicts:
        for first_task, second_task in conflicts:
            first_pet = find_pet_name(owner, first_task)
            second_pet = find_pet_name(owner, second_task)
            print(
                f"- Conflict: {first_task.title} for {first_pet} overlaps with "
                f"{second_task.title} for {second_pet}"
            )
    else:
        print("No conflicts found.")
    print()

    print("Filtered Example: Tasks for Luna")
    print("-" * 40)
    print_tasks(owner, luna_tasks)


if __name__ == "__main__":
    main()
