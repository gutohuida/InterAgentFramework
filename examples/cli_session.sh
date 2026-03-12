#!/bin/bash
# Example: CLI Session
# 
# This script demonstrates using AgentWeave via the command line.
# Run these commands in your terminal.

set -e

echo "=========================================="
echo "AgentWeave CLI Example Session"
echo "=========================================="
echo

# Step 1: Initialize
echo "Step 1: Initialize Session"
echo "--------------------------"
agentweave init --project "Demo API" --principal claude --mode hierarchical
echo

# Step 2: Check status
echo "Step 2: Check Status"
echo "--------------------------"
agentweave status
echo

# Step 3: Create tasks
echo "Step 3: Create Tasks"
echo "--------------------------"

# Task for Claude (as Principal)
agentweave task create \
    --title "Design API Architecture" \
    --assignee claude \
    --priority high \
    --description "Design REST API architecture"

# Task for Kimi (as Delegate)
agentweave task create \
    --title "Implement Authentication" \
    --assignee kimi \
    --priority high \
    --requirements "JWT tokens" "Password hashing" "Login/Register endpoints"

# Another task for Kimi
agentweave task create \
    --title "Write Tests" \
    --assignee kimi \
    --priority medium
echo

# Step 4: List tasks
echo "Step 4: List Tasks"
echo "--------------------------"
agentweave task list
echo

# Step 5: Quick delegation
echo "Step 5: Quick Delegation"
echo "--------------------------"
agentweave delegate --to kimi --task "Set up database" --priority high
echo

# Step 6: Check inbox
echo "Step 6: Check Kimi's Inbox"
echo "--------------------------"
agentweave inbox --agent kimi
echo

# Step 7: Update task status (simulating work)
echo "Step 7: Update Task Status"
echo "--------------------------"
# Get first task ID
TASK_ID=$(agentweave task list 2>/dev/null | grep "task-" | head -1 | awk '{print $2}' | tr -d ':')
if [ -n "$TASK_ID" ]; then
    echo "Updating task: $TASK_ID"
    agentweave task update "$TASK_ID" --status in_progress
    agentweave task update "$TASK_ID" --status completed
    agentweave task update "$TASK_ID" --status approved
else
    echo "No task found to update"
fi
echo

# Step 8: Send message
echo "Step 8: Send Message"
echo "--------------------------"
agentweave msg send --to kimi --subject "Great work!" --message "The implementation looks excellent. Approved!"
echo

# Step 9: Check final status
echo "Step 9: Final Status"
echo "--------------------------"
agentweave status
echo

echo "=========================================="
echo "Example Complete!"
echo "=========================================="
echo
echo "Files created in .agentweave/:"
ls -la .agentweave/
