import streamlit as st
import sqlite3
from datetime import date

# 1. Database setup
conn = sqlite3.connect("tracker.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS records (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        amount REAL,
        date_logged TEXT
    )
""")
conn.commit()

# 2. Web UI Header
st.title("🏸 Session & Fee Tracker")
st.caption("A simple database tool to track payments and members.")

# 3. Input Form
with st.form("entry_form", clear_on_submit=True):
    col1, col2 = st.columns(2)
    name = col1.text_input("Member Name")
    amount = col2.number_input("Fee Paid ($)", min_value=0.0, step=5.0, value=15.0)
    submitted = st.form_submit_button("Save Record")

    if submitted:
        if name.strip():
            cursor.execute(
                "INSERT INTO records (name, amount, date_logged) VALUES (?, ?, ?)",
                (name.strip(), amount, str(date.today()))
            )
            conn.commit()
            st.success(f"Added {name} (${amount:.2f}) to the database!")
        else:
            st.error("Please enter a valid name.")

# 4. Read & Display from Database
st.divider()

cursor.execute("SELECT SUM(amount), COUNT(*) FROM records")
total_sum, total_count = cursor.fetchone()
total_sum = total_sum if total_sum else 0.0
total_count = total_count if total_count else 0

metric_col1, metric_col2 = st.columns(2)
metric_col1.metric("Total Collected", f"${total_sum:.2f}")
metric_col2.metric("Total Entries", total_count)

st.subheader("All Records")
cursor.execute("SELECT id, name, amount, date_logged FROM records ORDER BY id DESC")
rows = cursor.fetchall()

if rows:
    st.dataframe(
        rows,
        column_config={
            0: "ID",
            1: "Member Name",
            2: st.column_config.NumberColumn("Amount ($)", format="$%.2f"),
            3: "Date Logged"
        },
        use_container_width=True
    )
else:
    st.info("No records logged yet. Add one above!")