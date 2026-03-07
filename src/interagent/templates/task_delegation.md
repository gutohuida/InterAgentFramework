# Task Delegation Template

**From:** {{ sender }} ({{ sender_role }})  
**To:** {{ recipient }} ({{ recipient_role }})  
**Date:** {{ date }}  
**Task ID:** {{ task_id }}

---

## Task: {{ title }}

### Description
{{ description }}

### Requirements
{% for req in requirements %}
- [ ] {{ req }}
{% endfor %}

### Acceptance Criteria
{% for criteria in acceptance_criteria %}
- [ ] {{ criteria }}
{% endfor %}

### Priority
{{ priority }}

### Context
{{ context }}

### Expected Deliverables
{% for deliverable in deliverables %}
- [ ] {{ deliverable }}
{% endfor %}

---

## Expected Response

Please respond with one of:

- ✅ **ACCEPT** - I can complete this task
- ❌ **REJECT** - I cannot complete this task (explain why)
- ❓ **CLARIFY** - I need more information

Once accepted, please provide:
1. Your approach/plan
2. Estimated time to complete
3. Any dependencies or blockers

---

## Communication

Use the following to update status:

```bash
# Start work
interagent task update {{ task_id }} --status in_progress

# Add note
interagent task update {{ task_id }} --note "Making progress..."

# Complete
interagent task update {{ task_id }} --status completed

# Request review
interagent msg send --to {{ sender }} --subject "Review Request" --message "Task complete!"
```
