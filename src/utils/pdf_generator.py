# src/utils/pdf_generator.py
import os
import tempfile
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable

def generate_medical_report_pdf(
    patient_name: str,
    email: str,
    symptoms: str,
    diagnosis,
    doctors: list,
    safety_res
) -> str:
    """
    Generates an official, formatted PDF clinical report and returns the local file path.
    """
    temp_dir = tempfile.gettempdir()
    clean_filename = f"Vaiddisha_Medical_Report_{patient_name.replace(' ', '_')}.pdf"
    file_path = os.path.join(temp_dir, clean_filename)
    
    doc = SimpleDocTemplate(
        file_path,
        pagesize=letter,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()
    
    # Palette Definition
    PRIMARY_COLOR = colors.HexColor("#0f172a")    # Slate Dark
    TEAL_COLOR = colors.HexColor("#0d9488")       # Primary Teal
    ALERT_COLOR = colors.HexColor("#ef4444")      # Emergency Red
    TEXT_COLOR = colors.HexColor("#334155")       # Body Text Slate

    # Typography Styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=20,
        textColor=PRIMARY_COLOR,
        spaceAfter=4
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        textColor=TEAL_COLOR,
        spaceAfter=15
    )

    section_heading = ParagraphStyle(
        'SectionHeading',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        textColor=PRIMARY_COLOR,
        spaceBefore=12,
        spaceAfter=6
    )

    body_style = ParagraphStyle(
        'BodyText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=TEXT_COLOR,
        spaceAfter=4
    )

    alert_style = ParagraphStyle(
        'AlertText',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=13,
        textColor=ALERT_COLOR,
        spaceAfter=4
    )

    story = []

    # 1. Header Banner
    story.append(Paragraph("🩺 VAIDDISHA AI — CLINICAL TRIAGE REPORT", title_style))
    story.append(Paragraph("Multilingual AI Clinical Decision-Support & Patient Diagnostic Summary", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=TEAL_COLOR, spaceAfter=12))

    # 2. Patient Profile & Metadata Table
    current_date = datetime.now().strftime("%B %d, %Y")
    patient_info_data = [
        [Paragraph("<b>Patient Name:</b>", body_style), Paragraph(patient_name or "Anonymous Patient", body_style),
         Paragraph("<b>Date:</b>", body_style), Paragraph(current_date, body_style)],
        [Paragraph("<b>Email:</b>", body_style), Paragraph(email or "N/A", body_style),
         Paragraph("<b>Urgency Level:</b>", body_style), Paragraph(f"<b>{diagnosis.urgency_level}</b>", body_style)]
    ]
    
    patient_table = Table(patient_info_data, colWidths=[90, 180, 80, 180])
    patient_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#f8fafc")),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#cbd5e1")),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('PADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(patient_table)
    story.append(Spacer(1, 10))

    # 3. Reported Symptoms
    story.append(Paragraph("1. Reported Symptoms & Presenting Complaints", section_heading))
    story.append(Paragraph(symptoms.strip(), body_style))
    story.append(Spacer(1, 8))

    # 4. Patient Safety & Emergency Alerts
    if not safety_res.is_safe or diagnosis.emergency_warning:
        story.append(Paragraph("⚠️ Patient Safety & Emergency Alerts", section_heading))
        if diagnosis.emergency_warning:
            story.append(Paragraph(f"<b>EMERGENCY PROTOCOL:</b> {diagnosis.emergency_warning.strip()}", alert_style))
        if not safety_res.is_safe:
            for w in safety_res.warnings:
                story.append(Paragraph(f"• <b>[{w.category}]</b> ({w.severity}): {w.message.strip()}", alert_style))
        story.append(Spacer(1, 8))

    # 5. Diagnostic Assessment Summary
    story.append(Paragraph("2. AI Clinical Assessment & Triage Summary", section_heading))
    story.append(Paragraph(diagnosis.summary.strip(), body_style))
    story.append(Paragraph(f"<b>Recommended Specialty:</b> {diagnosis.recommended_specialty.strip()}", body_style))
    story.append(Spacer(1, 8))

    # 6. Suspected Conditions Table
    story.append(Paragraph("3. Suspected Conditions & Clinical Rationale", section_heading))
    cond_table_data: list[list[str | Paragraph]] = [["Condition", "Probability", "Clinical Rationale"]]
    for cond in diagnosis.possible_conditions:
        cond_table_data.append([
            Paragraph(f"<b>{cond.name.strip()}</b>", body_style),
            Paragraph(cond.probability.strip(), body_style),
            Paragraph(cond.explanation.strip(), body_style)
        ])

    cond_table = Table(cond_table_data, colWidths=[130, 80, 320])
    cond_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), PRIMARY_COLOR),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ('PADDING', (0, 0), (-1, -1), 5),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    story.append(cond_table)
    story.append(Spacer(1, 10))

    # 7. Recommended Nearby Specialists
    story.append(Paragraph("4. Recommended Specialists Nearby", section_heading))
    if doctors:
        doc_table_data: list[list[str | Paragraph]] = [["Doctor Name", "Specialty", "Hospital / Location", "Contact & Fee"]]
        for doc_item in doctors[:3]:
            doc_table_data.append([
                Paragraph(f"Dr. {doc_item['name']}<br/><font size=7 color='#64748b'>{doc_item.get('qualification', '')}</font>", body_style),
                Paragraph(doc_item['speciality'], body_style),
                Paragraph(f"{doc_item['hospital']}, {doc_item['city']}", body_style),
                Paragraph(f"Phone: {doc_item['phone']}<br/>Fee: {doc_item['fee']}", body_style)
            ])
        doc_table = Table(doc_table_data, colWidths=[130, 110, 170, 120])
        doc_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), TEAL_COLOR),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
            ('PADDING', (0, 0), (-1, -1), 5),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ]))
        story.append(doc_table)
    else:
        story.append(Paragraph("<i>No registered local specialists found in your city. Please consult a General Practitioner.</i>", body_style))

    # 8. Footer & Legal Disclaimer
    story.append(Spacer(1, 15))
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#94a3b8"), spaceAfter=8))
    disclaimer_style = ParagraphStyle(
        'Disclaimer', 
        parent=styles['Normal'], 
        fontName='Helvetica-Oblique', 
        fontSize=7, 
        leading=10, 
        textColor=colors.HexColor("#64748b")
    )
    story.append(Paragraph("<b>LEGAL DISCLAIMER:</b> Vaiddisha AI operates solely as an informational Clinical Decision-Support Tool. This report does NOT constitute a formal medical diagnosis or prescription. Always consult a certified physician for medical treatment.", disclaimer_style))

    doc.build(story)
    return file_path