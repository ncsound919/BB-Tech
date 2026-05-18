from typing import Dict
import pandas as pd
from sklearn.naive_bayes import MultinomialNB
from sklearn.preprocessing import KBinsDiscretizer

import warnings

class ClinicalPredictor:
    """
    Multinomial Naive Bayes for disease prediction
    Combines discrete symptoms with discretized continuous variables
    """
    
    def __init__(self):
        # Ignore scikit-learn's KBinsDiscretizer quantile warning for clean execution
        warnings.filterwarnings(
            "ignore", 
            category=FutureWarning, 
            module="sklearn.preprocessing._discretization"
        )
        self.model = MultinomialNB()
        self.discretizer = KBinsDiscretizer(
            n_bins=5,
            encode='ordinal',
            strategy='quantile'
        )
        self.is_fitted = False
        
    def preprocess_circulatory_data(self, df: pd.DataFrame, fit_discretizer: bool = False) -> pd.DataFrame:
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
        
        # Verify columns exist
        for col in continuous_features:
            if col not in df.columns:
                raise ValueError(f"Required column {col} missing from input DataFrame")
                
        df_processed = df.copy()
        if fit_discretizer:
            df_processed[continuous_features] = self.discretizer.fit_transform(
                df[continuous_features]
            )
        else:
            df_processed[continuous_features] = self.discretizer.transform(
                df[continuous_features]
            )
        
        return df_processed
    
    def train(self, X: pd.DataFrame, y: pd.Series):
        """Train MNB classifier on preprocessed data"""
        X_processed = self.preprocess_circulatory_data(X, fit_discretizer=True)
        self.model.fit(X_processed, y)
        self.is_fitted = True
        
    def predict_disease_probabilities(self, X: pd.DataFrame) -> Dict[str, float]:
        """
        Predict disease probabilities using Bayes' theorem
        
        P(Disease|Symptoms) ∝ P(Disease) * ∏ P(Symptom_i|Disease)
        
        Returns:
            Dictionary mapping disease names to probabilities
        """
        if not self.is_fitted:
            raise ValueError("Model must be trained first")
            
        X_processed = self.preprocess_circulatory_data(X, fit_discretizer=False)
        probabilities = self.model.predict_proba(X_processed)[0]
        
        disease_probs = {
            disease: float(prob)
            for disease, prob in zip(self.model.classes_, probabilities)
        }
        
        return disease_probs
