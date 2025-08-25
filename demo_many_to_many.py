#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Demo script showing the many-to-many relationship between components and sessions.

This script demonstrates how treatment components can now be reused across 
multiple treatment sessions, providing better flexibility and maintainability.

Note: This is a conceptual demo showing the relationship structure.
In a real Odoo environment, you would use the web interface or odoo shell.
"""

def demo_many_to_many_relationship():
    """
    Conceptual demonstration of the new many-to-many relationship
    """
    print("=== Medical Treatment Component-Session Many-to-Many Relationship Demo ===\n")
    
    # Simulate creating treatment components (these would be Odoo records)
    components = {
        'warmup': {
            'name': 'Warm-up Exercise',
            'duration_minutes': 10,
            'description': 'Light exercises to prepare muscles'
        },
        'core_therapy': {
            'name': 'Core Therapy Session',
            'duration_minutes': 45,
            'description': 'Main therapeutic intervention'
        },
        'cooldown': {
            'name': 'Cool-down & Stretching',
            'duration_minutes': 15,
            'description': 'Relaxation and muscle recovery'
        },
        'assessment': {
            'name': 'Progress Assessment',
            'duration_minutes': 20,
            'description': 'Evaluate patient progress'
        }
    }
    
    # Simulate creating treatment sessions
    sessions = {
        'initial_session': {
            'name': 'Initial Treatment Session',
            'sequence': 1,
            'components': ['warmup', 'core_therapy', 'assessment', 'cooldown']
        },
        'standard_session': {
            'name': 'Standard Treatment Session',
            'sequence': 2,
            'components': ['warmup', 'core_therapy', 'cooldown']
        },
        'assessment_session': {
            'name': 'Assessment Session',
            'sequence': 3,
            'components': ['warmup', 'assessment', 'cooldown']
        },
        'final_session': {
            'name': 'Final Treatment Session',
            'sequence': 4,
            'components': ['warmup', 'core_therapy', 'assessment', 'cooldown']
        }
    }
    
    print("Created Components:")
    for comp_id, comp_data in components.items():
        print(f"  • {comp_data['name']} ({comp_data['duration_minutes']} min)")
    
    print(f"\nCreated {len(sessions)} Treatment Sessions:")
    for session_id, session_data in sessions.items():
        component_names = [components[c]['name'] for c in session_data['components']]
        total_duration = sum(components[c]['duration_minutes'] for c in session_data['components'])
        print(f"  • {session_data['name']}")
        print(f"    Components: {', '.join(component_names)}")
        print(f"    Total Duration: {total_duration} minutes")
    
    print(f"\n=== Component Reuse Analysis ===")
    
    # Analyze component reuse
    component_usage = {}
    for session_id, session_data in sessions.items():
        for comp_id in session_data['components']:
            if comp_id not in component_usage:
                component_usage[comp_id] = []
            component_usage[comp_id].append(session_data['name'])
    
    for comp_id, sessions_using in component_usage.items():
        comp_name = components[comp_id]['name']
        print(f"\n'{comp_name}' is used in {len(sessions_using)} sessions:")
        for session_name in sessions_using:
            print(f"  • {session_name}")
    
    print(f"\n=== Benefits of Many-to-Many Relationship ===")
    print("✓ Components can be reused across multiple sessions")
    print("✓ Easy to maintain - update component once, affects all sessions")
    print("✓ Flexible session composition - mix and match components")
    print("✓ Clear visibility of component usage across sessions")
    print("✓ Efficient duration calculations based on selected components")
    
    print(f"\n=== Usage Statistics ===")
    total_components = len(components)
    reused_components = sum(1 for usage in component_usage.values() if len(usage) > 1)
    efficiency = (reused_components / total_components) * 100 if total_components > 0 else 0
    
    print(f"Total components created: {total_components}")
    print(f"Components reused across sessions: {reused_components}")
    print(f"Component reuse efficiency: {efficiency:.1f}%")


if __name__ == '__main__':
    demo_many_to_many_relationship()
