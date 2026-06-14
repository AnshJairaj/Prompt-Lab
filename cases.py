"""
All 5 corporate business cases for the AI Prompt Engineering Lab.
"""

CASES = [
    # ── CASE 1: L&D ─────────────────────────────────────────────────────────
    {
        "icon": "🎓",
        "title": "Learning & Development",
        "subtitle": "Personalized AI Learning Roadmap Generator",
        "department": "HR · L&D",
        "difficulty": "Medium",
        "tags": ["Skill Analysis", "Gap Identification", "Learning Roadmap", "Career Planning", "Course Recommendation"],
        "business_case": (
            "Tata Steel is undergoing a digital transformation, and the Learning & Development team "
            "needs an intelligent assistant that can evaluate an employee's current skill set, identify "
            "gaps relative to their target role in Generative AI, and create a structured, time-bound "
            "learning roadmap with recommended certifications and hands-on project ideas."
        ),
        "scenario": (
            "Ramesh Kumar, a mechanical engineer with 5 years at Tata Steel, wants to transition into a "
            "Generative AI-related role. He knows Python basics and has some SQL experience but has never "
            "worked with ML frameworks. The L&D head wants an AI tool to assess Ramesh's skills and create "
            "a realistic 6-month roadmap."
        ),
        "objectives": [
            "Analyze the employee's current skills and experience level",
            "Identify specific skill gaps for the target GenAI role",
            "Create a structured, time-bound learning roadmap (week-by-week or month-by-month)",
            "Recommend relevant online courses, books, and certifications",
            "Suggest hands-on project ideas for practical experience",
            "Provide estimated time commitment per week",
        ],
        "inputs": [
            "Employee current skills list",
            "Target role / job description",
            "Time available per week",
            "Current experience level",
            "Learning style preferences",
            "Budget constraints",
        ],
        "expected_output": [
            "Skill Gap Analysis table (current vs. required)",
            "Priority-ranked list of skills to develop",
            "Month-wise Learning Roadmap",
            "Recommended courses with platform & duration",
            "Suggested certification path",
            "3–5 project ideas with increasing complexity",
            "Estimated total time investment",
        ],
        "starter_prompt": (
            "You are an expert Learning & Development advisor specializing in AI/ML career transitions.\n\n"
            "**Employee Profile:**\n"
            "- Name: [Employee Name]\n"
            "- Current Role: [Role]\n"
            "- Current Skills: [List skills]\n"
            "- Target Role: [Target GenAI role]\n"
            "- Time available: [X hours/week]\n\n"
            "**Task:** Please do the following:\n"
            "1. Analyze the employee's current skills vs. what's required for the target role\n"
            "2. Create a detailed skill gap analysis\n"
            "3. Build a 6-month learning roadmap (month by month)\n"
            "4. Recommend top 5 courses/certifications with platform names\n"
            "5. Suggest 3 progressive project ideas\n\n"
            "Format your response with clear headers, tables where appropriate, and be specific."
        ),
        "sample_context": (
            "Employee: Ramesh Kumar | Current Role: Mechanical Engineer, 5 years\n"
            "Current Skills: Python (basic), SQL (intermediate), Excel, AutoCAD\n"
            "Target Role: AI/ML Engineer\n"
            "Time: 10 hours/week | Budget: Free/low-cost courses preferred"
        ),
    },

    # ── CASE 2: RECRUITMENT ──────────────────────────────────────────────────
    {
        "icon": "👥",
        "title": "Recruitment & Talent Acquisition",
        "subtitle": "AI-Powered Resume Screening & Candidate Ranking",
        "department": "HR · Talent Acquisition",
        "difficulty": "High",
        "tags": ["Resume Screening", "Candidate Ranking", "Skill Matching", "JD Analysis", "Interview Questions"],
        "business_case": (
            "The HR department at Tata Steel has received 300+ applications for a Data Scientist position. "
            "Manual screening is time-consuming and inconsistent. The recruitment team needs an AI assistant "
            "to screen resumes against the job description, rank candidates objectively, identify strengths "
            "and weaknesses, and generate tailored interview questions for shortlisted candidates."
        ),
        "scenario": (
            "The Analytics & Digital team is hiring a Senior Data Scientist. The role requires expertise in "
            "Python, machine learning, SQL, and experience in manufacturing or industrial data analysis. "
            "The recruiter, Priya Sharma, needs to shortlist the top 5 from 300 resumes by end of week."
        ),
        "objectives": [
            "Screen resumes against specific job requirements",
            "Score and rank candidates on a standardized scale",
            "Identify skill matches and gaps for each candidate",
            "Highlight red flags or concerns in applications",
            "Generate role-specific interview questions per candidate",
            "Provide a final hiring recommendation with justification",
        ],
        "inputs": [
            "Candidate resume / CV",
            "Job description (JD)",
            "Required skills and qualifications",
            "Years of experience required",
            "Company culture & team fit notes",
            "Salary band (optional)",
        ],
        "expected_output": [
            "Match Score out of 100",
            "Skill-by-skill analysis table",
            "Top 3 Strengths of the candidate",
            "Top 3 Weaknesses / Gaps",
            "5–7 tailored interview questions",
            "Shortlist Recommendation: YES / MAYBE / NO with reason",
        ],
        "starter_prompt": (
            "You are an expert HR recruiter and talent acquisition specialist.\n\n"
            "**Job Description Summary:**\n[Paste JD here]\n\n"
            "**Candidate Resume:**\n[Paste resume here]\n\n"
            "**Instructions:**\n"
            "Evaluate this candidate and provide:\n"
            "1. Match Score (/100) with scoring breakdown\n"
            "2. Skills analysis: What matches vs. what's missing\n"
            "3. Top 3 strengths and top 3 weaknesses\n"
            "4. 5 tailored interview questions based on their background\n"
            "5. Clear hiring recommendation with justification\n\n"
            "Use tables for the skill analysis. Be objective and evidence-based."
        ),
        "sample_context": (
            "JD: Senior Data Scientist | Required: Python, SQL, ML (scikit-learn/TensorFlow), 4+ years, "
            "manufacturing domain preferred\n\n"
            "Resume: Ankit Verma | 5 years exp | Python (Expert), SQL (Advanced), "
            "TensorFlow, Keras | Previous: Infosys (FMCG analytics) | B.Tech CS | "
            "Projects: Demand forecasting, NLP chatbot | No manufacturing experience"
        ),
    },

    # ── CASE 3: PROCUREMENT ──────────────────────────────────────────────────
    {
        "icon": "🛒",
        "title": "Procurement & Vendor Selection",
        "subtitle": "AI Vendor Comparison & Best Supplier Recommendation",
        "department": "Finance · Procurement",
        "difficulty": "Medium",
        "tags": ["Vendor Analysis", "Cost Comparison", "Risk Assessment", "Warranty Evaluation", "Supplier Selection"],
        "business_case": (
            "Tata Steel's IT procurement team needs to purchase 100 laptops for new employees joining "
            "across three plants. Three vendors — Dell, Lenovo, and HP — have submitted quotations with "
            "different specifications, prices, warranty terms, and service agreements. The procurement "
            "officer needs AI help to objectively compare all options and recommend the best vendor."
        ),
        "scenario": (
            "Sunita Rao, Procurement Manager, has received three quotes totalling ₹45–52 lakhs for "
            "100 laptops. Management wants the decision in 48 hours. The requirements: i5/Ryzen 5 or "
            "above, 16GB RAM, 512GB SSD, Windows 11, 3-year warranty, onsite support within 24 hours."
        ),
        "objectives": [
            "Compare vendor quotations across all parameters",
            "Analyze total cost of ownership (TCO) including hidden costs",
            "Evaluate warranty period, terms, and SLA quality",
            "Assess vendor reliability and support reputation",
            "Identify risks in each option",
            "Recommend the best vendor with clear justification",
        ],
        "inputs": [
            "Vendor quotation details (price, specs, warranty)",
            "Company requirements / specifications",
            "Budget constraints",
            "Service level agreements (SLA)",
            "Vendor past performance data",
            "Delivery timeline requirements",
        ],
        "expected_output": [
            "Side-by-side comparison table of all vendors",
            "Total cost breakdown (unit + support + hidden costs)",
            "Warranty & SLA evaluation matrix",
            "Risk assessment for each vendor",
            "Score and ranking of vendors",
            "Final Recommendation: Best Vendor with reasoning",
            "Negotiation points / questions to ask vendors",
        ],
        "starter_prompt": (
            "You are a strategic procurement consultant with expertise in IT hardware sourcing.\n\n"
            "**Requirement:** 100 laptops for Tata Steel employees\n"
            "**Budget:** ₹50 lakhs maximum\n\n"
            "**Vendor Quotes:**\n[Paste vendor details here]\n\n"
            "**Task:** Analyze all vendors and provide:\n"
            "1. Comparative analysis table (specs, price, warranty, support)\n"
            "2. Total cost of ownership for each vendor\n"
            "3. Risk assessment (delivery, quality, support risks)\n"
            "4. Weighted score matrix (price 30%, specs 25%, warranty 25%, support 20%)\n"
            "5. Final recommendation with justification\n"
            "6. 3 negotiation points to use with the recommended vendor"
        ),
        "sample_context": (
            "Vendor A (Dell): ₹52,000/unit | i7-1255U | 16GB RAM | 512GB SSD | "
            "3yr onsite warranty | 24hr response | Delivery: 15 days\n\n"
            "Vendor B (Lenovo): ₹47,500/unit | Ryzen 5 7530U | 16GB RAM | 512GB SSD | "
            "3yr carry-in warranty | 48hr response | Delivery: 10 days\n\n"
            "Vendor C (HP): ₹49,000/unit | i5-1235U | 8GB RAM (upgradeable) | "
            "256GB SSD + 512GB HDD | 1yr onsite + 2yr parts | 24hr response | Delivery: 7 days"
        ),
    },

    # ── CASE 4: IT HELPDESK ──────────────────────────────────────────────────
    {
        "icon": "🖥️",
        "title": "IT Helpdesk Support",
        "subtitle": "AI-Powered VPN Troubleshooting & Escalation Assistant",
        "department": "IT · Service Desk",
        "difficulty": "Low",
        "tags": ["Troubleshooting", "Step-by-Step Diagnosis", "Root Cause Analysis", "Escalation Protocol", "User Guidance"],
        "business_case": (
            "Tata Steel's IT helpdesk receives 500+ tickets daily. A significant portion involves "
            "VPN connectivity issues from remote employees. The IT team wants an AI-powered first-level "
            "support assistant that can diagnose issues, guide employees through fixes, identify root "
            "causes, and escalate unresolved issues with a structured summary — reducing resolution time "
            "from 4 hours to under 30 minutes."
        ),
        "scenario": (
            "Mohan Singh, a finance analyst working from home in Delhi, cannot connect to the company "
            "VPN. He is using a Windows 11 laptop, Cisco AnyConnect VPN client, and a BSNL broadband "
            "connection. He reports the error: 'Unable to connect to VPN server.' This is happening "
            "since 9 AM and he has a critical deadline at 2 PM."
        ),
        "objectives": [
            "Diagnose the specific VPN connectivity issue",
            "Ask targeted, logical troubleshooting questions",
            "Provide step-by-step fix instructions in plain language",
            "Identify possible root causes (user error, network, server, config)",
            "Determine if self-resolution is possible or escalation is needed",
            "Generate an escalation ticket summary if unresolved",
        ],
        "inputs": [
            "Error message or description of the issue",
            "Employee OS and VPN client version",
            "Network type (broadband, mobile hotspot, etc.)",
            "Time issue started",
            "Previous troubleshooting steps tried",
            "Urgency level",
        ],
        "expected_output": [
            "Diagnostic questions to ask the user",
            "Probable root cause (from most to least likely)",
            "Step-by-step resolution guide (numbered, plain English)",
            "Self-check commands / actions for the user",
            "Decision: Resolved / Escalate to L2",
            "Escalation ticket summary (if unresolved) with all context",
        ],
        "starter_prompt": (
            "You are an expert IT support engineer specializing in enterprise VPN troubleshooting.\n\n"
            "**Issue Reported:**\n[Describe the VPN issue]\n\n"
            "**Employee Details:**\n"
            "- OS: [Windows/Mac version]\n"
            "- VPN Client: [Cisco AnyConnect/GlobalProtect/etc.]\n"
            "- Network: [Broadband/Hotspot]\n"
            "- Error Message: [Exact error]\n\n"
            "**Task:**\n"
            "1. Ask 3-5 clarifying questions to diagnose the issue\n"
            "2. List probable root causes (ranked by likelihood)\n"
            "3. Provide step-by-step troubleshooting instructions\n"
            "4. Decide: can the user fix this themselves?\n"
            "5. If not, generate a Level-2 escalation ticket summary\n\n"
            "Use numbered steps and simple, non-technical language for the user."
        ),
        "sample_context": (
            "User: Mohan Singh | Finance Analyst | Working from Home - Delhi\n"
            "OS: Windows 11 Home | VPN: Cisco AnyConnect v4.10\n"
            "Network: BSNL Broadband (50 Mbps) | ISP DNS\n"
            "Error: 'Connection attempt has timed out. Please verify internet connectivity.'\n"
            "Time: Issue since 9 AM | Steps tried: Restarted laptop once\n"
            "Urgency: HIGH - critical report due at 2 PM"
        ),
    },

    # ── CASE 5: LEAVE MANAGEMENT ─────────────────────────────────────────────
    {
        "icon": "📅",
        "title": "Leave Management & Workforce Planning",
        "subtitle": "AI Leave Approval Decision Support System",
        "department": "HR · Operations",
        "difficulty": "High",
        "tags": ["Leave Policy", "Team Availability", "Project Impact", "Risk Assessment", "Manager Decision Support"],
        "business_case": (
            "Tata Steel's HR system receives hundreds of leave requests daily. Managers struggle to "
            "balance employee welfare with project delivery timelines. An AI assistant is needed to "
            "help managers make fair, data-driven leave approval decisions by checking policy compliance, "
            "team availability, project impact, and staffing risks — and recommending approval or "
            "rejection with full justification."
        ),
        "scenario": (
            "Neha Gupta, a project lead on a critical ERP implementation, has applied for 10 days of "
            "leave (July 14–25). However, this coincides with the final testing phase of the ERP project "
            "(go-live: July 28). Her team has 4 members, one of whom is already on leave during this "
            "period. The project manager, Vikram, needs to decide by tomorrow."
        ),
        "objectives": [
            "Check if leave request complies with company leave policy",
            "Verify overall team availability during the requested period",
            "Assess the impact of the absence on ongoing projects",
            "Identify staffing risks and single points of failure",
            "Suggest alternatives (partial approval, remote work, handover plan)",
            "Recommend Approve / Approve with conditions / Reject with clear justification",
        ],
        "inputs": [
            "Employee leave request details (dates, type, reason)",
            "Leave policy document / summary",
            "Current team roster and availability",
            "Project timeline and milestone schedule",
            "Employee's current workload and responsibilities",
            "Available substitute resources",
        ],
        "expected_output": [
            "Policy Compliance Check: PASS / FAIL with explanation",
            "Team Availability Analysis during leave period",
            "Project Impact Assessment (Low / Medium / High / Critical)",
            "Risk Register: key risks if leave is approved",
            "Alternative Options (e.g., split leave, remote work)",
            "Final Recommendation: APPROVE / CONDITIONAL / REJECT",
            "Suggested conditions or handover requirements",
            "Communication draft for employee (email template)",
        ],
        "starter_prompt": (
            "You are an expert HR advisor and workforce planning specialist.\n\n"
            "**Leave Request:**\n"
            "- Employee: [Name] | Role: [Role]\n"
            "- Leave Type: [Annual/Sick/etc.] | Duration: [X days]\n"
            "- Dates: [Start date] to [End date]\n\n"
            "**Context:**\n"
            "- Project: [Project name] | Phase: [Current phase]\n"
            "- Go-live / Deadline: [Date]\n"
            "- Team size: [X members] | Members on leave: [Y]\n"
            "- Leave balance: [Z days]\n\n"
            "**Task:**\n"
            "1. Check policy compliance\n"
            "2. Analyze team availability and coverage\n"
            "3. Assess project impact (Low/Medium/High/Critical)\n"
            "4. Identify top 3 risks if approved\n"
            "5. Suggest 2 alternative arrangements\n"
            "6. Give final recommendation with justification\n"
            "7. Draft a brief email to the employee with the decision"
        ),
        "sample_context": (
            "Employee: Neha Gupta | Project Lead | 8 years experience\n"
            "Leave: Annual Leave | 10 days | July 14-25\n"
            "Reason: Family function (sister's wedding)\n"
            "Leave Balance: 18 days remaining\n\n"
            "Project: SAP ERP Implementation | Phase: Final UAT Testing\n"
            "Go-live: July 28 | Neha is the primary UAT coordinator\n"
            "Team: 4 members | 1 already on leave July 18-22\n"
            "No identified backup for Neha's UAT role"
        ),
    },
]
