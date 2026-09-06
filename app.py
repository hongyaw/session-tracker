import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

# Page configuration
st.set_page_config(page_title="Session & Fee Tracker", page_icon="🏸", layout="centered")

# --- DATABASE SETUP ---
def init_db():
    conn = sqlite3.connect("tracker.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            amount REAL NOT NULL,
            date_logged TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def add_record(name, amount, date_logged):
    conn = sqlite3.connect("tracker.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO records (name, amount, date_logged) VALUES (?, ?, ?)",
        (name, amount, date_logged)
    )
    conn.commit()
    conn.close()

def delete_record(record_id):
    conn = sqlite3.connect("tracker.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM records WHERE id = ?", (record_id,))
    conn.commit()
    conn.close()

def fetch_records():
    conn = sqlite3.connect("tracker.db")
    df = pd.read_sql_query("SELECT id, name, amount, date_logged FROM records ORDER BY id DESC", conn)
    conn.close()
    return df

# Initialize database table
init_db()

# --- UI HEADER ---
st.title("🏸 Session & Fee Tracker")
st.caption("A database tool to track payments, sessions, and records.")

# --- FORM: ADD RECORD ---
with st.form("entry_form", clear_on_submit=True):
    col1, col2 = st.columns([2, 1])
    with col1:
        name = st.text_input("Member Name")
    with col2:
        amount = st.number_input("Fee Paid ($)", min_value=0.0, value=15.0, step=1.0)
    
    submitted = st.form_submit_button("Save Record")
    if submitted:
        if name.strip():
            date_logged = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            add_record(name.strip(), amount, date_logged)
            st.success(f"Added record for {name.strip()}!")
            st.rerun()
        else:
            st.warning("Please enter a member name.")

# --- FETCH CURRENT DATA ---
df = fetch_records()

# --- KPI METRICS ---
col_m1, col_m2 = st.columns(2)
total_collected = df["amount"].sum() if not df.empty else 0.0
total_entries = len(df)

col_m1.metric("Total Collected", f"${total_collected:,.2f}")
col_m2.metric("Total Entries", total_entries)

st.divider()

# --- RECORDS SECTION ---
st.subheader("All Records")

if not df.empty:
    # 1. Search Bar
    search_query = st.text_input("🔍 Search by Member Name", placeholder="Type to filter...")
    filtered_df = df[df["name"].str.contains(search_query, case=False, na=False)] if search_query else df

    # Display Data Table
    st.dataframe(
        filtered_df,
        column_config={
            "id": "ID",
            "name": "Member Name",
            "amount": st.column_config.NumberColumn("Fee Paid ($)", format="$%.2f"),
            "date_logged": "Timestamp"
        },
        use_container_width=True,
        hide_index=True
    )

    # 2. Export to CSV & 3. Delete Record Section
    col_export, col_delete = st.columns([1, 1])

    with col_export:
        csv_data = filtered_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download CSV",
            data=csv_data,
            file_name="session_records.csv",
            mime="text/csv",
            use_container_width=True
        )

    with col_delete:
        with st.expander("🗑️ Delete a Record"):
            # Create a clean label for each record to show in dropdown
            options = {f"ID {row['id']} - {row['name']} (${row['amount']:.2f})": row['id'] for _, row in df.iterrows()}
            selected_label = st.selectbox("Select record to delete", list(options.keys()))
            
            if st.button("Confirm Delete", type="primary", use_container_width=True):
                delete_id = options[selected_label]
                delete_record(delete_id)
                st.toast(f"Deleted record ID {delete_id} successfully!")
                st.rerun()
else:
    st.info("No records logged yet. Add one above!")