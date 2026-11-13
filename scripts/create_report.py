from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, Preformatted, KeepTogether
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.colors import HexColor
from reportlab.graphics.shapes import Drawing, Rect, String, Line
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / 'Project_Report_Campusly.pdf'
PURPLE = HexColor('#7558D5'); INK = HexColor('#29283F'); MUTED = HexColor('#77768B'); PALE = HexColor('#F3F0FB'); LINE = HexColor('#E8E6EF')

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name='CoverTitle', parent=styles['Title'], fontName='Helvetica-Bold', fontSize=30, leading=36, textColor=INK, alignment=TA_LEFT, spaceAfter=8))
styles.add(ParagraphStyle(name='CoverSub', parent=styles['Normal'], fontName='Helvetica', fontSize=14, leading=21, textColor=MUTED, spaceAfter=12))
styles.add(ParagraphStyle(name='H1x', parent=styles['Heading1'], fontName='Helvetica-Bold', fontSize=19, leading=24, textColor=INK, spaceBefore=3, spaceAfter=12))
styles.add(ParagraphStyle(name='H2x', parent=styles['Heading2'], fontName='Helvetica-Bold', fontSize=12, leading=16, textColor=PURPLE, spaceBefore=10, spaceAfter=5))
styles.add(ParagraphStyle(name='Bodyx', parent=styles['BodyText'], fontName='Helvetica', fontSize=9.5, leading=15, textColor=HexColor('#45445A'), spaceAfter=8))
styles.add(ParagraphStyle(name='Smallx', parent=styles['BodyText'], fontName='Helvetica', fontSize=8, leading=12, textColor=MUTED, spaceAfter=5))
styles.add(ParagraphStyle(name='Captionx', parent=styles['BodyText'], fontName='Helvetica-Oblique', fontSize=8, leading=11, textColor=MUTED, alignment=TA_CENTER, spaceBefore=4, spaceAfter=7))
styles.add(ParagraphStyle(name='Codex', parent=styles['Code'], fontName='Courier', fontSize=7.4, leading=10, textColor=HexColor('#48445E'), backColor=HexColor('#F7F6FA'), borderColor=LINE, borderWidth=.5, borderPadding=9, leftIndent=3, rightIndent=3, spaceBefore=3, spaceAfter=9))

def footer(canvas, doc):
    canvas.saveState(); w,h=letter
    if doc.page > 1:
        canvas.setStrokeColor(LINE); canvas.setLineWidth(.5); canvas.line(.7*inch,.62*inch,w-.7*inch,.62*inch)
        canvas.setFont('Helvetica',8); canvas.setFillColor(MUTED)
        canvas.drawString(.72*inch,.43*inch,'CSCI426  |  Campusly Student Portal')
        canvas.drawRightString(w-.72*inch,.43*inch,f'{doc.page}')
    canvas.restoreState()

def p(text, style='Bodyx'): return Paragraph(text, styles[style])

doc = SimpleDocTemplate(str(OUT), pagesize=letter, rightMargin=.78*inch, leftMargin=.78*inch, topMargin=.72*inch, bottomMargin=.82*inch, title='Campusly Student Portal Project Report', author='CSCI426 Student Project')
story=[]
# Cover
story += [Spacer(1,.55*inch), p('PROJECT REPORT  /  PHASE 1','Smallx'), Spacer(1,.25*inch), p('Campusly Student Portal','CoverTitle'), p('A responsive web application for student courses, grades, and academic life.','CoverSub'), Spacer(1,.3*inch)]
d=Drawing(440,115)
d.add(Rect(0,0,440,115,rx=12,ry=12,fillColor=PALE,strokeColor=LINE,strokeWidth=1))
for x,label,val in [(28,'COURSES','04'),(140,'CURRENT GPA','3.72'),(252,'ATTENDANCE','94%'),(364,'CREDITS','13')]:
    d.add(String(x,79,label,fontName='Helvetica-Bold',fontSize=8,fillColor=MUTED)); d.add(String(x,42,val,fontName='Helvetica-Bold',fontSize=22,fillColor=INK))
    if x>28: d.add(Line(x-17,22,x-17,94,strokeColor=LINE,strokeWidth=1))
story += [d, Spacer(1,.12*inch), p('Illustrative dashboard metrics from the prototype; all records are fictional sample data.','Captionx'), Spacer(1,.4*inch)]
meta=[['Department','Computer Science and Information Technology'],['Course','CSCI426: Advanced Web Programming'],['Prepared by','[Student name(s)]'],['Instructor','[Instructor name]'],['Submission date','[Insert date]']]
t=Table([[p(f'<b>{a}</b>','Smallx'),p(b,'Bodyx')] for a,b in meta],colWidths=[1.25*inch,5.0*inch],hAlign='LEFT')
t.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('LINEBELOW',(0,0),(-1,-2),.45,LINE),('LEFTPADDING',(0,0),(-1,-1),5),('RIGHTPADDING',(0,0),(-1,-1),8),('TOPPADDING',(0,0),(-1,-1),8),('BOTTOMPADDING',(0,0),(-1,-1),3)]))
story += [t, Spacer(1,.32*inch), p('Project type: Student portal prototype','Smallx'), PageBreak()]
# Abstract + objectives
story += [p('Abstract','H1x'), p('Campusly is a responsive student portal prototype developed for CSCI426 Advanced Web Programming. It addresses a familiar student need: keeping course information, academic progress, weekly classes, and assignment reminders in one easy-to-scan interface. The application is built with React and provides eight connected pages: dashboard, courses, grades, schedule, profile, about, features, and contact. The main interactions include page navigation, a responsive weekly timetable, a checklist that can be toggled, and a contact form that displays local submission feedback.','Bodyx'), p('This phase focuses on the frontend and user experience. Sample records are stored in JavaScript and are fictional; there is no authentication, database, or real message delivery. The prototype demonstrates how a campus service could be organized and provides a foundation for a later backend.','Bodyx'), p('Problem and objectives','H2x'), p('Students often need to check several details while moving between classes: what they are studying, when the next class starts, and which tasks are due. Campusly groups those details into a single student-focused interface. The project applies React-based frontend development, responsive design, and consistent navigation while keeping common academic actions visible.','Bodyx'), p('System design','H1x'), p('The application uses a small client-side architecture. The browser loads the React application, React Router selects a page based on the current path, reusable components render shared interface patterns, and a sample data module supplies fictional student, course, assignment, and activity records. CSS handles responsive layout and styling. Since this is a frontend-only prototype, page interactions update browser state and no data is transmitted to a server.','Bodyx')]
# Diagram
dg=Drawing(455,130)
boxes=[(5,45,100,52,'Student','Uses portal'),(125,45,105,52,'React UI','Pages + components'),(250,45,95,52,'Sample data','src/data.js'),(365,45,85,52,'Browser state','Local actions')]
for x,y,w,h,title,sub in boxes:
    dg.add(Rect(x,y,w,h,rx=8,ry=8,fillColor=PALE if title in ['React UI','Browser state'] else colors.white,strokeColor=LINE,strokeWidth=1))
    dg.add(String(x+9,y+31,title,fontName='Helvetica-Bold',fontSize=9,fillColor=INK)); dg.add(String(x+9,y+15,sub,fontName='Helvetica',fontSize=7.5,fillColor=MUTED))
for x1,x2 in [(105,125),(230,250),(345,365)]:
    dg.add(Line(x1,71,x2,71,strokeColor=PURPLE,strokeWidth=1.5)); dg.add(Line(x2-4,74,x2,71,strokeColor=PURPLE,strokeWidth=1.5)); dg.add(Line(x2-4,68,x2,71,strokeColor=PURPLE,strokeWidth=1.5))
dg.add(String(5,18,'The arrows show how interface content is assembled in the frontend prototype.',fontName='Helvetica-Oblique',fontSize=7.5,fillColor=MUTED))
story += [Spacer(1,3),dg,p('Figure 1. Frontend system overview','Captionx'), PageBreak()]
# Design
story += [p('Pages and interaction design','H1x')]
rows=[['Page','Purpose and main content'],['Dashboard','Semester snapshot, course progress, next classes, assignment checklist, recent activity'],['My courses','Course cards with instructors, credits, meeting details, progress, and current sample grades'],['Grades','Course scores and cumulative GPA summary'],['Schedule','Weekly class timetable with responsive horizontal scrolling on narrow screens'],['My profile','Sample student identity and academic snapshot'],['About and Features','Project purpose and a readable overview of the portal tools'],['Contact','Support information and a form with client-side confirmation feedback']]
table=Table([[p(f'<b>{r[0]}</b>' if i else f'<b>{r[0]}</b>','Smallx'),p(r[1],'Smallx')] for i,r in enumerate(rows)],colWidths=[1.3*inch,4.95*inch],repeatRows=1)
table.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),PALE),('GRID',(0,0),(-1,-1),.4,LINE),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),8),('RIGHTPADDING',(0,0),(-1,-1),8),('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),4)]))
story += [table,p('Responsive design','H2x'),p('The interface uses a fixed sidebar on wider screens and a slide-in navigation menu on smaller screens. Dashboard cards and course grids collapse into fewer columns as the viewport narrows. The weekly calendar can scroll horizontally on a phone so the day columns remain legible. Buttons, labels, and status styles share consistent color and spacing choices.','Bodyx'),p('Technologies used','H1x'),p('<b>React</b> structures the interface as components and manages small local interactions. <b>React Router</b> connects the required pages. <b>Vite</b> provides local development and production builds. <b>CSS</b> implements the visual system and responsive breakpoints. <b>Lucide React</b> supplies interface icons. <b>Git</b> records the development history.','Bodyx'),p('Key implementation snippets','H1x'),p('1. Client-side page routing','H2x'),Preformatted("<Routes>\n  <Route path=\"/\" element={<Dashboard />} />\n  <Route path=\"/courses\" element={<Courses />} />\n  <Route path=\"/grades\" element={<Grades />} />\n  <Route path=\"/schedule\" element={<Schedule />} />\n  <Route path=\"/profile\" element={<Profile />} />\n</Routes>",styles['Codex'])]
story += [PageBreak(),p('Implementation and delivery','H1x'),p('2. Data-driven course component','H2x'),Preformatted("function CourseRow({ course }) {\n  const Icon = iconMap[course.icon] || BookOpen;\n  return (\n    <NavLink to=\"/courses\" className=\"course-row\">\n      <span className={`course-icon ${course.color}`}><Icon /></span>\n      <div><strong>{course.title}</strong><small>{course.id} · {course.instructor}</small></div>\n      <span className=\"course-grade\">{course.grade}</span>\n    </NavLink>\n  );\n}",styles['Codex']),p('3. Responsive layout rule','H2x'),Preformatted(".stats-grid {\n  display: grid;\n  grid-template-columns: repeat(4, minmax(0, 1fr));\n}\n@media (max-width: 600px) {\n  .stats-grid { grid-template-columns: repeat(2, 1fr); }\n  .dashboard-grid { grid-template-columns: 1fr; }\n}",styles['Codex']),p('Running the project','H2x'),p('Install Node.js 20 or newer, clone the repository, run <b>npm install</b>, then use <b>npm run dev</b> to start the local development server. Use <b>npm run build</b> to create the production site in the <b>dist</b> folder. The README contains the current setup and deployment notes.','Bodyx'),p('Version control and deployment','H2x'),p('The source repository should be maintained with Git commits that describe meaningful project milestones. The current project copy includes its initial setup commit; students should continue the history as they customize the portal. A student-owned GitHub repository and Vercel, Netlify, or GitHub Pages deployment are still required for the final course submission. Add the actual links below after publishing.','Bodyx')]
links=Table([[p('<b>GitHub repository</b>','Smallx'),p('[Add repository URL]','Smallx')],[p('<b>Live website</b>','Smallx'),p('[Add deployment URL]','Smallx')]],colWidths=[1.35*inch,4.9*inch])
links.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),HexColor('#FAF9FC')),('BOX',(0,0),(-1,-1),.5,LINE),('INNERGRID',(0,0),(-1,-1),.4,LINE),('VALIGN',(0,0),(-1,-1),'MIDDLE'),('LEFTPADDING',(0,0),(-1,-1),8),('TOPPADDING',(0,0),(-1,-1),8),('BOTTOMPADDING',(0,0),(-1,-1),5)]))
story += [links,Spacer(1,8),p('Limitations and next steps','H2x'),p('The prototype currently has no login, backend API, persistent database, administrator tools, real email delivery, or production deployment. A next phase could add authentication, connect course and grade records to a secure API, save checklist changes, and validate accessibility with students. Real student data should only be added in a properly authorized and protected system.','Bodyx')]
contrib=Table([[p('<b>Group member</b>','Smallx'),p('<b>Contribution</b>','Smallx')],[p('[Name]','Smallx'),p('[Describe actual design, development, documentation, or presentation work]','Smallx')],[p('[Name]','Smallx'),p('[Describe actual contribution, or remove this row if not applicable]','Smallx')]],colWidths=[1.55*inch,4.7*inch],rowHeights=[.32*inch,.55*inch,.55*inch])
contrib.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),PALE),('GRID',(0,0),(-1,-1),.4,LINE),('VALIGN',(0,0),(-1,-1),'MIDDLE'),('LEFTPADDING',(0,0),(-1,-1),8),('RIGHTPADDING',(0,0),(-1,-1),8)]))
story += [KeepTogether([p('Group contribution statement and final checks','H1x'),p('Complete this section with the actual group members and their work. Do not claim contributions that were not made.','Smallx'),contrib]),Spacer(1,12),p('Before submission','H2x'),p('[ ] Replace student and instructor details with the approved project information.<br/>[ ] Add real group members and accurate contribution descriptions.<br/>[ ] Capture desktop and mobile screenshots from the final running app.<br/>[ ] Add the GitHub repository and public deployment links.<br/>[ ] Check that the report, README, and deployed interface describe the same final version.','Bodyx'),p('All profile and academic records in the current prototype are demonstration data. Replace them only with information you have permission to publish.','Smallx')]

doc.build(story,onFirstPage=footer,onLaterPages=footer)
print(OUT)
