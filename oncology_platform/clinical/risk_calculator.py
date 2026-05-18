from typing import Dict, List
import numpy as np

class ContinuousRiskCalculator:
    """
    Continuous Individualized Risk Index (CIRI)
    Dynamic Bayesian updating of survival probability
    
    Analogous to in-game win probability in sports
    """
    
    def __init__(self):
        self.baseline_risk = 0.5
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
        risk_score = 0.0
        
        # Tumor size contribution
        if tumor_size > 0:
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
        baseline_prob = 1.0 - np.exp(-np.exp(risk_score))
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
        lr_shrinkage = np.exp(-tumor_shrinkage * 0.8)  # More shrinkage = better
        
        # Bayesian update
        eps = 1e-6
        prior_risk = min(max(self.baseline_risk, eps), 1.0 - eps)
        prior_odds = prior_risk / (1 - prior_risk)
        posterior_odds = prior_odds * lr_ctdna * lr_shrinkage
        posterior_prob = posterior_odds / (1 + posterior_odds)
        
        self.time_series_data.append({
            'time': time_point,
            'risk': posterior_prob,
            'ctdna': ctdna_level,
            'shrinkage': tumor_shrinkage
        })
        
        return posterior_prob
