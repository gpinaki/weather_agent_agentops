from dotenv import load_dotenv
import os
import agentops

def main():
    # Load environment variables
    load_dotenv()
    
    # Check for API key
    api_key = os.getenv("AGENTOPS_API_KEY")
    if not api_key:
        print("ERROR: No AgentOps API key found in environment")
        return
    
    print(f"Found API key starting with: {api_key[:4]}...")
    
    try:
        # Initialize AgentOps
        agentops.init(api_key)
        print("Successfully initialized AgentOps")
        
        # Try to create a session
        session_id = agentops.start_session(tags=["test"])
        print(f"Successfully created session: {session_id}")
        
        # Try to record an event
        agentops.record(
            agentops.ActionEvent(
                action_type="test_event",
                params="test parameters"
            )
        )
        print("Successfully recorded test event")
        
        # End the session
        agentops.end_session("Success")
        print("Successfully ended session")
        
    except Exception as e:
        print(f"ERROR: {str(e)}")
        raise

if __name__ == "__main__":
    main()