# PawPal+

## Overview

PawPal+ is a small pet care management project built for a Python OOP class.
It lets a user add pets, create and manage care tasks, and view a pet schedule in a simple dashboard.
The project also checks for overlapping tasks, supports simple recurring tasks, and allows the user to move between different schedule dates.

This project uses:

- Python OOP
- Streamlit
- pytest

## Live Demo

Streamlit app: [https://pawpal-pet-management-system.streamlit.app/](https://pawpal-pet-management-system.streamlit.app/)

## Features

- Add pets
- Add tasks for pets
- Edit tasks
- Delete tasks
- Show the schedule for a selected date
- Navigate between dates with previous, next, and today controls
- Sort tasks by time
- Filter tasks by pet
- Filter tasks by category
- Show conflict warnings for overlapping tasks
- Mark tasks as completed
- Detect overdue tasks automatically for the current day
- Support simple recurrence options:
  - `none`
  - `daily`
  - `weekly`
- Track recurring task completion by date so one completed occurrence does not mark all future occurrences as completed

## Project Structure

```text
pawpal-pet-management-system/
|- app.py
|- main.py
|- pawpal_system.py
|- requirements.txt
|- README.md
|- reflection.md
|- docs/
|  |- uml_diagram.md
|- tests/
|  |- test_pawpal.py
```

- `pawpal_system.py`: Core backend classes: `Task`, `Pet`, `Owner`, and `Scheduler`
- `main.py`: Simple CLI demo for testing the system in the terminal
- `app.py`: Streamlit app for adding pets, managing tasks, filtering the schedule, and viewing dates
- `tests/test_pawpal.py`: Beginner-friendly pytest tests for core features
- `docs/uml_diagram.md`: Mermaid class diagram for the project design

## How to Run the CLI Demo

1. Create and activate a virtual environment.
2. Install the requirements.
3. Run:

```bash
python3 main.py
```

## How to Run the Streamlit App

1. Create and activate a virtual environment.
2. Install the requirements.
3. Run:

```bash
streamlit run app.py
```

The Streamlit app stores data in `st.session_state` during the current session.
This means pets and tasks can be lost if the app is refreshed or the session resets.

## How to Run Tests

Run:

```bash
pytest tests/test_pawpal.py
```

## Demo Video

Demo video: [https://youtu.be/FMhza1Jw2e8](https://youtu.be/FMhza1Jw2e8)

The video demonstrates:

- Adding pets
- Creating tasks
- Editing and deleting tasks
- Filtering by pet and category
- Navigating between dates
- Detecting conflicts and overdue tasks
- Marking tasks as completed

## Known Limitations

- Data is only stored in session state during the current Streamlit session
- Refreshing the app can clear pets and tasks
- There is no database or file persistence yet
- The app is designed for one owner in the current session
- Recurrence rules are intentionally simple and only support `none`, `daily`, and `weekly`
- The UI is still simple because the project was built for a class assignment

## Future Improvements

- Save data to JSON or a simple database
- Add pet removal in the Streamlit app
- Improve the layout and styling
- Add more test coverage for recurring tasks, editing, and date navigation
- Support more advanced recurrence rules if the project grows later
