# import streamlit as st
# import google.generativeai as genai
# import json

# # --- CONFIGURATION ---
# # Note: Ensure your API key is kept secure
# API_KEY = "AIzaSyBXvRzp8YPRonQBqnp7CilyObl1VT6FuuM"
# genai.configure(api_key=API_KEY)

# def generate_curriculum(skill, level, semesters, weekly_hours, industry):
#     """Generates curriculum data using the current Gemini Flash model."""
#     # Updated model name to resolve 404 error
#     model = genai.GenerativeModel("gemini-2.5-flash") 
    
#     prompt = f"""
#     Act as an expert academic curriculum designer. Create a detailed {semesters}-semester 
#     curriculum for learning {skill} at a {level} level. 
#     The focus should be on {industry} industry relevance with {weekly_hours} hours of study per week.
    
#     Return the response strictly as a JSON object with this structure:
#     {{
#         "skill": "{skill}",
#         "level": "{level}",
#         "semesters": [
#             {{
#                 "semester_number": 1,
#                 "courses": [
#                     {{"name": "Course Name", "topics": ["Topic 1", "Topic 2"], "credits": 4}}
#                 ]
#             }}
#         ],
#         "capstone_project": "Description of final project"
#     }}
#     """
    
#     try:
#         response = model.generate_content(prompt)
#         # Robust JSON cleaning
#         text = response.text
#         if "```json" in text:
#             json_text = text.split("```json")[1].split("```")[0].strip()
#         elif "```" in text:
#             json_text = text.split("```")[1].split("```")[0].strip()
#         else:
#             json_text = text.strip()
            
#         return json.loads(json_text)
#     except Exception as e:
#         return {"error": str(e)}

# # --- STREAMLIT UI ---
# st.set_page_config(page_title="CurrHub: GenAI Curriculum Generator", layout="wide")

# st.title("🎓 CurrHub: AI Curriculum Generator")
# st.markdown("Transform skills into a structured semester-wise syllabus instantly.")

# with st.sidebar:
#     st.header("Curriculum Parameters")
#     skill = st.text_input("Skill/Technology", "Machine Learning", placeholder="e.g., Machine Learning")
#     level = st.selectbox("Education Level", ["Diploma", "BTech", "Master's Degree", "Certification"])
#     semesters = st.slider("Number of Semesters", 1, 8, 4)
#     weekly_hours = st.text_input("Weekly Hours", value="20-25")
#     industry = st.text_input("Industry Focus", "AI", placeholder="e.g., AI R&D, Web Dev")
    
#     generate_btn = st.button("Generate Curriculum", type="primary")

# if generate_btn:
#     if not skill or not API_KEY:
#         st.error("Please provide both a skill and your Google AI Studio API Key.")
#     else:
#         with st.spinner("Designing your curriculum with Gemini AI..."):
#             data = generate_curriculum(skill, level, semesters, weekly_hours, industry)
            
#             if "error" in data:
#                 st.error(f"Error: {data['error']}")
#                 st.info("Tip: Check if your API Key is correct and has access to gemini-1.5-flash.")
#             else:
#                 st.success(f"Curriculum for {skill} Generated!")
                
#                 # Display Results
#                 for sem in data.get('semesters', []):
#                     with st.expander(f"📅 Semester {sem['semester_number']}"):
#                         for course in sem.get('courses', []):
#                             st.subheader(course['name'])
#                             st.write(f"**Credits:** {course.get('credits', 4)}")
#                             st.write("**Topics:**")
#                             st.write(", ".join(course['topics']))
#                             st.divider()
                
#                 st.info(f"🚀 **Capstone Project:** {data.get('capstone_project', 'Not specified')}")
                
#                 # Export options
#                 st.download_button(
#                     label="Download JSON Syllabus",
#                     data=json.dumps(data, indent=4),
#                     file_name=f"{skill}_curriculum.json",
#                     mime="application/json"
#                 )



#2nd edition


# import streamlit as st
# import google.generativeai as genai
# import json
# from io import BytesIO
# from reportlab.lib.pagesizes import letter
# from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
# from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
# from reportlab.lib import colors

# # --- CONFIGURATION ---
# # Using the standard model name for 2026 stability
# API_KEY = "AIzaSyBXvRzp8YPRonQBqnp7CilyObl1VT6FuuM"
# genai.configure(api_key=API_KEY)

# def generate_curriculum(skill, level, semesters, weekly_hours, industry):
#     """Generates curriculum data using a supported 2026 Gemini model."""
#     # Corrected model ID to resolve 404 error
#     model = genai.GenerativeModel("gemini-3-flash-preview")
    
#     prompt = f"""
#     Act as an expert curriculum designer. Create a {semesters}-semester 
#     curriculum for {skill} at a {level} level for the {industry} industry. 
#     Weekly load: {weekly_hours} hours.
    
#     Return ONLY a JSON object:
#     {{
#         "skill": "{skill}",
#         "level": "{level}",
#         "semesters": [
#             {{
#                 "semester_number": 1,
#                 "courses": [
#                     {{"name": "Course Name", "code": "CS101", "topics": ["Topic A", "Topic B"], "credits": 4}}
#                 ]
#             }}
#         ],
#         "capstone_project": "Description"
#     }}
#     """
#     try:
#         response = model.generate_content(prompt)
#         # Clean markdown if present
#         json_text = response.text.strip().replace('```json', '').replace('```', '')
#         return json.loads(json_text)
#     except Exception as e:
#         return {"error": str(e)}

# def create_pdf(data):
#     """Generates a professional PDF using ReportLab logic."""
#     buffer = BytesIO()
#     doc = SimpleDocTemplate(buffer, pagesize=letter)
#     styles = getSampleStyleSheet()
#     story = []

#     # Styled Title [cite: 103, 393]
#     title_style = ParagraphStyle('Title', fontSize=22, textColor=colors.HexColor("#2E5B9A"), spaceAfter=12, alignment=1)
#     story.append(Paragraph(f"{data['skill'].upper()} LEARNING PLAN", title_style))
    
#     # Metadata Row [cite: 414]
#     meta = f"<b>Level:</b> {data['level']} | <b>Industry:</b> {data.get('industry', 'N/A')} | <b>Capstone:</b> {data['capstone_project']}"
#     story.append(Paragraph(meta, styles["Normal"]))
#     story.append(Spacer(1, 20))

#     # Semester Tables [cite: 103, 929]
#     for sem in data['semesters']:
#         story.append(Paragraph(f"Semester {sem['semester_number']}", styles["Heading3"]))
#         table_data = [["Code", "Course Name", "Cr", "Key Topics"]]
        
#         for course in sem['courses']:
#             topics = ", ".join(course['topics'][:4])
#             table_data.append([course['code'], course['name'], str(course['credits']), topics])
        
#         t = Table(table_data, colWidths=[50, 160, 30, 220])
#         t.setStyle(TableStyle([
#             ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
#             ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
#             ('FONTSIZE', (0,0), (-1,-1), 9),
#             ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
#         ]))
#         story.append(t)
#         story.append(Spacer(1, 15))

#     doc.build(story)
#     buffer.seek(0)
#     return buffer

# # --- STREAMLIT UI ---
# st.set_page_config(page_title="CurrHub AI", page_icon="🎓")
# st.title("🎓 CurrHub: AI Curriculum Generator")

# with st.sidebar:
#     st.header("Project Settings")
#     skill_input = st.text_input("Skill", "Full Stack Development")
#     level_input = st.selectbox("Level", ["Diploma", "BTech", "Masters", "Certification"])
#     sem_count = st.slider("Duration (Semesters)", 1, 8, 4)
#     industry_input = st.text_input("Industry", "Web Tech")
#     hours_input = st.text_input("Weekly Hours", "25")
#     generate_btn = st.button("Generate Syllabus", type="primary")

# if generate_btn:
#     with st.spinner("AI is architecting your curriculum..."):
#         data = generate_curriculum(skill_input, level_input, sem_count, hours_input, industry_input)
        
#         if "error" in data:
#             if "429" in data["error"]:
#                 st.error("Quota exceeded. Please wait 60 seconds and try again.")
#             else:
#                 st.error(f"Error: {data['error']}")
#         else:
#             st.success("Curriculum Ready!")
            
#             # PDF Generation 
#             pdf_data = create_pdf(data)
            
#             st.download_button(
#                 label="📥 Download Professional PDF",
#                 data=pdf_data,
#                 file_name=f"{skill_input.replace(' ', '_')}_Syllabus.pdf",
#                 mime="application/pdf"
#             )
            
#             # On-screen Preview [cite: 114]
#             for sem in data['semesters']:
#                 with st.expander(f"Semester {sem['semester_number']}"):
#                     for c in sem['courses']:
#                         st.markdown(f"**{c['code']}: {c['name']}** ({c['credits']} Credits)")
#                         st.write(", ".join(c['topics']))



#3rd edition



# import streamlit as st
# import google.generativeai as genai
# import json
# from io import BytesIO
# from reportlab.lib.pagesizes import letter
# from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
# from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
# from reportlab.lib import colors

# # --- CONFIGURATION ---
# # Using the most stable production model to avoid 404 errors
# API_KEY = "AIzaSyBXvRzp8YPRonQBqnp7CilyObl1VT6FuuM"
# genai.configure(api_key=API_KEY)

# def generate_curriculum(skill, level, semesters, weekly_hours, industry):
#     """Generates curriculum data using the stable Gemini 1.5 Flash model."""
#     model = genai.GenerativeModel("gemini-2.5-flash")
    
#     prompt = f"""
#     Act as an expert academic curriculum designer. Create a {semesters}-semester 
#     curriculum for {skill} at a {level} level for the {industry} industry. 
    
#     Return ONLY a JSON object with this exact structure:
#     {{
#         "skill": "{skill}",
#         "level": "{level}",
#         "semesters": [
#             {{
#                 "semester_number": 1,
#                 "courses": [
#                     {{"name": "Course Name", "code": "CODE101", "topics": ["Topic A", "Topic B"], "credits": 4}}
#                 ]
#             }}
#         ],
#         "capstone_project": "Description of the final project"
#     }}
#     """
#     try:
#         response = model.generate_content(prompt)
#         json_text = response.text.strip().replace('```json', '').replace('```', '')
#         return json.loads(json_text)
#     except Exception as e:
#         return {"error": str(e)}

# def create_pdf(data):
#     """Generates a professional PDF with proper text wrapping and styling."""
#     buffer = BytesIO()
#     doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
#     styles = getSampleStyleSheet()
#     story = []

#     # Custom Styles for better structure
#     title_style = ParagraphStyle('Title', fontSize=22, textColor=colors.HexColor("#1F4E79"), alignment=1, spaceAfter=20)
#     cell_text_style = ParagraphStyle('CellText', fontSize=9, leading=11)
    
#     # Title and Metadata
#     story.append(Paragraph(f"{data['skill'].upper()} SYLLABUS", title_style))
#     story.append(Paragraph(f"<b>Level:</b> {data['level']} | <b>Industry:</b> {data.get('industry', 'General')}", styles["Normal"]))
#     story.append(Spacer(1, 20))

#     # Semester Tables
#     for sem in data['semesters']:
#         story.append(Paragraph(f"Semester {sem['semester_number']}", styles["Heading3"]))
        
#         # Headers with Paragraphs to enable wrapping
#         table_data = [[
#             Paragraph("<b>Code</b>", cell_text_style), 
#             Paragraph("<b>Course Name</b>", cell_text_style), 
#             Paragraph("<b>Cr</b>", cell_text_style), 
#             Paragraph("<b>Topics</b>", cell_text_style)
#         ]]
        
#         for course in sem['courses']:
#             # Bullet point formatting for topics
#             topics_formatted = "<br/>• " + "<br/>• ".join(course['topics'])
#             table_data.append([
#                 Paragraph(course['code'], cell_text_style),
#                 Paragraph(course['name'], cell_text_style),
#                 Paragraph(str(course['credits']), cell_text_style),
#                 Paragraph(topics_formatted, cell_text_style)
#             ])
        
#         # Adjusted Column Widths to prioritize the "Topics" section
#         t = Table(table_data, colWidths=[50, 140, 30, 310])
#         t.setStyle(TableStyle([
#             ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#D6EAF8")),
#             ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
#             ('VALIGN', (0,0), (-1,-1), 'TOP'),
#             ('LEFTPADDING', (0,0), (-1,-1), 5),
#             ('RIGHTPADDING', (0,0), (-1,-1), 5),
#             ('TOPPADDING', (0,0), (-1,-1), 5),
#             ('BOTTOMPADDING', (0,0), (-1,-1), 5),
#         ]))
#         story.append(t)
#         story.append(Spacer(1, 15))

#     story.append(Spacer(1, 10))
#     story.append(Paragraph("<b>Capstone Project:</b>", styles["Normal"]))
#     story.append(Paragraph(data['capstone_project'], styles["Normal"]))

#     doc.build(story)
#     buffer.seek(0)
#     return buffer

# # --- STREAMLIT UI ---
# st.set_page_config(page_title="AI Curriculum Generator", layout="wide")
# st.title("🎓 AI Curriculum Generator")

# with st.sidebar:
#     st.header("Syllabus Settings")
#     skill_in = st.text_input("Skill", "Full Stack Development")
#     level_in = st.selectbox("Level", ["Diploma", "BTech", "Masters", "Certification"])
#     sem_in = st.slider("Semesters", 1, 8, 4)
#     ind_in = st.text_input("Industry", "Web Tech")
#     gen_btn = st.button("Generate & Download PDF", type="primary")

# if gen_btn:
#     with st.spinner("Designing curriculum..."):
#         data = generate_curriculum(skill_in, level_in, sem_in, "20", ind_in)
        
#         if "error" in data:
#             if "429" in data["error"]:
#                 st.error("Quota full. Please wait 60 seconds and try again.")
#             else:
#                 st.error(f"Error: {data['error']}")
#         else:
#             st.success("Generation Complete!")
#             pdf_data = create_pdf(data)
#             st.download_button(
#                 label="📥 Download Professional Syllabus (PDF)",
#                 data=pdf_data,
#                 file_name=f"{skill_in}_Syllabus.pdf",
#                 mime="application/pdf"
#             )
#             st.json(data)

#4th edition


# import streamlit as st
# import google.generativeai as genai
# import json
# from io import BytesIO
# from reportlab.lib.pagesizes import letter
# from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
# from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
# from reportlab.lib import colors
# import base64

# # --- CONFIGURATION ---
# # February 2026 Stable Model ID
# API_KEY = "AIzaSyBXvRzp8YPRonQBqnp7CilyObl1VT6FuuM"
# genai.configure(api_key=API_KEY)

# def generate_curriculum(skill, level, semesters, weekly_hours, industry):
#     """Generates curriculum data using the Gemini 2.5 Flash model."""
#     model = genai.GenerativeModel("gemini-2.5-flash") 
    
#     prompt = f"""
#     Act as an expert curriculum architect. Design a {semesters}-semester 
#     syllabus for {skill} at a {level} level for the {industry} industry. 
    
#     Return ONLY a JSON object:
#     {{
#         "skill": "{skill}",
#         "level": "{level}",
#         "semesters": [
#             {{
#                 "semester_number": 1,
#                 "courses": [
#                     {{"name": "Course Name", "code": "CODE101", "topics": ["Topic 1", "Topic 2"], "credits": 4}}
#                 ]
#             }}
#         ],
#         "capstone_project": "Detailed final project requirements."
#     }}
#     """
#     try:
#         response = model.generate_content(prompt)
#         json_text = response.text.strip().replace('```json', '').replace('```', '')
#         return json.loads(json_text)
#     except Exception as e:
#         return {"error": str(e)}

# def create_pdf(data):
#     """Generates a professional, accreditation-ready PDF document."""
#     buffer = BytesIO()
#     doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
#     styles = getSampleStyleSheet()
#     story = []

#     # Custom Academic Styles
#     title_style = ParagraphStyle('Title', fontSize=24, textColor=colors.HexColor("#1F4E79"), alignment=1, spaceAfter=20, fontName="Helvetica-Bold")
#     cell_style = ParagraphStyle('Cell', fontSize=9, leading=11)
#     header_style = ParagraphStyle('Header', fontSize=14, textColor=colors.HexColor("#2E5B9A"), spaceBefore=12, spaceAfter=8, fontName="Helvetica-Bold")

#     # Document Title & Metadata
#     story.append(Paragraph(f"{data['skill'].upper()} SYLLABUS", title_style))
#     meta = f"<b>Level:</b> {data['level']} | <b>Industry:</b> {data.get('industry', 'N/A')} | <b>Duration:</b> {len(data['semesters'])} Semesters"
#     story.append(Paragraph(meta, styles["Normal"]))
#     story.append(Spacer(1, 20))

#     # Semester Tables
#     for sem in data['semesters']:
#         story.append(Paragraph(f"Semester {sem['semester_number']}", header_style))
        
#         table_data = [[
#             Paragraph("<b>Code</b>", cell_style), 
#             Paragraph("<b>Course Name</b>", cell_style), 
#             Paragraph("<b>Credits</b>", cell_style), 
#             Paragraph("<b>Learning Outcomes/Topics</b>", cell_style)
#         ]]
        
#         for course in sem['courses']:
#             topics = "• " + "<br/>• ".join(course['topics'])
#             table_data.append([
#                 Paragraph(course['code'], cell_style),
#                 Paragraph(course['name'], cell_style),
#                 Paragraph(str(course['credits']), cell_style),
#                 Paragraph(topics, cell_style)
#             ])
        
#         # Table Layout: 50pt Code, 140pt Name, 40pt Cr, 300pt Topics
#         t = Table(table_data, colWidths=[50, 140, 50, 300])
#         t.setStyle(TableStyle([
#             ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#D4E6F1")),
#             ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
#             ('VALIGN', (0,0), (-1,-1), 'TOP'),
#             ('BOTTOMPADDING', (0,0), (-1,-1), 6),
#             ('TOPPADDING', (0,0), (-1,-1), 6),
#         ]))
#         story.append(t)
#         story.append(Spacer(1, 15))

#     # Capstone Section
#     story.append(Spacer(1, 10))
#     story.append(Paragraph("Capstone Project Requirements", header_style))
#     story.append(Paragraph(data['capstone_project'], styles["Normal"]))

#     doc.build(story)
#     buffer.seek(0)
#     return buffer

# # --- STREAMLIT UI ---
# st.set_page_config(page_title="CurrHub AI", page_icon="🎓")
# st.title("🎓 CurrHub: AI Syllabus Architect")
# st.markdown("Use this tool to generate industry-ready PDF curricula for any technical skill.")

# with st.sidebar:
#     st.header("Settings")
#     skill_in = st.text_input("Skillset", "Full Stack Development")
#     level_in = st.selectbox("Level", ["Diploma", "BTech", "Masters", "Certification"])
#     sem_in = st.slider("Duration (Semesters)", 1, 8, 4)
#     ind_in = st.text_input("Industry Target", "FinTech / SaaS")
#     generate_btn = st.button("Generate & Prepare PDF", type="primary")

# if generate_btn:
#     with st.spinner("AI is designing your curriculum..."):
#         # The prompt is handled behind the scenes; the user only sees the success state and download
#         data = generate_curriculum(skill_in, level_in, sem_in, "20", ind_in)
        
#         if "error" in data:
#             st.error(f"Error: {data['error']}")
#         else:
#             st.success("Curriculum Architected Successfully!")
            
#             # Generate the professional PDF
#             pdf_data = create_pdf(data)
            
#             # Show download button prominently
#             st.download_button(
#                 label="📄 Download Professional Syllabus (PDF)",
#                 data=pdf_data,
#                 file_name=f"{skill_in.replace(' ', '_')}_Syllabus.pdf",
#                 mime="application/pdf"
#             )
            
#             # Show a clean visual summary instead of raw JSON
#             st.info("The generated syllabus has been formatted into a publication-ready PDF. Click the button above to download.")
#             st.subheader("📄 PDF Preview")
#             base64_pdf = base64.b64encode(st.session_state.pdf_bytes).decode('utf-8')
#             pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="1000" type="application/pdf"></iframe>'
#             st.markdown(pdf_display, unsafe_allow_html=True)
            

#5th edition



# import streamlit as st
# import google.generativeai as genai
# import json
# import base64
# from io import BytesIO
# from reportlab.lib.pagesizes import letter
# from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
# from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
# from reportlab.lib import colors

# # --- CONFIGURATION ---
# API_KEY = "AIzaSyBXvRzp8YPRonQBqnp7CilyObl1VT6FuuM"
# genai.configure(api_key=API_KEY)

# # --- SESSION STATE ---
# # This prevents the app from refreshing/losing data after download
# if 'curriculum' not in st.session_state:
#     st.session_state.curriculum = None
# if 'pdf_bytes' not in st.session_state:
#     st.session_state.pdf_bytes = None

# def generate_curriculum(skill, level, semesters, industry):
#     model = genai.GenerativeModel("gemini-2.5-flash") 
#     # Strict prompt to prevent KeyError
#     prompt = f"""
#     Create a {semesters}-semester syllabus for {skill} at {level} level for {industry}.
#     Return ONLY a JSON object with keys: "skill", "level", "semesters", "capstone_project".
#     Each semester must have "semester_number" and "courses" (name, code, credits, topics).
#     """
#     try:
#         response = model.generate_content(prompt)
#         json_text = response.text.strip().replace('```json', '').replace('```', '')
#         return json.loads(json_text)
#     except Exception as e:
#         return {"error": str(e)}

# def create_pdf(data):
#     buffer = BytesIO()
#     doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=50, leftMargin=50, topMargin=50, bottomMargin=50)
#     styles = getSampleStyleSheet()
#     story = []

#     # Safeguard against KeyError using .get()
#     skill_name = data.get('skill', 'New Curriculum').upper()
    
#     title_style = ParagraphStyle('Title', fontSize=22, textColor=colors.HexColor("#1F4E79"), alignment=1)
#     story.append(Paragraph(f"{skill_name} SYLLABUS", title_style))
#     story.append(Spacer(1, 20))

#     for sem in data.get('semesters', []):
#         story.append(Paragraph(f"Semester {sem.get('semester_number')}", styles["Heading3"]))
#         table_data = [["Code", "Course Name", "Credits", "Topics"]]
        
#         for c in sem.get('courses', []):
#             # Wrap topics in Paragraph for text wrapping
#             topics = Paragraph(", ".join(c.get('topics', [])), styles["Normal"])
#             table_data.append([c.get('code'), c.get('name'), str(c.get('credits')), topics])
        
#         t = Table(table_data, colWidths=[50, 140, 40, 300])
#         t.setStyle(TableStyle([
#             ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
#             ('BACKGROUND', (0,0), (-1,0), colors.lightblue),
#             ('VALIGN', (0,0), (-1,-1), 'TOP')
#         ]))
#         story.append(t)
#         story.append(Spacer(1, 15))

#     doc.build(story)
#     buffer.seek(0)
#     return buffer

# # --- STREAMLIT UI ---
# st.set_page_config(page_title="CurrHub AI", layout="wide")
# st.title("🎓 CurrHub: AI Syllabus Architect")

# with st.sidebar:
#     skill_input = st.text_input("Skill", "Full Stack Development")
#     level_input = st.selectbox("Level", ["Diploma", "BTech", "Masters"])
#     sem_input = st.slider("Semesters", 1, 8, 4)
#     ind_input = st.text_input("Industry", "Web Tech")
    
#     if st.button("Generate", type="primary"):
#         with st.spinner("Designing..."):
#             result = generate_curriculum(skill_input, level_input, sem_input, ind_input)
#             if "error" not in result:
#                 st.session_state.curriculum = result
#                 st.session_state.pdf_bytes = create_pdf(result).getvalue()
#             else:
#                 st.error(result["error"])

# # --- DISPLAY & PREVIEW ---
# if st.session_state.curriculum:
    
#         st.success("Generation Complete")
#         # Download button uses session state to avoid refresh
#         st.download_button(
#             label="📥 Download PDF",
#             data=st.session_state.pdf_bytes,
#             file_name=f"{skill_input}_Syllabus.pdf",
#             mime="application/pdf"
#         )

#         #with col2:
#         st.subheader("PDF Preview")
#         # Encode PDF for on-screen display
#         base64_pdf = base64.b64encode(st.session_state.pdf_bytes).decode('utf-8')
#         pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="800" type="application/pdf"></iframe>'
#         st.markdown(pdf_display, unsafe_allow_html=True)


#6th edition



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

with st.sidebar:
    st.header("Settings")
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