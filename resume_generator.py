from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from io import BytesIO

def generate_resume_pdf(resume_data):
    """
    Generate FREE PDF resume from resume data
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer, 
        pagesize=letter, 
        topMargin=0.5*inch,
        bottomMargin=0.5*inch,
        leftMargin=0.5*inch,
        rightMargin=0.5*inch
    )
    
    # Get styles
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=22,
        spaceAfter=12,
        textColor=colors.darkblue,
        alignment=1,  # Center alignment
        fontName='Helvetica-Bold'
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        spaceAfter=6,
        spaceBefore=12,
        textColor=colors.darkblue,
        fontName='Helvetica-Bold',
        borderWidth=1,
        borderColor=colors.darkblue,
        borderPadding=3
    )
    
    contact_style = ParagraphStyle(
        'ContactStyle',
        parent=styles['Normal'],
        fontSize=10,
        alignment=1,  # Center alignment
        spaceAfter=12
    )
    
    # Build resume content
    story = []
    
    # Header with personal info
    personal_info = resume_data['personal_info']
    story.append(Paragraph(personal_info['name'], title_style))
    
    # Contact information
    contact_parts = [personal_info['email'], personal_info['phone']]
    if personal_info.get('location'):
        contact_parts.append(personal_info['location'])
    if personal_info.get('linkedin'):
        contact_parts.append(personal_info['linkedin'])
    if personal_info.get('github'):
        contact_parts.append(personal_info['github'])
    
    contact_info = " | ".join(contact_parts)
    story.append(Paragraph(contact_info, contact_style))
    
    # Professional Summary
    story.append(Paragraph("PROFESSIONAL SUMMARY", heading_style))
    story.append(Paragraph(resume_data['summary'], styles['Normal']))
    story.append(Spacer(1, 12))
    
    # Work Experience
    story.append(Paragraph("WORK EXPERIENCE", heading_style))
    for exp in resume_data['experiences']:
        if not exp['title'] or not exp['company']:
            continue
            
        # Job title and company
        job_header = f"<b>{exp['title']}</b> | {exp['company']}"
        if exp.get('start_date') and exp.get('end_date'):
            job_header += f" | {exp['start_date']} - {exp['end_date']}"
        
        story.append(Paragraph(job_header, styles['Normal']))
        
        # Job description
        description = exp.get('enhanced_description', exp['description'])
        if description:
            # Handle bullet points
            if '•' in description:
                story.append(Paragraph(description, styles['Normal']))
            else:
                # Add bullet points if not present
                lines = description.split('\n')
                for line in lines:
                    if line.strip():
                        story.append(Paragraph(f"• {line.strip()}", styles['Normal']))
        
        story.append(Spacer(1, 8))
    
    # Education
    story.append(Paragraph("EDUCATION", heading_style))
    education = resume_data['education']
    edu_text = f"<b>{education['degree']}</b>"
    if education.get('university'):
        edu_text += f" | {education['university']}"
    if education.get('graduation_year'):
        edu_text += f" | {education['graduation_year']}"
    if education.get('gpa'):
        edu_text += f" | {education['gpa']}"
    
    story.append(Paragraph(edu_text, styles['Normal']))
    story.append(Spacer(1, 12))
    
    # Skills
    story.append(Paragraph("SKILLS", heading_style))
    story.append(Paragraph(resume_data['skills'], styles['Normal']))
    
    # Build PDF
    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()
