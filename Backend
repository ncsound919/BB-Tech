# ==============================================================================
# ONCOLOGY ANALYTICS PLATFORM - DEEP BACKEND SCAFFOLD
# Integration of Sports Analytics with Cancer Biology
# ==============================================================================

"""
PROJECT STRUCTURE:
oncology_platform/
├── core/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── analytics/
│   ├── __init__.py
│   ├── models.py          # Data models
│   ├── ter_engine.py      # Tumor Efficiency Rating
│   ├── four_factors.py    # Four Factors calculation
│   ├── spatial_metrics.py # Voronoi, Ripley's K
│   └── game_theory.py     # Evolutionary game models
├── clinical/
│   ├── __init__.py
│   ├── models.py
│   ├── mnb_predictor.py   # Multinomial Naive Bayes
│   ├── discretizer.py     # Continuous → Categorical
│   ├── fhir_mapper.py     # FHIR resource generation
│   └── risk_calculator.py # CIRI implementation
├── agents/
│   ├── __init__.py
│   ├── orchestrator.py    # Multi-agent coordinator
│   ├── triage_agent.py    # Clinical triage
│   ├── scheduling_agent.py
│   └── followup_agent.py
├── blockchain/
│   ├── __init__.py
│   ├── polygon_bridge.py  # Web3 integration
│   ├── contracts.sol      # Smart contracts
│   └── consent_manager.py
├── iot/
│   ├── __init__.py
│   ├── ble_handler.py     # Bluetooth integration
│   ├── signal_processor.py
│   └── fhir_observation.py
├── simulation/
│   ├── __init__.py
│   ├── mesa_model.py      # Agent-based modeling
│   └── stackelberg.py     # Game theory optimization
└── api/
    ├── __init__.py
    ├── views.py
    ├── serializers.py
    └── permissions.py
"""

# ==============================================================================
# 1. ANALYTICS MODULE - TER ENGINE
# ==============================================================================

from dataclasses import dataclass
from typing import List, Dict, Optional
import numpy as np
from scipy.spatial import Voronoi
from sklearn.preprocessing import KBinsDiscretizer
from sklearn.naive_bayes import MultinomialNB
import pandas as pd

@dataclass
class TERComponents:
    """Tumor Efficiency Rating Components (Basketball → Biology)"""
    field_goals: float = 0.0        # Standard mitotic divisions
    three_pointers: float = 0.0     # Division under stress (hypoxia/chemo)
    assists: float = 0.0            # Paracrine signaling (VEGF, etc.)
    offensive_rebounds: float = 0.0 # Autophagy/metabolic scavenging
    turnovers: float = 0.0          # Apoptosis/necrosis
    personal_fouls: float = 0.0     # Deleterious mutations
    
    # Weights from NBA PER formula
    WEIGHTS = {
        'fg': 1.65,
        '3p': 2.65,
        'ast': 0.67,
        'orb': 0.79,
        'tov': -1.04,
        'pf': -0.35
    }
    
class TumorEfficiencyCalculator:
    """
    Calculate Tumor Efficiency Rating (TER)
    Adapted from John Hollinger's Player Efficiency Rating
    
    TER quantifies malignant potential per cell cycle
    """
    
    def __init__(self):
        self.league_average_pace = 100  # Cell cycles per unit time
        
    def calculate_ter(self, components: TERComponents, 
                     cell_cycle_time: float) -> float:
        """
        Calculate composite TER score
        
        Args:
            components: TERComponents with biological events
            cell_cycle_time: Duration of cell cycle (analogous to minutes played)
            
        Returns:
            Tumor Efficiency Rating (normalized to league average = 15.0)
        """
        unadjusted_ter = (
            components.WEIGHTS['fg'] * components.field_goals +
            components.WEIGHTS['3p'] * components.three_pointers +
            components.WEIGHTS['ast'] * components.assists +
            components.WEIGHTS['orb'] * components.offensive_rebounds +
            components.WEIGHTS['tov'] * components.turnovers +
            components.WEIGHTS['pf'] * components.personal_fouls
        )
        
        # Normalize by cell cycle time (per-minute rating)
        ter_per_cycle = unadjusted_ter / cell_cycle_time
        
        # Adjust to league average (15.0 standard)
        adjusted_ter = ter_per_cycle * (self.league_average_pace / 100)
        
        return adjusted_ter
    
    def classify_malignancy(self, ter: float) -> str:
        """Classify tumor aggressiveness by TER threshold"""
        if ter > 25:
            return "ELITE_MALIGNANT"  # MVP-level threat
        elif ter > 20:
            return "HIGH_AGGRESSIVE"
        elif ter > 15:
            return "MODERATE"
        else:
            return "LOW_AGGRESSIVE"


class FourFactorsCalculator:
    """
    Dean Oliver's Four Factors adapted to oncology
    
    Factor 1: Shooting (eFG%) → Proliferation (Ki-67)
    Factor 2: Turnovers (TOV%) → Clearance Rate (Apoptotic Index)
    Factor 3: Rebounding (ORB%) → Angiogenesis (MVD)
    Factor 4: Free Throws (FTR) → Metastatic Efficiency (CTC)
    """
    
    FACTOR_WEIGHTS = {
        'proliferation': 0.40,
        'clearance': 0.25,
        'angiogenesis': 0.20,
        'metastasis': 0.15
    }
    
    def calculate_proliferation_score(self, ki67_index: float) -> float:
        """
        Factor 1: Proliferation Intensity
        
        Args:
            ki67_index: Percentage of Ki-67+ cells (0-100)
            
        Returns:
            Normalized proliferation score (0-100)
        """
        # Ki-67 thresholds from clinical data
        # TNBC: 40-80%, Luminal A: <20%, HER2+: 20-60%
        return min(ki67_index, 100.0)
    
    def calculate_clearance_rate(self, apoptotic_index: float,
                                 division_rate: float) -> float:
        """
        Factor 2: Turnover Percentage
        
        TOV% = Turnovers / (FGA + 0.44*FTA + TOV)
        Biology: Apoptosis / (Divisions + Arrests + Apoptosis)
        """
        total_events = division_rate + apoptotic_index
        if total_events == 0:
            return 0.0
        return (apoptotic_index / total_events) * 100
    
    def calculate_angiogenesis_score(self, microvessel_density: float) -> float:
        """
        Factor 3: Offensive Rebounding (Resource Acquisition)
        
        Args:
            microvessel_density: MVD count per high-power field
        """
        # Normalize MVD (typical range: 10-200)
        return min((microvessel_density / 200) * 100, 100.0)
    
    def calculate_metastatic_efficiency(self, ctc_count: float,
                                       tumor_burden: float) -> float:
        """
        Factor 4: Free Throw Rate (Metastatic Efficiency)
        
        FTR = FTA / FGA
        Biology: CTCs / Total Tumor Cells
        """
        if tumor_burden == 0:
            return 0.0
        return (ctc_count / tumor_burden) * 100
    
    def composite_score(self, factors: Dict[str, float]) -> float:
        """
        Calculate weighted composite of four factors
        
        Returns:
            Overall oncological "winning percentage"
        """
        return (
            self.FACTOR_WEIGHTS['proliferation'] * factors['proliferation'] +
            self.FACTOR_WEIGHTS['clearance'] * factors['clearance'] +
            self.FACTOR_WEIGHTS['angiogenesis'] * factors['angiogenesis'] +
            self.FACTOR_WEIGHTS['metastasis'] * factors['metastasis']
        )


# ==============================================================================
# 2. SPATIAL ANALYTICS - VORONOI & RIPLEY'S K
# ==============================================================================

class SpatialTumorAnalyzer:
    """
    Spatial pattern analysis using computational geometry
    
    Implements:
    - Voronoi tessellation for tumor architecture
    - Ripley's K-function for immune cell clustering
    - Cross-K for tumor-immune interactions
    """
    
    def __init__(self):
        self.voronoi_computed = False
        
    def compute_voronoi_tessellation(self, cell_positions: np.ndarray) -> Voronoi:
        """
        Compute Voronoi diagram from cell nuclei coordinates
        
        Args:
            cell_positions: Nx2 array of (x,y) coordinates
            
        Returns:
            scipy.spatial.Voronoi object
        """
        vor = Voronoi(cell_positions)
        self.voronoi_computed = True
        return vor
    
    def calculate_spatial_disorganization_index(self, vor: Voronoi) -> float:
        """
        Quantify entropy of Voronoi tessellation
        
        Healthy tissue: Regular hexagonal packing (low entropy)
        Malignant tissue: Irregular polygons (high entropy)
        
        Returns:
            Shannon entropy of polygon side distribution
        """
        if not self.voronoi_computed:
            raise ValueError("Must compute Voronoi first")
            
        # Count sides of each Voronoi polygon
        polygon_sides = []
        for region_idx in vor.regions:
            if -1 not in region_idx and len(region_idx) > 0:
                polygon_sides.append(len(region_idx))
        
        # Calculate Shannon entropy
        side_counts = np.bincount(polygon_sides)
        probabilities = side_counts / side_counts.sum()
        entropy = -np.sum(probabilities * np.log2(probabilities + 1e-10))
        
        return entropy
    
    def ripleys_k_function(self, points: np.ndarray, 
                          radii: np.ndarray,
                          area: float) -> np.ndarray:
        """
        Ripley's K-function for point pattern analysis
        
        K(r) = (Area / n²) * Σ Σ I(d_ij < r)
        
        Args:
            points: Nx2 array of point coordinates
            radii: Array of distance thresholds
            area: Total area of observation window
            
        Returns:
            K(r) values for each radius
        """
        n = len(points)
        k_values = []
        
        for r in radii:
            count = 0
            for i in range(n):
                for j in range(i+1, n):
                    dist = np.linalg.norm(points[i] - points[j])
                    if dist < r:
                        count += 2  # Count both i→j and j→i
            
            k = (area / (n * n)) * count
            k_values.append(k)
        
        return np.array(k_values)
    
    def calculate_L_function(self, k_values: np.ndarray, 
                            radii: np.ndarray) -> np.ndarray:
        """
        Normalized Ripley's K (L-function)
        
        L(r) = sqrt(K(r) / π) - r
        
        L(r) > 0: Clustering (immune cells around tumor)
        L(r) = 0: Random distribution
        L(r) < 0: Dispersion (immune exclusion)
        """
        return np.sqrt(k_values / np.pi) - radii


# ==============================================================================
# 3. CLINICAL MODULE - MULTINOMIAL NAIVE BAYES
# ==============================================================================

class ClinicalPredictor:
    """
    Multinomial Naive Bayes for disease prediction
    Combines discrete symptoms with discretized continuous variables
    """
    
    def __init__(self):
        self.model = MultinomialNB()
        self.discretizer = KBinsDiscretizer(
            n_bins=5,
            encode='ordinal',
            strategy='quantile'
        )
        self.is_fitted = False
        
    def preprocess_circulatory_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Discretize continuous physiological variables
        
        Bins continuous features into clinically relevant categories:
        - Blood Pressure: Normal, Elevated, Stage 1, Stage 2
        - Heart Rate: Bradycardia, Normal, Tachycardia
        - Cholesterol: Optimal, Borderline, High
        """
        continuous_features = [
            'age', 'resting_blood_pressure', 
            'cholesterol', 'max_heart_rate'
        ]
        
        df_processed = df.copy()
        df_processed[continuous_features] = self.discretizer.fit_transform(
            df[continuous_features]
        )
        
        return df_processed
    
    def train(self, X: pd.DataFrame, y: pd.Series):
        """Train MNB classifier on preprocessed data"""
        X_processed = self.preprocess_circulatory_data(X)
        self.model.fit(X_processed, y)
        self.is_fitted = True
        
    def predict_disease_probabilities(self, 
                                     X: pd.DataFrame) -> Dict[str, float]:
        """
        Predict disease probabilities using Bayes' theorem
        
        P(Disease|Symptoms) ∝ P(Disease) * ∏ P(Symptom_i|Disease)
        
        Returns:
            Dictionary mapping disease names to probabilities
        """
        if not self.is_fitted:
            raise ValueError("Model must be trained first")
            
        X_processed = self.preprocess_circulatory_data(X)
        probabilities = self.model.predict_proba(X_processed)[0]
        
        disease_probs = {
            disease: prob 
            for disease, prob in zip(self.model.classes_, probabilities)
        }
        
        return disease_probs


class ContinuousRiskCalculator:
    """
    Continuous Individualized Risk Index (CIRI)
    Dynamic Bayesian updating of survival probability
    
    Analogous to in-game win probability in sports
    """
    
    def __init__(self):
        self.baseline_risk = None
        self.time_series_data = []
        
    def calculate_baseline_risk(self, 
                                tumor_size: float,
                                grade: int,
                                age: float,
                                receptor_status: Dict[str, bool]) -> float:
        """
        Pre-game probability (diagnosis)
        
        Uses Cox proportional hazards model structure
        """
        # Simplified risk calculation (real would use validated nomogram)
        risk_score = 0.0
        
        # Tumor size contribution
        risk_score += np.log(tumor_size) * 0.3
        
        # Grade (1-3)
        risk_score += grade * 0.2
        
        # Age
        risk_score += (age / 100) * 0.15
        
        # Receptor status (protective)
        if receptor_status.get('ER_positive', False):
            risk_score -= 0.4
        if receptor_status.get('HER2_positive', False):
            risk_score += 0.3  # Without treatment, increases risk
            
        # Convert to 5-year recurrence probability
        baseline_prob = 1 - np.exp(-np.exp(risk_score))
        self.baseline_risk = baseline_prob
        
        return baseline_prob
    
    def update_risk_dynamic(self, 
                           ctdna_level: float,
                           tumor_shrinkage: float,
                           time_point: int) -> float:
        """
        Dynamic Bayesian update (in-game adjustment)
        
        Args:
            ctdna_level: Circulating tumor DNA concentration
            tumor_shrinkage: Percentage reduction in tumor volume
            time_point: Time since treatment start (months)
            
        Returns:
            Updated probability of recurrence
        """
        # Likelihood ratio based on biomarkers
        lr_ctdna = np.exp(-ctdna_level * 0.5)  # Lower ctDNA = better
        lr_shrinkage = np.exp(tumor_shrinkage * 0.8)  # More shrinkage = better
        
        # Bayesian update
        prior_odds = self.baseline_risk / (1 - self.baseline_risk)
        posterior_odds = prior_odds * lr_ctdna * lr_shrinkage
        posterior_prob = posterior_odds / (1 + posterior_odds)
        
        self.time_series_data.append({
            'time': time_point,
            'risk': posterior_prob,
            'ctdna': ctdna_level,
            'shrinkage': tumor_shrinkage
        })
        
        return posterior_prob


# ==============================================================================
# 4. AGENT FRAMEWORK - AUTONOMOUS CLINICAL WORKFLOWS
# ==============================================================================

from enum import Enum
from abc import ABC, abstractmethod

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
        
        max_risk_prob = max(
            prediction.get(disease, 0) 
            for disease in high_risk_diseases
        )
        
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


class SchedulingAgent(BaseAgent):
    """
    Autonomous appointment scheduling
    Optimizes provider calendars based on clinical urgency
    """
    
    def __init__(self, agent_id: str):
        super().__init__(agent_id)
        self.calendar_api = None  # Would connect to Google Calendar, etc.
        
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
        # Placeholder - would integrate with real calendar API
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
        
        # For lower priority, could optimize further
        # (e.g., minimize travel, preferred provider)
        return slots[0]['time'] if slots else 'QUEUE_FOR_NEXT_OPENING'
    
    def act(self, action: str) -> Dict:
        """Book the appointment"""
        if action == 'NO_SLOTS_AVAILABLE':
            return {'status': 'failed', 'reason': 'No capacity'}
        
        # Would call calendar API to create event
        result = {
            'status': 'success',
            'appointment_time': action,
            'confirmation_sent': True
        }
        
        self.log_action(f'BOOKED_{action}', result)
        return result


# ==============================================================================
# 5. BLOCKCHAIN INTEGRATION - POLYGON BRIDGE
# ==============================================================================

from web3 import Web3
from eth_account import Account
import json

class PolygonBridge:
    """
    Interface to Polygon blockchain for:
    - Smart contract escrow payments
    - Data integrity hashing
    - Patient consent management
    """
    
    def __init__(self, provider_url: str, contract_address: str):
        self.w3 = Web3(Web3.HTTPProvider(provider_url))
        self.contract_address = contract_address
        self.contract = None
        
    def load_contract(self, abi_path: str):
        """Load smart contract ABI"""
        with open(abi_path, 'r') as f:
            abi = json.load(f)
        self.contract = self.w3.eth.contract(
            address=self.contract_address,
            abi=abi
        )
    
    def book_consultation_escrow(self, 
                                 patient_address: str,
                                 doctor_address: str,
                                 fee_matic: float,
                                 private_key: str) -> str:
        """
        Create escrow for medical consultation
        
        Args:
            patient_address: Patient's wallet
            doctor_address: Provider's wallet
            fee_matic: Consultation fee in MATIC
            private_key: Patient's private key for signing
            
        Returns:
            Transaction hash
        """
        # Build transaction
        nonce = self.w3.eth.get_transaction_count(patient_address)
        
        txn = self.contract.functions.bookConsultation(
            doctor_address
        ).build_transaction({
            'from': patient_address,
            'value': self.w3.to_wei(fee_matic, 'ether'),
            'gas': 200000,
            'gasPrice': self.w3.eth.gas_price,
            'nonce': nonce
        })
        
        # Sign transaction
        signed_txn = self.w3.eth.account.sign_transaction(
            txn, private_key=private_key
        )
        
        # Send transaction
        tx_hash = self.w3.eth.send_raw_transaction(
            signed_txn.rawTransaction
        )
        
        return tx_hash.hex()
    
    def hash_medical_record(self, record_data: Dict) -> str:
        """
        Create SHA-256 hash of medical record for on-chain storage
        
        Ensures data integrity without exposing PHI
        """
        # Serialize record to deterministic JSON
        record_json = json.dumps(record_data, sort_keys=True)
        record_hash = self.w3.keccak(text=record_json)
        
        return record_hash.hex()
    
    def store_hash_onchain(self, 
                          record_hash: str,
                          patient_address: str,
                          private_key: str) -> str:
        """
        Store hash on Polygon for immutable audit trail
        """
        nonce = self.w3.eth.get_transaction_count(patient_address)
        
        txn = self.contract.functions.storeRecordHash(
            record_hash
        ).build_transaction({
            'from': patient_address,
            'gas': 100000,
            'gasPrice': self.w3.eth.gas_price,
            'nonce': nonce
        })
        
        signed_txn = self.w3.eth.account.sign_transaction(
            txn, private_key=private_key
        )
        
        tx_hash = self.w3.eth.send_raw_transaction(
            signed_txn.rawTransaction
        )
        
        return tx_hash.hex()


# ==============================================================================
# 6. EVOLUTIONARY GAME THEORY - STACKELBERG OPTIMIZATION
# ==============================================================================

from scipy.optimize import minimize

class StackelbergTherapyOptimizer:
    """
    Stackelberg game model for adaptive therapy
    
    Leader: Physician chooses drug dose D(t)
    Follower: Tumor evolves resistance frequency f_r(t)
    
    Objective: Maximize time to progression (TTP)
    """
    
    def __init__(self):
        self.sensitive_fitness = 1.0
        self.resistant_fitness = 0.85  # Cost of resistance
        self.drug_kill_rate = 0.7
        
    def tumor_growth_ode(self, state, t, drug_dose):
        """
        Lotka-Volterra competition model
        
        dS/dt = r_s * S * (1 - (S+R)/K) - d * drug_dose * S
        dR/dt = r_r * R * (1 - (S+R)/K)
        
        S: Sensitive cells
        R: Resistant cells
        """
        S, R = state
        K = 1e9  # Carrying capacity
        
        r_s = self.sensitive_fitness
        r_r = self.resistant_fitness
        d = self.drug_kill_rate
        
        dS = r_s * S * (1 - (S + R)/K) - d * drug_dose * S
        dR = r_r * R * (1 - (S + R)/K)
        
        return [dS, dR]
    
    def adaptive_dosing_strategy(self, 
                                 current_tumor_size: float,
                                 target_size: float) -> float:
        """
        Adaptive therapy: Dose to maintain stable size
        
        Args:
            current_tumor_size: Current total cells
            target_size: Desired tumor burden (50% of baseline)
            
        Returns:
            Optimal drug dose
        """
        if current_tumor_size < target_size * 0.9:
            return 0.0  # Holiday - let sensitive cells grow back
        elif current_tumor_size > target_size * 1.1:
            return 1.0  # Full dose to shrink
        else:
            # Proportional control
            error = (current_tumor_size - target_size) / target_size
            dose = 0.5 + 0.5 * error  # PID-like control
            return max(0.0, min(1.0, dose))
    
    def calculate_time_to_progression(self, 
                                     dosing_strategy: str,
                                     simulation_days: int = 365) -> float:
        """
        Simulate TTP under different strategies
        
        Args:
            dosing_strategy: 'MTD' or 'ADAPTIVE'
            simulation_days: Simulation duration
            
        Returns:
            Time to progression (days)
        """
        # Initial conditions
        S0 = 1e8  # Sensitive cells
        R0 = 1e6  # Resistant cells (1% of total)
        
        tumor_sizes = []
        time_points = np.linspace(0, simulation_days, simulation_days)
        
        for t in
