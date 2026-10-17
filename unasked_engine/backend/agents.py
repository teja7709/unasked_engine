import os, json
from dotenv import load_dotenv
from google import genai
load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
MODEL = "gemini-3.8-flash"

def ask(prompt):
    r = client.models.generate_content(
        model=MODEL, contents=prompt,
        config={"response_mime_type": "application/json"})
    return json.loads(r.text)

def analyze(doc):
    # Agent 1: extract
    facts = ask(f"""Extract from this document: goals, stated assumptions,
constraints. Return JSON {{"goals":[],"assumptions":[],"constraints":[]}}.
DOCUMENT: {doc}""")

    # Agent 2: find gaps, each asked by a persona
    gaps = ask(f"""You are a panel of critical reviewers: Investor, Legal,
End User, Engineer, Operations. Given the document and facts, find missing
assumptions, overlooked constraints, and questions the author has not
considered. Give 8 to 12 gaps. For each return: question, persona (which
reviewer would ask it), category, evidence (a short exact quote from the
document, or "not mentioned"), why_it_matters.
Return JSON {{"gaps":[...]}}.
FACTS: {facts}
DOCUMENT: {doc}""")

    # Agent 3: score, rank, recommend
    final = ask(f"""For each gap add: impact (1-5), likelihood (1-5),
priority (impact*likelihood, an integer) and a one-line recommendation.
Sort by priority descending. Also give a readiness score from 0 to 100
(100 = the document is fully thought through, lower if there are many
serious gaps) and score_reason (one short sentence).
Keep all original fields.
Return JSON {{"score":0,"score_reason":"","results":[...]}}.
GAPS: {gaps}""")
    return final