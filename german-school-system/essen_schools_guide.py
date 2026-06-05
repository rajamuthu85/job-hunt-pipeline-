#!/usr/bin/env python3
"""
Generate a comprehensive PDF guide about German school systems,
universities near Essen, and top Gymnasiums near Heinickestrasse.
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm, mm
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak, KeepTogether
)
from reportlab.platypus.flowables import HRFlowable
from reportlab.lib.colors import HexColor
import os

# Color palette
DARK_BLUE = HexColor('#1a3a5c')
MID_BLUE = HexColor('#2d6a9f')
LIGHT_BLUE = HexColor('#d0e8f8')
ACCENT_GOLD = HexColor('#c8a415')
LIGHT_GRAY = HexColor('#f5f5f5')
DARK_GRAY = HexColor('#444444')
WHITE = colors.white
BLACK = colors.black
GREEN = HexColor('#2e7d32')
ORANGE = HexColor('#e65100')
TABLE_HEADER = HexColor('#1a3a5c')
TABLE_ROW_ALT = HexColor('#eaf4fb')
TABLE_ROW = HexColor('#ffffff')

OUTPUT_FILE = "/home/user/job-hunt-pipeline-/Essen_German_Schools_Guide.pdf"


def build_styles():
    styles = getSampleStyleSheet()

    styles.add(ParagraphStyle(
        name='MainTitle',
        fontName='Helvetica-Bold',
        fontSize=24,
        textColor=WHITE,
        spaceAfter=6,
        alignment=TA_CENTER,
        leading=30,
    ))
    styles.add(ParagraphStyle(
        name='SubTitle',
        fontName='Helvetica',
        fontSize=13,
        textColor=LIGHT_BLUE,
        spaceAfter=4,
        alignment=TA_CENTER,
        leading=18,
    ))
    styles.add(ParagraphStyle(
        name='ChapterTitle',
        fontName='Helvetica-Bold',
        fontSize=16,
        textColor=WHITE,
        spaceBefore=0,
        spaceAfter=0,
        alignment=TA_LEFT,
        leftIndent=8,
        leading=22,
    ))
    styles.add(ParagraphStyle(
        name='SectionTitle',
        fontName='Helvetica-Bold',
        fontSize=13,
        textColor=DARK_BLUE,
        spaceBefore=10,
        spaceAfter=4,
        leading=18,
    ))
    styles['BodyText'].fontName = 'Helvetica'
    styles['BodyText'].fontSize = 10
    styles['BodyText'].textColor = DARK_GRAY
    styles['BodyText'].spaceAfter = 5
    styles['BodyText'].leading = 15
    styles['BodyText'].alignment = TA_JUSTIFY
    styles.add(ParagraphStyle(
        name='BulletText',
        fontName='Helvetica',
        fontSize=10,
        textColor=DARK_GRAY,
        leftIndent=15,
        spaceAfter=3,
        leading=14,
        bulletText='•',
    ))
    styles.add(ParagraphStyle(
        name='SmallNote',
        fontName='Helvetica-Oblique',
        fontSize=8.5,
        textColor=HexColor('#777777'),
        spaceAfter=4,
        leading=13,
    ))
    styles.add(ParagraphStyle(
        name='TableHeader',
        fontName='Helvetica-Bold',
        fontSize=9,
        textColor=WHITE,
        alignment=TA_CENTER,
        leading=13,
    ))
    styles.add(ParagraphStyle(
        name='TableCell',
        fontName='Helvetica',
        fontSize=8.5,
        textColor=DARK_GRAY,
        alignment=TA_LEFT,
        leading=12,
    ))
    styles.add(ParagraphStyle(
        name='TableCellCenter',
        fontName='Helvetica',
        fontSize=8.5,
        textColor=DARK_GRAY,
        alignment=TA_CENTER,
        leading=12,
    ))
    styles.add(ParagraphStyle(
        name='SchoolName',
        fontName='Helvetica-Bold',
        fontSize=11,
        textColor=MID_BLUE,
        spaceBefore=8,
        spaceAfter=2,
        leading=15,
    ))
    styles.add(ParagraphStyle(
        name='HighlightBox',
        fontName='Helvetica',
        fontSize=9.5,
        textColor=DARK_BLUE,
        leading=14,
        leftIndent=8,
        rightIndent=8,
    ))
    styles.add(ParagraphStyle(
        name='FooterText',
        fontName='Helvetica-Oblique',
        fontSize=8,
        textColor=HexColor('#999999'),
        alignment=TA_CENTER,
    ))
    return styles


def chapter_header(title, styles):
    """Returns a visually distinct chapter banner."""
    tbl = Table([[Paragraph(title, styles['ChapterTitle'])]], colWidths=[17*cm])
    tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), DARK_BLUE),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
        ('RIGHTPADDING', (0,0), (-1,-1), 12),
        ('ROUNDEDCORNERS', [4, 4, 4, 4]),
    ]))
    return tbl


def info_box(text, styles, bg=LIGHT_BLUE):
    """A simple highlighted info box."""
    p = Paragraph(text, styles['HighlightBox'])
    tbl = Table([[p]], colWidths=[17*cm])
    tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), bg),
        ('TOPPADDING', (0,0), (-1,-1), 7),
        ('BOTTOMPADDING', (0,0), (-1,-1), 7),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
        ('BOX', (0,0), (-1,-1), 1, MID_BLUE),
        ('ROUNDEDCORNERS', [3, 3, 3, 3]),
    ]))
    return tbl


def make_table(headers, rows, styles, col_widths=None):
    """Generic styled table."""
    header_row = [Paragraph(h, styles['TableHeader']) for h in headers]
    data = [header_row]
    for i, row in enumerate(rows):
        data.append([Paragraph(str(cell), styles['TableCellCenter'] if j > 0 else styles['TableCell'])
                     for j, cell in enumerate(row)])

    if col_widths is None:
        total = 17 * cm
        col_widths = [total / len(headers)] * len(headers)

    tbl = Table(data, colWidths=col_widths, repeatRows=1)
    ts = TableStyle([
        ('BACKGROUND', (0,0), (-1,0), TABLE_HEADER),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [TABLE_ROW, TABLE_ROW_ALT]),
        ('GRID', (0,0), (-1,-1), 0.4, HexColor('#bbccdd')),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('ROWBACKGROUNDS', (0,0), (0,0), [TABLE_HEADER]),
    ])
    tbl.setStyle(ts)
    return tbl


def build_pdf():
    styles = build_styles()
    doc = SimpleDocTemplate(
        OUTPUT_FILE,
        pagesize=A4,
        rightMargin=2*cm,
        leftMargin=2*cm,
        topMargin=2.5*cm,
        bottomMargin=2.5*cm,
        title="German School & University Guide – Essen",
        author="Education Guide"
    )

    story = []
    W = 17 * cm  # usable width

    # ─────────────────────────────────────────
    # COVER PAGE
    # ─────────────────────────────────────────
    cover_bg = Table(
        [[Paragraph("GERMAN EDUCATION GUIDE", styles['MainTitle']),]],
        colWidths=[W]
    )
    cover_bg.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), DARK_BLUE),
        ('TOPPADDING', (0,0), (-1,-1), 30),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10),
        ('LEFTPADDING', (0,0), (-1,-1), 20),
        ('RIGHTPADDING', (0,0), (-1,-1), 20),
    ]))
    story.append(cover_bg)

    sub_cover = Table(
        [[Paragraph("School System · Universities · Gymnasiums near Heinickestraße, Essen", styles['SubTitle'])]],
        colWidths=[W]
    )
    sub_cover.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), MID_BLUE),
        ('TOPPADDING', (0,0), (-1,-1), 10),
        ('BOTTOMPADDING', (0,0), (-1,-1), 18),
        ('LEFTPADDING', (0,0), (-1,-1), 20),
        ('RIGHTPADDING', (0,0), (-1,-1), 20),
    ]))
    story.append(sub_cover)
    story.append(Spacer(1, 0.5*cm))

    story.append(info_box(
        "<b>A plain-language guide for families, newcomers, and anyone wanting to understand how "
        "German education works</b> — from first school days to university graduation, with a "
        "special focus on Essen and the surrounding Ruhr metropolitan area.",
        styles
    ))
    story.append(Spacer(1, 0.3*cm))

    toc_items = [
        ("1", "The German School System – Overview"),
        ("2", "School Types Explained Simply"),
        ("3", "From Abitur to University"),
        ("4", "Vocational Training (Ausbildung) & Dual System"),
        ("5", "Universities & Colleges Near Essen"),
        ("6", "Top 10 Gymnasiums Near Heinickestraße, Essen"),
        ("7", "Gymnasium Comparison Table"),
        ("8", "Glossary of Key Terms"),
    ]
    toc_data = [[Paragraph(f"<b>Chapter {n}</b>", styles['TableCell']),
                 Paragraph(title, styles['TableCell'])] for n, title in toc_items]
    toc_tbl = Table(toc_data, colWidths=[2.5*cm, 14.5*cm])
    toc_tbl.setStyle(TableStyle([
        ('ROWBACKGROUNDS', (0,0), (-1,-1), [WHITE, LIGHT_GRAY]),
        ('GRID', (0,0), (-1,-1), 0.3, HexColor('#cccccc')),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(Paragraph("<b>TABLE OF CONTENTS</b>", styles['SectionTitle']))
    story.append(toc_tbl)
    story.append(PageBreak())

    # ─────────────────────────────────────────
    # CHAPTER 1: OVERVIEW
    # ─────────────────────────────────────────
    story.append(chapter_header("Chapter 1 · The German School System – Overview", styles))
    story.append(Spacer(1, 0.3*cm))

    story.append(Paragraph(
        "Germany has one of the world's oldest and most structured education systems. "
        "Unlike many countries where all children follow the same path, Germany separates "
        "students into different school types based on academic ability and interests — "
        "usually after just four years of primary school. Think of it like three main "
        "lanes on a motorway: each lane goes somewhere, and you can sometimes switch lanes.",
        styles['BodyText']
    ))
    story.append(Spacer(1, 0.2*cm))

    # School pathway diagram as table
    story.append(Paragraph("<b>The Education Pathway at a Glance</b>", styles['SectionTitle']))

    pathway_data = [
        ["Age", "Stage", "School Type", "Duration", "Goal / Certificate"],
        ["0–3", "Early Childhood", "Krippe (Crèche)", "3 yrs", "Care & early development"],
        ["3–6", "Pre-Primary", "Kindergarten", "3 yrs", "Play-based learning (voluntary)"],
        ["6–10", "Primary", "Grundschule\n(Primary School)", "4 yrs", "Core literacy, numeracy & arts"],
        ["10–18/19", "Secondary", "Gymnasium", "8–9 yrs", "Abitur → University entry"],
        ["10–16", "Secondary", "Realschule", "6 yrs", "Mittlere Reife → Vocational / FH"],
        ["10–15/16", "Secondary", "Hauptschule", "5–6 yrs", "Hauptschulabschluss → Apprenticeship"],
        ["10–18", "Secondary", "Gesamtschule\n(Comprehensive)", "8–9 yrs", "All certificates incl. Abitur"],
        ["15–19", "Vocational", "Berufsschule\n+ Firm (Dual System)", "2–3.5 yrs", "Vocational qualification"],
        ["18+", "Higher Education", "Universität / FH / HS", "3–5 yrs", "Bachelor / Master / Diplom"],
    ]
    pathway_tbl = make_table(
        ["Age", "Stage", "School Type", "Duration", "Goal / Certificate"],
        [row[1:] for row in pathway_data[1:]],
        styles,
        col_widths=[1.6*cm, 2.5*cm, 3.5*cm, 2*cm, 7.4*cm]
    )
    story.append(pathway_tbl)
    story.append(Spacer(1, 0.2*cm))
    story.append(Paragraph(
        "Note: Education in Germany is a responsibility of the 16 federal states (Bundesländer), "
        "so there are minor variations between states. This guide focuses on North Rhine-Westphalia "
        "(NRW), where Essen is located.",
        styles['SmallNote']
    ))
    story.append(PageBreak())

    # ─────────────────────────────────────────
    # CHAPTER 2: SCHOOL TYPES
    # ─────────────────────────────────────────
    story.append(chapter_header("Chapter 2 · School Types Explained Simply", styles))
    story.append(Spacer(1, 0.3*cm))

    schools_info = [
        (
            "🏫 Grundschule (Primary School) — Ages 6–10",
            "The starting point for every child in Germany. All children attend Grundschule "
            "together regardless of background or ability. Classes cover reading, writing, "
            "mathematics, science basics, arts, and sports. After Grade 4, teachers write a "
            "recommendation for secondary school, but parents have the final say in NRW.",
            MID_BLUE
        ),
        (
            "🎓 Gymnasium — Ages 10–18/19 (University Prep)",
            "The most academic school type. Students study for 8–9 years (until Grade 12 or 13) "
            "and sit the <b>Abitur</b> exam — Germany's university entrance qualification. "
            "Gymnasium teaches languages, sciences, maths, history, arts, and often offers "
            "specialisations. In NRW, Grade 13 was reintroduced in 2021 (the 'G9' reform). "
            "Think of it like the British A-Level pathway but more comprehensive.",
            DARK_BLUE
        ),
        (
            "📘 Realschule — Ages 10–16 (Intermediate Track)",
            "A practical-academic middle path. Students complete Grade 10 and earn the "
            "<b>Mittlere Reife</b> certificate. This opens doors to vocational training, "
            "technical colleges (Berufskolleg), or transfer to a Gymnasium's upper school. "
            "About 40% of German students attend Realschule. In NRW many Realschulen merged "
            "into comprehensive schools (Gesamtschule).",
            HexColor('#1565c0')
        ),
        (
            "🔧 Hauptschule — Ages 10–15/16 (Vocational Track)",
            "Focuses on preparing students for apprenticeships and skilled trades. Students earn "
            "the <b>Hauptschulabschluss</b> after Grade 9 (or extended Grade 10). The curriculum "
            "emphasises practical skills alongside core subjects. Germany's world-class vocational "
            "system means this path leads to well-paid, respected careers as mechanics, electricians, "
            "chefs, and hundreds of other trades.",
            HexColor('#4527a0')
        ),
        (
            "🏗️ Gesamtschule (Comprehensive School) — Ages 10–18",
            "Combines all three tracks under one roof. Students are not sorted early on; instead "
            "they are grouped by ability per subject. This gives late-developing students more time "
            "to prove themselves. Gesamtschulen can award all certificates including the Abitur. "
            "Very popular in NRW.",
            HexColor('#00695c')
        ),
        (
            "🎨 Special-Profile Schools",
            "<b>Montessori Schools, Waldorf Schools (Rudolf Steiner), Sports-Gymnasium, "
            "Music-Gymnasium, IB World Schools:</b> Germany also has specialised schools catering "
            "to specific learning philosophies or talents. Several exist in Essen (e.g. "
            "Goetheschule offers the International Baccalaureate; Helmholtz-Gymnasium is an "
            "elite sports school).",
            HexColor('#bf360c')
        ),
    ]

    for title, desc, color in schools_info:
        title_tbl = Table([[Paragraph(f"<b>{title}</b>", styles['SectionTitle'])]], colWidths=[W])
        title_tbl.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), HexColor('#e8f4fd')),
            ('LEFTPADDING', (0,0), (-1,-1), 10),
            ('TOPPADDING', (0,0), (-1,-1), 6),
            ('BOTTOMPADDING', (0,0), (-1,-1), 6),
            ('LINEBELOW', (0,0), (-1,-1), 2, color),
        ]))
        story.append(title_tbl)
        story.append(Paragraph(desc, styles['BodyText']))
        story.append(Spacer(1, 0.15*cm))

    story.append(PageBreak())

    # ─────────────────────────────────────────
    # CHAPTER 3: ABITUR & UNIVERSITY
    # ─────────────────────────────────────────
    story.append(chapter_header("Chapter 3 · From Abitur to University", styles))
    story.append(Spacer(1, 0.3*cm))

    story.append(Paragraph(
        "The <b>Abitur</b> is Germany's most important school certificate — equivalent to "
        "A-Levels (UK) or the final year of high school (USA). Achieving it unlocks the door "
        "to German universities. Here's how it works:",
        styles['BodyText']
    ))
    story.append(Spacer(1, 0.15*cm))

    abitur_data = [
        ["Aspect", "Details"],
        ["What is it?", "Final examination at the end of Gymnasium (Grade 12 or 13 in NRW)"],
        ["Subjects", "Students choose 2 advanced courses (Leistungskurse) + 2 basic courses (Grundkurse) + oral exam"],
        ["Grades", "Scale 0–15 points per subject; overall grade 1.0 (best) to 4.0 (minimum pass)"],
        ["Numerus Clausus (NC)", "Competitive entry: popular courses (medicine, law) require very high grades (often 1.0–1.5)"],
        ["University Types", "Universität (research-focused), Fachhochschule/HS (applied sciences), Kunsthochschule (arts)"],
        ["Studium", "Bachelor = 3 years; Master = 1–2 years; State Exam (Medicine/Law) = 5–6 years"],
        ["Tuition", "Public universities charge only semester fees (~€300–€400); private unis charge full tuition"],
        ["International Baccalaureate (IB)", "A globally recognised alternative Abitur; accepted by universities worldwide including Oxford, MIT"],
        ["Fachhochschulreife", "A 'lesser' university entrance qualification for Fachhochschulen (applied sciences universities) only"],
    ]
    abi_tbl = make_table(
        ["Aspect", "Details"],
        [row for row in abitur_data[1:]],
        styles,
        col_widths=[4.5*cm, 12.5*cm]
    )
    story.append(abi_tbl)
    story.append(Spacer(1, 0.3*cm))
    story.append(info_box(
        "<b>Tip for International Families:</b> If you hold foreign qualifications (e.g. Indian "
        "12th Standard, British A-Levels, French Baccalauréat), they may be recognised as "
        "equivalent to the Abitur. Contact the university's admissions office or the "
        "<i>anabin</i> database (anabin.kmk.org) for recognition details.",
        styles
    ))
    story.append(PageBreak())

    # ─────────────────────────────────────────
    # CHAPTER 4: VOCATIONAL / DUAL SYSTEM
    # ─────────────────────────────────────────
    story.append(chapter_header("Chapter 4 · Vocational Training & the Dual System", styles))
    story.append(Spacer(1, 0.3*cm))

    story.append(Paragraph(
        "Germany's vocational training system is world-famous. About <b>50% of young Germans</b> "
        "choose an <i>Ausbildung</i> (apprenticeship) over university — and it's no lesser path. "
        "Skilled tradespeople in Germany earn good salaries and are highly respected.",
        styles['BodyText']
    ))
    story.append(Spacer(1, 0.15*cm))

    dual_items = [
        ("What is the 'Dual System'?",
         "Training splits between a <b>company</b> (3–4 days/week, real work) and a "
         "<b>Berufsschule</b> (vocational school, 1–2 days/week). You earn a salary while "
         "learning. Duration: 2–3.5 years depending on the trade."),
        ("Who qualifies?",
         "Hauptschulabschluss holders can enter many trades. Mittlere Reife opens more options. "
         "Even Abitur graduates choose apprenticeships in banking, IT, or business."),
        ("Popular fields in NRW / Essen",
         "Information Technology (Fachinformatiker), Health & Social Care (Pflegefachmann), "
         "Electrical trades, Mechanical engineering, Commerce & retail, Banking & insurance."),
        ("Berufskolleg (Vocational College)",
         "A higher-level vocational school that can lead to the Fachhochschulreife or even "
         "full Abitur. Combines professional qualification with academic progression."),
        ("After Ausbildung",
         "With experience, apprentices can become Meister (master craftspeople) — a highly "
         "respected title. Some trades require a Meisterbrief to open your own business. "
         "Meister qualifications are now considered equivalent to a Bachelor's degree in the EU."),
    ]

    for title, desc in dual_items:
        story.append(Paragraph(f"<b>{title}</b>", styles['SectionTitle']))
        story.append(Paragraph(desc, styles['BodyText']))

    story.append(PageBreak())

    # ─────────────────────────────────────────
    # CHAPTER 5: UNIVERSITIES NEAR ESSEN
    # ─────────────────────────────────────────
    story.append(chapter_header("Chapter 5 · Universities & Colleges Near Essen", styles))
    story.append(Spacer(1, 0.3*cm))

    story.append(Paragraph(
        "Essen sits in the heart of the <b>Ruhr Metropolitan Area</b> — Germany's largest "
        "urban agglomeration with over 5 million people. This region has an exceptional "
        "density of universities. The three largest (Bochum, Dortmund, Duisburg-Essen) "
        "form the <b>University Alliance Ruhr (UA Ruhr)</b>, one of Europe's strongest "
        "research consortia. Distances below are approximate driving distances from "
        "Heinickestraße 8, 45128 Essen.",
        styles['BodyText']
    ))
    story.append(Spacer(1, 0.2*cm))

    unis = [
        # Name, Location, Type, Distance, Key Specializations, Students, Website
        (
            "University of Duisburg-Essen (UDE)",
            "Universitätsstr. 2, 45141 Essen (Essen Campus)\nForsthausweg 2, 47057 Duisburg (Duisburg Campus)",
            "Public Research University",
            "~4 km (Essen campus)",
            "Engineering, Medicine, Business, Natural Sciences, Social Sciences, Humanities, Computer Science, Educational Sciences",
            "~40,000",
            "uni-due.de"
        ),
        (
            "Folkwang University of the Arts",
            "Klemensborn 39, 45239 Essen-Werden\n(also: Zeche Zollverein, Essen)",
            "Public Arts University",
            "~12 km",
            "Music, Theatre, Dance, Design, Art History, Film, Photography",
            "~1,500",
            "folkwang-uni.de"
        ),
        (
            "FOM University of Applied Sciences",
            "Leimkugelstr. 6, 45141 Essen",
            "Private Univ. of Applied Sciences",
            "~4 km",
            "Business Administration, Economics, Engineering, IT, Health Management, Psychology (part-time / evening programmes)",
            "~57,000 (Germany-wide)",
            "fom.de"
        ),
        (
            "HBK Essen – Academy of Visual Arts",
            "Moltkeplatz 2, 45138 Essen",
            "Private Arts Academy",
            "~1.5 km",
            "Fine Arts, Product Design, Communication Design, Art Education",
            "~500",
            "hbk-essen.de"
        ),
        (
            "Ruhr University Bochum (RUB)",
            "Universitätsstr. 150, 44801 Bochum",
            "Public Research University",
            "~20 km",
            "Engineering, Natural Sciences, Medicine, Social Sciences, Law, Humanities, IT Security, Solvation Science",
            "~43,000",
            "ruhr-uni-bochum.de"
        ),
        (
            "TU Dortmund University",
            "August-Schmidt-Str. 4, 44227 Dortmund",
            "Public Technical University",
            "~35 km",
            "Engineering, Computer Science, Statistics, Natural Sciences, Social Sciences, Journalism, Educational Sciences",
            "~30,300",
            "tu-dortmund.de"
        ),
        (
            "Hochschule Ruhr West (HRW)",
            "Duisburger Str. 100, 45479 Mülheim an der Ruhr",
            "Public Univ. of Applied Sciences",
            "~9 km",
            "Engineering (Mechanical, Electrical, Civil), Computer Science, Business, Natural Sciences",
            "~5,200",
            "hochschule-ruhr-west.de"
        ),
        (
            "TH Georg Agricola (THGA)",
            "Herner Str. 45, 44787 Bochum",
            "Private Technical University",
            "~18 km",
            "Mining Engineering, Mechanical Engineering, Resource Efficiency, Industry 4.0, Post-Mining, Environmental Technology",
            "~2,300",
            "thga.de"
        ),
        (
            "Westfälische Hochschule",
            "Neidenburger Str. 43, 45897 Gelsenkirchen\n(also: Bocholt, Recklinghausen)",
            "Public Univ. of Applied Sciences",
            "~15 km",
            "Engineering, Computer Science, Business, Design, Online/Digital Media",
            "~8,000",
            "w-hs.de"
        ),
        (
            "Heinrich Heine University Düsseldorf",
            "Universitätsstr. 1, 40225 Düsseldorf",
            "Public Research University",
            "~35 km",
            "Medicine, Law, Business, Natural Sciences, Philosophy, Mathematics, Information Science",
            "~38,000",
            "hhu.de"
        ),
        (
            "Hochschule Düsseldorf (HSD)",
            "Münsterstr. 156, 40476 Düsseldorf",
            "Public Univ. of Applied Sciences",
            "~38 km",
            "Engineering, Social Work, Media, Business, Architecture, Design",
            "~11,000",
            "hs-duesseldorf.de"
        ),
    ]

    uni_headers = ["University", "Location & Address", "Type", "Dist. from Heinickestr.", "Key Fields", "Students"]
    uni_rows = []
    for u in unis:
        uni_rows.append([
            f"<b>{u[0]}</b>",
            u[1],
            u[2],
            u[3],
            u[4],
            u[5],
        ])

    uni_col_widths = [3.8*cm, 3.8*cm, 2.6*cm, 1.9*cm, 3.5*cm, 1.4*cm]

    # Build table manually with paragraph cells
    header_row_data = [Paragraph(h, styles['TableHeader']) for h in uni_headers]
    uni_table_data = [header_row_data]
    for i, row in enumerate(uni_rows):
        uni_table_data.append([
            Paragraph(row[0], styles['TableCell']),
            Paragraph(row[1], styles['SmallNote']),
            Paragraph(row[2], styles['TableCellCenter']),
            Paragraph(row[3], styles['TableCellCenter']),
            Paragraph(row[4], styles['SmallNote']),
            Paragraph(row[5], styles['TableCellCenter']),
        ])

    uni_tbl = Table(uni_table_data, colWidths=uni_col_widths, repeatRows=1)
    uni_tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), TABLE_HEADER),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [TABLE_ROW, TABLE_ROW_ALT]),
        ('GRID', (0,0), (-1,-1), 0.4, HexColor('#bbccdd')),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(uni_tbl)
    story.append(Spacer(1, 0.2*cm))
    story.append(info_box(
        "<b>University Alliance Ruhr (UA Ruhr):</b> UDE, Ruhr Uni Bochum, and TU Dortmund collaborate "
        "extensively — students can take courses at all three, and research centres are shared. "
        "Together they have ~120,000 students, making the UA Ruhr one of the largest university "
        "alliances in Europe. Website: uaruhr.de",
        styles
    ))
    story.append(PageBreak())

    # ─────────────────────────────────────────
    # CHAPTER 6: TOP 10 GYMNASIUMS NEAR HEINICKESTRASSE
    # ─────────────────────────────────────────
    story.append(chapter_header("Chapter 6 · Top 10 Gymnasiums Near Heinickestraße, Essen", styles))
    story.append(Spacer(1, 0.25*cm))

    story.append(info_box(
        "<b>Reference Point:</b> Heinickestraße 8, 45128 Essen (Innenstadt-Süd / Südviertel). "
        "Distances are approximate straight-line / walking or driving estimates.",
        styles
    ))
    story.append(Spacer(1, 0.2*cm))

    gymnasiums = [
        {
            "rank": 1,
            "name": "Viktoria-Gymnasium Essen",
            "address": "Kürfürstenplatz 1, 45138 Essen",
            "distance": "~0.5 km",
            "type": "Municipal Co-educational",
            "founded": "1891",
            "languages": "English, French, Latin, Spanish",
            "specialization": "Theatre Pedagogy, Arts, Multi-language programme. One of Essen's oldest gymnasiums. Theatre-AG, Video Production, Art as advanced subject.",
            "abitur": "Yes (G9 from 2021)",
            "ib": "No",
            "review": (
                "One of Essen's historic gymnasiums near the city centre. "
                "Strong arts and theatre programme draws creative students. "
                "Compact school community (~500 students) means personal attention. "
                "Currently transitioning/merging with Burggymnasium at the upper-school level, "
                "offering joint advanced courses. Parents appreciate the diverse language options "
                "and the central location — easy to reach by tram."
            ),
            "rating": "★★★★☆ (4/5)",
            "website": "essen.de (city directory)",
        },
        {
            "rank": 2,
            "name": "HBK-Schule / Burggymnasium Essen",
            "address": "Burgplatz 4, 45131 Essen",
            "distance": "~1.8 km",
            "type": "Municipal Co-educational",
            "founded": "1897",
            "languages": "English, French, Latin, Spanish",
            "specialization": "Language specialisation (bilingual track), Music, MINT (Science/Tech). Cooperates with Viktoria in upper school. ~590 students.",
            "abitur": "Yes (G9)",
            "ib": "No",
            "review": (
                "Community-oriented atmosphere with a strong emphasis on languages — "
                "a bilingual (German-English) track begins from lower school. "
                "Good music programme and active MINT projects. Parents rate the school "
                "highly for communication and teacher accessibility. "
                "The building has a historic character close to Essen's Rüttenscheid quarter. "
                "Active school events and open days praised on review platforms."
            ),
            "rating": "★★★★☆ (4.1/5)",
            "website": "burggymnasium.de",
        },
        {
            "rank": 3,
            "name": "Helmholtz-Gymnasium Essen",
            "address": "Rosastraße 83, 45130 Essen",
            "distance": "~1.5 km",
            "type": "Municipal Co-educational",
            "founded": "1899",
            "languages": "English, French, Latin, Spanish",
            "specialization": "Elite Sports School – dedicated sports classes from Grade 5. Sports science as advanced course. Cooperation with professional sports clubs. Also strong in natural sciences.",
            "abitur": "Yes (G9)",
            "ib": "No",
            "review": (
                "The go-to school for sporty and athletically gifted children in Essen. "
                "Sports classes allow extra training while maintaining full academic curriculum. "
                "Past students have competed nationally and internationally. "
                "The school is neighbour to the Maria-Wächtler-Gymnasium and the two "
                "share some advanced courses — beneficial for students in upper school. "
                "Solid academic record alongside its sports profile. Well-regarded by parents."
            ),
            "rating": "★★★★☆ (4/5)",
            "website": "helmholtz-gymnasium-essen.de",
        },
        {
            "rank": 4,
            "name": "Maria-Wächtler-Gymnasium (MWG)",
            "address": "Rosastraße 75, 45130 Essen",
            "distance": "~1.5 km",
            "type": "Municipal Co-educational (Europaschule)",
            "founded": "1913",
            "languages": "English (bilingual), French, Latin, Spanish",
            "specialization": "Bilingual Europaschule since 1972: Biology (Gr.7), Geography (Gr.8), Politics (Gr.9) taught in English. Strong MINT programme (certified). Exchange programmes.",
            "abitur": "Yes (G9) — bilingual Abitur available",
            "ib": "No",
            "review": (
                "Highly regarded bilingual school — one of the first in NRW to introduce bilingual "
                "education (1972). Parents consistently praise the high academic standards and "
                "the confident English proficiency graduates develop. "
                "MINT certification demonstrates strong science teaching. "
                "Active international exchanges (France, UK, USA). "
                "Slightly larger school (~800 students), well-organised. "
                "Often the top choice for families wanting a bilingual academic track close to the city."
            ),
            "rating": "★★★★★ (4.5/5)",
            "website": "mwg-essen.de",
        },
        {
            "rank": 5,
            "name": "Goetheschule Essen (IB World School)",
            "address": "Ruschenstraße 1, 45133 Essen",
            "distance": "~2.5 km",
            "type": "Municipal Co-educational (IB World School)",
            "founded": "1901",
            "languages": "English (bilingual & IB), French, Latin, Spanish",
            "specialization": "Only state school in Essen offering the International Baccalaureate (IB) in addition to Abitur. International learning from Grade 5. Dual Diploma (Abitur + IB).",
            "abitur": "Yes (G9) + IB Diploma",
            "ib": "YES – since 2007",
            "review": (
                "Essen's most internationally connected state school and one of only ~30 "
                "state schools in all Germany offering the IB. Ideal for families who may relocate "
                "internationally or want globally recognised qualifications. "
                "In 2015, students achieved results qualifying for Oxford and other elite universities. "
                "IB programme requires a few extra weekly English hours alongside normal classes. "
                "Inspectors praised the excellent academic prerequisites and experienced teaching staff. "
                "High parental satisfaction; vibrant international atmosphere."
            ),
            "rating": "★★★★★ (4.6/5)",
            "website": "goetheschule-essen.de",
        },
        {
            "rank": 6,
            "name": "Grashof Gymnasium Essen",
            "address": "Grashofstraße 55, 45133 Essen",
            "distance": "~3.0 km",
            "type": "Municipal Co-educational",
            "founded": "1965",
            "languages": "English (bilingual), French, Latin, Spanish",
            "specialization": "German-English bilingual track. MINT focus. Modern building in Rüttenscheid area. Active extracurricular programme.",
            "abitur": "Yes (G9)",
            "ib": "No",
            "review": (
                "Well-established gymnasium in the popular Rüttenscheid district. "
                "The bilingual programme (German-English) is a highlight, drawing families "
                "who want academic rigour with strong language skills. "
                "MINT subjects are well-resourced. "
                "Reviewers note a friendly, supportive school culture and active student "
                "participation in school governance. "
                "Good public transport links via Rüttenscheid tram stops."
            ),
            "rating": "★★★★☆ (4.2/5)",
            "website": "grashof-gymnasium.de",
        },
        {
            "rank": 7,
            "name": "Gymnasium Essen Nord-Ost",
            "address": "Katzenbruchstraße 79, 45141 Essen",
            "distance": "~5.5 km",
            "type": "Municipal Co-educational",
            "founded": "1966",
            "languages": "English, French, Latin",
            "specialization": "Natural sciences and MINT focus. Media education. Modern school building. Active sports programme.",
            "abitur": "Yes (G9)",
            "ib": "No",
            "review": (
                "Solid comprehensive gymnasium serving the northern-eastern parts of Essen. "
                "Strong science programme with well-equipped labs. "
                "Media education and digital learning are emphasised more than at many other schools. "
                "The school community is described as tight-knit and supportive. "
                "Slightly further from the city centre but well-connected by U-Bahn. "
                "Review ratings on local portals are consistently positive."
            ),
            "rating": "★★★★☆ (3.9/5)",
            "website": "gtgeno.de",
        },
        {
            "rank": 8,
            "name": "Leibniz-Gymnasium Essen",
            "address": "Stankeitstraße 22, 45326 Essen",
            "distance": "~9 km",
            "type": "Municipal Co-educational",
            "founded": "1928",
            "languages": "English (bilingual), French, Latin",
            "specialization": "German-English bilingual programme. Focus on sciences and mathematics. Located in Altenessen-Süd district.",
            "abitur": "Yes (G9)",
            "ib": "No",
            "review": (
                "Popular school in the Altenessen area of Essen. The bilingual programme "
                "(German-English) and strong maths/science teaching are its main attractions. "
                "School community is described as inclusive and diverse, reflecting the "
                "multicultural neighbourhood. "
                "Teachers are noted for their commitment. "
                "Good results in state-level Abitur statistics."
            ),
            "rating": "★★★★☆ (4.0/5)",
            "website": "leibniz-gymnasium-essen.de",
        },
        {
            "rank": 9,
            "name": "Gymnasium Essen-Werden",
            "address": "Grafenstraße 9, 45239 Essen-Werden",
            "distance": "~10 km",
            "type": "Municipal Co-educational",
            "founded": "1907",
            "languages": "English, French, Latin, Spanish",
            "specialization": "Traditional academic gymnasium in the scenic Werden district near the Ruhr river. Strong in humanities and social sciences. Close to Folkwang University.",
            "abitur": "Yes (G9)",
            "ib": "No",
            "review": (
                "Beloved school in the picturesque Essen-Werden neighbourhood — a charming "
                "setting next to the Ruhr river and medieval abbey. "
                "Strong academic tradition with emphasis on humanities, languages and social sciences. "
                "Proximity to Folkwang University of the Arts creates a culturally rich environment. "
                "Smaller class sizes than inner-city schools; community atmosphere. "
                "Particularly popular with families in the southern Essen suburbs."
            ),
            "rating": "★★★★☆ (4.2/5)",
            "website": "gymnasium-essen-werden.de",
        },
        {
            "rank": 10,
            "name": "Mariengymnasium Essen-Werden",
            "address": "Grafenstraße 11, 45239 Essen-Werden",
            "distance": "~10 km",
            "type": "Catholic Co-educational",
            "founded": "1925",
            "languages": "English, French, Latin, Spanish",
            "specialization": "Catholic confessional gymnasium. Values-based education alongside strong academics. Music profile. Located adjacent to the historic Werden Abbey and Folkwang University.",
            "abitur": "Yes (G9)",
            "ib": "No",
            "review": (
                "A warmly regarded Catholic gymnasium emphasising values-based education "
                "alongside academic excellence. "
                "Strong music programme, with school choir and orchestra well known in Essen. "
                "The school community has a close-knit, family feel. "
                "Alumni report strong teacher-student relationships and good pastoral care. "
                "The beautiful Werden Abbey surroundings make it a unique school environment. "
                "Consistently good Abitur results."
            ),
            "rating": "★★★★☆ (4.3/5)",
            "website": "mariengymnasium.net",
        },
    ]

    for g in gymnasiums:
        rank_color = ACCENT_GOLD if g['rank'] <= 3 else MID_BLUE

        header_data = [[
            Paragraph(f"<b>#{g['rank']}  {g['name']}</b>", styles['SchoolName']),
            Paragraph(f"<b>{g['rating']}</b>", ParagraphStyle(
                name=f'r{g["rank"]}', fontName='Helvetica-Bold', fontSize=10,
                textColor=ACCENT_GOLD, alignment=TA_CENTER, leading=14)),
        ]]
        h_tbl = Table(header_data, colWidths=[12*cm, 5*cm])
        h_tbl.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), HexColor('#eaf4fb')),
            ('LINEBELOW', (0,0), (-1,-1), 2, rank_color),
            ('TOPPADDING', (0,0), (-1,-1), 5),
            ('BOTTOMPADDING', (0,0), (-1,-1), 5),
            ('LEFTPADDING', (0,0), (-1,-1), 8),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ]))
        story.append(h_tbl)

        meta_data = [
            [
                Paragraph(f"<b>Address:</b> {g['address']}", styles['SmallNote']),
                Paragraph(f"<b>Distance:</b> {g['distance']}", styles['SmallNote']),
                Paragraph(f"<b>Type:</b> {g['type']}", styles['SmallNote']),
            ],
            [
                Paragraph(f"<b>Founded:</b> {g['founded']}", styles['SmallNote']),
                Paragraph(f"<b>IB Programme:</b> {g['ib']}", styles['SmallNote']),
                Paragraph(f"<b>Web:</b> {g['website']}", styles['SmallNote']),
            ],
        ]
        meta_tbl = Table(meta_data, colWidths=[6.5*cm, 4*cm, 6.5*cm])
        meta_tbl.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), HexColor('#f9fdff')),
            ('TOPPADDING', (0,0), (-1,-1), 3),
            ('BOTTOMPADDING', (0,0), (-1,-1), 3),
            ('LEFTPADDING', (0,0), (-1,-1), 8),
            ('GRID', (0,0), (-1,-1), 0.3, HexColor('#ddeeff')),
        ]))
        story.append(meta_tbl)

        spec_lang = Table([[
            Paragraph(f"<b>Languages:</b> {g['languages']}", styles['SmallNote']),
            Paragraph(f"<b>Specialisation:</b> {g['specialization']}", styles['SmallNote']),
        ]], colWidths=[5*cm, 12*cm])
        spec_lang.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), HexColor('#f0f8ff')),
            ('TOPPADDING', (0,0), (-1,-1), 3),
            ('BOTTOMPADDING', (0,0), (-1,-1), 3),
            ('LEFTPADDING', (0,0), (-1,-1), 8),
            ('GRID', (0,0), (-1,-1), 0.3, HexColor('#ddeeff')),
        ]))
        story.append(spec_lang)

        review_tbl = Table([[
            Paragraph(f"<b>Parent & Student Review:</b> {g['review']}", styles['BodyText']),
        ]], colWidths=[W])
        review_tbl.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), WHITE),
            ('TOPPADDING', (0,0), (-1,-1), 4),
            ('BOTTOMPADDING', (0,0), (-1,-1), 4),
            ('LEFTPADDING', (0,0), (-1,-1), 8),
            ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ]))
        story.append(review_tbl)
        story.append(Spacer(1, 0.25*cm))

    story.append(PageBreak())

    # ─────────────────────────────────────────
    # CHAPTER 7: COMPARISON TABLE
    # ─────────────────────────────────────────
    story.append(chapter_header("Chapter 7 · Gymnasium Comparison Table", styles))
    story.append(Spacer(1, 0.3*cm))

    story.append(Paragraph(
        "The table below offers a side-by-side comparison of all 10 gymnasiums to help "
        "you choose the right school for your child's strengths and interests.",
        styles['BodyText']
    ))
    story.append(Spacer(1, 0.15*cm))

    comp_headers = [
        "School", "Dist.", "Founded", "Bilingual", "IB", "Sports", "Arts/Music",
        "MINT", "Values", "Overall Rating"
    ]
    comp_rows = [
        ["Viktoria-Gymnasium",     "0.5km", "1891", "No",  "No",  "●●○", "●●●", "●●○", "Civic",       "★★★★☆"],
        ["Burggymnasium",          "1.8km", "1897", "DE/EN","No", "●●○", "●●●", "●●○", "Community",   "★★★★☆"],
        ["Helmholtz-Gymnasium",    "1.5km", "1899", "No",  "No",  "●●●", "●●○", "●●○", "Achievement", "★★★★☆"],
        ["Maria-Wächtler-Gym.",    "1.5km", "1913", "DE/EN","No", "●●○", "●●○", "●●●", "Excellence",  "★★★★½"],
        ["Goetheschule (IB)",      "2.5km", "1901", "EN",  "YES", "●●○", "●●○", "●●○", "International","★★★★½"],
        ["Grashof Gymnasium",      "3.0km", "1965", "DE/EN","No", "●●○", "●●○", "●●●", "Community",   "★★★★☆"],
        ["Gym. Nord-Ost",          "5.5km", "1966", "No",  "No",  "●●○", "●○○", "●●●", "Innovation",  "★★★★○"],
        ["Leibniz-Gymnasium",      "9.0km", "1928", "DE/EN","No", "●○○", "●●○", "●●●", "Diversity",   "★★★★○"],
        ["Gym. Essen-Werden",      "10km",  "1907", "No",  "No",  "●●○", "●●○", "●●○", "Tradition",   "★★★★☆"],
        ["Mariengymnasium Werden", "10km",  "1925", "No",  "No",  "●●○", "●●●", "●●○", "Catholic",    "★★★★☆"],
    ]

    comp_col_widths = [3.6*cm, 1.3*cm, 1.7*cm, 1.7*cm, 1.0*cm, 1.5*cm, 1.7*cm, 1.3*cm, 2.0*cm, 2.2*cm]

    comp_header_row = [Paragraph(h, styles['TableHeader']) for h in comp_headers]
    comp_table_data = [comp_header_row]
    for i, row in enumerate(comp_rows):
        comp_table_data.append([
            Paragraph(row[j], styles['TableCell'] if j == 0 else styles['TableCellCenter'])
            for j in range(len(row))
        ])

    comp_tbl = Table(comp_table_data, colWidths=comp_col_widths, repeatRows=1)
    comp_tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), TABLE_HEADER),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [TABLE_ROW, TABLE_ROW_ALT]),
        ('GRID', (0,0), (-1,-1), 0.4, HexColor('#bbccdd')),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        # Highlight IB school row
        ('BACKGROUND', (0,5), (-1,5), HexColor('#fff8e1')),
        # Highlight bilingual schools
        ('TEXTCOLOR', (3,1), (3,-1), GREEN),
    ]))
    story.append(comp_tbl)
    story.append(Spacer(1, 0.2*cm))

    legend_data = [[
        Paragraph("<b>Legend:</b>  ●●● Exceptional  ●●○ Good  ●○○ Standard  "
                  "DE/EN = German-English bilingual  EN = English-medium (IB)  "
                  "★★★★½ = 4.5/5  ★★★★☆ = 4/5  ★★★★○ = ~3.9/5", styles['SmallNote']),
    ]]
    legend_tbl = Table(legend_data, colWidths=[W])
    legend_tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), LIGHT_GRAY),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('BOX', (0,0), (-1,-1), 0.5, HexColor('#bbbbbb')),
    ]))
    story.append(legend_tbl)
    story.append(Spacer(1, 0.3*cm))

    # Best for different profiles
    story.append(Paragraph("<b>Which Gymnasium is Best for Your Child?</b>", styles['SectionTitle']))
    profile_data = [
        ["If your child is…", "Recommended Gymnasium(s)"],
        ["…academically ambitious and wants international recognition", "Goetheschule Essen (IB + Abitur)"],
        ["…a gifted athlete or sports-lover", "Helmholtz-Gymnasium"],
        ["…keen on languages and cultural exchange", "Maria-Wächtler-Gymnasium / Burggymnasium / Grashof Gymnasium"],
        ["…creative, loves theatre and arts", "Viktoria-Gymnasium / Mariengymnasium Werden"],
        ["…interested in science, tech, maths (MINT)", "Maria-Wächtler-Gymnasium / Grashof / Nord-Ost"],
        ["…in a family that may relocate internationally", "Goetheschule (IB)"],
        ["…looking for a values/faith-based environment", "Mariengymnasium Essen-Werden (Catholic)"],
        ["…preferring a quieter, community-oriented school", "Gymnasium Essen-Werden / Mariengymnasium Werden"],
        ["…in the city centre for easy daily travel", "Viktoria-Gymnasium or Helmholtz / MWG"],
    ]
    profile_tbl = make_table(
        ["If your child is…", "Recommended Gymnasium(s)"],
        [row for row in profile_data[1:]],
        styles,
        col_widths=[8*cm, 9*cm]
    )
    story.append(profile_tbl)
    story.append(PageBreak())

    # ─────────────────────────────────────────
    # CHAPTER 8: GLOSSARY
    # ─────────────────────────────────────────
    story.append(chapter_header("Chapter 8 · Glossary of Key German Education Terms", styles))
    story.append(Spacer(1, 0.3*cm))

    glossary = [
        ("Abitur", "Germany's university entrance qualification. Awarded after completing Gymnasium (Grade 12/13)."),
        ("Ausbildung", "Apprenticeship / vocational training. Combines on-the-job training with Berufsschule classes."),
        ("Berufskolleg", "Vocational college offering professional qualifications + possibility of Fachhochschulreife or Abitur."),
        ("Berufsschule", "Vocational school; the school component of the dual Ausbildung system."),
        ("Bundesland", "Federal state (Germany has 16). Each controls its own education system."),
        ("Fachhochschulreife", "Qualification allowing entry to universities of applied sciences (Fachhochschule) but NOT full universities."),
        ("Fachhochschule (FH) / Hochschule (HS)", "University of applied sciences; more practical orientation than Universität. Now often called 'Hochschule'."),
        ("G8 / G9", "8-year vs 9-year Gymnasium. NRW returned to G9 (Grade 13 Abitur) in 2021."),
        ("Gesamtschule", "Comprehensive school combining Hauptschule, Realschule, and Gymnasium tracks in one institution."),
        ("Grundschule", "Primary school, years 1–4 (or 1–6 in some states). For ages 6–10."),
        ("Hauptschule", "Basic secondary school preparing students mainly for apprenticeships. Ends at Grade 9/10."),
        ("Hauptschulabschluss", "Leaving certificate from Hauptschule. Opens doors to apprenticeships."),
        ("IB (International Baccalaureate)", "International diploma, globally recognised, awarded in addition to or instead of Abitur at select schools."),
        ("Kindergarten", "Pre-school for ages 3–6 (voluntary). State-funded; fees depend on income."),
        ("Krippe", "Day nursery for ages 0–3."),
        ("Leistungskurs", "Advanced (A-level style) course chosen by Gymnasium students in upper school (Oberstufe)."),
        ("Meister", "Master craftsperson qualification. Highly respected; legally required in many trades. EU-level 6."),
        ("Mittlere Reife", "Intermediate school leaving certificate from Realschule (Grade 10). Opens vocational and FH paths."),
        ("NC (Numerus Clausus)", "Entry restriction for university courses: a minimum Abitur grade required (e.g. 1.0 for Medicine)."),
        ("NRW", "North Rhine-Westphalia – Germany's most populous state, where Essen is located."),
        ("Oberstufe", "Upper school of Gymnasium (Grades 11–12/13); students choose specialisation courses."),
        ("Realschule", "Intermediate secondary school ending at Grade 10 with Mittlere Reife certificate."),
        ("Universität", "Research university; admits students with Abitur. Offers all academic degrees."),
        ("Zeugnis", "School report card. Issued twice yearly in most German states."),
    ]

    for term, definition in glossary:
        story.append(Table([[
            Paragraph(f"<b>{term}</b>", styles['TableCell']),
            Paragraph(definition, styles['TableCell']),
        ]], colWidths=[4.5*cm, 12.5*cm]))

    story.append(Spacer(1, 0.4*cm))
    story.append(HRFlowable(width=W, color=MID_BLUE, thickness=1))
    story.append(Spacer(1, 0.2*cm))
    story.append(Paragraph(
        "Sources: Make-it-in-Germany (BMBF), Wikipedia, Schulen.de, City of Essen (essen.de), "
        "IBO.org, University official websites, UA Ruhr (uaruhr.de), BIBB vocational training data. "
        "Distances are approximate and based on Heinickestraße 8, 45128 Essen as the reference point. "
        "School ratings are compiled from community review portals (werkenntdenbesten.de, schulen.de, golocal.de). "
        "Always verify current school information directly with each institution as details may change.",
        styles['SmallNote']
    ))
    story.append(Spacer(1, 0.1*cm))
    story.append(Paragraph(
        f"Generated June 2026  |  For informational purposes only",
        styles['FooterText']
    ))

    doc.build(story)
    print(f"PDF created: {OUTPUT_FILE}")


if __name__ == '__main__':
    build_pdf()
