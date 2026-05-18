from typing import Dict, List
import time
from oncology_platform.agents.triage_agent import BaseAgent, AgentState
from oncology_platform.simulation.stackelberg import StackelbergTherapyOptimizer
from oncology_platform.blockchain.polygon_bridge import PolygonBridge

class CoachAgent(BaseAgent):
    """
    Autonomous Coach (Simulation Agent) for running adaptive therapy game plan
    simulations, comparing MTD vs Adaptive schedules, and recommending optimal strategies.
    """
    
    def __init__(self, agent_id: str, bridge: PolygonBridge = None):
        super().__init__(agent_id)
        self.bridge = bridge or PolygonBridge("https://rpc-mumbai.matic.today", "0x5c32bF8DdB24eDE89e5306B626C1F789182343F4")
        self.optimizer = StackelbergTherapyOptimizer()
        
    def perceive(self, environment: Dict) -> Dict:
        """
        Sense patient tumor profile parameters
        
        Args:
            environment: Contains 'patient_id', 'tumor_burden' (int), 'resistant_fraction' (float)
        """
        return {
            'patient_id': environment.get('patient_id', 'PATIENT-T100'),
            'tumor_burden': environment.get('tumor_burden', 1e9),
            'resistant_fraction': environment.get('resistant_fraction', 0.05),
            'simulation_days': environment.get('simulation_days', 365)
        }
        
    def decide(self, perception: Dict) -> str:
        """
        Decide to run optimization game-plan simulation
        """
        if not perception.get('patient_id'):
            return 'IDLE'
        return 'RUN_THERAPY_OPTIMIZATION'
        
    def act(self, action: str, perception: Dict = None) -> Dict:
        """
        Run Lotka-Volterra competition solver, compare schedules, and output recommendations
        """
        if action == 'IDLE' or not perception:
            self.state = AgentState.IDLE
            return {'status': 'No active patient profile', 'strategy_recommendation': {}}
            
        self.state = AgentState.ACTING
        patient_id = perception['patient_id']
        simulation_days = perception['simulation_days']
        
        # 1. Simulate Maximum Tolerated Dose (MTD)
        ttp_mtd = self.optimizer.calculate_time_to_progression(
            dosing_strategy='MTD', 
            simulation_days=simulation_days
        )
        
        # 2. Simulate Adaptive Game-Theory Dosing
        ttp_adaptive = self.optimizer.calculate_time_to_progression(
            dosing_strategy='ADAPTIVE', 
            simulation_days=simulation_days
        )
        
        # Calculate improvements
        day_delay = ttp_adaptive - ttp_mtd
        pct_improvement = (day_delay / ttp_mtd) * 100 if ttp_mtd > 0 else 0.0
        
        # Determine recommended strategy
        if day_delay > 15:
            recommended_strategy = 'ADAPTIVE_LOTKA_VOLTERRA'
            rational = f"Adaptive dosing delayed progression by +{day_delay:.1f} days (+{pct_improvement:.1f}%) compared to MTD by exploiting competitive suppression (sensitive cells box out resistant clones)."
        else:
            recommended_strategy = 'MAXIMUM_TOLERATED_DOSE'
            rational = "Low resistant cell fraction or slow growth pace makes MTD sufficient for complete initial clearance without causing rapid competitive release."
            
        recommendation_report = {
            'patient_id': patient_id,
            'simulated_days': simulation_days,
            'mtd_time_to_progression_days': ttp_mtd,
            'adaptive_time_to_progression_days': ttp_adaptive,
            'clinical_delay_days': day_delay,
            'delay_improvement_percentage': pct_improvement,
            'recommended_strategy': recommended_strategy,
            'clinical_rational': rational,
            'timestamp': time.time()
        }
        
        # Secure ledger audit trail hashing
        record_hash = self.bridge.hash_medical_record(recommendation_report)
        tx_hash = self.bridge.store_hash_onchain(record_hash, "0xBBTechCoachAgent", "0xAgentPrivateKey")
        
        recommendation_report['record_hash'] = record_hash
        recommendation_report['tx_hash'] = tx_hash
        
        self.state = AgentState.COMPLETE
        
        self.log_action(action, {
            'recommendation': recommendation_report
        })
        
        return {
            'status': 'SUCCESS',
            'patient_id': patient_id,
            'recommendation': recommendation_report
        }
