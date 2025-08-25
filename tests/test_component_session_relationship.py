# -*- coding: utf-8 -*-

from odoo.tests.common import TransactionCase


class TestMedicalTreatmentComponentSession(TransactionCase):
    """Test the many-to-many relationship between components and sessions"""
    
    def setUp(self):
        super().setUp()
        # Create test treatment
        self.treatment = self.env['medical.treatment'].create({
            'name': 'Test Treatment',
            'code': 'TEST001',
        })
        
        # Create test sessions
        self.session1 = self.env['medical.treatment.session'].create({
            'name': 'Test Session 1',
            'treatment_id': self.treatment.id,
            'sequence': 1,
        })
        
        self.session2 = self.env['medical.treatment.session'].create({
            'name': 'Test Session 2',
            'treatment_id': self.treatment.id,
            'sequence': 2,
        })
        
        # Create test components
        self.component1 = self.env['medical.treatment.component'].create({
            'name': 'Test Component 1',
            'duration_minutes': 30,
        })
        
        self.component2 = self.env['medical.treatment.component'].create({
            'name': 'Test Component 2',
            'duration_minutes': 45,
        })
    
    def test_component_can_be_used_in_multiple_sessions(self):
        """Test that a component can be used in multiple sessions"""
        # Add component1 to both sessions
        self.session1.treatment_component_ids = [(4, self.component1.id)]
        self.session2.treatment_component_ids = [(4, self.component1.id)]
        
        # Verify the component is linked to both sessions
        self.assertEqual(len(self.component1.session_ids), 2)
        self.assertIn(self.session1, self.component1.session_ids)
        self.assertIn(self.session2, self.component1.session_ids)
        
        # Verify session counts are correct
        self.assertEqual(self.component1.session_count, 2)
    
    def test_session_can_have_multiple_components(self):
        """Test that a session can have multiple components"""
        # Add both components to session1
        self.session1.treatment_component_ids = [(4, self.component1.id), (4, self.component2.id)]
        
        # Verify the session has both components
        self.assertEqual(len(self.session1.treatment_component_ids), 2)
        self.assertIn(self.component1, self.session1.treatment_component_ids)
        self.assertIn(self.component2, self.session1.treatment_component_ids)
        
        # Verify component counts are correct
        self.assertEqual(self.session1.component_count, 2)
    
    def test_estimated_duration_calculation(self):
        """Test that estimated duration is calculated correctly"""
        # Add components to session
        self.session1.treatment_component_ids = [(4, self.component1.id), (4, self.component2.id)]
        
        # Verify estimated duration is sum of component durations
        expected_duration = 30 + 45  # component1 + component2
        self.assertEqual(self.session1.estimated_duration, expected_duration)
    
    def test_action_view_sessions_from_component(self):
        """Test the action to view sessions from a component"""
        # Add component to multiple sessions
        self.session1.treatment_component_ids = [(4, self.component1.id)]
        self.session2.treatment_component_ids = [(4, self.component1.id)]
        
        # Test action with multiple sessions
        action = self.component1.action_view_sessions()
        self.assertEqual(action['domain'], [('treatment_component_ids', 'in', [self.component1.id])])
        
        # Test action with single session
        self.component2.session_ids = [(4, self.session1.id)]
        action = self.component2.action_view_sessions()
        self.assertEqual(action['res_id'], self.session1.id)
    
    def test_action_view_components_from_session(self):
        """Test the action to view components from a session"""
        # Add multiple components to session
        self.session1.treatment_component_ids = [(4, self.component1.id), (4, self.component2.id)]
        
        # Test action with multiple components
        action = self.session1.action_view_components()
        self.assertEqual(action['domain'], [('session_ids', 'in', [self.session1.id])])
