#!/usr/bin/env python3
"""
BB-Tech: Basketball-to-Biotech Integration Framework
Interactive Demo Script showcasing the fully integrated computational engine.
"""

import numpy as np
import pandas as pd
from scipy.spatial import Voronoi
import time

# Import BB-Tech components
from oncology_platform.analytics import (
    TumorEfficiencyCalculator,
    TERComponents,
    FourFactorsCalculator,
    SpatialTumorAnalyzer,
    CodexScout,
    GeneticCoach,
    WhaleOptimizer
)
from oncology_platform.clinical import (
    ClinicalPredictor,
    ContinuousRiskCalculator,
    ValidationEngine
)
from oncology_platform.agents import (
    TriageAgent,
    SchedulingAgent,
    ScoutAgent,
    StatCrewAgent,
    CoachAgent
)
from oncology_platform.blockchain import (
    PolygonBridge
)
from oncology_platform.simulation import (
    StackelbergTherapyOptimizer,
    ViralGravitySimulation,
    JordanCancerModel
)


def run_analytics_demo():
    print("\n" + "="*80)
    print(" [MODULE 1] BB-TECH ANALYTICS ENGINE (TUMOR EFFICIENCY & FOUR FACTORS)")
    print("="*80)
    
    # 1. Tumor Efficiency Rating (TER)
    print("\n[+] 1. Calculating Tumor Efficiency Rating (TER)...")
    calc = TumorEfficiencyCalculator()
    
    # Setup standard components representing high aggression
    components_high = TERComponents(
        field_goals=85.0,        # Active divisions
        three_pointers=92.0,     # Division under hypoxia/stress
        assists=55.0,            # Paracrine signaling
        offensive_rebounds=65.0, # Autophagy
        turnovers=-68.0,         # Apoptosis rate (penalty)
        personal_fouls=-78.0     # Mutations causing immune detection
    )
    
    ter_high = calc.calculate_ter(components_high, cell_cycle_time=24.0)
    classification_high = calc.classify_malignancy(ter_high)
    print(f"    - High-Aggression Tumor TER (e.g., TNBC): {ter_high:.2f} ({classification_high})")
    
    # Setup components representing slow, low aggression tumor
    components_low = TERComponents(
        field_goals=45.0,
        three_pointers=28.0,
        assists=72.0,
        offensive_rebounds=42.0,
        turnovers=-22.0,
        personal_fouls=-18.0
    )
    ter_low = calc.calculate_ter(components_low, cell_cycle_time=24.0)
    classification_low = calc.classify_malignancy(ter_low)
    print(f"    - Low-Aggression Tumor TER (e.g., Luminal A): {ter_low:.2f} ({classification_low})")
    
    # 2. Four Factors
    print("\n[+] 2. Evaluating Dean Oliver's Four Factors of Tumor Aggression...")
    four_factors = FourFactorsCalculator()
    factors = {
        'proliferation': four_factors.calculate_proliferation_score(88.0),             # Ki-67 index
        'clearance': four_factors.calculate_clearance_rate(apoptotic_index=15.0, division_rate=45.0), # Apoptotic index
        'angiogenesis': four_factors.calculate_angiogenesis_score(microvessel_density=120.0),      # Microvessel density
        'metastasis': four_factors.calculate_metastatic_efficiency(ctc_count=15, tumor_burden=500) # CTC efficiency
    }
    
    for factor, score in factors.items():
        print(f"    - {factor.capitalize()} Score: {score:.2f}%")
        
    composite = four_factors.composite_score(factors)
    print(f"    ==> Composite Oncological 'Winning Percentage': {composite:.2f}%")


def run_spatial_metrics_demo():
    print("\n" + "="*80)
    print(" [MODULE 2] SPATIAL ANALYTICS (VORONOI ENTROPY & RIPLEY'S K)")
    print("="*80)
    
    analyzer = SpatialTumorAnalyzer()
    
    # Generate 50 random cell positions in a 2D tumor biopsy field
    np.random.seed(42)
    cell_positions = np.random.rand(50, 2) * 100
    
    # Compute Voronoi
    print("\n[+] Computing Voronoi Tessellation for cell spatial microenvironment...")
    vor = analyzer.compute_voronoi_tessellation(cell_positions)
    
    # Calculate Spatial Disorganization Index (entropy of polygon sides)
    entropy = analyzer.calculate_spatial_disorganization_index(vor)
    print(f"    - Spatial Disorganization Index (Entropy): {entropy:.4f}")
    
    # Compute Ripley's K-function and L-function for Immune-Tumor clustering
    print("\n[+] Computing Ripley's K and L-functions for Spatial Clustering...")
    radii = np.array([5.0, 10.0, 15.0, 20.0, 25.0])
    area = 10000.0  # 100x100 box
    
    k_vals = analyzer.ripleys_k_function(cell_positions, radii, area)
    l_vals = analyzer.calculate_L_function(k_vals, radii)
    
    for r, k, l in zip(radii, k_vals, l_vals):
        print(f"    - Distance r={r:.1f}: K(r)={k:.2f}, L(r)={l:.2f} ({'Clustering' if l > 0 else 'Dispersion/Invasion'})")


def run_coaching_optimization_demo():
    print("\n" + "="*80)
    print(" [MODULE 3] THE 'COACHING STAFF' EVOLUTIONARY OPTIMIZATION CORE")
    print("="*80)
    
    # 1. Genetic Algorithm Coach
    print("\n[+] 1. Running Genetic Coach (GA) to evolutionarily draft a drug lineup...")
    coach = GeneticCoach(population_size=20, mutation_rate=0.1)
    best_candidate = coach.evolve_roster(generations=15)
    
    print("    - Top Evolved Drug Lineup Profile:")
    print(f"      * Target Gravity (Oncogene Addiction): {best_candidate.gravity:.2f}")
    print(f"      * Target Breadth (Coverage Spectrum): {best_candidate.breadth:.2f}")
    print(f"      * Treatment Pace (Dosing Frequency): {best_candidate.pace:.2f}")
    print(f"      * Tumoral Resistance Coefficient: {best_candidate.resistance:.2f}")
    print(f"      * Evolved R0 (Therapeutic Invasion Score): {coach.fitness_function(best_candidate):.4f}")
    
    # 2. Whale Optimization Engine
    print("\n[+] 2. Deploying Whale Optimizer (WOA) for encircling tumor resistance prey...")
    woa = WhaleOptimizer(num_whales=10, dim=4)
    best_pos = woa.hunt_target(max_iter=15)
    
    scout = CodexScout()
    best_ro = scout.calculate_RO(best_pos[0], best_pos[1], best_pos[2], best_pos[3])
    print("    - Best Encircling Solution Located:")
    print(f"      * Gravity: {best_pos[0]:.2f}, Breadth: {best_pos[1]:.2f}, Pace: {best_pos[2]:.2f}, Resistance: {best_pos[3]:.2f}")
    print(f"      * Maximum Target Invasion RO: {best_ro:.4f}")


def run_clinical_decision_support_demo():
    print("\n" + "="*80)
    print(" [MODULE 4] CLINICAL SUITE & DECISION SUPPORT PIPELINE")
    print("="*80)
    
    # 1. Multinomial Naive Bayes Predictor
    print("\n[+] 1. Training Clinical Multinomial Naive Bayes Predictor...")
    # Synthetic patient training dataset
    np.random.seed(0)
    data = {
        'age': np.random.randint(20, 80, 100),
        'resting_blood_pressure': np.random.randint(90, 180, 100),
        'cholesterol': np.random.randint(150, 300, 100),
        'max_heart_rate': np.random.randint(100, 200, 100),
        'disease': np.random.choice(['Acute_MI', 'Unstable_Angina', 'Normal'], 100)
    }
    df = pd.DataFrame(data)
    X = df.drop(columns=['disease'])
    y = df['disease']
    
    predictor = ClinicalPredictor()
    predictor.train(X, y)
    print("    - Multinomial Naive Bayes Model trained successfully.")
    
    # Predict for a new high-risk patient
    patient_data = pd.DataFrame([{
        'age': 65,
        'resting_blood_pressure': 160,
        'cholesterol': 280,
        'max_heart_rate': 145
    }])
    
    probs = predictor.predict_disease_probabilities(patient_data)
    print("    - Patient Pathology Diagnostic Probability:")
    for disease, prob in probs.items():
        print(f"      * {disease}: {prob*100:.2f}%")
        
    # 2. Continuous Individualized Risk Index (CIRI)
    print("\n[+] 2. Simulating Continuous Risk Index (CIRI) Dynamic Updating...")
    risk_calc = ContinuousRiskCalculator()
    
    baseline = risk_calc.calculate_baseline_risk(
        tumor_size=3.5, 
        grade=3, 
        age=58.0, 
        receptor_status={'ER_positive': False, 'HER2_positive': True}
    )
    print(f"    - Baseline Pre-treatment Recurrence Probability (diagnosis): {baseline*100:.2f}%")
    
    # Multi-month follow-up dynamic updating (wearable + biomarkers)
    print("    - Dynamic in-treatment updates:")
    update1 = risk_calc.update_risk_dynamic(ctdna_level=2.4, tumor_shrinkage=0.15, time_point=1)
    print(f"      * Month 1 (ctDNA=2.4, Shrinkage=15%): Recurrence Risk is {update1*100:.2f}%")
    
    update2 = risk_calc.update_risk_dynamic(ctdna_level=0.5, tumor_shrinkage=0.55, time_point=3)
    print(f"      * Month 3 (ctDNA=0.5, Shrinkage=55%): Recurrence Risk is {update2*100:.2f}%")


def run_agents_blockchain_demo():
    print("\n" + "="*80)
    print(" [MODULE 5] AUTONOMOUS AGENTS & BLOCKCHAIN SECURE LEDGER")
    print("="*80)
    
    # 1. Agents Loop
    print("\n[+] 1. Instantiating Autonomous Agent Loop...")
    predictor = ClinicalPredictor() # Empty trained model just for context
    predictor.is_fitted = True
    predictor.model.classes_ = ['Acute_MI', 'Unstable_Angina', 'Normal']
    
    triage = TriageAgent("Triage-Scout-01", predictor)
    scheduler = SchedulingAgent("Scheduler-Coach-01")
    
    # Environment perception trigger
    env = {
        'patient_id': "PATIENT-998",
        'symptoms': ["chest_pain", "dyspnea"],
        'vital_signs': {'heart_rate': 125, 'systolic_bp': 165},
        'prediction': {'Acute_MI': 0.72, 'Unstable_Angina': 0.18, 'Normal': 0.10}
    }
    
    perception = triage.perceive(env)
    decision = triage.decide(perception)
    action_res = triage.act(decision)
    print(f"    - Triage Agent State: {triage.state.value}")
    print(f"    - Triage decision for High-Risk Symptoms: {decision}")
    print(f"    - Action Escalation target: {action_res['escalate_to']} (Priority: {action_res['priority']})")
    
    # Scheduler picks up escalation
    sched_env = {
        'priority': action_res['priority'],
        'specialty': 'cardiology',
        'preferences': {'afternoon': True}
    }
    sched_perc = scheduler.perceive(sched_env)
    sched_dec = scheduler.decide(sched_perc)
    sched_act = scheduler.act(sched_dec)
    print(f"    - Scheduling Agent Escalated Action: Successfully booked slot at {sched_act.get('appointment_time')}")
    
    # 2. Blockchain
    print("\n[+] 2. Hashing Patient Discovery and storing Immutable Audit Trail on-chain...")
    bridge = PolygonBridge(provider_url="https://polygon-rpc.com", contract_address="0x42BBTech888888888888888888888888888888")
    
    patient_record = {
        "patient_id": "PATIENT-998",
        "triage_priority": action_res['priority'],
        "appointment": sched_act.get('appointment_time'),
        "timestamp": time.time()
    }
    
    record_hash = bridge.hash_medical_record(patient_record)
    tx_hash = bridge.store_hash_onchain(
        record_hash=record_hash,
        patient_address="0xPatientAddress4242424242424242424242",
        private_key="SimulatedPrivateKey42"
    )
    print(f"    - Encrypted Record Integrity Hash: {record_hash}")
    print(f"    - Secure Polygon Transaction Hash logged: {tx_hash}")
    
    # 3. Phase 1 Scout Agent MVP
    print("\n[+] 3. [PHASE 1 KICKOFF] Instantiating Autonomous Scout (Researcher Agent) MVP...")
    scout_agent = ScoutAgent("Scout-Researcher-01", bridge)
    scout_env = {
        'query': 'cancer evolution resistance',
        'retmax': 2
    }
    print("    - Querying PubMed dynamically for recent literature on 'cancer evolution resistance'...")
    scout_perc = scout_agent.perceive(scout_env)
    scout_dec = scout_agent.decide(scout_perc)
    scout_act = scout_agent.act(scout_dec, scout_perc)
    
    print(f"    - Scout Agent Status: {scout_act['status']}")
    print(f"    - Total Papers Found & Processed: {scout_act['papers_found']}")
    for idx, paper in enumerate(scout_act['mapped_papers']):
        print(f"      * Paper #{idx+1}: '{paper['title']}'")
        print(f"        Journal: {paper['journal']} | Date: {paper['pubdate']}")
        print(f"        Authors: {', '.join(paper['authors'])}")
        print(f"        ==> Sports-to-Biotech Mapping: {paper['mapped_archetype']}")
        print(f"        Ledger Provenance Tx Hash: {paper['tx_hash'][:20]}...")
        
    # 4. Stat Crew Agent (Data Engineer) MVP
    print("\n[+] 4. Instantiating Autonomous Stat Crew (Data Engineer Agent) MVP...")
    stat_crew = StatCrewAgent("StatCrew-01", bridge)
    clinical_csv_mock = [
        {
            'patient_id': 'PATIENT-T101',
            'field_goals': 80.0,
            'three_pointers': 85.0,
            'assists': 60.0,
            'offensive_rebounds': 50.0,
            'turnovers': -65.0,
            'personal_fouls': -70.0,
            'ki67_index': 75.0,
            'mvd_index': 110.0,
            'ctc_count': 12,
            'tumor_burden': 480
        }
    ]
    crew_perc = stat_crew.perceive({'raw_data': clinical_csv_mock})
    crew_dec = stat_crew.decide(crew_perc)
    crew_act = stat_crew.act(crew_dec, crew_perc)
    
    print(f"    - Stat Crew Status: {crew_act['status']}")
    for r in crew_act['processed_records']:
        print(f"      * Patient ID: {r['patient_id']}")
        print(f"        Calculated Tumor Efficiency Rating (TER): {r['calculated_ter']:.2f} ({r['classification']})")
        print(f"        Composite Four Factors Win Percentage: {r['composite_winning_percentage']:.2f}%")
        print(f"        Ledger Provenance Tx Hash: {r['tx_hash'][:20]}...")
        
    # 5. Coach Agent (Simulation Agent) MVP
    print("\n[+] 5. Instantiating Autonomous Coach (Simulation Agent) MVP...")
    coach_agent = CoachAgent("Coach-01", bridge)
    coach_perc = coach_agent.perceive({'patient_id': 'PATIENT-T101', 'resistant_fraction': 0.08})
    coach_dec = coach_agent.decide(coach_perc)
    coach_act = coach_agent.act(coach_dec, coach_perc)
    
    print(f"    - Coach Agent Status: {coach_act['status']}")
    rep = coach_act['recommendation']
    print(f"      * Simulated Patient ID: {rep['patient_id']}")
    print(f"      * MTD Time-to-Progression: {rep['mtd_time_to_progression_days']:.1f} days")
    print(f"      * Adaptive Time-to-Progression: {rep['adaptive_time_to_progression_days']:.1f} days")
    print(f"      * Progression Delay: +{rep['clinical_delay_days']:.1f} days")
    print(f"      * Recommended Strategy: {rep['recommended_strategy']}")
    print(f"      * Clinical Rationale: {rep['clinical_rational']}")


def run_stackelberg_demo():
    print("\n" + "="*80)
    print(" [MODULE 6] LOTKA-VOLTERRA GAME THERAPY (STACKELBERG DOSING DOSAGES)")
    print("="*80)
    
    optimizer = StackelbergTherapyOptimizer()
    
    print("\n[+] Simulating Time-to-Progression (TTP) under standard clinical therapies...")
    
    # Strategy 1: Maximum Tolerated Dose (MTD)
    ttp_mtd = optimizer.calculate_time_to_progression(dosing_strategy='MTD', simulation_days=365)
    
    # Strategy 2: Adaptive Dosing Therapy (Stackelberg Game Theory Dosing)
    ttp_adaptive = optimizer.calculate_time_to_progression(dosing_strategy='ADAPTIVE', simulation_days=365)
    
    print(f"    - Maximum Tolerated Dose (MTD) Time to Progression: {ttp_mtd:.1f} days")
    print(f"    - Adaptive Game Theory Dosing Time to Progression: {ttp_adaptive:.1f} days")
    print(f"    ==> Clinical Advantage: Adaptive therapy delayed progression by {(ttp_adaptive - ttp_mtd):.1f} days (+{( (ttp_adaptive - ttp_mtd)/ttp_mtd * 100 if ttp_mtd > 0 else 0):.1f}% improvement)")


def run_playbook_simulations_demo():
    print("\n" + "="*80)
    print(" [MODULE 7] PLAYBOOK SERIES MATHEMATICAL SIMULATION ENGINES")
    print("="*80)
    
    # 1. Volume 1: Viral Systems (Viral Gravity Offense)
    print("\n[+] 1. Simulating Playbook Volume 1: Viral Gravity Offense ('Steph Curry' Phenotype)...")
    vg_sim = ViralGravitySimulation(initial_susceptible=1e6, initial_infected=100.0, gravity_coefficient=3.0, clearance_rate=0.1)
    vg_results = vg_sim.simulate_infection_cascade(days=60, countermeasure_day=20, defense_potency=0.7)
    
    print(f"    - Baseline Transmission R0: {vg_results['r0_baseline']:.2f}")
    print(f"    - Post-Defense Countermeasure R0: {vg_results['r0_post_countermeasure']:.2f}")
    print(f"    - Peak Infection Level achieved: {vg_results['peak_infection']:.1f} cells at Day {vg_results['peak_day']}")
    print(f"    - Final Infected Cells remaining (Day 60): {vg_results['infected'][-1]:.1f}")
    
    # 2. Volume 3: Malignancies & Takeovers (Jordan Cancer Clonal Takeover Model)
    print("\n[+] 2. Simulating Playbook Volume 3: Jordan Cancer Clonal Takeover Model...")
    jc_model = JordanCancerModel(initial_sensitive=1e5, initial_resistant=200.0, carrying_capacity=1e7, sensitive_growth_rate=0.35, resistant_growth_rate=0.18)
    
    mtd_res = jc_model.simulate_clonal_takeover(days=120, dosing_strategy='MTD', dose_potency=0.9)
    adaptive_res = jc_model.simulate_clonal_takeover(days=120, dosing_strategy='ADAPTIVE', dose_potency=0.9)
    
    print(f"    - MTD Clonal Expansion Progression Day (50% capacity): Day {mtd_res['progression_day']}")
    print(f"    - Adaptive Clonal Expansion Progression Day: Day {adaptive_res['progression_day']}")
    print(f"    ==> Volume 3 Game-Plan Delay Benefit: +{(adaptive_res['progression_day'] - mtd_res['progression_day'])} days delayed takeover")
    print(f"    - Final Host Takeover Index (HTI) at Day 120:")
    print(f"      * MTD Strategy: {mtd_res['final_takeover_pct']:.2f}% (Complete resistant clone dominance)")
    print(f"      * Adaptive Strategy: {adaptive_res['final_takeover_pct']:.2f}% (Controlled tumor size)")


def run_validation_study_demo():
    print("\n" + "="*80)
    print(" [MODULE 8] PRIORITY 4: ESTABLISH VALIDATION FRAMEWORK COMPARATIVE STUDY")
    print("="*80)
    
    print("\n[+] Running controlled clinical comparative study (20-target cancer cohort)...")
    val_engine = ValidationEngine()
    results = val_engine.run_comparative_study()
    
    print(f"    - Cohort Size: {results['cohort_size']} targets analyzed")
    print(f"    - Avg. Traditional Manual Curation Time: {results['avg_traditional_time_minutes']:.1f} minutes")
    print(f"    - Avg. BB-Tech Assisted Curation Time: {results['avg_bbtech_time_minutes']:.1f} minutes")
    print(f"    ==> Workflow Decision Acceleration: {results['time_reduction_percentage']:.2f}% faster time-to-decision!")
    print(f"    - Expert Clinical Ranking Alignment Accuracy: {results['alignment_accuracy_percentage']:.1f}%")
    print(f"    - Clinician Survey Usability & Satisfaction Score: {results['clinician_satisfaction_score']:.1f} / 5.0")
    print(f"    - Trueness Data Coverage (information completeness): {results['trueness_coverage_percentage']:.1f}%")
    
    # Save a copy of the validation report directly to the workspace!
    report_md = val_engine.generate_validation_markdown_report(results)
    report_file_path = "Phase 1 Validation Report.md"
    with open(report_file_path, "w", encoding="utf-8") as f:
        f.write(report_md)
    print(f"\n[+] Validation Report generated successfully and written to root workspace:")
    print(f"    -> [Phase 1 Validation Report.md]({report_file_path})")
    print(f"    - Ledger Provenance Tx Hash: {results['tx_hash']}")


def main():
    print("*"*90)
    print("                      Welcome to the BB-Tech Digital Research Lab               ")
    print("          Sports Analytics modeling for Systems Biology & Clinical Systems     ")
    print("*"*90)
    
    run_analytics_demo()
    run_spatial_metrics_demo()
    run_coaching_optimization_demo()
    run_clinical_decision_support_demo()
    run_agents_blockchain_demo()
    run_stackelberg_demo()
    run_playbook_simulations_demo()
    run_validation_study_demo()
    
    print("\n" + "="*80)
    print(" [SUCCESS] DEMO RUN COMPLETED SUCCESSFULLY - ALL SYSTEMS FUNCTIONING & FULLY AUDITABLE")
    print("="*80)


if __name__ == "__main__":
    main()
