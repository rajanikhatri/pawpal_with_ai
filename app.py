from datetime import date, time

import streamlit as st

from pawpal_system import Owner, Pet, Scheduler, Task


st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")


def find_pet_by_name(owner: Owner, pet_name: str) -> Pet | None:
    """Return the pet with the matching name."""
    for pet in owner.get_pets():
        if pet.name == pet_name:
            return pet
    return None


def find_pet_name_for_task(owner: Owner, task: Task) -> str:
    """Return the name of the pet that owns the task."""
    for pet in owner.get_pets():
        for pet_task in pet.get_tasks():
            if pet_task is task:
                return pet.name
    return "Unknown"


if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="Jordan")


owner = st.session_state.owner


st.title("🐾 PawPal+")
st.write("Add pets, create tasks, and view today's schedule.")

st.subheader("Owner")
st.write(f"Current owner: **{owner.name}**")

st.subheader("Add a Pet")

with st.form("add_pet_form", clear_on_submit=True):
    pet_name = st.text_input("Pet name")
    species = st.selectbox("Species", ["Dog", "Cat", "Other"])
    add_pet_submitted = st.form_submit_button("Add Pet")

    if add_pet_submitted:
        pet_name = pet_name.strip()

        if pet_name:
            owner.add_pet(Pet(name=pet_name, species=species))
            st.success(f"{pet_name} was added.")
        else:
            st.warning("Please enter a pet name.")


st.subheader("Current Pets")

if owner.get_pets():
    for index, pet in enumerate(owner.get_pets(), start=1):
        st.write(f"{index}. {pet.name} ({pet.species})")
else:
    st.info("No pets added yet.")


st.subheader("Add a Task")

if owner.get_pets():
    pet_names = [pet.name for pet in owner.get_pets()]

    with st.form("add_task_form", clear_on_submit=True):
        selected_pet_name = st.selectbox("Pet", pet_names)
        title = st.text_input("Task title")
        category = st.text_input("Category", value="Feeding")
        task_date = st.date_input("Date", value=date.today())
        start_time = st.time_input("Time", value=time(9, 0))
        duration_minutes = st.number_input(
            "Duration (minutes)",
            min_value=1,
            max_value=240,
            value=30,
            step=5,
        )
        repeat = st.selectbox("Repeat", ["none", "daily", "weekly"])
        add_task_submitted = st.form_submit_button("Add Task")

        if add_task_submitted:
            title = title.strip()
            category = category.strip()

            selected_pet = find_pet_by_name(owner, selected_pet_name)

            if not title:
                st.warning("Please enter a task title.")
            elif not category:
                st.warning("Please enter a category.")
            elif selected_pet is None:
                st.warning("Please select a valid pet.")
            else:
                new_task = Task(
                    title=title,
                    category=category,
                    date=task_date,
                    start_time=start_time,
                    duration_minutes=int(duration_minutes),
                    repeat=repeat,
                )
                selected_pet.add_task(new_task)
                st.success(f"{title} was added for {selected_pet.name}.")
else:
    st.info("Add a pet before creating tasks.")


st.subheader("Today's Schedule")

today = date.today()
scheduler = Scheduler(owner)
todays_tasks = scheduler.get_todays_tasks(today)
sorted_tasks = scheduler.sort_by_time(todays_tasks)

if sorted_tasks:
    for task in sorted_tasks:
        pet_name = find_pet_name_for_task(owner, task)
        start = task.start_time.strftime("%I:%M %p")
        end = task.get_end_time().strftime("%I:%M %p")
        st.write(
            f"{start} - {end} | {task.title} ({task.category}) "
            f"for {pet_name} | repeat: {task.repeat}"
        )

    conflicts = scheduler.find_conflicts(sorted_tasks)

    if conflicts:
        st.subheader("Conflict Warnings")
        for first_task, second_task in conflicts:
            first_pet = find_pet_name_for_task(owner, first_task)
            second_pet = find_pet_name_for_task(owner, second_task)
            st.warning(
                f"{first_task.title} for {first_pet} overlaps with "
                f"{second_task.title} for {second_pet}."
            )
else:
    st.info("No tasks scheduled for today.")
