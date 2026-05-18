from typing import Dict, List
import pandas as pd
from oncology_platform.agents.triage_agent import BaseAgent, AgentState
from oncology_platform.analytics.ter_engine import TumorEfficiencyCalculator, TERComponents
from oncology_platform.analytics.four_factors import FourFactorsCalculator
from oncology_platform.blockchain.polygon_bridge import PolygonBridge

class StatCrewAgent(BaseAgent):
    """
    Autonomous Stat Crew (Data Engineer Agent) for clinical dataset validation,
    Codex metric calculation, and quality reporting.
    """
    
    def __init__(self, agent_id: str, bridge: PolygonBridge = None):
        super().__init__(agent_id)
        self.bridge = bridge or PolygonBridge("https://rpc-mumbai.matic.today", "0x5c32bF8DdB24eDE89e5306B626C1F789182343F4")
        self.ter_calc = TumorEfficiencyCalculator()
        self.four_factors_calc = FourFactorsCalculator()
        
    def perceive(self, environment: Dict) -> Dict:
        """
        Sense raw dataset input
        
        Args:
            environment: Contains 'raw_data' (list of Dict or pd.DataFrame)
        """
        raw_data = environment.get('raw_data', [])
        if isinstance(raw_data, list):
            df = pd.DataFrame(raw_data)
        elif isinstance(raw_data, pd.DataFrame):
            df = raw_data
        else:
            df = pd.DataFrame()
            
        return {'dataset': df}
        
    def decide(self, perception: Dict) -> str:
        """
        Decide action based on data availability
        """
        df = perception.get('dataset')
        if df is None or df.empty:
            return 'IDLE'
        return 'PROCESS_DATASET'
        
    def act(self, action: str, perception: Dict = None) -> Dict:
        """
        Validate schema, calculate TER & Four Factors, and output clean feature table
        """
        if action == 'IDLE' or not perception:
            self.state = AgentState.IDLE
            return {'status': 'No data to process', 'processed_records': []}
            
        self.state = AgentState.ACTING
        df = perception['dataset']
        
        # Required columns for schema validation
        required_cols = [
            'patient_id', 'field_goals', 'three_pointers', 
            'assists', 'offensive_rebounds', 'turnovers', 'personal_fouls'
        ]
        
        # Check missing columns
        missing_cols = [c for c in required_cols if c not in df.columns]
        if missing_cols:
            self.state = AgentState.IDLE
            return {
                'status': 'SCHEMA_VALIDATION_FAILED',
                'error': f'Missing required columns: {missing_cols}',
                'processed_records': []
            }
            
        processed_records = []
        
        # Ingest and process each patient record
        for _, row in df.iterrows():
            patient_id = row['patient_id']
            
            # Setup components for TER computation
            components = TERComponents(
                field_goals=float(row['field_goals']),
                three_pointers=float(row['three_pointers']),
                assists=float(row['assists']),
                offensive_rebounds=float(row['offensive_rebounds']),
                turnovers=float(row['turnovers']),
                personal_fouls=float(row['personal_fouls'])
            )
            
            # Compute TER (cell cycle time assumed 24h as standard)
            ter = self.ter_calc.calculate_ter(components, cell_cycle_time=24.0)
            classification = self.ter_calc.classify_malignancy(ter)
            
            # Compute Four Factors adaptation (proliferation, clearance, etc.)
            factors = {
                'proliferation': self.four_factors_calc.calculate_proliferation_score(float(row.get('ki67_index', 70.0))),
                'clearance': self.four_factors_calc.calculate_clearance_rate(
                    apoptotic_index=abs(float(row['turnovers'])),
                    division_rate=float(row['field_goals'])
                ),
                'angiogenesis': self.four_factors_calc.calculate_angiogenesis_score(float(row.get('mvd_index', 100.0))),
                'metastasis': self.four_factors_calc.calculate_metastatic_efficiency(
                    ctc_count=int(row.get('ctc_count', 10)),
                    tumor_burden=int(row.get('tumor_burden', 500))
                )
            }
            composite_percentage = self.four_factors_calc.composite_score(factors)
            
            record = {
                'patient_id': patient_id,
                'calculated_ter': ter,
                'classification': classification,
                'factors': factors,
                'composite_winning_percentage': composite_percentage
            }
            
            # Secure record integrity hashing
            record_hash = self.bridge.hash_medical_record(record)
            tx_hash = self.bridge.store_hash_onchain(record_hash, "0xBBTechStatCrewAgent", "0xAgentPrivateKey")
            
            record['record_hash'] = record_hash
            record['tx_hash'] = tx_hash
            
            processed_records.append(record)
            
        self.state = AgentState.COMPLETE
        
        self.log_action(action, {
            'records_processed': len(processed_records),
            'records': processed_records
        })
        
        return {
            'status': 'SUCCESS',
            'records_processed_count': len(processed_records),
            'processed_records': processed_records
        }
