import streamlit as st
import os
from dotenv import load_dotenv
from ai_enhancer import enhance_content
from resume_generator import generate_resume_pdf

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Free AI Resume Builder",
    page_icon="📄",
    layout="wide"
)

def main():
    st.title("🤖 Free AI-Powered Resume Builder")
    st.markdown("Create professional, ATS-friendly resumes with **FREE** AI assistance!")
    st.info("✨ Powered by Google Gemini - Completely Free!")
    
    # Initialize session state for form data
    if 'resume_generated' not in st.session_state:
        st.session_state.resume_generated = False
        st.session_state.pdf_data = None
        st.session_state.resume_data = None
    
    # Main form
    with st.form("resume_form"):
        st.header("📝 Personal Information")
        col1, col2 = st.columns(2)
        
        with col1:
            full_name = st.text_input("Full Name*", placeholder="John Doe")
            email = st.text_input("Email*", placeholder="john.doe@email.com")
            phone = st.text_input("Phone*", placeholder="+91 98765 43210")
        
        with col2:
            linkedin = st.text_input("LinkedIn Profile", placeholder="linkedin.com/in/johndoe")
            github = st.text_input("GitHub Profile", placeholder="github.com/johndoe")
            location = st.text_input("Location", placeholder="Mumbai, Maharashtra")
        
        # Professional Summary
        st.header("💼 Professional Summary")
        summary = st.text_area(
            "Brief professional summary (AI will enhance this)*",
            placeholder="Software developer with 2 years experience in web development using React and Python...",
            height=100
        )
        
        # Work Experience
        st.header("🏢 Work Experience")
        num_jobs = st.number_input("Number of jobs to add", min_value=1, max_value=5, value=1)
        
        experiences = []
        for i in range(num_jobs):
            st.subheader(f"Job {i+1}")
            col1, col2 = st.columns(2)
            
            with col1:
                job_title = st.text_input(f"Job Title {i+1}*", key=f"job_title_{i}")
                company = st.text_input(f"Company {i+1}*", key=f"company_{i}")
            
            with col2:
                start_date = st.text_input(f"Start Date {i+1}", key=f"start_date_{i}", placeholder="Jan 2023")
                end_date = st.text_input(f"End Date {i+1}", key=f"end_date_{i}", placeholder="Present")
            
            job_description = st.text_area(
                f"Job Description {i+1} (AI will enhance this)*",
                key=f"job_desc_{i}",
                placeholder="Developed web applications, worked with team, improved processes...",
                height=100
            )
            
            experiences.append({
                "title": job_title,
                "company": company,
                "start_date": start_date,
                "end_date": end_date,
                "description": job_description
            })
        
        # Education
        st.header("🎓 Education")
        degree = st.text_input("Degree*", placeholder="Bachelor of Technology in Computer Science")
        university = st.text_input("University*", placeholder="Indian Institute of Technology")
        graduation_year = st.text_input("Graduation Year", placeholder="2022")
        gpa = st.text_input("CGPA/Percentage (optional)", placeholder="8.5/10 or 85%")
        
        # Skills
        st.header("🛠️ Skills")
        skills = st.text_area(
            "Skills (comma-separated, AI will suggest more)*",
            placeholder="Python, JavaScript, React, Node.js, MongoDB, Git, AWS",
            height=80
        )
        
        # Submit button (ONLY for processing, not downloading)
        submitted = st.form_submit_button("🚀 Generate Free AI Resume", use_container_width=True)
        
        if submitted:
            # Validation
            required_fields = [full_name, email, phone, summary, degree, university, skills]
            job_fields = [experiences[0]["title"], experiences[0]["company"], experiences[0]["description"]]
            
            if not all(required_fields + job_fields):
                st.error("❌ Please fill in all required fields marked with *")
                return
            
            # Show progress
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            try:
                # Step 1: Enhance content with AI
                status_text.text("🤖 Enhancing content with FREE AI...")
                progress_bar.progress(25)
                
                enhanced_summary = enhance_content(summary, "professional_summary")
                enhanced_experiences = []
                
                for exp in experiences:
                    if exp["description"]:
                        enhanced_desc = enhance_content(exp["description"], "job_description")
                        exp["enhanced_description"] = enhanced_desc
                        enhanced_experiences.append(exp)
                
                enhanced_skills = enhance_content(skills, "skills")
                
                # Step 2: Generate resume data
                status_text.text("📄 Generating resume...")
                progress_bar.progress(50)
                
                resume_data = {
                    "personal_info": {
                        "name": full_name,
                        "email": email,
                        "phone": phone,
                        "linkedin": linkedin,
                        "github": github,
                        "location": location
                    },
                    "summary": enhanced_summary,
                    "experiences": enhanced_experiences,
                    "education": {
                        "degree": degree,
                        "university": university,
                        "graduation_year": graduation_year,
                        "gpa": gpa
                    },
                    "skills": enhanced_skills
                }
                
                # Step 3: Generate PDF
                status_text.text("📋 Creating PDF...")
                progress_bar.progress(75)
                
                pdf_buffer = generate_resume_pdf(resume_data)
                
                # Step 4: Store in session state
                progress_bar.progress(100)
                status_text.text("✅ Resume generated successfully!")
                
                # Store data in session state
                st.session_state.resume_generated = True
                st.session_state.pdf_data = pdf_buffer
                st.session_state.resume_data = resume_data
                st.session_state.file_name = f"{full_name.replace(' ', '_')}_AI_Resume.pdf"
                
                st.success("🎉 Your FREE AI-enhanced resume is ready!")
                
            except Exception as e:
                st.error(f"❌ An error occurred: {str(e)}")
                st.info("💡 Please check your Gemini API key and try again.")
    
    # Download button OUTSIDE the form
    if st.session_state.resume_generated and st.session_state.pdf_data:
        st.download_button(
            label="📥 Download Your Free AI Resume",
            data=st.session_state.pdf_data,
            file_name=st.session_state.file_name,
            mime="application/pdf",
            use_container_width=True,
            type="primary"
        )
        
        # Show preview
        with st.expander("🔍 Preview Enhanced Content"):
            resume_data = st.session_state.resume_data
            st.subheader("✨ AI-Enhanced Professional Summary")
            st.write(resume_data["summary"])
            
            st.subheader("💼 AI-Enhanced Job Descriptions")
            for i, exp in enumerate(resume_data["experiences"]):
                st.write(f"**{exp['title']} at {exp['company']}**")
                st.write(exp.get('enhanced_description', exp['description']))
                st.write("---")
            
            st.subheader("🛠️ AI-Enhanced Skills")
            st.write(resume_data["skills"])

if __name__ == "__main__":
    main()
