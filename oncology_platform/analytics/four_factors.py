from typing import Dict

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
        return min(max(ki67_index, 0.0), 100.0)
    
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
            self.FACTOR_WEIGHTS['proliferation'] * factors.get('proliferation', 0.0) +
            self.FACTOR_WEIGHTS['clearance'] * factors.get('clearance', 0.0) +
            self.FACTOR_WEIGHTS['angiogenesis'] * factors.get('angiogenesis', 0.0) +
            self.FACTOR_WEIGHTS['metastasis'] * factors.get('metastasis', 0.0)
        )
