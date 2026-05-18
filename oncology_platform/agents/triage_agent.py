from enum import Enum
from abc import ABC, abstractmethod
from typing import Dict, List
import pandas as pd
from oncology_platform.clinical.mnb_predictor import ClinicalPredictor

class AgentState(Enum):
    IDLE = "idle"
    ANALYZING = "analyzing"
    ACTING = "acting"
    WAITING = "waiting"
    COMPLETE = "complete"

class BaseAgent(ABC):
    """Abstract base class for autonomous agents"""
    
    def __init__(self, agent_id: str):
        self.agent_id = agent_id
        self.state = AgentState.IDLE
        self.memory = []
        
    @abstractmethod
    def perceive(self, environment: Dict) -> Dict:
        """Sense the current state"""
        pass
    
    @abstractmethod
    def decide(self, perception: Dict) -> str:
        """Determine action based on perception"""
        pass
    
    @abstractmethod
    def act(self, action: str) -> Dict:
        """Execute the decided action"""
        pass
    
    def log_action(self, action: str, result: Dict):
        """Maintain agent memory for ISO 42001 compliance"""
        self.memory.append({
            'timestamp': pd.Timestamp.now(),
            'action': action,
            'result': result,
            'state': self.state.value
        })

class TriageAgent(BaseAgent):
    """
    Autonomous triage agent for clinical prioritization
    
    Combines MNB predictions with rule-based protocols
    (Manchester Triage System)
    """
    
    def __init__(self, agent_id: str, predictor: ClinicalPredictor):
        super().__init__(agent_id)
        self.predictor = predictor
        self.urgency_threshold = 0.8
        
    def perceive(self, environment: Dict) -> Dict:
        """
        Ingest patient data and prediction results
        
        Args:
            environment: Contains patient_data, sensor_readings, prediction
        """
        return {
            'patient_id': environment.get('patient_id'),
            'symptoms': environment.get('symptoms', []),
            'vital_signs': environment.get('vital_signs', {}),
            'prediction': environment.get('prediction', {})
        }
    
    def decide(self, perception: Dict) -> str:
        """
        Determine triage level
        
        Returns:
            Action: 'EMERGENCY', 'URGENT', 'ROUTINE', 'MONITOR'
        """
        prediction = perception['prediction']
        
        # Check for high-risk conditions
        high_risk_diseases = [
            'Acute_MI', 'Unstable_Angina', 'Pulmonary_Embolism'
        ]
        
        max_risk_prob = 0.0
        if prediction:
            risk_values = [
                prediction.get(disease, 0.0) 
                for disease in high_risk_diseases if disease in prediction
            ]
            if risk_values:
                max_risk_prob = max(risk_values)
        
        vital_signs = perception['vital_signs']
        hr = vital_signs.get('heart_rate', 70)
        sbp = vital_signs.get('systolic_bp', 120)
        
        # Rule-based escalation
        if max_risk_prob > 0.85 or hr > 140 or sbp > 180:
            return 'EMERGENCY'
        elif max_risk_prob > 0.65 or hr > 120:
            return 'URGENT'
        elif max_risk_prob > 0.4:
            return 'ROUTINE'
        else:
            return 'MONITOR'
    
    def act(self, action: str) -> Dict:
        """
        Execute triage action
        
        Returns:
            Action result with assigned priority and next steps
        """
        action_map = {
            'EMERGENCY': {
                'priority': 1,
                'escalate_to': 'emergency_services',
                'max_wait_minutes': 0
            },
            'URGENT': {
                'priority': 2,
                'escalate_to': 'scheduling_agent',
                'max_wait_minutes': 60
            },
            'ROUTINE': {
                'priority': 3,
                'escalate_to': 'scheduling_agent',
                'max_wait_minutes': 1440  # 24 hours
            },
            'MONITOR': {
                'priority': 4,
                'escalate_to': 'followup_agent',
                'max_wait_minutes': 10080  # 7 days
            }
        }
        
        result = action_map.get(action, action_map['MONITOR'])
        self.log_action(action, result)
        
        return result
