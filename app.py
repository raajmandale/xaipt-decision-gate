import streamlit as st
import qrcode
from governance import Request
from audit_log import log, get_logs
from io import BytesIO

st.set_page_config(page_title="XAIPT Decision Gate", page_icon="🔐")

st.title("🔐 XAIPT — QR Authority Decision Gate (Prototype)")
st.caption("Minimal QR-based approval layer for high-risk actions")

if "requests" not in st.session_state:
    st.session_state.requests = {}

# Create new request
st.subheader("1️⃣ Create High-Risk Action")
action_text = st.text_area("Describe the action (e.g., Send ₹50,000 to Vendor A)")

if st.button("Create Request"):
    if action_text.strip():
        req = Request(action_text)
        st.session_state.requests[req.request_id] = req
        log(req.request_id, "CREATED")
        st.success(f"Request Created: {req.request_id}")
    else:
        st.warning("Enter action text.")

st.divider()

# Display requests
st.subheader("2️⃣ Active Requests")

for rid, req in st.session_state.requests.items():
    with st.expander(f"{rid} — {req.status}"):

        st.write("Action:", req.action_text)
        st.write("Created:", req.created_at)
        st.write("Status:", req.status)

        # Generate QR for HOLD state
        if req.status == "HOLD":
            qr_data = f"{req.request_id}|{req.token}"

            qr = qrcode.make(qr_data)
            buffer = BytesIO()
            qr.save(buffer)
            st.image(buffer.getvalue(), caption="Authority QR Code")

            token_input = st.text_input("Enter Approval Token", key=f"tok_{rid}")

            if st.button("Approve", key=f"approve_{rid}"):
                if req.approve(token_input):
                    log(rid, "APPROVED")
                    st.success("Approved.")
                else:
                    st.error("Invalid token.")

        if req.status == "APPROVED":
            if st.button("Execute Action", key=f"exec_{rid}"):
                if req.execute():
                    log(rid, "EXECUTED")
                    st.success("Action Executed.")

st.divider()

st.subheader("3️⃣ Audit Log")
st.write(get_logs())