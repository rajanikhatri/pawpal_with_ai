from datetime import date, datetime, time, timedelta
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
    "feeding": "#C8B58A",
    "medicine": "#A6BFA8",
    "exercise": "#8EAE8A",
    "grooming": "#9DB8A8",
    "vet visit": "#9DAF97",
    "other": "#A7B0A0",
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
    st.session_state.task_form_date = st.session_state.schedule_date
    st.session_state.show_task_dialog = True


def close_task_dialog() -> None:
    """Close the add-task dialog."""
    st.session_state.show_task_dialog = False


def get_task_end_datetime(task: Task, reference_date: date) -> datetime:
    """Return the end datetime for a task on the reference date."""
    start_datetime = datetime.combine(reference_date, task.start_time)
    return start_datetime + timedelta(minutes=task.duration_minutes)


def complete_task(task: Task) -> None:
    """Mark a task complete and show a success message."""
    task.mark_complete()
    st.session_state.flash_message = f"{task.title} was marked as complete."


def get_task_status(task: Task, reference_date: date, current_datetime: datetime) -> str:
    """Return the display status for a task on the current day."""
    if task.completed:
        return "Completed"

    if reference_date == current_datetime.date() and task.occurs_on(reference_date):
        end_datetime = get_task_end_datetime(task, reference_date)
        if current_datetime > end_datetime:
            return "Overdue"

    return "Pending"


def render_task_card(owner: Owner, task: Task, reference_date: date, current_datetime: datetime) -> None:
    """Render one task as a dashboard-style card."""
    pet_name = find_pet_name_for_task(owner, task)
    start = task.start_time.strftime("%I:%M %p")
    end = get_task_end_datetime(task, reference_date).strftime("%I:%M %p")
    status = get_task_status(task, reference_date, current_datetime)
    category_name = task.category.strip() or "Other"
    category_key = category_name.lower()
    category_color = CATEGORY_COLORS.get(category_key, CATEGORY_COLORS["other"])
    status_class = f"status-{status.lower()}"
    card_class = f"card-{status.lower()}"
    button_key = f"complete_{id(task)}"

    with st.container():
        st.markdown(
            f"""
            <div class="task-card {card_class}" style="border-left: 6px solid {category_color};">
                <div class="task-card-top">
                    <div>
                        <div class="task-time">{escape(start)}</div>
                        <div class="task-end">Ends {escape(end)}</div>
                    </div>
                    <div class="task-side">
                        <div class="task-pet">{escape(pet_name)}</div>
                        <div class="status-badge {status_class}">{escape(status)}</div>
                    </div>
                </div>
                <div class="task-title">{escape(task.title)}</div>
                <div class="task-meta">
                    <span class="meta-pill" style="background:{category_color}22; color:{category_color}; border-color:{category_color}33;">
                        {escape(category_name)}
                    </span>
                    <span class="meta-pill">Repeat: {escape(task.repeat.title())}</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if status == "Pending":
            action_col, _ = st.columns([1, 4])
            with action_col:
                if st.button(
                    "Mark as Complete",
                    key=button_key,
                    type="primary",
                    use_container_width=True,
                ):
                    complete_task(task)
                    st.rerun()

        elif status == "Overdue":
            action_col, _ = st.columns([1, 4])
            with action_col:
                if st.button(
                    "Mark as Complete",
                    key=button_key,
                    use_container_width=True,
                ):
                    complete_task(task)
                    st.rerun()


def render_category_menu() -> None:
    """Render the sidebar category filter buttons."""
    st.markdown('<div class="section-label">CATEGORIES</div>', unsafe_allow_html=True)

    for category in CATEGORY_OPTIONS:
        button_type = "primary" if st.session_state.selected_category == category else "secondary"
        if st.button(category, key=f"category_{category}", use_container_width=True, type=button_type):
            st.session_state.selected_category = category


def render_pet_menu(owner: Owner) -> None:
    """Render the sidebar pet filter buttons."""
    all_pets_type = "primary" if st.session_state.selected_pet == "All Pets" else "secondary"
    if st.button("All Pets", key="pet_all", use_container_width=True, type=all_pets_type):
        st.session_state.selected_pet = "All Pets"

    for pet in owner.get_pets():
        button_type = "primary" if st.session_state.selected_pet == pet.name else "secondary"
        label = f"{pet.name} ({pet.species})"
        if st.button(label, key=f"pet_{pet.name}", use_container_width=True, type=button_type):
            st.session_state.selected_pet = pet.name


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

    with st.form("add_task_form_dialog"):
        selected_pet_name = st.selectbox("Pet", pet_names)
        title = st.text_input("Task title")
        category = st.selectbox(
            "Category",
            ["Feeding", "Medicine", "Exercise", "Grooming", "Vet Visit", "Other"],
        )
        task_date = st.date_input("Date", key="task_form_date")
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
        selected_task_date = st.session_state.task_form_date

        if not title:
            st.warning("Please enter a task title.")
            return

        if selected_pet is None:
            st.warning("Please select a valid pet.")
            return

        new_task = Task(
            title=title,
            category=category,
            date=selected_task_date,
            start_time=start_time,
            duration_minutes=int(duration_minutes),
            repeat=repeat,
        )
        selected_pet.add_task(new_task)
        st.session_state.flash_message = f"{title} was added for {selected_pet.name}."
        st.session_state.task_form_date = st.session_state.schedule_date
        close_task_dialog()
        st.rerun()

    if st.button("Cancel", use_container_width=True):
        st.session_state.task_form_date = st.session_state.schedule_date
        close_task_dialog()
        st.rerun()


if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="Jordan")

if "selected_category" not in st.session_state:
    st.session_state.selected_category = "All Categories"

if "selected_pet" not in st.session_state:
    st.session_state.selected_pet = "All Pets"

if "schedule_date" not in st.session_state:
    st.session_state.schedule_date = date.today()

if "task_form_date" not in st.session_state:
    st.session_state.task_form_date = st.session_state.schedule_date

if "show_task_dialog" not in st.session_state:
    st.session_state.show_task_dialog = False

if "flash_message" not in st.session_state:
    st.session_state.flash_message = ""


st.markdown(
    """
    <style>
    .block-container {
        padding-top: 2.2rem;
        padding-bottom: 2rem;
        max-width: 1440px;
    }

    .header-control-spacer {
        height: 1.75rem;
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
        background: #EEF4EC;
        border: 1px solid #D3E0CF;
        color: #5F7A5A;
        font-size: 1.15rem;
        margin-top: 0.1rem;
    }

    .task-side {
        display: flex;
        flex-direction: column;
        align-items: flex-end;
        gap: 0.45rem;
    }

    .task-card {
        background: #FFFFFF;
        border: 1px solid #E1E8ED;
        border-radius: 16px;
        padding: 1rem 1rem 0.95rem 1rem;
        margin-bottom: 0.9rem;
        box-shadow: 0 2px 10px rgba(44, 62, 80, 0.05);
        transition: all 0.15s ease;
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

    .card-pending {
        background: #FFFFFF;
    }

    .card-overdue {
        background: #FFF9F0;
        border-color: #EBCB97;
        box-shadow: 0 3px 14px rgba(217, 157, 72, 0.12);
    }

    .card-completed {
        background: #F6FAF5;
        border-color: #D3E0CF;
        opacity: 0.72;
    }

    .task-end {
        color: #6B7A89;
        font-size: 0.88rem;
        margin-top: 0.2rem;
    }

    .task-pet {
        color: #6D8A67;
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
        background: #F4F8F2;
        border: 1px solid #D8E4D3;
        color: #5A6C7D;
        font-size: 0.82rem;
    }

    .status-badge {
        display: inline-block;
        padding: 0.35rem 0.7rem;
        border-radius: 999px;
        font-size: 0.8rem;
        font-weight: 700;
        border: 1px solid transparent;
    }

    .status-completed {
        background: #E7F1E4;
        color: #55714F;
        border-color: #C9DBC2;
    }

    .status-overdue {
        background: #FFF1DA;
        color: #A56A12;
        border-color: #F0CF92;
    }

    .status-pending {
        background: #EEF4EC;
        color: #5F7A5A;
        border-color: #D3E0CF;
    }

    div.stButton > button {
        border-radius: 10px;
    }

    div.stButton > button[kind="primary"] {
        background: #7D9A74;
        border-color: #7D9A74;
        color: #FFFFFF;
    }

    div.stButton > button[kind="primary"]:hover {
        background: #6E8B66;
        border-color: #6E8B66;
        color: #FFFFFF;
    }

    div.stButton > button[kind="secondary"] {
        background: #F7FAF5;
        border-color: #D8E4D3;
        color: #546A51;
    }

    div.stButton > button[kind="secondary"]:hover {
        background: #EEF4EC;
        border-color: #C8D7C2;
        color: #4B6148;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


owner = st.session_state.owner
scheduler = Scheduler(owner)
today = date.today()
viewed_date = st.session_state.schedule_date
current_datetime = datetime.now()
todays_tasks = scheduler.get_todays_tasks(today)
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
    st.markdown('<div class="header-control-spacer"></div>', unsafe_allow_html=True)
    st.text_input(
        "Search",
        placeholder="Search tasks...",
        label_visibility="collapsed",
        key="search_placeholder",
    )

with header_action_col:
    st.markdown('<div class="header-control-spacer"></div>', unsafe_allow_html=True)
    st.button(
        "Add Task",
        icon="➕",
        type="primary",
        use_container_width=True,
        on_click=open_task_dialog,
    )

with header_profile_col:
    st.markdown('<div class="header-control-spacer"></div>', unsafe_allow_html=True)
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
            render_pet_menu(owner)
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
    main_header_col, main_date_col = st.columns([1.5, 1.8])

    with main_header_col:
        st.subheader("Schedule")
        st.caption(
            f"Showing: {st.session_state.selected_pet} | "
            f"{st.session_state.selected_category}"
        )

    with main_date_col:
        nav_prev_col, nav_today_col, nav_next_col, nav_picker_col = st.columns([0.8, 0.8, 0.8, 2.1])

        with nav_prev_col:
            if st.button("Previous Day", use_container_width=True):
                st.session_state.schedule_date = st.session_state.schedule_date - timedelta(days=1)
                st.rerun()

        with nav_today_col:
            if st.button("Today", use_container_width=True):
                st.session_state.schedule_date = date.today()
                st.rerun()

        with nav_next_col:
            if st.button("Next Day", use_container_width=True):
                st.session_state.schedule_date = st.session_state.schedule_date + timedelta(days=1)
                st.rerun()

        with nav_picker_col:
            st.date_input(
                "View date",
                key="schedule_date",
                label_visibility="collapsed",
            )

    viewed_date = st.session_state.schedule_date
    st.caption(f"Viewing date: {viewed_date.strftime('%B %d, %Y')}")

    selected_category = None
    if st.session_state.selected_category != "All Categories":
        selected_category = st.session_state.selected_category

    selected_pet = None
    if st.session_state.selected_pet != "All Pets":
        selected_pet = st.session_state.selected_pet

    filtered_tasks = scheduler.filter_tasks(
        scheduler.get_todays_tasks(viewed_date),
        category=selected_category,
        pet_name=selected_pet,
    )

    sorted_filtered_tasks = scheduler.sort_by_time(filtered_tasks)
    visible_conflicts = scheduler.find_conflicts(sorted_filtered_tasks)

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
            render_task_card(owner, task, viewed_date, current_datetime)
    else:
        if (
            st.session_state.selected_category == "All Categories"
            and st.session_state.selected_pet == "All Pets"
        ):
            st.info("No tasks scheduled for today.")
        else:
            st.info(
                "No tasks found for the current pet and category filters."
            )
