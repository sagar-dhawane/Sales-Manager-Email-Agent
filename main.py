import asyncio
from agents import Runner, trace
from src.agents import sales_manager

async def main():
    # You can change this prompt to test different personas
    prompt = "Send a cold sales email to Sagar, the CEO of a Tech Startup."

    print(f"--- Starting Sales Agent Run for: {prompt} ---")
    
    # Run the workflow
    with trace("Automated SDR"):
        result = await Runner.run(sales_manager, prompt)
        
        print("\n--- Final Result ---")
        
        # FIX: Access the last message safely
        if hasattr(result, 'messages') and result.messages:
            last_msg = result.messages[-1]
            
            # Check if it's a Dictionary or an Object
            if isinstance(last_msg, dict):
                print(last_msg.get("content", "No content found"))
            else:
                print(getattr(last_msg, "content", str(last_msg)))
        else:
            print(result)

if __name__ == "__main__":
    asyncio.run(main())