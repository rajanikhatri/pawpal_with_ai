# PawPal+ Project Reflection

## 1. Initial Design

When I first planned PawPal+, I wanted the design to be simple and easy to understand. I chose the classes `Owner`, `Pet`, `Task`, and `Scheduler` because each one had a clear job.

- `Owner` represents the person using the system and keeps track of their pets.
- `Pet` represents one pet and stores the tasks for that pet.
- `Task` represents one care activity like feeding, walking, grooming, or medication.
- `Scheduler` handles the scheduling logic, like finding today's tasks, sorting them by time, and checking for conflicts.

I liked this design because it matched the problem in a natural way. Instead of putting everything into one big file with mixed logic, each class had one main responsibility.

## 2. Design Changes

During development, I simplified the design a lot. At the beginning, it was easy to imagine adding more things like unique IDs, extra helper classes, database storage, or more advanced scheduling rules. But for this project, I realized that would make the code more complicated without adding much value.

One example is that I decided not to use IDs for pets and tasks. For a larger app, IDs would probably be helpful, but for this class project I could just use pet names and task titles when needed.

I also kept recurrence very simple with only three options: `none`, `daily`, and `weekly`. I did not try to support more advanced rules because that would make the project harder to manage.

I avoided overengineering because I wanted the code to stay readable and realistic for a student project. My goal was not to build a full production app. My goal was to build something that works, shows OOP design clearly, and is easy to explain.

## 3. Algorithmic Tradeoffs

My scheduling logic is intentionally simple. The scheduler collects tasks from all pets, checks which ones happen today, sorts them by start time, and then checks for overlaps.

This works well for a class project, but it has limitations:

- it does not automatically resolve conflicts
- it does not choose the "best" schedule
- it does not use priority scoring or optimization
- it does not handle advanced recurrence patterns

I accepted these limits because I wanted the system to stay focused on the core features. Instead of building a complicated scheduling algorithm, I built one that is easy to understand and test. I think that was the right choice for this project because it let me finish a working system instead of getting stuck trying to make it too smart.

## 4. AI Collaboration

I used AI tools like Codex and Claude to help with planning, coding structure, and improving small parts of the project. AI was especially helpful when I was:

- organizing the class design
- turning the UML idea into class skeletons
- writing method stubs
- building small pytest tests
- improving the README and reflection writing

The most helpful prompts were specific ones. For example, it worked better when I asked for only one class at a time or one file at a time instead of asking for the whole project at once.

One example where I changed an AI suggestion was during the design stage. Some suggestions made the project more complex than I needed, like adding IDs everywhere or making the scheduler more advanced. I decided not to follow that direction and kept the design smaller with just the four main classes and simple recurrence rules. I also checked the code by running the CLI demo, testing the Streamlit app, and running pytest instead of assuming every AI suggestion was correct.

A more technical example came later when I found a bug with recurring task completion. At first, if a daily task was marked complete on one day, it stayed completed on future days too. That showed me that I was treating a recurring task like one permanent object instead of thinking about each occurrence on each date. With AI help, I worked through a cleaner fix: the `Task` model needed to track completion by date for recurring tasks, and the Streamlit UI also needed to check completion based on the currently viewed schedule date. I still had to review the solution carefully, but that change helped me understand the difference between a recurring task definition and a specific occurrence of that task.

## 5. What I Learned

One thing I learned about system design is that a simple design is often better than a complicated one, especially early on. Having four clear classes made the project easier to build step by step. It also made debugging easier because I could focus on one class at a time.

I also learned that frontend and backend decisions are connected more than I expected. As I improved the Streamlit UI, I sometimes had to revisit backend logic too, especially for recurring tasks and overdue detection. A better interface exposed edge cases that were easy to miss earlier.

I also learned that AI is most useful when I give it clear boundaries. If I ask something broad, the answer can become too big or too complicated. If I ask for one small step at a time, the help is much more useful. I also learned that I still need to review and test everything myself. AI helped me move faster, but I still had to make the final decisions and verify that the code matched my project goals.

Overall, this project helped me practice object-oriented design, basic scheduling logic, testing, and working with AI in a more thoughtful way.
