import sendgrid
from sendgrid.helpers.mail import Mail, Email, To, Content
from src.config import SENDGRID_API_KEY, SENDER_EMAIL, TARGET_EMAIL
from agents import function_tool

# Import the verification function
from src.guardrails import verify_email_safety

# NOTE: Async is required because verify_email_safety is async
@function_tool
async def send_html_email(subject: str, html_body: str):
    """ 
    Send out an email with the given subject and HTML body.
    Includes a safety audit before sending.
    """
    print(f"🔧 Tool: send_html_email called. Subject: {subject}")
    
    # --- 🛑 OUTPUT GUARDRAIL CHECK (Safe Wrapper) ---
    # We wrap this in try/except so a guardrail crash doesn't break the whole agent
    try:
        print("🛡️ Output Guardrail: Auditing email draft...")
        is_safe, risk_reason = await verify_email_safety(html_body)
        
        if not is_safe:
            msg = f"⛔ BLOCKED by Auditor. Reason: {risk_reason}"
            print(msg)
            # Return "blocked" status so the Agent knows it finished (and won't retry)
            return {"status": "blocked", "message": msg}

    except Exception as e:
        # This catches if the Guardrail logic itself crashes (e.g. OpenAI API error)
        error_msg = f"⚠️ Guardrail System Crashed: {str(e)}"
        print(error_msg)
        # We return this as an error so the agent knows something went wrong.
        return {"status": "error", "message": error_msg}
    
    # --- ✅ SENDGRID EXECUTION ---
    print("✅ Audit Passed. Connecting to SendGrid...")
    
    try:
        sg = sendgrid.SendGridAPIClient(api_key=SENDGRID_API_KEY)
        from_email = Email(SENDER_EMAIL)
        to_email_obj = To(TARGET_EMAIL) 
        content = Content("text/html", html_body)
        
        mail = Mail(from_email, to_email_obj, subject, content).get()
        sg.client.mail.send.post(request_body=mail)
        return {"status": "success", "message": f"Email sent to {TARGET_EMAIL}"}
        
    except Exception as e:
        print(f"❌ SendGrid Error: {str(e)}")
        return {"status": "error", "message": f"SendGrid API Error: {str(e)}"}