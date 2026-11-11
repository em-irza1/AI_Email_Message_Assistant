MESSAGE_TYPES = [
    "Professional Email",
    "Student Message",
    "Leave Application",
    "Formal Request",
]

TONES = ["Professional", "Polite", "Friendly"]


def build_prompt(message_type, tone, rough_message):
    """Build a clear, reusable prompt from the user's selections."""
    category_instructions = {
        "Professional Email": (
            "Format this as a professional email. Add a concise subject line "
            "when suitable, followed by an appropriate greeting, body, and closing."
        ),
        "Student Message": (
            "Format this as a clear, natural message suitable for communication "
            "between a student and a teacher or classmate, depending on context."
        ),
        "Leave Application": (
            "Format this as a respectful leave application. Do not add dates, "
            "student details, reasons, or other facts that the user did not provide."
        ),
        "Formal Request": (
            "Format this as a respectful and well-structured formal request."
        ),
    }

    return f"""
Improve the text below.

MESSAGE CATEGORY: {message_type}
WRITING TONE: {tone}

CATEGORY INSTRUCTIONS:
{category_instructions[message_type]}

REQUIREMENTS:
- Correct spelling, grammar, punctuation, and sentence structure.
- Improve clarity and readability while preserving the original meaning.
- Use the selected tone consistently.
- Do not invent names, dates, deadlines, reasons, titles, contact details, or other unsupported information.
- Do not add claims or promises that were not in the original text.
- Keep the result appropriately concise.
- Return only the improved message, with no explanation or commentary.
- If an email subject is appropriate, include it as: Subject: ...

USER'S ROUGH TEXT:
{rough_message}
""".strip()
