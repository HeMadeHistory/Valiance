# streamlit_app_valiance.py

import streamlit as st
import openai
import graphviz

# Replace with your OpenAI API key or other LLM API key
openai.api_key = "YOUR_API_KEY_HERE"

# ---- UI ----

st.set_page_config(page_title="Valiance - Ultimate Business & Estate Planning AI", layout="wide")

st.title("🛡️ Valiance")
st.subheader("Your Personal AI Architect for Perpetual Wealth, Liability Protection, and Freedom")

st.markdown("""
Valiance builds for you:
- Ultimate Business Structures
- Advanced Estate & Tax Strategies (Trusts, C Corps, LLCs, S Corps, Holding Companies)
- Family Banking (IUL, Private Lending)
- Rockefeller Strategy: Own Nothing, Control Everything
- Franchise & Real Estate Structures
- Bank Setup & Flow of Funds
- Perpetual Family Wealth Engine
- All mapped to current elite strategies & laws
""")

# ---- User Input ----

st.header("Step 1: Tell Valiance Your Current Situation")

with st.form("user_input_form"):
    individual_or_family = st.radio("Are you setting this up for an Individual, Couple, or Family?", 
                                    ["Individual", "Husband & Wife", "Family"])

    current_businesses = st.text_area("List your existing businesses (name, state, type of entity)")

    existing_trust = st.text_area("Do you already have a Trust? If so, name and type of trust (revocable, irrevocable, ecclesiastical, etc.)")

    key_people = st.text_area("Who should run and control everything? List key people and their desired roles.")

    personal_goals = st.text_area("What are your personal goals? (Liability protection, never be bankrupt personally, wealth compounding, family freedom, privacy, etc.)")

    other_notes = st.text_area("Anything else Valiance should know about your situation? (Franchises, IULs, family dynamics, inheritance desires, funding goals, etc.)")

    submitted = st.form_submit_button("Generate My Plan")

# ---- Prompt Template ----

def build_valiance_prompt():
    prompt = f"""
You are Valiance, the ultimate AI Architect for building elite business structures and estate plans.
Your job is to analyze the user's situation and produce a clear written action plan and visual structure
based on the following principles:

- Rockefeller strategy of "own nothing, control everything"
- C Corps, S Corps, LLCs, Holding Companies, Trusts
- Use Wyoming entities where advantageous
- Advanced estate planning based on structures used by the top 1% and major corporations
- Family trust as the ultimate owner
- Flow of funds optimized for liability protection, asset protection, privacy, and tax optimization
- Franchise and IUL planning included
- Instructions on how to change company names and deeds
- Strategy for opening business bank accounts and moving money properly
- Visual org chart with arrows showing proper structure
- Written so a college graduate can easily understand it
- Provide step-by-step instructions when necessary
- Reference best practices from elite estate and tax planning books and actual strategies used by family offices

Here is the user's input:

Individual/Family: {individual_or_family}

Existing Businesses: {current_businesses}

Existing Trust: {existing_trust}

Key People: {key_people}

Personal Goals: {personal_goals}

Other Notes: {other_notes}

Please provide:
1. Written Action Plan
2. Visual Org Chart (textual format using arrows ->)
3. Any Step-by-Step Guidance Needed
4. Key Laws and Best Practices Referenced

Remember: You are an expert across all relevant domains. Do not skip details. Optimize for perpetual wealth and liability protection.
"""
    return prompt

# ---- LLM Call ----

def call_openai(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-4o", # You can use gpt-4-turbo or gpt-4o
        messages=[
            {"role": "system", "content": "You are Valiance, the ultimate AI agent for business structuring, estate planning, and wealth protection."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=4096,
        temperature=0.4
    )
    return response['choices'][0]['message']['content']

# ---- Graph Builder ----

def build_graph_chart(org_chart_text):
    dot = graphviz.Digraph()

    # Simple parsing (expects format like: Family Trust -> Holding Co -> LLC 1)
    lines = org_chart_text.strip().split('\n')
    for line in lines:
        parts = [p.strip() for p in line.split("->")]
        for i in range(len(parts) - 1):
            dot.edge(parts[i], parts[i+1])

    return dot

# ---- Main Logic ----

if submitted:
    st.header("📜 Your Personalized Action Plan")

    with st.spinner("Valiance is building your optimized structure..."):
        full_prompt = build_valiance_prompt()
        llm_response = call_openai(full_prompt)

    # Split sections
    try:
        plan_part, chart_part = llm_response.split("Visual Org Chart")
    except:
        plan_part = llm_response
        chart_part = ""

    # Display written plan
    st.markdown("### Written Action Plan")
    st.markdown(plan_part)

    # Extract org chart if possible
    if chart_part:
        st.markdown("### Visual Organizational Chart")
        st.markdown(chart_part)

        st.graphviz_chart(build_graph_chart(chart_part))

    # Display original full text as expandable section
    with st.expander("See Full Raw AI Response"):
        st.text(llm_response)
