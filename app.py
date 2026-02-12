import streamlit as st
import google.generativeai as genai
import json

# --- CONFIGURATION ---
# Note: Ensure your API key is kept secure
API_KEY = "AIzaSyBXvRzp8YPRonQBqnp7CilyObl1VT6FuuM"
genai.configure(api_key=API_KEY)

def generate_curriculum(skill, level, semesters, weekly_hours, industry):
    """Generates curriculum data using the current Gemini Flash model."""
    # Updated model name to resolve 404 error
    model = genai.GenerativeModel("gemini-2.5-flash") 
    
    prompt = f"""
    Act as an expert academic curriculum designer. Create a detailed {semesters}-semester 
    curriculum for learning {skill} at a {level} level. 
    The focus should be on {industry} industry relevance with {weekly_hours} hours of study per week.
    
    Return the response strictly as a JSON object with this structure:
    {{
        "skill": "{skill}",
        "level": "{level}",
        "semesters": [
            {{
                "semester_number": 1,
                "courses": [
                    {{"name": "Course Name", "topics": ["Topic 1", "Topic 2"], "credits": 4}}
                ]
            }}
        ],
        "capstone_project": "Description of final project"
    }}
    """
    
    try:
        response = model.generate_content(prompt)
        # Robust JSON cleaning
        text = response.text
        if "```json" in text:
            json_text = text.split("```json")[1].split("```")[0].strip()
        elif "```" in text:
            json_text = text.split("```")[1].split("```")[0].strip()
        else:
            json_text = text.strip()
            
        return json.loads(json_text)
    except Exception as e:
        return {"error": str(e)}

# --- STREAMLIT UI ---
st.set_page_config(page_title="CurrHub: GenAI Curriculum Generator", layout="wide")

st.title("🎓 CurrHub: AI Curriculum Generator")
st.markdown("Transform skills into a structured semester-wise syllabus instantly.")

with st.sidebar:
    st.header("Curriculum Parameters")
    skill = st.text_input("Skill/Technology", "Machine Learning", placeholder="e.g., Machine Learning")
    level = st.selectbox("Education Level", ["Diploma", "BTech", "Master's Degree", "Certification"])
    semesters = st.slider("Number of Semesters", 1, 8, 4)
    weekly_hours = st.text_input("Weekly Hours", value="20-25")
    industry = st.text_input("Industry Focus", "AI", placeholder="e.g., AI R&D, Web Dev")
    
    generate_btn = st.button("Generate Curriculum", type="primary")

if generate_btn:
    if not skill or not API_KEY:
        st.error("Please provide both a skill and your Google AI Studio API Key.")
    else:
        with st.spinner("Designing your curriculum with Gemini AI..."):
            data = generate_curriculum(skill, level, semesters, weekly_hours, industry)
            
            if "error" in data:
                st.error(f"Error: {data['error']}")
                st.info("Tip: Check if your API Key is correct and has access to gemini-1.5-flash.")
            else:
                st.success(f"Curriculum for {skill} Generated!")
                
                # Display Results
                for sem in data.get('semesters', []):
                    with st.expander(f"📅 Semester {sem['semester_number']}"):
                        for course in sem.get('courses', []):
                            st.subheader(course['name'])
                            st.write(f"**Credits:** {course.get('credits', 4)}")
                            st.write("**Topics:**")
                            st.write(", ".join(course['topics']))
                            st.divider()
                
                st.info(f"🚀 **Capstone Project:** {data.get('capstone_project', 'Not specified')}")
                
                # Export options
                st.download_button(
                    label="Download JSON Syllabus",
                    data=json.dumps(data, indent=4),
                    file_name=f"{skill}_curriculum.json",
                    mime="application/json"
                )