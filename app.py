from datetime import date, time
from html import escape

import streamlit as st

from pawpal_system import Owner, Pet, Scheduler, Task


st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="wide")


CATEGORY_OPTIONS = [
    "All Categories",
    "Feeding",
    "Medicine",
    "Exercise",
    "Grooming",
    "Vet Visit",
    "Other",
]

CATEGORY_COLORS = {
    "feeding": "#FF9E80",
    "medicine": "#F48FB1",
    "exercise": "#81C784",
    "grooming": "#64B5F6",
    "vet visit": "#BA68C8",
    "other": "#90A4AE",
}


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


def show_flash_message() -> None:
    """Display a one-time success message after a rerun."""
    message = st.session_state.get("flash_message")
    if message:
        st.success(message)
        st.session_state.flash_message = ""


def open_task_dialog() -> None:
    """Open the add-task dialog."""
    st.session_state.show_task_dialog = True


def close_task_dialog() -> None:
    """Close the add-task dialog."""
    st.session_state.show_task_dialog = False


def render_task_card(owner: Owner, task: Task) -> None:
    """Render one task as a dashboard-style card."""
    pet_name = find_pet_name_for_task(owner, task)
    start = task.start_time.strftime("%I:%M %p")
    end = task.get_end_time().strftime("%I:%M %p")
    status = "Completed" if task.completed else "Pending"
    category_name = task.category.strip() or "Other"
    category_key = category_name.lower()
    category_color = CATEGORY_COLORS.get(category_key, CATEGORY_COLORS["other"])

    st.markdown(
        f"""
        <div class="task-card" style="border-left: 6px solid {category_color};">
            <div class="task-card-top">
                <div>
                    <div class="task-time">{escape(start)}</div>
                    <div class="task-end">Ends {escape(end)}</div>
                </div>
                <div class="task-pet">{escape(pet_name)}</div>
            </div>
            <div class="task-title">{escape(task.title)}</div>
            <div class="task-meta">
                <span class="meta-pill" style="background:{category_color}22; color:{category_color}; border-color:{category_color}33;">
                    {escape(category_name)}
                </span>
                <span class="meta-pill">Repeat: {escape(task.repeat.title())}</span>
                <span class="meta-pill">Status: {escape(status)}</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_category_menu() -> None:
    """Render the sidebar category filter buttons."""
    st.markdown('<div class="section-label">CATEGORIES</div>', unsafe_allow_html=True)

    for category in CATEGORY_OPTIONS:
        button_type = "primary" if st.session_state.selected_category == category else "secondary"
        if st.button(category, key=f"category_{category}", use_container_width=True, type=button_type):
            st.session_state.selected_category = category


@st.dialog("Add Task", width="large", on_dismiss=close_task_dialog)
def show_add_task_dialog(owner: Owner) -> None:
    """Show the add-task form in a dialog."""
    if not owner.get_pets():
        st.info("Add a pet before creating tasks.")
        if st.button("Close", use_container_width=True):
            close_task_dialog()
            st.rerun()
        return

    pet_names = [pet.name for pet in owner.get_pets()]

    with st.form("add_task_form_dialog", clear_on_submit=True):
        selected_pet_name = st.selectbox("Pet", pet_names)
        title = st.text_input("Task title")
        category = st.selectbox(
            "Category",
            ["Feeding", "Medicine", "Exercise", "Grooming", "Vet Visit", "Other"],
        )
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
        add_task_submitted = st.form_submit_button("Save Task", type="primary")

    if add_task_submitted:
        title = title.strip()
        selected_pet = find_pet_by_name(owner, selected_pet_name)

        if not title:
            st.warning("Please enter a task title.")
            return

        if selected_pet is None:
            st.warning("Please select a valid pet.")
            return

        new_task = Task(
            title=title,
            category=category,
            date=task_date,
            start_time=start_time,
            duration_minutes=int(duration_minutes),
            repeat=repeat,
        )
        selected_pet.add_task(new_task)
        st.session_state.flash_message = f"{title} was added for {selected_pet.name}."
        close_task_dialog()
        st.rerun()

    if st.button("Cancel", use_container_width=True):
        close_task_dialog()
        st.rerun()


if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="Jordan")

if "selected_category" not in st.session_state:
    st.session_state.selected_category = "All Categories"

if "show_task_dialog" not in st.session_state:
    st.session_state.show_task_dialog = False

if "flash_message" not in st.session_state:
    st.session_state.flash_message = ""


st.markdown(
    """
    <style>
    .block-container {
        padding-top: 1.2rem;
        padding-bottom: 2rem;
        max-width: 1440px;
    }

    .section-label {
        font-size: 0.78rem;
        font-weight: 700;
        letter-spacing: 0.08em;
        color: #66788A;
        margin-bottom: 0.75rem;
    }

    .profile-pill {
        display: flex;
        align-items: center;
        justify-content: center;
        width: 42px;
        height: 42px;
        border-radius: 999px;
        background: #F4F7FB;
        border: 1px solid #E1E8ED;
        font-size: 1.15rem;
        margin-top: 0.1rem;
    }

    .pet-row {
        padding: 0.55rem 0.7rem;
        border-radius: 10px;
        background: #F7F9FC;
        border: 1px solid #EEF3F8;
        margin-bottom: 0.5rem;
        font-size: 0.95rem;
    }

    .task-card {
        background: #FFFFFF;
        border: 1px solid #E1E8ED;
        border-radius: 16px;
        padding: 1rem 1rem 0.95rem 1rem;
        margin-bottom: 0.9rem;
        box-shadow: 0 2px 10px rgba(44, 62, 80, 0.05);
    }

    .task-card-top {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        gap: 1rem;
    }

    .task-time {
        font-size: 1.45rem;
        font-weight: 700;
        color: #2C3E50;
        line-height: 1.1;
    }

    .task-end {
        color: #6B7A89;
        font-size: 0.88rem;
        margin-top: 0.2rem;
    }

    .task-pet {
        color: #4A90E2;
        font-weight: 600;
        font-size: 0.95rem;
    }

    .task-title {
        margin-top: 0.8rem;
        margin-bottom: 0.75rem;
        font-size: 1.08rem;
        font-weight: 700;
        color: #2C3E50;
    }

    .task-meta {
        display: flex;
        flex-wrap: wrap;
        gap: 0.5rem;
    }

    .meta-pill {
        display: inline-block;
        padding: 0.35rem 0.65rem;
        border-radius: 999px;
        background: #F4F7FB;
        border: 1px solid #E1E8ED;
        color: #5A6C7D;
        font-size: 0.82rem;
    }

    div.stButton > button {
        border-radius: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


owner = st.session_state.owner
scheduler = Scheduler(owner)
today = date.today()
todays_tasks = scheduler.get_todays_tasks(today)
sorted_today_tasks = scheduler.sort_by_time(todays_tasks)
total_tasks = len(todays_tasks)
completed_tasks = sum(1 for task in todays_tasks if task.completed)
pending_tasks = total_tasks - completed_tasks

header_title_col, header_search_col, header_action_col, header_profile_col = st.columns(
    [2.4, 1.5, 0.9, 0.3]
)

with header_title_col:
    st.title("🐾 PawPal+")
    st.caption("Pet care dashboard")

with header_search_col:
    st.text_input(
        "Search",
        placeholder="Search tasks...",
        label_visibility="collapsed",
        key="search_placeholder",
    )

with header_action_col:
    st.write("")
    st.button(
        "Add Task",
        icon="➕",
        type="primary",
        use_container_width=True,
        on_click=open_task_dialog,
    )

with header_profile_col:
    st.markdown('<div class="profile-pill">👤</div>', unsafe_allow_html=True)


if st.session_state.show_task_dialog:
    show_add_task_dialog(owner)


show_flash_message()


sidebar_col, main_col = st.columns([1, 2.4], gap="large")

with sidebar_col:
    with st.container(border=True):
        st.markdown('<div class="section-label">TODAY\'S STATS</div>', unsafe_allow_html=True)
        stat_col_1, stat_col_2, stat_col_3 = st.columns(3)
        stat_col_1.metric("Total", total_tasks)
        stat_col_2.metric("Pending", pending_tasks)
        stat_col_3.metric("Completed", completed_tasks)

    with st.container(border=True):
        st.markdown('<div class="section-label">MY PETS</div>', unsafe_allow_html=True)
        st.caption(f"Owner: {owner.name}")

        if owner.get_pets():
            for pet in owner.get_pets():
                st.markdown(
                    f'<div class="pet-row">{escape(pet.name)} ({escape(pet.species)})</div>',
                    unsafe_allow_html=True,
                )
        else:
            st.info("No pets added yet.")

        with st.expander("Add Pet"):
            with st.form("add_pet_form", clear_on_submit=True):
                pet_name = st.text_input("Pet name")
                species = st.selectbox("Species", ["Dog", "Cat", "Other"])
                add_pet_submitted = st.form_submit_button("Save Pet")

                if add_pet_submitted:
                    pet_name = pet_name.strip()

                    if pet_name:
                        owner.add_pet(Pet(name=pet_name, species=species))
                        st.session_state.flash_message = f"{pet_name} was added."
                        st.rerun()
                    else:
                        st.warning("Please enter a pet name.")

    with st.container(border=True):
        render_category_menu()

with main_col:
    st.markdown('<div class="section-label">TODAY\'S SCHEDULE</div>', unsafe_allow_html=True)
    main_header_col, main_date_col = st.columns([2, 1])

    with main_header_col:
        st.subheader("Today's Schedule")
        st.caption(f"Showing: {st.session_state.selected_category}")

    with main_date_col:
        st.caption(f"Date: {today.strftime('%B %d, %Y')}")

    if st.session_state.selected_category == "All Categories":
        filtered_tasks = todays_tasks
    else:
        filtered_tasks = scheduler.filter_tasks(
            todays_tasks,
            category=st.session_state.selected_category,
        )

    sorted_filtered_tasks = scheduler.sort_by_time(filtered_tasks)
    all_conflicts = scheduler.find_conflicts(sorted_today_tasks)

    if st.session_state.selected_category == "All Categories":
        visible_conflicts = all_conflicts
    else:
        selected_key = st.session_state.selected_category.strip().lower()
        visible_conflicts = [
            (first_task, second_task)
            for first_task, second_task in all_conflicts
            if first_task.category.strip().lower() == selected_key
            or second_task.category.strip().lower() == selected_key
        ]

    if visible_conflicts:
        st.markdown('<div class="section-label">CONFLICT WARNINGS</div>', unsafe_allow_html=True)
        for first_task, second_task in visible_conflicts:
            first_pet = find_pet_name_for_task(owner, first_task)
            second_pet = find_pet_name_for_task(owner, second_task)
            st.warning(
                f"{first_task.title} for {first_pet} overlaps with "
                f"{second_task.title} for {second_pet}."
            )

    if sorted_filtered_tasks:
        for task in sorted_filtered_tasks:
            render_task_card(owner, task)
    else:
        if st.session_state.selected_category == "All Categories":
            st.info("No tasks scheduled for today.")
        else:
            st.info(f"No tasks found for {st.session_state.selected_category}.")
