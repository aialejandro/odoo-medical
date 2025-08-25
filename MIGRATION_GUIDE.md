# Migration Guide: Component-Session Many-to-Many Relationship

## Overview
This guide helps developers understand the changes made to convert the treatment component-session relationship from one-to-many to many-to-many.

## Breaking Changes

### 1. Field Changes
- **Medical Treatment Component**:
  - ❌ `session_id` (Many2one) - REMOVED
  - ✅ `session_ids` (Many2many) - Use this instead

### 2. Method Changes
- **Medical Treatment Session**:
  - `action_view_components()` domain changed from `[('session_id', '=', self.id)]` to `[('session_ids', 'in', [self.id])]`

### 3. View Changes
- Component form view now shows multiple sessions instead of single session
- Session form view enhanced with better component editing interface

## Code Migration Examples

### Before (One-to-Many):
```python
# Creating a component for a specific session
component = env['medical.treatment.component'].create({
    'name': 'Exercise Component',
    'session_id': session.id,  # ❌ This field no longer exists
    'duration_minutes': 30
})

# Finding components for a session
components = env['medical.treatment.component'].search([
    ('session_id', '=', session.id)  # ❌ This field no longer exists
])
```

### After (Many-to-Many):
```python
# Creating a component (no longer tied to specific session)
component = env['medical.treatment.component'].create({
    'name': 'Exercise Component',
    'duration_minutes': 30
})

# Linking component to sessions
component.session_ids = [(4, session1.id), (4, session2.id)]
# OR
session1.treatment_component_ids = [(4, component.id)]

# Finding components for a session
components = env['medical.treatment.component'].search([
    ('session_ids', 'in', [session.id])  # ✅ Use this instead
])

# Alternative: Get components through session
components = session.treatment_component_ids
```

## Database Migration (If Needed)

If you have existing data, you would need to migrate it. Since you mentioned there's no existing data, this is not needed, but here's the concept:

```sql
-- Hypothetical migration (not needed in your case)
-- This would move existing session_id relationships to the many2many table

INSERT INTO medical_session_component_rel (session_id, component_id)
SELECT session_id, id 
FROM medical_treatment_component 
WHERE session_id IS NOT NULL;

-- Then remove the old session_id column
ALTER TABLE medical_treatment_component DROP COLUMN session_id;
```

## Testing Changes

Run the included tests to validate the new functionality:

```bash
# In Odoo shell or test environment
python -m pytest odoo-custom-addons/odoo_medical/tests/test_component_session_relationship.py
```

## New Capabilities

### 1. Component Reuse
```python
# Create reusable components
warmup = env['medical.treatment.component'].create({
    'name': 'Warm-up Exercise',
    'duration_minutes': 10
})

# Use in multiple sessions
session1.treatment_component_ids = [(4, warmup.id)]
session2.treatment_component_ids = [(4, warmup.id)]
session3.treatment_component_ids = [(4, warmup.id)]

# Check usage
print(f"Warm-up used in {warmup.session_count} sessions")
```

### 2. Flexible Session Composition
```python
# Mix and match components for different session types
initial_session.treatment_component_ids = [
    (4, warmup.id), (4, assessment.id), (4, therapy.id), (4, cooldown.id)
]

standard_session.treatment_component_ids = [
    (4, warmup.id), (4, therapy.id), (4, cooldown.id)
]

assessment_only_session.treatment_component_ids = [
    (4, warmup.id), (4, assessment.id), (4, cooldown.id)
]
```

### 3. Better Maintenance
```python
# Update component once, affects all sessions using it
warmup.write({
    'duration_minutes': 15,  # Changed from 10 to 15
    'instructions': 'Updated warm-up instructions'
})
# All sessions using this component automatically get the updates
```

## UI Changes

### Component Form
- Now shows session count in button box
- Sessions tab shows all related sessions
- Session field replaced with many2many tags widget

### Session Form  
- Components tab enhanced with tree/form views
- Better editing experience for component details
- Sequence handling preserved

## Best Practices

1. **Create Generic Components**: Design components to be reusable across sessions
2. **Use Descriptive Names**: Component names should be clear since they're used in multiple contexts
3. **Maintain Sequences**: Use sequence fields to maintain proper ordering within sessions
4. **Leverage Computed Fields**: Use `session_count` and `component_count` for quick insights
5. **Test Thoroughly**: Validate that duration calculations work correctly with new relationships

## Troubleshooting

### Common Issues:
1. **Components not showing in session**: Check the many2many relationship is properly set
2. **Duration not calculating**: Ensure components have `duration_minutes` set
3. **Access errors**: Verify security permissions haven't changed

### Debug Commands:
```python
# Check component-session relationships
component.session_ids  # Sessions using this component
session.treatment_component_ids  # Components in this session

# Verify counts
len(component.session_ids)  # Should match session_count
len(session.treatment_component_ids)  # Should match component_count
```
