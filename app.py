import os
import pandas as pd
import streamlit as st

import database as db
import face_verify as fv
from ticket_qr import make_ticket, decode_qr

st.set_page_config(page_title="Railway AI Verification", page_icon="🚆", layout="wide")
st.title("🚆 AI Railway Ticket–Passenger Reconciliation")
st.caption("Educational prototype · dummy tickets · consenting test participants only")

engine = fv.backend()
menu = st.sidebar.radio("Navigation", [
    "Dashboard", "Register Passenger", "Verify Passenger",
    "Passenger Records", "Verification History", "Settings"])
st.sidebar.markdown("---")
st.sidebar.write("Face engine:", f"**{engine}**" if engine else "❌ not available")
if engine is None:
    st.sidebar.error("Install face-recognition, or run `python download_models.py`.")

# ---------------------------------------------------------------- Dashboard
if menu == "Dashboard":
    s = db.stats()
    c = st.columns(4)
    c[0].metric("Registered passengers", s["passengers"])
    c[1].metric("Verification attempts", s["checks"])
    c[2].metric("Matches", s["MATCH"])
    c[3].metric("Mismatches (manual review)", s["MISMATCH"])
    st.subheader("Latest verifications")
    logs = db.list_logs()[:5]
    if logs:
        st.dataframe(pd.DataFrame(logs, columns=["ID", "Ticket", "Result", "Score", "Time"]),
                     use_container_width=True, hide_index=True)
    else:
        st.info("No checks yet. Register a passenger, then verify.")

# ------------------------------------------------------------- Registration
elif menu == "Register Passenger":
    st.subheader("Passenger Registration")
    st.warning("Face photos are biometric data. Use only consenting participants.")
    with st.form("reg"):
        tid = st.text_input("Ticket ID", placeholder="T1001").strip()
        name = st.text_input("Passenger name")
        seat = st.text_input("Seat number", placeholder="S5-32")
        train = st.text_input("Train", value="DEMO EXPRESS")
        photo = st.file_uploader("Reference face photo", type=["jpg", "jpeg", "png"])
        go = st.form_submit_button("Register Passenger")
    if go:
        if not (tid and name and seat and photo):
            st.error("Please complete all fields.")
        elif engine is None:
            st.error("No face engine available.")
        elif db.get_passenger(tid):
            st.error("Ticket ID already exists.")
        elif fv.encode_face(photo.getvalue()) is None:
            st.error("Photo must contain exactly one clearly detectable face.")
        else:
            path = os.path.join(db.FACES_DIR, f"{tid}.jpg")
            with open(path, "wb") as f:
                f.write(photo.getvalue())
            db.add_passenger(tid, name, seat, train, path)
            card = make_ticket(tid, name, seat, train)
            st.success("Demo passenger registered.")
            st.image(card, caption="Demo ticket with QR code")
            with open(card, "rb") as f:
                st.download_button("Download ticket", f, file_name=f"{tid}.png")

# ------------------------------------------------------------ Verification
elif menu == "Verify Passenger":
    st.subheader("Ticket–Passenger Verification")
    mode = st.radio("Ticket input", ["Type ticket ID", "Scan QR (upload / camera)"],
                    horizontal=True)
    tid = ""
    if mode == "Type ticket ID":
        tid = st.text_input("Ticket ID").strip()
    else:
        qr_img = st.camera_input("Show the QR code to the camera", key="qrcam") \
            or st.file_uploader("…or upload the ticket image", type=["png", "jpg", "jpeg"])
        if qr_img is not None:
            tid = decode_qr(qr_img.getvalue()) or ""
            st.write("QR content:", tid if tid else "⚠️ no QR code detected")

    face = st.camera_input("Capture passenger face", key="facecam")

    if st.button("Verify Passenger", type="primary"):
        if not tid or face is None:
            st.warning("Provide a ticket (ID or QR) and capture a face.")
        elif engine is None:
            st.error("No face engine available.")
        else:
            p = db.get_passenger(tid)
            if not p:
                result, score = "NOT FOUND", None
                st.error(f"Ticket '{tid}' not found.")
            else:
                _, name, seat, train, face_file, _ = p
                with open(face_file, "rb") as f:
                    known = f.read()
                result, score = fv.compare_faces(
                    known, face.getvalue(),
                    dlib_threshold=st.session_state.get("dlib_t"),
                    cosine_threshold=st.session_state.get("cos_t"))
                c1, c2, c3 = st.columns(3)
                c1.metric("Passenger", name)
                c2.metric("Seat", seat)
                c3.metric("Train", train)
                a, b = st.columns(2)
                a.image(face_file, caption="Registered photo", width=220)
                b.image(face, caption="Captured photo", width=220)
                if result == "MATCH":
                    st.success("✅ PASSENGER MATCH — staff confirmation still required.")
                elif result == "MISMATCH":
                    st.error("🚨 PASSENGER MISMATCH — manual review required (not proof of fraud).")
                else:
                    st.warning("⚠️ Could not reliably compare — retake photo (one face, good light).")
                if score is not None:
                    st.caption(f"Similarity score: {score:.3f}")
            db.add_log(tid, result, score)

# ------------------------------------------------------------------ Records
elif menu == "Passenger Records":
    st.subheader("Registered passengers")
    rows = db.list_passengers()
    if rows:
        st.dataframe(pd.DataFrame(rows, columns=["Ticket", "Name", "Seat", "Train", "Registered"]),
                     use_container_width=True, hide_index=True)
        sel = st.selectbox("View ticket / delete passenger", [r[0] for r in rows])
        tpath = os.path.join(db.TICKETS_DIR, f"{sel}.png")
        if os.path.exists(tpath):
            st.image(tpath, width=400)
        if st.button("Delete this passenger"):
            db.delete_passenger(sel)
            st.rerun()
    else:
        st.info("No passengers registered.")

# ------------------------------------------------------------------ History
elif menu == "Verification History":
    st.subheader("Verification History")
    rows = db.list_logs()
    if rows:
        df = pd.DataFrame(rows, columns=["ID", "Ticket", "Result", "Score", "Time"])
        pick = st.multiselect("Filter result", sorted(df["Result"].unique()),
                              default=list(df["Result"].unique()))
        df = df[df["Result"].isin(pick)]
        st.dataframe(df, use_container_width=True, hide_index=True)
        st.download_button("Download CSV", df.to_csv(index=False), "history.csv", "text/csv")
    else:
        st.info("No verification records yet.")

# ----------------------------------------------------------------- Settings
elif menu == "Settings":
    st.subheader("Settings")
    st.write("Thresholds are demo values; calibrate on your own test participants.")
    st.session_state["dlib_t"] = st.slider("dlib: max distance for MATCH", 0.30, 0.70,
                                           st.session_state.get("dlib_t", fv.DLIB_MAX_DISTANCE), 0.01)
    st.session_state["cos_t"] = st.slider("OpenCV SFace: min cosine for MATCH", 0.20, 0.70,
                                          st.session_state.get("cos_t", fv.SFACE_MIN_COSINE), 0.01)
    st.divider()
    st.error("Delete all test data (photos, tickets, records)")
    if st.checkbox("I understand this cannot be undone") and st.button("Wipe all data"):
        db.wipe_all()
        st.success("All data deleted.")

st.divider()
st.caption("Academic demonstration only. A mismatch is not proof of fraud; a match is not proof of identity.")
