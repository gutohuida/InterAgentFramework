#!/bin/bash
# Example: CLI Session
# 
# This script demonstrates using InterAgent via the command line.
# Run these commands in your terminal.

set -e

echo "=========================================="
echo "InterAgent CLI Example Session"
echo "=========================================="
echo

# Step 1: Initialize
echo "Step 1: Initialize Session"
echo "--------------------------"
interagent init --project "Demo API" --principal claude --mode hierarchical
echo

# Step 2: Check status
echo "Step 2: Check Status"
echo "--------------------------"
interagent status
echo

# Step 3: Create tasks
echo "Step 3: Create Tasks"
echo "--------------------------"

# Task for Claude (as Principal)
interagent task create \
    --title "Design API Architecture" \
    --assignee claude \
    --priority high \
    --description "Design REST API architecture"

# Task for Kimi (as Delegate)
interagent task create \
    --title "Implement Authentication" \
    --assignee kimi \
    --priority high \
    --requirements "JWT tokens" "Password hashing" "Login/Register endpoints"

# Another task for Kimi
interagent task create \
    --title "Write Tests" \
    --assignee kimi \
    --priority medium
echo

# Step 4: List tasks
echo "Step 4: List Tasks"
echo "--------------------------"
interagent task list
echo

# Step 5: Quick delegation
echo "Step 5: Quick Delegation"
echo "--------------------------"
interagent delegate --to kimi --task "Set up database" --priority high
echo

# Step 6: Check inbox
echo "Step 6: Check Kimi's Inbox"
echo "--------------------------"
interagent inbox --agent kimi
echo

# Step 7: Update task status (simulating work)
echo "Step 7: Update Task Status"
echo "--------------------------"
# Get first task ID
TASK_ID=$(interagent task list 2>/dev/null | grep "task-" | head -1 | awk '{print $2}' | tr -d ':')
if [ -n "$TASK_ID" ]; then
    echo "Updating task: $TASK_ID"
    interagent task update "$TASK_ID" --status in_progress
    interagent task update "$TASK_ID" --status completed
    interagent task update "$TASK_ID" --status approved
else
    echo "No task found to update"
fi
echo

# Step 8: Send message
echo "Step 8: Send Message"
echo "--------------------------"
interagent msg send --to kimi --subject "Great work!" --message "The implementation looks excellent. Approved!"
echo

# Step 9: Check final status
echo "Step 9: Final Status"
echo "--------------------------"
interagent status
echo

echo "=========================================="
echo "Example Complete!"
echo "=========================================="
echo
echo "Files created in .interagent/:"
ls -la .interagent/
