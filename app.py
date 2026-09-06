import streamlit as st
import pandas as pd
from datetime import datetime
from supabase import create_client, Client

# Page configuration
st.set_page_config(page_title="Session & Fee Tracker", page_icon="🏸", layout="centered")

# --- SUPABASE CONNECTION ---
@st.cache_resource
def get_supabase_client() -> Client:
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)

supabase = get_supabase_client()

# --- DATABASE CRUD HELPERS ---
def add_record(name: str, amount: float, date_logged: str):
    supabase.table("records").insert({
        "name": name,
        "amount": amount,
        "date_logged": date_logged
    }).execute()

def delete_record(record_id: int):
    supabase.table("records").delete().eq("id", record_id).execute()

def fetch_records() -> pd.DataFrame:
    response = supabase.table("records").select("id, name, amount, date_logged").order("id", desc=True).execute()
    data = response.data
    if data:
        return pd.DataFrame(data)
    return pd.DataFrame(columns=["id", "name", "amount", "date_logged"])

# --- UI HEADER ---
st.title("🏸 Session & Fee Tracker")
st.caption("A cloud database tool to track payments, sessions, and records.")

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
total_collected = float(df["amount"].sum()) if not df.empty else 0.0
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
        csv_data = filtered_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Download CSV",
            data=csv_data,
            file_name="session_records.csv",
            mime="text/csv",
            use_container_width=True
        )

    with col_delete:
        with st.expander("🗑️ Delete a Record"):
            options = {f"ID {row['id']} - {row['name']} (${float(row['amount']):.2f})": int(row["id"]) for _, row in df.iterrows()}
            selected_label = st.selectbox("Select record to delete", list(options.keys()))
            
            if st.button("Confirm Delete", type="primary", use_container_width=True):
                delete_id = options[selected_label]
                delete_record(delete_id)
                st.toast(f"Deleted record ID {delete_id} successfully!")
                st.rerun()
else:
    st.info("No records logged yet. Add one above!")