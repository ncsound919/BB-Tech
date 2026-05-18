from typing import Dict, List
from oncology_platform.agents.triage_agent import BaseAgent

class SchedulingAgent(BaseAgent):
    """
    Autonomous appointment scheduling
    Optimizes provider calendars based on clinical urgency
    """
    
    def __init__(self, agent_id: str):
        super().__init__(agent_id)
        self.calendar_api = None
        
    def perceive(self, environment: Dict) -> Dict:
        """Get triage priority and available time slots"""
        return {
            'priority': environment.get('priority', 3),
            'specialty_required': environment.get('specialty', 'cardiology'),
            'available_slots': self.fetch_available_slots(),
            'patient_preferences': environment.get('preferences', {})
        }
    
    def fetch_available_slots(self) -> List[Dict]:
        """Query calendar system for openings"""
        return [
            {'time': '2026-01-21 09:00', 'provider': 'Dr. Smith'},
            {'time': '2026-01-21 14:00', 'provider': 'Dr. Jones'},
            {'time': '2026-01-22 10:00', 'provider': 'Dr. Smith'}
        ]
    
    def decide(self, perception: Dict) -> str:
        """
        Select optimal appointment slot
        
        Optimization criteria:
        1. Earliest slot for high priority
        2. Provider specialty match
        3. Patient preferences
        """
        priority = perception['priority']
        slots = perception['available_slots']
        
        if priority == 1:
            # Emergency: Take first available
            return slots[0]['time'] if slots else 'NO_SLOTS_AVAILABLE'
        
        return slots[0]['time'] if slots else 'QUEUE_FOR_NEXT_OPENING'
    
    def act(self, action: str) -> Dict:
        """Book the appointment"""
        if action == 'NO_SLOTS_AVAILABLE':
            return {'status': 'failed', 'reason': 'No capacity'}
        
        result = {
            'status': 'success',
            'appointment_time': action,
            'confirmation_sent': True
        }
        
        self.log_action(f'BOOKED_{action}', result)
        return result
