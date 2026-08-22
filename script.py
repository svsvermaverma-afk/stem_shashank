import streamlit as st
import os
import shutil

st.set_page_config(page_title="STEM Lab Profile Manager", page_icon="🔬", layout="wide")

# Directory setup to store uploaded records
UPLOAD_DIR = "stem_lab_records"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Complete 50 STEM Record categories
CATEGORIES = {
    "1. Administration & Planning": [
        (1, "STEM Lab Profile", ["pdf", "docx", "doc"]),
        (2, "Lab Objectives & Guidelines", ["pdf"]),
        (3, "Coordinator / SPOC Details", ["pdf", "docx", "doc"]),
        (4, "Annual STEM Plan", ["xlsx", "xls", "pdf"]),
        (5, "Monthly Activity Plan", ["xlsx", "xls"]),
        (6, "Class-wise Timetable", ["xlsx", "xls", "pdf"]),
        (7, "Session/Lesson Plans", ["pdf", "docx", "doc"]),
        (8, "Student List", ["xlsx", "xls"]),
        (9, "Student Attendance", ["xlsx", "xls", "csv"]),
        (10, "Teacher Attendance", ["xlsx", "xls", "csv"]),
    ],
    "2. Inventory & Safety": [
        (11, "Lab Inventory", ["xlsx", "xls", "csv"]),
        (12, "Equipment Details", ["xlsx", "xls"]),
        (13, "Equipment Photos", ["jpg", "png", "jpeg"]),
        (14, "Equipment Purchase Records", ["pdf"]),
        (15, "Maintenance Records", ["xlsx", "xls", "pdf"]),
        (16, "Lab Safety Rules", ["pdf"]),
        (17, "Safety Checklist", ["xlsx", "xls", "pdf"]),
    ],
    "3. Activities & Projects": [
        (18, "STEM Activities", ["pdf", "docx", "doc"]),
        (19, "Activity Worksheets", ["pdf"]),
        (20, "Activity Photos", ["jpg", "png", "jpeg"]),
        (21, "Activity Videos", ["mp4", "mov", "avi"]),
        (22, "Student Projects", ["pdf", "docx", "doc"]),
        (23, "Prototype Details", ["pdf"]),
        (24, "Problem Statements", ["docx", "doc", "xlsx", "xls"]),
        (25, "Innovation Ideas", ["xlsx", "xls"]),
        (26, "Project Photos", ["jpg", "png", "jpeg"]),
        (27, "Project Videos", ["mp4", "mov", "avi"]),
    ],
    "4. Assessment & Competitions": [
        (28, "Assessment Rubrics", ["xlsx", "xls", "pdf"]),
        (29, "Student Assessment", ["xlsx", "xls"]),
        (30, "Student Performance", ["xlsx", "xls", "csv"]),
        (31, "STEM SPARK Registration", ["pdf", "xlsx", "xls"]),
        (32, "STEM SPARK Team Details", ["xlsx", "xls"]),
        (33, "STEM SPARK Submissions", ["pdf"]),
        (34, "VVM Records", ["pdf", "xlsx", "xls"]),
        (35, "Other Competitions", ["pdf", "xlsx", "xls"]),
    ],
    "5. Training & Communication": [
        (36, "Teacher Training Records", ["xlsx", "xls", "pdf"]),
        (37, "Training Certificates", ["pdf", "jpg", "png", "jpeg"]),
        (38, "Training Attendance", ["xlsx", "xls"]),
        (39, "Workshop Reports", ["docx", "doc", "pdf"]),
        (40, "Workshop Photos", ["jpg", "png", "jpeg"]),
        (41, "Government Circulars", ["pdf"]),
        (42, "School Circulars", ["pdf"]),
        (43, "Official Emails", ["pdf", "jpg", "png"]),
        (44, "Meeting Minutes", ["docx", "doc", "pdf"]),
    ],
    "6. Reports & Achievements": [
        (45, "Monthly Reports", ["pdf"]),
        (46, "Quarterly Reports", ["pdf"]),
        (47, "Annual Report", ["pdf"]),
        (48, "Student Certificates", ["pdf", "jpg", "png", "jpeg"]),
        (49, "Student Achievements", ["xlsx", "xls", "pdf"]),
        (50, "STEM Lab Event Photos", ["jpg", "png", "jpeg"]),
    ]
}

# Sidebar Navigation
st.sidebar.title("🔬 STEM Lab Portal")
section = st.sidebar.radio("Navigation", list(CATEGORIES.keys()) + ["📊 View All Uploaded Records"])

if section != "📊 View All Uploaded Records":
    st.header(f"📁 {section}")
    st.write("Specific format ke files upload karein aur manage karein:")

    items = CATEGORIES[section]

    for sno, title, formats in items:
        with st.expander(f"**#{sno}. {title}** (Allowed: `.{', .'.join(formats)}`)", expanded=False):
            rec_folder = os.path.join(UPLOAD_DIR, f"{sno}_{title.replace(' ', '_').replace('/', '_')}")
            os.makedirs(rec_folder, exist_ok=True)

            uploaded_files = st.file_uploader(
                f"Upload for #{sno} {title}",
                type=formats,
                accept_multiple_files=True,
                key=f"uploader_{sno}"
            )

            if uploaded_files:
                for file in uploaded_files:
                    file_path = os.path.join(rec_folder, file.name)
                    with open(file_path, "wb") as f:
                        f.write(file.getbuffer())
                st.success(f"{len(uploaded_files)} file(s) successfully saved!")

            # Show existing files
            saved_files = os.listdir(rec_folder)
            if saved_files:
                st.markdown("**Saved Files:**")
                for f_name in saved_files:
                    f_path = os.path.join(rec_folder, f_name)
                    col_a, col_b = st.columns([4, 1])
                    with col_a:
                        st.text(f"📄 {f_name}")
                    with col_b:
                        with open(f_path, "rb") as cur_f:
                            st.download_button(
                                label="Download",
                                data=cur_f.read(),
                                file_name=f_name,
                                key=f"dl_{sno}_{f_name}"
                            )
            else:
                st.info("Abhi tak koi document upload nahi kiya gaya.")

else:
    st.header("📊 STEM Lab Records Overview & Status")

    total_records = 50
    uploaded_counts = 0
    table_data = []

    for sec_name, items in CATEGORIES.items():
        for sno, title, formats in items:
            rec_folder = os.path.join(UPLOAD_DIR, f"{sno}_{title.replace(' ', '_').replace('/', '_')}")
            files = os.listdir(rec_folder) if os.path.exists(rec_folder) else []
            count = len(files)
            if count > 0:
                uploaded_counts += 1
                status = f"✅ Uploaded ({count} files)"
            else:
                status = "❌ Pending"

            table_data.append({
                "S.No.": sno,
                "Record Name": title,
                "Section": sec_name,
                "Allowed Formats": ", ".join(formats).upper(),
                "Status": status
            })

    col1, col2 = st.columns(2)
    col1.metric("Total Parameters", total_records)
    col2.metric("Completed / Uploaded", f"{uploaded_counts} / {total_records}")

    st.dataframe(table_data, use_container_width=True)