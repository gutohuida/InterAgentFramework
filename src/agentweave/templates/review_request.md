# Review Request

**Task:** {{ task_title }}  
**Task ID:** {{ task_id }}  
**Submitted By:** {{ author }}  
**Date:** {{ date }}  
**Requested Reviewer:** {{ reviewer }}

---

## Summary

{{ summary }}

## Changes

{% for change in changes %}
- **{{ change.file }}**: {{ change.description }}
{% endfor %}

## Testing

{% if tests %}
- [x] Tests written and passing
- Coverage: {{ coverage }}%
{% else %}
- [ ] Tests pending
{% endif %}

## Specific Areas for Review

Please focus on:

{% for area in focus_areas %}
- [ ] {{ area }}
{% endfor %}

---

## Review Response Template

**Reviewer:** {{ reviewer }}  
**Date:** {{ review_date }}

### Overall Assessment
- [ ] **APPROVED** - Ready to merge
- [ ] **NEEDS_REVISION** - Changes required
- [ ] **DISCUSSION_NEEDED** - Need to discuss

### Feedback

**What's Good:**
{% for good in feedback_good %}
- {{ good }}
{% endfor %}

**Suggestions:**
{% for suggestion in feedback_suggestions %}
- {{ suggestion }}
{% endfor %}

**Required Changes (if any):**
{% for change in required_changes %}
- [ ] {{ change }}
{% endfor %}

### Next Steps
{{ next_steps }}
