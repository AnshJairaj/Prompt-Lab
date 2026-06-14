"""
Utility functions: prompt quality scoring, evaluation, and tips.
"""

import re


def score_prompt_quality(prompt: str, case: dict) -> dict:
    """
    Score a prompt across 5 criteria, each out of 20 → total /100.
    Returns dict with criteria breakdown and total.
    """
    prompt_lower = prompt.lower()
    words = prompt.split()
    word_count = len(words)

    # ── 1. Clarity & Specificity (20 pts) ─────────────────────────────────────
    clarity = 0
    if word_count >= 30: clarity += 5
    if word_count >= 80: clarity += 5
    if word_count >= 150: clarity += 5
    specific_words = ["specifically", "exactly", "must", "should", "ensure", "provide", "include", "format", "structure"]
    clarity += min(5, sum(1 for w in specific_words if w in prompt_lower))

    # ── 2. Role & Context Setting (20 pts) ────────────────────────────────────
    role_score = 0
    role_keywords = ["you are", "act as", "as an", "expert", "specialist", "advisor", "assistant", "role"]
    if any(kw in prompt_lower for kw in role_keywords):
        role_score += 10
    context_keywords = ["context", "background", "company", "tata", "organization", "department", "team"]
    if any(kw in prompt_lower for kw in context_keywords):
        role_score += 5
    if len(prompt) > 200:
        role_score += 5

    # ── 3. Task Definition (20 pts) ───────────────────────────────────────────
    task_score = 0
    task_indicators = ["task:", "instructions:", "do the following", "please", "analyze", "provide", "create", "generate", "evaluate", "compare", "recommend"]
    task_count = sum(1 for kw in task_indicators if kw in prompt_lower)
    task_score += min(10, task_count * 2)

    # Numbered instructions
    if re.search(r'\n\d+[\.\)]\s', prompt) or re.search(r'^\d+[\.\)]\s', prompt, re.MULTILINE):
        task_score += 5
    if any(kw in prompt_lower for kw in ["step by step", "numbered", "bullet", "list"]):
        task_score += 5

    # ── 4. Output Format Specification (20 pts) ───────────────────────────────
    output_score = 0
    format_keywords = ["output", "format", "response", "table", "summary", "report", "provide", "include", "return", "generate"]
    output_count = sum(1 for kw in format_keywords if kw in prompt_lower)
    output_score += min(10, output_count * 2)

    # Structure indicators
    if any(kw in prompt_lower for kw in ["header", "section", "structured", "organized", "clear"]):
        output_score += 5
    if any(kw in prompt_lower for kw in ["/100", "score", "rating", "rank", "recommendation"]):
        output_score += 5

    # ── 5. Completeness & Professional Quality (20 pts) ───────────────────────
    complete_score = 0
    # Case-specific keywords
    case_tags = [tag.lower() for tag in case.get("tags", [])]
    tag_matches = sum(1 for tag in case_tags if any(word in prompt_lower for word in tag.split()))
    complete_score += min(10, tag_matches * 2)

    # Tone / constraints
    if any(kw in prompt_lower for kw in ["professional", "formal", "concise", "brief", "detailed", "tone"]):
        complete_score += 5
    # Objective coverage
    objectives_hit = sum(
        1 for obj in case.get("objectives", [])
        if any(word.lower() in prompt_lower for word in obj.split()[:3])
    )
    complete_score += min(5, objectives_hit)

    total = clarity + role_score + task_score + output_score + complete_score

    return {
        "total": min(100, total),
        "criteria": {
            "Clarity & Specificity": min(20, clarity),
            "Role & Context Setting": min(20, role_score),
            "Task Definition": min(20, task_score),
            "Output Format": min(20, output_score),
            "Completeness": min(20, complete_score),
        }
    }


def evaluate_prompt(prompt: str, case: dict) -> str:
    """
    Return a short human-readable evaluation paragraph.
    """
    if not prompt.strip():
        return "No prompt provided yet."

    wc = len(prompt.split())
    has_role = any(kw in prompt.lower() for kw in ["you are", "act as", "expert", "specialist"])
    has_format = any(kw in prompt.lower() for kw in ["output", "format", "table", "provide"])
    has_numbered = bool(re.search(r'\n?\d+[\.\)]\s', prompt))
    has_context = len(prompt) > 150

    parts = []

    if wc < 30:
        parts.append("⚠️ <b>Too brief:</b> Your prompt is only {wc} words. Effective prompts typically need at least 80–150 words to give the AI enough guidance.".format(wc=wc))
    elif wc < 80:
        parts.append(f"📏 <b>Length:</b> Your prompt has {wc} words — decent, but adding more specific instructions will improve output quality.")
    else:
        parts.append(f"✅ <b>Length:</b> Good — {wc} words gives the model plenty of context to work with.")

    if has_role:
        parts.append("✅ <b>Role definition:</b> Great — you've defined a persona/role for the AI, which anchors its expertise and tone.")
    else:
        parts.append("❌ <b>Role definition missing:</b> Start with 'You are a [role]...' to set expertise and tone.")

    if has_format:
        parts.append("✅ <b>Output format:</b> You've specified what output you want, helping the model structure its response correctly.")
    else:
        parts.append("⚠️ <b>Output format unclear:</b> Tell the AI exactly how to format the response — tables, numbered lists, headers, etc.")

    if has_numbered:
        parts.append("✅ <b>Structured instructions:</b> Using numbered steps makes it easier for the AI to follow all requirements.")
    else:
        parts.append("💡 <b>Tip:</b> Try numbering your instructions (1. Analyze... 2. Compare... 3. Recommend...) for cleaner, more complete responses.")

    if has_context:
        parts.append("✅ <b>Context depth:</b> Solid context provided — the AI has enough background to give a relevant, case-specific response.")
    else:
        parts.append("⚠️ <b>Add more context:</b> Include business context, constraints, and specific requirements for this scenario.")

    return "<br><br>".join(parts)


def get_prompt_tips(score_data: dict, case: dict) -> list:
    """
    Return a list of targeted improvement tips based on score breakdown.
    """
    tips = []
    criteria = score_data["criteria"]

    if criteria["Clarity & Specificity"] < 14:
        tips.append(
            "🎯 <b>Be more specific:</b> Instead of 'analyze the candidate', say 'analyze the candidate's skills against these 5 required competencies and rate each from 1–10'."
        )

    if criteria["Role & Context Setting"] < 14:
        tips.append(
            "👤 <b>Set a strong role:</b> Open with 'You are a senior [role] with X years of experience in [domain] at a large manufacturing company like Tata Steel.'"
        )

    if criteria["Task Definition"] < 14:
        tips.append(
            "📋 <b>Structure your tasks:</b> Use numbered instructions — '1. Do X. 2. Analyze Y. 3. Recommend Z.' This prevents the AI from missing steps."
        )

    if criteria["Output Format"] < 14:
        tips.append(
            "📊 <b>Specify output format:</b> Tell the AI exactly what to produce — 'Respond with: (a) a comparison table, (b) a risk matrix, (c) a 3-sentence recommendation.'"
        )

    if criteria["Completeness"] < 14:
        tips.append(
            f"✅ <b>Cover all objectives:</b> This case requires addressing: {', '.join(case['objectives'][:3])}... Make sure your prompt asks for all of these."
        )

    if not tips:
        tips.append(
            "🌟 <b>Strong prompt!</b> To push further: try adding constraints ('respond in under 300 words', 'use only verified facts'), specify tone ('write for a non-technical manager'), or add examples of the output format you expect."
        )

    if score_data["total"] < 50:
        tips.insert(0,
            "🚀 <b>Quick win:</b> The fastest way to improve your score is to (1) add a role definition at the top, (2) number your instructions, and (3) specify the output format clearly."
        )

    return tips
