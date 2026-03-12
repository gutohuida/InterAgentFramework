@echo off
REM Example: CLI Session for Windows
REM 
REM This script demonstrates using AgentWeave via the command line.
REM Run these commands in your terminal.

echo ==========================================
echo AgentWeave CLI Example Session
echo ==========================================
echo.

REM Step 1: Initialize
echo Step 1: Initialize Session
echo --------------------------
agentweave init --project "Demo API" --principal claude --mode hierarchical
echo.

REM Step 2: Check status
echo Step 2: Check Status
echo --------------------------
agentweave status
echo.

REM Step 3: Create tasks
echo Step 3: Create Tasks
echo --------------------------

REM Task for Claude
agentweave task create --title "Design API Architecture" --assignee claude --priority high --description "Design REST API architecture"

REM Task for Kimi
agentweave task create --title "Implement Authentication" --assignee kimi --priority high --requirements "JWT tokens" "Password hashing" "Login/Register endpoints"

REM Another task for Kimi
agentweave task create --title "Write Tests" --assignee kimi --priority medium
echo.

REM Step 4: List tasks
echo Step 4: List Tasks
echo --------------------------
agentweave task list
echo.

REM Step 5: Quick delegation
echo Step 5: Quick Delegation
echo --------------------------
agentweave delegate --to kimi --task "Set up database" --priority high
echo.

REM Step 6: Check inbox
echo Step 6: Check Kimi's Inbox
echo --------------------------
agentweave inbox --agent kimi
echo.

REM Step 7: Send message
echo Step 7: Send Message
echo --------------------------
agentweave msg send --to kimi --subject "Great work!" --message "The implementation looks excellent. Approved!"
echo.

REM Step 8: Check final status
echo Step 8: Final Status
echo --------------------------
agentweave status
echo.

echo ==========================================
echo Example Complete!
echo ==========================================
echo.
echo Files created in .agentweave/:
dir .agentweave /s

pause
