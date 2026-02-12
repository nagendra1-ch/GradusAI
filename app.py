

import streamlit as st
import google.generativeai as genai
import json
import base64
import time
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

# --- CONFIGURATION ---
API_KEY = "AIzaSyCnADQYn27JtjSpkJBjGRCF6Vjw5el5HRk"
genai.configure(api_key=API_KEY)

# Use Session State to prevent losing data and hitting quotas repeatedly
if 'curriculum' not in st.session_state:
    st.session_state.curriculum = None
if 'pdf_bytes' not in st.session_state:
    st.session_state.pdf_bytes = None

def generate_curriculum(skill, level, semesters, industry):
    """Generates curriculum using a model with higher free-tier limits."""
    # Using 1.5-flash instead of 2.5 to avoid the 20-request daily cap
    model = genai.GenerativeModel("gemini-2.5-flash") 
    
    prompt = f"""
    Design a {semesters}-semester syllabus for {skill} at a {level} level for {industry}. 
    Return ONLY a JSON object:
    {{
        "skill": "{skill}",
        "level": "{level}",
        "semesters": [
            {{
                "semester_number": 1,
                "courses": [
                    {{"name": "Course Name", "code": "CODE101", "topics": ["Topic 1", "Topic 2"], "credits": 4}}
                ]
            }}
        ],
        "capstone_project": "Detailed final project requirements."
    }}
    """
    try:
        response = model.generate_content(prompt)
        json_text = response.text.strip().replace('```json', '').replace('```', '')
        return json.loads(json_text)
    except Exception as e:
        return {"error": str(e)}

def create_pdf(data):
    """Generates the professional PDF with text wrapping."""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
    styles = getSampleStyleSheet()
    story = []

    title_style = ParagraphStyle('Title', fontSize=22, textColor=colors.HexColor("#1F4E79"), alignment=1, fontName="Helvetica-Bold")
    cell_style = ParagraphStyle('Cell', fontSize=9, leading=11)
    
    story.append(Paragraph(f"{data.get('skill', 'New').upper()} SYLLABUS", title_style))
    story.append(Spacer(1, 20))

    for sem in data.get('semesters', []):
        story.append(Paragraph(f"Semester {sem['semester_number']}", styles["Heading3"]))
        table_data = [[Paragraph("<b>Code</b>", cell_style), Paragraph("<b>Course Name</b>", cell_style), Paragraph("<b>Credits</b>", cell_style), Paragraph("<b>Topics</b>", cell_style)]]
        
        for course in sem['courses']:
            topics = "• " + "<br/>• ".join(course['topics'])
            table_data.append([Paragraph(course['code'], cell_style), Paragraph(course['name'], cell_style), Paragraph(str(course['credits']), cell_style), Paragraph(topics, cell_style)])
        
        t = Table(table_data, colWidths=[50, 140, 70, 300])
        t.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,0), colors.HexColor("#D4E6F1")), ('GRID', (0,0), (-1,-1), 0.5, colors.grey), ('VALIGN', (0,0), (-1,-1), 'TOP')]))
        story.append(t)
        story.append(Spacer(1, 15))

    doc.build(story)
    buffer.seek(0)
    return buffer

# --- STREAMLIT UI ---
st.set_page_config(page_title="CurrHub AI", layout="wide")
st.title("🎓 CurrHub: AI Syllabus Architect")
st.markdown("Transform skills into a structured semester-wise syllabus instantly.")

with st.sidebar:
    st.header("Requirements")
    skill_in = st.text_input("Skill", "Full Stack Development")
    level_in = st.selectbox("Level", ["Diploma", "BTech", "Masters"])
    sem_in = st.slider("Duration (Semesters)", 1, 8, 4)
    ind_in = st.text_input("Industry", "Web Tech")
    
    if st.button("Generate & Preview", type="primary"):
        with st.spinner("AI is designing..."):
            data = generate_curriculum(skill_in, level_in, sem_in, ind_in)
            if "error" not in data:
                st.session_state.pdf_bytes = create_pdf(data).getvalue()
                st.session_state.curriculum = data
            else:
                if "429" in data["error"]:
                    st.error("Daily Free Limit Reached! Switching to the 1.5-Flash model might help, or wait 24 hours.")
                else:
                    st.error(data["error"])

# --- PREVIEW SECTION ---
if st.session_state.pdf_bytes:
    
        st.success("Generation Complete!")
        st.download_button(label="📥 Download PDF", data=st.session_state.pdf_bytes, file_name=f"{skill_in}_Syllabus.pdf", mime="application/pdf")
        st.write(f"**Program:** {st.session_state.curriculum.get('skill')}")

        st.subheader("📄 PDF Preview")
        base64_pdf = base64.b64encode(st.session_state.pdf_bytes).decode('utf-8')
        pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="900" type="application/pdf"></iframe>'
        st.markdown(pdf_display, unsafe_allow_html=True)