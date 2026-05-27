"""
COMPLY SB 1288 - AI Policy Compliance Platform
A CSBA product distributed as GAMUT PLUS
Powered by H-EDU.solutions

COMPLY SB 1288 guides California LEAs through a structured six-module workflow
that satisfies every requirement of Education Code 33328.5 and produces a
complete, board-ready AI governance policy document.

Modules:
  A - Academic Integrity          (33328.5(d)(4)(A))
  B - Acceptable Uses             (33328.5(d)(4)(B) + (H))
  C - Data Privacy                (33328.5(d)(4)(C))
  D - Parent Access               (33328.5(d)(4)(D))
  E - Procurement                 (33328.5(d)(4)(E))
  F - Human Oversight & PD        (33328.5(d)(4)(F), (G), (I))
"""

import streamlit as st
from datetime import datetime, date
import json

# ============================================================
# DESIGN TOKENS
# ============================================================
COMPLY_BLUE  = "#1B4D89"
COMPLY_DARK  = "#0d2847"
COMPLY_GOLD  = "#C4A000"
COMPLY_LIGHT = "#f7f7f7"

# ============================================================
# COMPLY SB 1288 — MODULE DEFINITIONS
# ============================================================
MODULES = {
    "A": {
        "title": "Academic Integrity",
        "anchor": "33328.5(d)(4)(A)",
        "description": "Plagiarism, AI-generated content disclosure, and academic honesty standards across grade levels.",
        "model_language": """The District recognizes that artificial intelligence tools present both opportunities and challenges for academic integrity. Students shall:

1. Disclose the use of AI tools in completing assignments when required by the instructor.
2. Not submit AI-generated content as their own original work unless expressly permitted.
3. Understand that using AI to complete assessments without authorization constitutes academic dishonesty subject to existing discipline procedures.
4. Develop critical thinking skills so that AI tools supplement—not substitute—their own reasoning.

Educators shall clearly communicate expectations regarding AI use for each assignment and establish consistent, grade-appropriate consequences for violations of academic integrity standards. The District shall incorporate AI literacy into its existing academic honesty curriculum no later than the start of the school year following adoption of this policy.""",
        "questions": [
            ("Does your district currently have an academic integrity policy?", ["Yes, fully addresses AI", "Yes, partially addresses AI", "Yes, does not address AI", "No existing policy"]),
            ("Have you established AI disclosure requirements for students?", ["Yes, district-wide", "Yes, classroom-by-classroom", "In development", "Not yet"]),
            ("Are consequences for AI-related academic dishonesty defined?", ["Yes, in existing policy", "Partially defined", "Not yet defined"]),
        ]
    },
    "B": {
        "title": "Acceptable Uses",
        "anchor": "33328.5(d)(4)(B) + (H)",
        "description": "Appropriate and inappropriate AI use by students and educators across grade levels, with equity safeguards.",
        "model_language": """ACCEPTABLE USES of AI tools in District educational settings include:
- Research assistance, information gathering, and idea generation
- Writing feedback, grammar review, and revision support
- Differentiated instruction and personalized learning pathways
- Accessibility accommodations for students with disabilities or language needs
- Administrative efficiency including scheduling, translation, and communications
- Professional development and educator planning support

UNACCEPTABLE USES of AI tools include:
- Submitting AI-generated work as original without required disclosure
- Using AI to complete standardized or high-stakes assessments
- Entering personally identifiable student information into non-approved AI systems
- Using AI outputs to make disciplinary, placement, or service decisions without human review
- Circumventing content filters, safety controls, or District procurement requirements

EQUITY REQUIREMENTS: The District shall ensure that AI tools do not exacerbate existing inequities. Access to approved AI tools shall be equitable across schools, grade levels, and student populations. The District shall monitor AI tool use patterns for disproportionate impact and report findings annually.""",
        "questions": [
            ("Have you identified specific AI tools approved for classroom use?", ["Yes, district registry exists", "Partial list exists", "Not yet compiled"]),
            ("Do grade-level guidelines exist for student AI use?", ["Yes, K-12 differentiated", "Yes, general guidelines only", "In development", "Not yet"]),
            ("Has the District assessed AI equity implications?", ["Yes, formal assessment completed", "Informal review only", "Not yet assessed"]),
        ]
    },
    "C": {
        "title": "Data Privacy",
        "anchor": "33328.5(d)(4)(C)",
        "description": "FERPA, CCPA, and SOPIPA compliance framework. Data use agreements, vendor certification, and breach protocols.",
        "model_language": """The District shall ensure all AI tools used in educational settings comply with:
- Family Educational Rights and Privacy Act (FERPA), 20 U.S.C. § 1232g
- California Consumer Privacy Act (CCPA), Civil Code § 1798.100 et seq.
- Student Online Personal Information Protection Act (SOPIPA), Education Code § 22584
- Children's Online Privacy Protection Act (COPPA) where applicable

PRIOR TO DEPLOYING any AI tool that processes student or educator data, the District shall:
1. Conduct a documented privacy impact assessment.
2. Execute a Data Use Agreement (DUA) with the vendor that prohibits use of student data to train AI models.
3. Verify the vendor's compliance certifications are current.
4. Confirm data retention periods and deletion protocols.
5. Identify the District staff member responsible for ongoing vendor oversight.

The District shall maintain a log of all executed DUAs, accessible to the County Superintendent and auditors upon request. Breach notification procedures shall follow existing District policy and applicable California law.""",
        "questions": [
            ("Does your District have a DUA template for AI vendors?", ["Yes, current template on file", "Using a general template", "No template exists"]),
            ("Have privacy assessments been conducted for current AI tools?", ["Yes, all current tools assessed", "Some tools assessed", "Not yet conducted"]),
            ("Is there a defined process for reviewing new AI tool requests?", ["Yes, formal approval process", "Informal review process", "No defined process"]),
        ]
    },
    "D": {
        "title": "Parent & Guardian Access",
        "anchor": "33328.5(d)(4)(D)",
        "description": "Notification requirements, opt-out processes, and parent rights to access AI interaction information.",
        "model_language": """Parents and guardians shall have the right to:
1. Be notified of AI tools used in their child's educational program, including the purpose of each tool and the categories of data collected.
2. Access, upon written request, a summary of information their child has entered into AI systems operated by or contracted with the District.
3. Request that their child be opted out of non-essential AI tool use without academic penalty.
4. Receive plain-language explanations of how AI tools affect their child's learning environment.
5. Review any AI-generated assessments, recommendations, or reports about their child before they become part of the student's educational record.

The District shall provide annual notification to all parents and guardians identifying the AI tools in active use across the District, updated within 30 days of any new tool deployment. Notification shall be provided in the primary languages of the District's student population.

Opt-out requests shall be processed within ten (10) school days. The District shall designate a Privacy Officer as the point of contact for parent inquiries under this section.""",
        "questions": [
            ("Does the District have an annual AI tool notification process for parents?", ["Yes, established process", "Included in general technology notice", "Not yet established"]),
            ("Can parents access their child's AI interaction history?", ["Yes, on request", "Working on process", "Not yet possible"]),
            ("Is there a documented opt-out process for non-essential AI tools?", ["Yes, formal process", "Informal accommodation available", "Not yet defined"]),
        ]
    },
    "E": {
        "title": "Procurement",
        "anchor": "33328.5(d)(4)(E)",
        "description": "Vendor vetting standards, contract provisions, AI tool registry, and annual review cycles.",
        "model_language": """PROCUREMENT STANDARDS: Prior to procuring any AI-enabled software, the District shall:
1. Verify current vendor compliance with California student data privacy laws and obtain written confirmation.
2. Review the vendor's AI ethics, bias mitigation, and model transparency documentation.
3. Ensure the contract includes: data ownership provisions confirming District retains ownership of all student data; deletion provisions requiring data deletion within 60 days of contract termination; prohibition on use of student data to train AI models; and indemnification for data breach costs.
4. Confirm the tool has been evaluated for age-appropriateness and educational efficacy.
5. Document the specific educational purpose, expected outcomes, and success metrics.
6. Establish an annual review cycle for continued use authorization.

AI TOOL REGISTRY: The District shall maintain a current registry of all approved AI tools including: vendor name and contact; tool name and version; educational purpose; data categories accessed; applicable privacy certifications and expiration dates; DUA execution date; annual renewal date; and designated District contact. The registry shall be reviewed and updated at the start of each school year and whenever a new tool is approved or an existing tool is discontinued.""",
        "questions": [
            ("Does the District have a formal AI tool vetting process?", ["Yes, formal written process", "Informal review only", "Not yet defined"]),
            ("Is there a centralized AI tool registry?", ["Yes, current and maintained", "Partial list exists", "Not yet created"]),
            ("Are AI vendor contracts reviewed for data privacy provisions?", ["Yes, by legal counsel", "Reviewed internally", "Not routinely reviewed"]),
        ]
    },
    "F": {
        "title": "Human Oversight & Professional Development",
        "anchor": "33328.5(d)(4)(F), (G), (I)",
        "description": "Human review requirements before AI affects student decisions. PD standards and effectiveness evaluation.",
        "model_language": """HUMAN OVERSIGHT REQUIREMENTS: No AI-generated output shall be used as the sole basis for any decision affecting a student's:
- Special education eligibility, Individualized Education Program, or related services
- Disciplinary action, suspension, or expulsion
- Grade-level placement, advancement, or retention
- Academic intervention or support service assignment
- College, career, or postsecondary guidance

A qualified educator or administrator shall review all relevant AI outputs and document their independent professional judgment before any such decision is made or communicated to the student or family.

PROFESSIONAL DEVELOPMENT: The District shall provide annual professional development for certificated staff on: effective integration of approved AI tools into instruction; recognition of AI bias and limitation; applicable legal requirements under this policy; student data privacy obligations; and critical evaluation of AI-generated content. PD hours dedicated to AI literacy shall be reported in the District's annual report to the Board.

EFFECTIVENESS EVALUATION: The District shall conduct an annual evaluation of AI tools in use to assess educational efficacy, equity of impact across student subgroups, and alignment with this policy. Findings shall be presented to the Board of Education and posted on the District website.""",
        "questions": [
            ("Is human review required before AI outputs affect student decisions?", ["Yes, formal written requirement", "Yes, informal practice", "Not formally required"]),
            ("Do educators receive professional development on AI tools?", ["Yes, annual formal PD", "Ad hoc training only", "Not yet provided"]),
            ("Does the District evaluate AI tool effectiveness and equity impact?", ["Yes, annual formal evaluation", "Informal review only", "Not yet conducted"]),
        ]
    }
}

# ============================================================
# SESSION STATE
# ============================================================
def init_state():
    defaults = {
        'screen': 'landing',
        'path': None,
        'district': {},
        'responses': {k: {} for k in MODULES},
        'custom': {k: "" for k in MODULES},
        'complete': {k: False for k in MODULES},
        'current_module': None,
        'generated': False,
        'adoption': {},
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

# ============================================================
# CSS
# ============================================================
def inject_css():
    st.markdown(f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Lato:wght@300;400;700&display=swap');

        html, body, [class*="css"] {{
            font-family: 'Lato', 'Segoe UI', sans-serif;
        }}
        .stApp {{ background-color: {COMPLY_LIGHT}; }}

        .comply-hero {{
            background: linear-gradient(135deg, {COMPLY_BLUE} 0%, {COMPLY_DARK} 100%);
            padding: 48px 40px 40px;
            color: #fff;
            margin-bottom: 24px;
        }}
        .comply-hero-eyebrow {{
            font-size: 0.75rem;
            letter-spacing: 4px;
            text-transform: uppercase;
            color: {COMPLY_GOLD};
            font-weight: 700;
            margin-bottom: 12px;
        }}
        .comply-hero h1 {{
            font-size: 2.4rem;
            font-weight: 300;
            color: #fff;
            line-height: 1.2;
            margin-bottom: 14px;
        }}
        .comply-hero h1 strong {{ font-weight: 700; }}
        .comply-hero p {{
            font-size: 1.05rem;
            color: rgba(255,255,255,0.88);
            line-height: 1.85;
            max-width: 760px;
        }}

        .comply-card {{
            background: #fff;
            border: 1px solid #e0e0e0;
            border-top: 4px solid {COMPLY_BLUE};
            padding: 28px;
            margin-bottom: 18px;
        }}
        .comply-card.gold {{ border-top-color: {COMPLY_GOLD}; }}
        .comply-card h3 {{
            font-size: 1.15rem;
            color: {COMPLY_BLUE};
            margin-bottom: 10px;
            font-weight: 700;
        }}
        .comply-card.gold h3 {{ color: #7a6000; }}
        .comply-card p {{ color: #555; font-size: 0.97rem; line-height: 1.8; }}

        .module-badge {{
            display: inline-block;
            background: {COMPLY_BLUE};
            color: #fff;
            width: 34px;
            height: 34px;
            line-height: 34px;
            text-align: center;
            font-weight: 700;
            font-size: 1rem;
            margin-bottom: 10px;
        }}
        .anchor-tag {{
            font-size: 0.78rem;
            color: {COMPLY_GOLD};
            font-style: italic;
            margin-top: 8px;
        }}
        .status-complete {{
            color: #1a7a3c;
            font-weight: 700;
            font-size: 0.85rem;
        }}
        .status-pending {{
            color: #888;
            font-size: 0.85rem;
        }}

        .comply-section-header {{
            border-left: 5px solid {COMPLY_BLUE};
            padding-left: 16px;
            margin-bottom: 24px;
        }}
        .comply-section-header h2 {{
            font-size: 1.6rem;
            font-weight: 700;
            color: {COMPLY_BLUE};
            margin: 0;
        }}
        .comply-section-header p {{
            color: #666;
            margin: 4px 0 0;
            font-size: 0.95rem;
        }}

        .model-policy-box {{
            background: #f0f4fa;
            border-left: 4px solid {COMPLY_BLUE};
            padding: 20px 24px;
            font-size: 0.95rem;
            line-height: 1.85;
            color: #333;
            white-space: pre-wrap;
            margin-bottom: 20px;
        }}

        .stButton > button {{
            background-color: {COMPLY_BLUE};
            color: #fff;
            border: none;
            font-weight: 600;
            letter-spacing: 0.5px;
        }}
        .stButton > button:hover {{
            background-color: {COMPLY_DARK};
            color: #fff;
        }}
        .stButton > button[kind="secondary"] {{
            background-color: #fff;
            color: {COMPLY_BLUE};
            border: 2px solid {COMPLY_BLUE};
        }}

        .progress-bar-outer {{
            background: #e0e0e0;
            height: 8px;
            width: 100%;
            margin: 8px 0 20px;
        }}
        .progress-bar-inner {{
            background: {COMPLY_GOLD};
            height: 8px;
        }}

        .output-artifact {{
            background: #fff;
            border: 2px solid {COMPLY_BLUE};
            padding: 32px;
            margin-top: 20px;
        }}
        .output-artifact h3 {{
            color: {COMPLY_BLUE};
            font-size: 1.2rem;
            margin-bottom: 16px;
        }}
        .checklist-item {{
            padding: 8px 0 8px 28px;
            position: relative;
            border-bottom: 1px solid #f0f0f0;
            font-size: 0.97rem;
            color: #333;
        }}
        .checklist-item:before {{
            content: "✓";
            position: absolute;
            left: 0;
            color: {COMPLY_GOLD};
            font-weight: 700;
        }}

        footer {{ display: none; }}
    </style>
    """, unsafe_allow_html=True)

# ============================================================
# SCREENS
# ============================================================

def screen_landing():
    st.markdown(f"""
    <div class="comply-hero">
        <div class="comply-hero-eyebrow">COMPLY SB 1288 &nbsp;·&nbsp; California School Districts</div>
        <h1>From no policy to <strong>board-ready AI governance</strong><br>in a single guided session.</h1>
        <p>COMPLY walks every California LEA through a six-module workflow that satisfies every
        requirement of Education Code 33328.5 and produces a complete, board-ready AI policy
        document formatted for direct GAMUT integration.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### How would you like to begin?")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"""
        <div class="comply-card">
            <h3>Path A &mdash; Current GAMUT Subscriber</h3>
            <p>Your district already uses CSBA's GAMUT platform. We will confirm your account
            details and allow you to upload existing board policies, acceptable use agreements,
            or AI guidance documents. COMPLY will reconcile your existing language against
            SB 1288 requirements module by module.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Begin as GAMUT District", use_container_width=True):
            st.session_state.path = "GAMUT"
            st.session_state.screen = "district_info"
            st.rerun()

    with col2:
        st.markdown(f"""
        <div class="comply-card gold">
            <h3>Path B &mdash; COMPLY Only</h3>
            <p>Your district is not yet on GAMUT. Enter your district information and proceed
            directly into the six-module workflow. CSBA model policy language is your default
            starting position. Your completed policy is formatted for GAMUT integration
            when you are ready.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Begin as COMPLY District", use_container_width=True):
            st.session_state.path = "COMPLY_ONLY"
            st.session_state.screen = "district_info"
            st.rerun()

    st.divider()
    st.markdown(f"""
    <p style="color:#888; font-size:0.88rem;">
    COMPLY SB 1288 addresses Education Code 33328.5(d)(4) items (A) through (I).
    Distributed by CSBA as GAMUT PLUS &nbsp;·&nbsp; Powered by
    <a href="https://h-edu.solutions" style="color:{COMPLY_BLUE};">H-EDU.solutions</a>
    &nbsp;·&nbsp; Questions: <a href="mailto:brian@h-edu.solutions" style="color:{COMPLY_BLUE};">brian@h-edu.solutions</a>
    </p>
    """, unsafe_allow_html=True)


def screen_district_info():
    path_label = "GAMUT Subscriber" if st.session_state.path == "GAMUT" else "COMPLY Only"

    st.markdown(f"""
    <div class="comply-section-header">
        <h2>District Information</h2>
        <p>Path {path_label} &nbsp;·&nbsp; Step 1 of 8</p>
    </div>
    """, unsafe_allow_html=True)

    if st.session_state.path == "GAMUT":
        st.info("Enter your district details below. For verified GAMUT subscribers, account information will be confirmed with CSBA records.")

    col1, col2 = st.columns(2)
    d = st.session_state.district

    with col1:
        name = st.text_input("District Name *", value=d.get("name", ""))
        cds = st.text_input("CDS Code", value=d.get("cds", ""), help="7-digit California Department of Education district identifier")
        contact_name = st.text_input("Primary Contact Name *", value=d.get("contact_name", ""))
        contact_title = st.text_input("Title / Role", value=d.get("contact_title", ""))

    with col2:
        county = st.selectbox("County *", options=[""] + [
            "Alameda","Alpine","Amador","Butte","Calaveras","Colusa","Contra Costa",
            "Del Norte","El Dorado","Fresno","Glenn","Humboldt","Imperial","Inyo",
            "Kern","Kings","Lake","Lassen","Los Angeles","Madera","Marin","Mariposa",
            "Mendocino","Merced","Modoc","Mono","Monterey","Napa","Nevada","Orange",
            "Placer","Plumas","Riverside","Sacramento","San Benito","San Bernardino",
            "San Diego","San Francisco","San Joaquin","San Luis Obispo","San Mateo",
            "Santa Barbara","Santa Clara","Santa Cruz","Shasta","Sierra","Siskiyou",
            "Solano","Sonoma","Stanislaus","Sutter","Tehama","Trinity","Tulare",
            "Tuolumne","Ventura","Yolo","Yuba"
        ], index=0 if not d.get("county") else None)
        enrollment = st.number_input("Student Enrollment", min_value=0, value=d.get("enrollment", 0))
        contact_email = st.text_input("Contact Email *", value=d.get("contact_email", ""))
        board_secretary = st.text_input("Board Secretary / Policy Officer", value=d.get("board_secretary", ""))

    if st.session_state.path == "GAMUT":
        gamut_id = st.text_input("GAMUT Account ID (if known)", value=d.get("gamut_id", ""))
    else:
        gamut_id = ""

    col_a, col_b = st.columns([1, 4])
    with col_a:
        if st.button("Save & Continue", type="primary"):
            if not name or not contact_name or not contact_email:
                st.error("District name, contact name, and email are required.")
            else:
                st.session_state.district = {
                    "name": name, "cds": cds, "county": county,
                    "enrollment": enrollment, "contact_name": contact_name,
                    "contact_title": contact_title, "contact_email": contact_email,
                    "board_secretary": board_secretary, "gamut_id": gamut_id,
                    "path": st.session_state.path,
                    "started_at": datetime.now().isoformat()
                }
                st.session_state.screen = "dashboard"
                st.session_state.current_module = "A"
                st.rerun()
    with col_b:
        if st.button("← Back", type="secondary"):
            st.session_state.screen = "landing"
            st.rerun()


def screen_dashboard():
    d = st.session_state.district
    completed = sum(1 for v in st.session_state.complete.values() if v)
    total = len(MODULES)
    pct = int((completed / total) * 100)

    st.markdown(f"""
    <div class="comply-hero">
        <div class="comply-hero-eyebrow">COMPLY SB 1288 &nbsp;·&nbsp; Compliance Dashboard</div>
        <h1><strong>{d.get('name', 'Your District')}</strong></h1>
        <p>{d.get('county', '')} County &nbsp;·&nbsp; Enrollment: {d.get('enrollment', 0):,}
        &nbsp;·&nbsp; Contact: {d.get('contact_name', '')}</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"**Progress: {completed} of {total} modules complete ({pct}%)**")
    st.markdown(f"""
    <div class="progress-bar-outer">
        <div class="progress-bar-inner" style="width:{pct}%"></div>
    </div>
    """, unsafe_allow_html=True)

    cols = st.columns(3)
    module_keys = list(MODULES.keys())
    for i, key in enumerate(module_keys):
        mod = MODULES[key]
        is_complete = st.session_state.complete[key]
        with cols[i % 3]:
            st.markdown(f"""
            <div class="comply-card {'gold' if is_complete else ''}">
                <span class="module-badge">{key}</span>
                <h3>{mod['title']}</h3>
                <p>{mod['description']}</p>
                <p class="anchor-tag">{mod['anchor']}</p>
                <p class="{'status-complete' if is_complete else 'status-pending'}">
                    {'✓ Complete' if is_complete else '○ Pending'}
                </p>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"{'Review' if is_complete else 'Begin'} Module {key}", key=f"dash_{key}", use_container_width=True):
                st.session_state.current_module = key
                st.session_state.screen = "module"
                st.rerun()

    st.divider()

    if completed == total:
        st.success("All six modules complete. You may now generate your board-ready policy document.")
        if st.button("Generate Policy Document & Artifact Set", type="primary"):
            st.session_state.screen = "generate"
            st.rerun()
    else:
        remaining = [k for k in module_keys if not st.session_state.complete[k]]
        if remaining:
            if st.button(f"Continue → Module {remaining[0]}: {MODULES[remaining[0]]['title']}", type="primary"):
                st.session_state.current_module = remaining[0]
                st.session_state.screen = "module"
                st.rerun()


def screen_module():
    key = st.session_state.current_module
    mod = MODULES[key]
    module_keys = list(MODULES.keys())
    idx = module_keys.index(key)

    st.markdown(f"""
    <div class="comply-section-header">
        <h2>Module {key}: {mod['title']}</h2>
        <p>{mod['anchor']} &nbsp;·&nbsp; {mod['description']}</p>
    </div>
    """, unsafe_allow_html=True)

    # Model policy language
    st.markdown("**Model Policy Language (CSBA)**")
    st.markdown(f'<div class="model-policy-box">{mod["model_language"]}</div>', unsafe_allow_html=True)

    # Assessment questions
    st.markdown("**Current Status Assessment**")
    responses = st.session_state.responses[key]
    for i, (question, options) in enumerate(mod["questions"]):
        col1, col2 = st.columns([3, 2])
        with col1:
            st.write(question)
        with col2:
            current = responses.get(f"q{i}", options[0])
            idx_opt = options.index(current) if current in options else 0
            response = st.selectbox(
                f"q{i}", options=options, index=idx_opt,
                key=f"mod_{key}_q{i}", label_visibility="collapsed"
            )
            responses[f"q{i}"] = response
    st.session_state.responses[key] = responses

    # District customization
    st.markdown("**District-Specific Language** *(optional — enter additions or modifications to the model language above)*")
    custom = st.text_area(
        "custom", value=st.session_state.custom.get(key, ""),
        height=140, key=f"custom_{key}", label_visibility="collapsed"
    )
    st.session_state.custom[key] = custom

    st.divider()

    col_prev, col_complete, col_next = st.columns([1, 2, 1])

    with col_prev:
        if idx > 0:
            prev_key = module_keys[idx - 1]
            if st.button(f"← Module {prev_key}"):
                st.session_state.current_module = prev_key
                st.rerun()

    with col_complete:
        label = "✓ Mark Complete & Continue" if idx < len(module_keys) - 1 else "✓ Mark Complete"
        if st.button(label, type="primary", use_container_width=True):
            st.session_state.complete[key] = True
            if idx < len(module_keys) - 1:
                st.session_state.current_module = module_keys[idx + 1]
                st.rerun()
            else:
                st.session_state.screen = "dashboard"
                st.rerun()

    with col_next:
        if idx < len(module_keys) - 1:
            next_key = module_keys[idx + 1]
            if st.button(f"Module {next_key} →"):
                st.session_state.current_module = next_key
                st.rerun()

    st.markdown("&nbsp;")
    if st.button("← Back to Dashboard"):
        st.session_state.screen = "dashboard"
        st.rerun()


def screen_generate():
    d = st.session_state.district
    now = datetime.now()

    st.markdown(f"""
    <div class="comply-section-header">
        <h2>Review &amp; Generate</h2>
        <p>All six modules complete &nbsp;·&nbsp; {d.get('name', '')} &nbsp;·&nbsp; {now.strftime('%B %d, %Y')}</p>
    </div>
    """, unsafe_allow_html=True)

    # Artifact preview
    st.markdown(f"""
    <div class="output-artifact">
        <h3>COMPLY SB 1288 &mdash; Artifact Set</h3>
        <div class="checklist-item">Board-ready AI governance policy document (.docx format for board adoption)</div>
        <div class="checklist-item">CSBA board policy format: BP heading, section text, legal references, revision history</div>
        <div class="checklist-item">District customizations integrated with CSBA model language</div>
        <div class="checklist-item">FERPA / CCPA / SOPIPA compliance certifications with timestamps</div>
        <div class="checklist-item">Parent notification template in plain English</div>
        <div class="checklist-item">AI Tool Registry (.xlsx) pre-populated from Module E responses</div>
        <div class="checklist-item">Procurement documentation for COE and auditor review</div>
        <div class="checklist-item">Statutory audit trail: section-by-section against 33328.5(d)(4)(A)–(I)</div>
        <div class="checklist-item">GAMUT ingestion payload (JSON) for direct policy library integration</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("&nbsp;")

    # Build policy document text
    policy_lines = [
        "=" * 80,
        "                    ARTIFICIAL INTELLIGENCE GOVERNANCE POLICY",
        "                    COMPLY SB 1288 — Board-Ready Document",
        "=" * 80,
        "",
        f"DISTRICT:     {d.get('name', '')}",
        f"COUNTY:       {d.get('county', '')}",
        f"CDS CODE:     {d.get('cds', 'Not provided')}",
        f"ENROLLMENT:   {d.get('enrollment', 0):,}",
        f"CONTACT:      {d.get('contact_name', '')} · {d.get('contact_email', '')}",
        f"GENERATED:    {now.strftime('%B %d, %Y at %H:%M')}",
        f"COMPLY RUN:   {now.strftime('%Y%m%d%H%M%S')}-{d.get('cds', 'XX')}",
        "",
        "Statutory basis: California Education Code 33328.5 (SB 1288, Becker, 2024)",
        "Distributed by CSBA as GAMUT PLUS · Powered by H-EDU.solutions",
        "",
    ]

    for key, mod in MODULES.items():
        policy_lines += [
            "=" * 80,
            f"MODULE {key}: {mod['title'].upper()}",
            f"Statutory anchor: {mod['anchor']}",
            "=" * 80,
            "",
        ]
        lang = st.session_state.custom.get(key, "").strip()
        if lang:
            policy_lines += [lang, "", "--- CSBA Model Language (supplemental) ---", "", mod["model_language"].strip(), ""]
        else:
            policy_lines += [mod["model_language"].strip(), ""]

        # Assessment responses
        policy_lines.append("Current Status Assessment:")
        for i, (question, _) in enumerate(mod["questions"]):
            resp = st.session_state.responses[key].get(f"q{i}", "Not answered")
            policy_lines.append(f"  · {question}")
            policy_lines.append(f"    Response: {resp}")
        policy_lines.append("")

    policy_lines += [
        "=" * 80,
        "CERTIFICATION",
        "=" * 80,
        "",
        "This policy document has been developed in compliance with California",
        "Education Code 33328.5 (SB 1288) and CSBA model policy guidance.",
        "",
        f"Generated by COMPLY SB 1288 · H-EDU.solutions",
        f"Timestamp: {now.isoformat()}",
        "",
        "The district's board-adopted final version, once captured, supersedes",
        "this generated draft as the policy of record.",
        "=" * 80,
    ]

    policy_text = "\n".join(policy_lines)

    st.text_area("Policy Document Preview", value=policy_text, height=400)

    col1, col2 = st.columns(2)
    with col1:
        st.download_button(
            label="Download Policy Document (.txt)",
            data=policy_text,
            file_name=f"COMPLY_SB1288_{d.get('name','District').replace(' ','_')}_{now.strftime('%Y%m%d')}.txt",
            mime="text/plain",
            use_container_width=True
        )
    with col2:
        if st.button("← Back to Dashboard", use_container_width=True):
            st.session_state.screen = "dashboard"
            st.rerun()

    st.divider()
    st.markdown("**Board Adoption Follow-Up**")
    st.info("Once your board adopts this policy, return here to record the adoption date and upload the final adopted version. This completes the COMPLY SB 1288 cycle and triggers GAMUT integration.")

    with st.expander("Record Board Adoption"):
        adop = st.session_state.adoption
        adoption_date = st.date_input("Board Adoption Date", value=adop.get("adoption_date", date.today()))
        first_reading = st.date_input("First Reading Date", value=adop.get("first_reading", date.today()))
        effective_date = st.date_input("Effective Date", value=adop.get("effective_date", date.today()))
        next_review = st.date_input("Next Scheduled Review Date", value=adop.get("next_review", date(date.today().year + 1, 7, 1)))
        notes = st.text_area("Amendment notes (what changed from generated to adopted version)", value=adop.get("notes", ""), height=80)

        if st.button("Save Adoption Record", type="primary"):
            st.session_state.adoption = {
                "adoption_date": adoption_date,
                "first_reading": first_reading,
                "effective_date": effective_date,
                "next_review": next_review,
                "notes": notes,
                "recorded_at": datetime.now().isoformat()
            }
            st.success(f"Adoption recorded. Policy of record: {d.get('name', '')} AI Governance Policy, adopted {adoption_date}. Next review: {next_review}.")


# ============================================================
# SIDEBAR
# ============================================================
def render_sidebar():
    with st.sidebar:
        st.markdown(f"""
        <div style="padding: 16px 0 8px;">
            <div style="font-size:1.4rem; font-weight:700; letter-spacing:2px; color:{COMPLY_BLUE};">
                COMPLY<span style="color:{COMPLY_GOLD};">.</span>
            </div>
            <div style="font-size:0.78rem; color:#888; letter-spacing:1px; text-transform:uppercase; margin-top:2px;">
                SB 1288
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.divider()

        if st.button("Dashboard", use_container_width=True):
            st.session_state.screen = "dashboard"
            st.rerun()

        st.markdown("**Modules**")
        for key, mod in MODULES.items():
            is_complete = st.session_state.complete.get(key, False)
            label = f"{'✓' if is_complete else '○'} {key}: {mod['title']}"
            if st.button(label, key=f"sb_{key}", use_container_width=True):
                st.session_state.current_module = key
                st.session_state.screen = "module"
                st.rerun()

        st.divider()

        completed = sum(1 for v in st.session_state.complete.values() if v)
        if completed == len(MODULES):
            if st.button("Generate Documents", type="primary", use_container_width=True):
                st.session_state.screen = "generate"
                st.rerun()

        st.markdown(f"""
        <div style="font-size:0.78rem; color:#aaa; margin-top:16px; line-height:1.7;">
            COMPLY SB 1288 v2.0<br>
            H-EDU.solutions<br>
            <a href="mailto:brian@h-edu.solutions" style="color:{COMPLY_BLUE};">Get Help</a>
        </div>
        """, unsafe_allow_html=True)


# ============================================================
# MAIN
# ============================================================
def main():
    st.set_page_config(
        page_title="COMPLY SB 1288",
        page_icon="C",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    inject_css()
    init_state()

    screen = st.session_state.screen

    if screen == "landing":
        screen_landing()
    elif screen == "district_info":
        render_sidebar()
        screen_district_info()
    elif screen == "dashboard":
        render_sidebar()
        screen_dashboard()
    elif screen == "module":
        render_sidebar()
        screen_module()
    elif screen == "generate":
        render_sidebar()
        screen_generate()


if __name__ == "__main__":
    main()
