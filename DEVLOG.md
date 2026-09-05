# Developer Log - Session Tracker

### [2026-09-05] - Day 1: Local SQLite + Streamlit Baseline

- **What I built:**
  - Initialized a Git repository and set up a local workspace inside `freelance-projects/session-tracker`.
  - Built a Streamlit web application connected directly to a local SQLite database (`tracker.db`).
  - Added a responsive form to submit member names and fee payments.
  - Added live metric cards (Total Collected, Total Entries) and an interactive data table displaying stored records.

- **Questions I Asked & Clarifications:**
  - *Q: What is Streamlit?*
    - **Takeaway:** It is a Python framework that converts pure Python code into interactive web UI components without writing HTML/CSS/JS.
  - *Q: Should I keep all projects in one repository or separate them?*
    - **Takeaway:** Always separate repositories per project. Single-purpose repositories prevent deployment bugs on hosting platforms and make sharing clean links with clients straightforward.
  - *Q: What do `pip install` and `touch` mean?*
    - **Takeaway:** `pip install` downloads external Python packages from PyPI; `touch` creates new files instantly from the terminal without overwriting existing data.
  - *Q: Was changing Python 3.14 to Anaconda changing the compiler?*
    - **Takeaway:** No, Python uses an interpreter, not a compiler. The fix resolved an interpreter/environment mismatch so VS Code could locate packages installed in the Anaconda environment.

- **Next Steps:**
  - Commit all project files via Sourcetree and push to GitHub.
  - Deploy the repository to Streamlit Community Cloud to generate a live, shareable URL.