# Developer Log - Session Tracker

### [2026-09-05] - Day 1: Local SQLite Baseline & Streamlit Cloud Deployment

- **What I built:**
  - Initialized a dedicated Git repository and local workspace inside `~/Documents/GitHub/freelance-projects/session-tracker`.
  - Built a Streamlit web application connected directly to a local SQLite database (`tracker.db`).
  - Implemented an interactive input form to submit member names, fee amounts, and payment dates.
  - Implemented live KPI metric cards (Total Collected, Total Entries) and an interactive data table displaying stored database records.
  - Version-controlled the codebase using Sourcetree, pushed to GitHub, and deployed to Streamlit Community Cloud for a live, public URL.

- **Questions I Asked & Core Concepts Learned:**
  - *Q: What is Streamlit?*
    - **Takeaway:** A lightweight Python framework that turns pure Python scripts into interactive, reactive web apps without having to manually write HTML, CSS, or JavaScript.
  - *Q: Should I keep multiple projects in one repo or separate them?*
    - **Takeaway:** Always maintain separate repositories per project. Single-purpose repos prevent dependency conflicts, make cloud deployments clean and predictable, and allow sharing isolated links with clients.
  - *Q: What do `pip install` and `touch` do?*
    - **Takeaway:** `pip install` downloads and installs third-party packages from PyPI into the active Python environment; `touch` creates empty files instantly via the terminal without overwriting existing data.
  - *Q: Was changing Python 3.14 to Anaconda changing the compiler?*
    - **Takeaway:** No, Python uses an interpreter rather than a compiler. The fix resolved an interpreter/environment mismatch so VS Code pointed to the Anaconda environment where Streamlit was actually installed.
  - *Q: When Streamlit asks for an email on first run, does it save it or write it to the database?*
    - **Takeaway:** No. Hitting enter without entering an email stores nothing. The prompt is strictly a CLI utility flag (`~/.streamlit/credentials.toml`) to prevent recurring terminal prompts; it has zero connection to the application code or SQLite database.
  - *Q: What does `feat:` mean in commit messages?*
    - **Takeaway:** It stands for "feature" under the Conventional Commits specification, clearly signaling that a commit introduces new application functionality.
  - *Q: Why deploy now if SQLite has limitations in the cloud?*
    - **Takeaway:** Deploying early validates the production build pipeline, `requirements.txt`, and cloud hosting environment. However, Streamlit Cloud containers are ephemeral, meaning local SQLite changes reset on server reboot. This sets up the natural next step: migrating to an external persistent cloud database.

- **Next Steps:**
  - Connect the app to a persistent external cloud database (e.g., Supabase / hosted PostgreSQL) so cloud data survives container restarts.
  - Add search/filtering by member name and date range.
  - Implement a delete/edit record action for data hygiene.