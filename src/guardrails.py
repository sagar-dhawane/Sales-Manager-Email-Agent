from pydantic import BaseModel, Field
from agents import Agent, Runner, input_guardrail, GuardrailFunctionOutput

# 1. Define the Structure (The Decision)
class SafetyCheckOutput(BaseModel):
    is_safe: bool = Field(description="True if content is safe. False if it contains abuse, defamation, or sexual content.")
    violation_reason: str = Field(description="If unsafe, explain why (e.g., 'Sexual Content', 'Hate Speech'). If safe, write 'None'.")

# 2. Define the Safety Agent (The "Bouncer")
safety_agent = Agent(
    name="Safety Officer",
    instructions="""
    You are a Content Safety Guard. Check the user's message for prohibited content.
    
    **PROHIBITED CATEGORIES:**
    1. **Sexual Content:** Any mentions of sexual acts, organs, or innuendos.
    2. **Defamation:** Insults, attacks on reputation, or unverified accusations against people/companies.
    3. **Abuse/Hate:** Harassment, swearing, or hate speech.
    
    **TASK:**
    - If the message contains ANY of these, set 'is_safe' to False.
    - Otherwise, set 'is_safe' to True.
    """,
    output_type=SafetyCheckOutput,
    model="gpt-4o-mini"
)

# 3. Define the Guardrail Function
@input_guardrail
async def guardrail_against_toxicity(ctx, agent, message):
    print(f"🛡️ Safety Guardrail: Scanning input for toxicity...")
    
    # Run the safety agent
    result = await Runner.run(safety_agent, message, context=ctx.context)
    decision = result.final_output
    
    if not decision.is_safe:
        print(f"🚨 BLOCKED: {decision.violation_reason}")
        # Stop the workflow. The main agent will NOT run.
        return GuardrailFunctionOutput(
            output_info={"block_reason": decision.violation_reason},
            tripwire_triggered=True 
        )
    
    print("✅ Input is Safe.")
    # Proceed normally
    return GuardrailFunctionOutput(
        output_info={"status": "safe"},
        tripwire_triggered=False
    )

# ==========================================
# OUTPUT GUARDRAIL (Email Compliance Auditor)
# ==========================================

# 1. Define Output Structure
class EmailSafetyOutput(BaseModel):
    is_compliant: bool = Field(description="True if safe. False if abuse/defamation/sex content.")
    risk_report: str = Field(description="If unsafe, specify category. Else 'None'.")

# 2. Define Auditor Agent
email_auditor = Agent(
    name="Email Compliance Auditor",
    instructions="""
    You are a strictly conservative Email Compliance Officer.
    Rules: No sexual content, no defamation, no abuse.
    Decision: Return is_compliant=True ONLY if professional.
    """,
    output_type=EmailSafetyOutput,
    model="gpt-4o-mini"
)

# 3. Helper Function (Call this from src/tools.py)
# NOTE: DO NOT use @output_guardrail here because we call this manually inside the tool.
async def verify_email_safety(email_body: str):
    """
    Runs the Auditor Agent on the email body.
    Returns: (bool, str) -> (is_safe, reason)
    """
    print("🛡️ Output Guardrail: Auditing email draft...")
    
    try:
        # Run the agent explicitly
        result = await Runner.run(email_auditor, f"Audit this email draft:\n\n{email_body}")
        
        if not result.final_output:
            return False, "Auditor produced no output."

        decision = result.final_output
        return decision.is_compliant, decision.risk_report

    except Exception as e:
        print(f"❌ Output Guardrail CRASH: {str(e)}")
        # If audit fails, default to unsafe
        return False, f"Guardrail Error: {str(e)}"