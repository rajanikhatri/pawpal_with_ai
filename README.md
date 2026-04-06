# PawPal+

## Overview

PawPal+ is a small pet care management project built for a Python OOP class.
It lets a user add pets, create tasks for those pets, and view today's schedule.
The project also checks for overlapping tasks and supports simple recurring tasks.

This project uses:

- Python OOP
- Streamlit
- pytest

## Features

- Add pets
- Add tasks for pets
- Show today's schedule
- Sort tasks by time
- Show conflict warnings for overlapping tasks
- Support simple recurrence options:
  - `none`
  - `daily`
  - `weekly`

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
- `app.py`: Streamlit app for adding pets, adding tasks, and viewing today's schedule
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

## Screenshot Placeholder

Add screenshots here later, such as:

- Streamlit home screen
- Pet creation form
- Task creation form
- Today's schedule with conflict warnings

## Known Limitations

- Data is only stored in session state during the current Streamlit session
- Refreshing the app can clear pets and tasks
- There is no database or file persistence yet
- The app is designed for one owner in the current session
- The UI is simple and built for a class project
- Task editing and deletion are not included yet

## Future Improvements

- Save data to JSON or a simple database
- Add task editing and deletion
- Add pet removal in the Streamlit app
- Add filters for pet name or task category in the UI
- Improve the layout and styling
- Add more test coverage for recurring tasks and schedule behavior
