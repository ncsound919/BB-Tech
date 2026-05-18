import React, { useState } from 'react';
import { BarChart, Bar, LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar } from 'recharts';
import { Activity, Database, Cpu, Network, Shield, TrendingUp, Users, Clock } from 'lucide-react';

const OncologyAnalyticsPlatform = () => {
  const [activePhase, setActivePhase] = useState('foundation');
  const [selectedMetric, setSelectedMetric] = useState('TER');

  // Tumor Efficiency Rating (TER) sample data
  const terData = [
    { metric: 'Division (FG)', weight: 1.65, tnbc: 85, luminalA: 45, her2: 62 },
    { metric: 'Stress Division (3P)', weight: 2.65, tnbc: 92, luminalA: 28, her2: 58 },
    { metric: 'Paracrine (AST)', weight: 0.67, tnbc: 55, luminalA: 72, her2: 65 },
    { metric: 'Apoptosis (TOV)', weight: -1.04, tnbc: 68, luminalA: 22, her2: 45 },
    { metric: 'Mutations (PF)', weight: -0.35, tnbc: 78, luminalA: 18, her2: 42 }
  ];

  // Four Factors comparison
  const fourFactorsData = [
    { factor: 'Proliferation', weight: 40, tnbc: 88, luminalA: 35, her2: 65 },
    { factor: 'Clearance Rate', weight: 25, tnbc: 72, luminalA: 15, her2: 48 },
    { factor: 'Angiogenesis', weight: 20, tnbc: 65, luminalA: 42, her2: 78 },
    { factor: 'Metastatic Efficiency', weight: 15, tnbc: 82, luminalA: 28, her2: 58 }
  ];

  // Radar chart for subtype comparison
  const subtypeRadarData = [
    { metric: 'Ki-67 Index', TNBC: 80, LuminalA: 30, HER2: 60, fullMark: 100 },
    { metric: 'Doubling Speed', TNBC: 85, LuminalA: 20, HER2: 55, fullMark: 100 },
    { metric: 'MVD Score', TNBC: 65, LuminalA: 40, HER2: 75, fullMark: 100 },
    { metric: 'PD-L1 Expression', TNBC: 70, LuminalA: 25, HER2: 45, fullMark: 100 },
    { metric: 'CTC Efficiency', TNBC: 78, LuminalA: 30, HER2: 52, fullMark: 100 }
  ];

  // Timeline data
  const timelinePhases = [
    {
      id: 'foundation',
      name: 'Phase 1: Foundation & PoC',
      months: '0-4',
      color: 'bg-blue-500',
      deliverables: [
        'TER Calculation Engine implementation',
        'FHIR Pipeline integration',
        'ABM Model (Mesa Framework)',
        'Blockchain consent layer (Polygon testnet)'
      ],
      gate: 'Gate 1: TER validates against METABRIC/TCGA datasets'
    },
    {
      id: 'clinical',
      name: 'Phase 2: Clinical Translation',
      months: '4-8',
      color: 'bg-green-500',
      deliverables: [
        'Multinomial Naïve Bayes predictor',
        'Agentic system (LangGraph)',
        'Production FHIR resources',
        'HIPAA/GDPR compliance framework'
      ],
      gate: 'Gate 2: MNB achieves >75% accuracy on validation cohort'
    },
    {
      id: 'validation',
      name: 'Phase 3: Validation & Market',
      months: '8-12',
      color: 'bg-orange-500',
      deliverables: [
        'Clinical pilot (50 patients)',
        'Regulatory strategy (ISO 42001)',
        'Business intelligence dashboards',
        'Federated learning network'
      ],
      gate: 'Gate 3: Pilot demonstrates clinical utility & safety'
    },
    {
      id: 'ecosystem',
      name: 'Phase 4: Ecosystem',
      months: '12-18',
      color: 'bg-purple-500',
      deliverables: [
        'LLM agent deployment',
        'Blockchain mainnet launch',
        'Multi-hospital federation',
        'Commercial gamification platform'
      ],
      gate: 'Gate 4: Platform achieves regulatory approval & market adoption'
    }
  ];

  const technicalStack = [
    {
      category: 'Data Layer',
      icon: Database,
      components: [
        { name: 'Time-Series DB', tech: 'InfluxDB/Timestream', purpose: 'Wearable sensor data' },
        { name: 'Data Lake', tech: 'AWS S3', purpose: 'Raw clinical data' },
        { name: 'RDBMS', tech: 'PostgreSQL', purpose: 'Structured patient records' },
        { name: 'FHIR Server', tech: 'HAPI FHIR', purpose: 'Healthcare interoperability' }
      ]
    },
    {
      category: 'Compute Layer',
      icon: Cpu,
      components: [
        { name: 'ML Engine', tech: 'Python/scikit-learn', purpose: 'MNB & TER calculation' },
        { name: 'Agent Framework', tech: 'LangGraph/LangChain', purpose: 'Autonomous workflows' },
        { name: 'ABM Simulator', tech: 'Mesa/NetLogo', purpose: 'Tumor evolution modeling' },
        { name: 'API Gateway', tech: 'Django REST', purpose: 'Service orchestration' }
      ]
    },
    {
      category: 'Blockchain Layer',
      icon: Shield,
      components: [
        { name: 'Smart Contracts', tech: 'Solidity/Polygon', purpose: 'Payment escrow & consent' },
        { name: 'Identity Layer', tech: 'DIDs/SBTs', purpose: 'Patient sovereignty' },
        { name: 'Hash Registry', tech: 'On-chain hashes', purpose: 'Data integrity verification' },
        { name: 'Bridge Service', tech: 'web3.py', purpose: 'Off-chain to on-chain sync' }
      ]
    },
    {
      category: 'IoT/Sensor Layer',
      icon: Activity,
      components: [
        { name: 'BLE Gateway', tech: 'GATT/Android/iOS', purpose: 'Wearable data ingestion' },
        { name: 'Signal Processing', tech: 'BioSPPy/NeuroKit2', purpose: 'ECG/PPG analysis' },
        { name: 'Edge Compute', tech: 'Smartphone SDK', purpose: 'Local preprocessing' },
        { name: 'Quality Assessment', tech: 'SQI algorithms', purpose: 'Data validation' }
      ]
    }
  ];

  const formulas = [
    {
      id: 1,
      name: 'Reinforcement Protocol',
      foundation: 'Bochner Integral + RKHS',
      formula: 'R = ∫ K(t,s) r(s) dμ(s) + λ⟨ψᵣ, A⟩',
      application: 'AI reward alignment in treatment optimization'
    },
    {
      id: 2,
      name: 'Recursive IP Builder',
      foundation: 'Banach Fixed-Point Theorem',
      formula: 'Iₙ₊₁ = T(Iₙ) where ‖T(x) - T(y)‖ ≤ α‖x - y‖',
      application: 'Patent portfolio optimization'
    },
    {
      id: 9,
      name: 'Compositional Integrity Matrix',
      foundation: 'Bell Matrices',
      formula: 'B[f ∘ g] = B[f] · B[g]',
      application: 'Multi-stage treatment pipeline analysis'
    },
    {
      id: 10,
      name: 'Geometric Conservation Flow',
      foundation: 'Euler-Poincaré Reduction',
      formula: 'd/dt(δl/δξ) = ad*ξ(δl/δξ)',
      application: 'Preserving patient health invariants during therapy'
    }
  ];

  const phaseDetails = timelinePhases.find(p => p.id === activePhase);

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900 text-white p-8">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold mb-2 bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">
            Biotech Platform for Integrated Sports Analytics & Oncology
          </h1>
          <p className="text-gray-300">Transforming cancer treatment through advanced mathematical modeling and AI</p>
        </div>

        {/* Key Metrics Overview */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
          <div className="bg-blue-900/30 backdrop-blur-sm border border-blue-500/30 rounded-lg p-4">
            <div className="flex items-center justify-between mb-2">
              <TrendingUp className="text-blue-400" size={24} />
              <span className="text-2xl font-bold">12</span>
            </div>
            <p className="text-sm text-gray-300">Advanced Formulas</p>
          </div>
          <div className="bg-green-900/30 backdrop-blur-sm border border-green-500/30 rounded-lg p-4">
            <div className="flex items-center justify-between mb-2">
              <Users className="text-green-400" size={24} />
              <span className="text-2xl font-bold">3</span>
            </div>
            <p className="text-sm text-gray-300">Cancer Subtypes Modeled</p>
          </div>
          <div className="bg-purple-900/30 backdrop-blur-sm border border-purple-500/30 rounded-lg p-4">
            <div className="flex items-center justify-between mb-2">
              <Network className="text-purple-400" size={24} />
              <span className="text-2xl font-bold">4</span>
            </div>
            <p className="text-sm text-gray-300">Technical Layers</p>
          </div>
          <div className="bg-orange-900/30 backdrop-blur-sm border border-orange-500/30 rounded-lg p-4">
            <div className="flex items-center justify-between mb-2">
              <Clock className="text-orange-400" size={24} />
              <span className="text-2xl font-bold">18</span>
            </div>
            <p className="text-sm text-gray-300">Month Roadmap</p>
          </div>
        </div>

        {/* Tabs for different sections */}
        <div className="bg-slate-800/50 backdrop-blur-sm rounded-lg border border-slate-700 mb-8">
          <div className="flex border-b border-slate-700">
            {['TER Metrics', 'Four Factors', 'Roadmap', 'Tech Stack', 'Formulas'].map((tab) => (
              <button
                key={tab}
                onClick={() => setSelectedMetric(tab.split(' ')[0].toUpperCase())}
                className={`px-6 py-3 font-medium transition-colors ${
                  selectedMetric === tab.split(' ')[0].toUpperCase()
                    ? 'bg-blue-600 text-white'
                    : 'text-gray-400 hover:text-white hover:bg-slate-700/50'
                }`}
              >
                {tab}
              </button>
            ))}
          </div>

          <div className="p-6">
            {/* TER Metrics View */}
            {selectedMetric === 'TER' && (
              <div>
                <h2 className="text-2xl font-bold mb-4">Tumor Efficiency Rating (TER) Components</h2>
                <p className="text-gray-300 mb-6">
                  A composite per-cell-cycle rating derived from NBA's Player Efficiency Rating (PER), 
                  quantifying malignant potential across breast cancer subtypes.
                </p>
                <ResponsiveContainer width="100%" height={400}>
                  <BarChart data={terData}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
                    <XAxis dataKey="metric" stroke="#94a3b8" />
                    <YAxis stroke="#94a3b8" />
                    <Tooltip 
                      contentStyle={{ backgroundColor: '#1e293b', border: '1px solid #475569' }}
                      labelStyle={{ color: '#e2e8f0' }}
                    />
                    <Legend />
                    <Bar dataKey="tnbc" fill="#ef4444" name="TNBC" />
                    <Bar dataKey="luminalA" fill="#10b981" name="Luminal A" />
                    <Bar dataKey="her2" fill="#8b5cf6" name="HER2+" />
                  </BarChart>
                </ResponsiveContainer>
                <div className="mt-6 grid grid-cols-1 md:grid-cols-3 gap-4">
                  <div className="bg-red-900/20 border border-red-500/30 rounded-lg p-4">
                    <h3 className="font-bold text-red-400 mb-2">TNBC Profile</h3>
                    <p className="text-sm text-gray-300">High-pace "Seven Seconds or Less" offense. High division under stress (92), high turnovers (68). Vulnerable to dose-dense chemotherapy.</p>
                  </div>
                  <div className="bg-green-900/20 border border-green-500/30 rounded-lg p-4">
                    <h3 className="font-bold text-green-400 mb-2">Luminal A Profile</h3>
                    <p className="text-sm text-gray-300">Slow "Princeton" offense. High paracrine signaling (72), low turnover (22). Requires extended endocrine therapy (5-10 years).</p>
                  </div>
                  <div className="bg-purple-900/20 border border-purple-500/30 rounded-lg p-4">
                    <h3 className="font-bold text-purple-400 mb-2">HER2+ Profile</h3>
                    <p className="text-sm text-gray-300">"Superstar" system dependent on HER2 receptor. Moderate pace. Responsive to targeted dual-blockade therapy (Trastuzumab/Pertuzumab).</p>
                  </div>
                </div>
              </div>
            )}

            {/* Four Factors View */}
            {selectedMetric === 'FOUR' && (
              <div>
                <h2 className="text-2xl font-bold mb-4">Four Factors of Oncological Success</h2>
                <p className="text-gray-300 mb-6">
                  Adapted from Dean Oliver's basketball analytics, these factors explain the majority of tumor "wins" (patient mortality).
                </p>
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                  <ResponsiveContainer width="100%" height={400}>
                    <BarChart data={fourFactorsData} layout="vertical">
                      <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
                      <XAxis type="number" stroke="#94a3b8" />
                      <YAxis dataKey="factor" type="category" stroke="#94a3b8" />
                      <Tooltip 
                        contentStyle={{ backgroundColor: '#1e293b', border: '1px solid #475569' }}
                      />
                      <Legend />
                      <Bar dataKey="weight" fill="#3b82f6" name="Importance (%)" />
                    </BarChart>
                  </ResponsiveContainer>
                  <ResponsiveContainer width="100%" height={400}>
                    <RadarChart data={subtypeRadarData}>
                      <PolarGrid stroke="#475569" />
                      <PolarAngleAxis dataKey="metric" stroke="#94a3b8" />
                      <PolarRadiusAxis stroke="#94a3b8" />
                      <Radar name="TNBC" dataKey="TNBC" stroke="#ef4444" fill="#ef4444" fillOpacity={0.3} />
                      <Radar name="Luminal A" dataKey="LuminalA" stroke="#10b981" fill="#10b981" fillOpacity={0.3} />
                      <Radar name="HER2+" dataKey="HER2" stroke="#8b5cf6" fill="#8b5cf6" fillOpacity={0.3} />
                      <Legend />
                    </RadarChart>
                  </ResponsiveContainer>
                </div>
                <div className="mt-6 grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div className="bg-slate-800/50 border border-slate-600 rounded-lg p-4">
                    <h3 className="font-bold text-blue-400 mb-2">Factor 1: Proliferation (40%)</h3>
                    <p className="text-sm text-gray-300 mb-2">Proxy: Ki-67 Index</p>
                    <p className="text-xs text-gray-400">TNBC: 40-80% (fast doubling ~124 days) | Luminal A: &lt;20% (slow ~200+ days)</p>
                  </div>
                  <div className="bg-slate-800/50 border border-slate-600 rounded-lg p-4">
                    <h3 className="font-bold text-blue-400 mb-2">Factor 2: Clearance Rate (25%)</h3>
                    <p className="text-sm text-gray-300 mb-2">Proxy: Apoptotic Index</p>
                    <p className="text-xs text-gray-400">Chemotherapy forces "turnovers" (DNA errors). High genomic instability = vulnerability.</p>
                  </div>
                  <div className="bg-slate-800/50 border border-slate-600 rounded-lg p-4">
                    <h3 className="font-bold text-blue-400 mb-2">Factor 3: Angiogenesis (20%)</h3>
                    <p className="text-sm text-gray-300 mb-2">Proxy: Microvessel Density (MVD)</p>
                    <p className="text-xs text-gray-400">Anti-angiogenic drugs (Bevacizumab) "box out" the tumor from offensive rebounds.</p>
                  </div>
                  <div className="bg-slate-800/50 border border-slate-600 rounded-lg p-4">
                    <h3 className="font-bold text-blue-400 mb-2">Factor 4: Metastatic Efficiency (15%)</h3>
                    <p className="text-sm text-gray-300 mb-2">Proxy: CTC Count</p>
                    <p className="text-xs text-gray-400">TNBC targets visceral organs (lung/brain). HR+ prefers bone. HER2+ targets liver/brain.</p>
                  </div>
                </div>
              </div>
            )}

            {/* Roadmap View */}
            {selectedMetric === 'ROADMAP' && (
              <div>
                <h2 className="text-2xl font-bold mb-4">18-Month Development Roadmap</h2>
                <div className="mb-6">
                  <div className="flex gap-2 mb-4">
                    {timelinePhases.map((phase) => (
                      <button
                        key={phase.id}
                        onClick={() => setActivePhase(phase.id)}
                        className={`px-4 py-2 rounded-lg font-medium transition-all ${
                          activePhase === phase.id
                            ? phase.color + ' text-white'
                            : 'bg-slate-700 text-gray-300 hover:bg-slate-600'
                        }`}
                      >
                        {phase.name}
                      </button>
                    ))}
                  </div>
                </div>
                {phaseDetails && (
                  <div className="bg-slate-800/50 border border-slate-600 rounded-lg p-6">
                    <div className="flex items-center justify-between mb-4">
                      <h3 className="text-xl font-bold">{phaseDetails.name}</h3>
                      <span className="px-3 py-1 bg-blue-600 rounded-full text-sm">
                        Months {phaseDetails.months}
                      </span>
                    </div>
                    <div className="mb-4">
                      <h4 className="font-semibold text-blue-400 mb-2">Key Deliverables:</h4>
                      <ul className="space-y-2">
                        {phaseDetails.deliverables.map((item, idx) => (
                          <li key={idx} className="flex items-start">
                            <span className="text-green-400 mr-2">✓</span>
                            <span className="text-gray-300">{item}</span>
                          </li>
                        ))}
                      </ul>
                    </div>
                    <div className="bg-orange-900/20 border border-orange-500/30 rounded-lg p-4">
                      <h4 className="font-semibold text-orange-400 mb-2">Gate Review:</h4>
                      <p className="text-gray-300">{phaseDetails.gate}</p>
                    </div>
                  </div>
                )}
              </div>
            )}

            {/* Tech Stack View */}
            {selectedMetric === 'TECH' && (
              <div>
                <h2 className="text-2xl font-bold mb-4">Technical Architecture Stack</h2>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  {technicalStack.map((layer) => {
                    const Icon = layer.icon;
                    return (
                      <div key={layer.category} className="bg-slate-800/50 border border-slate-600 rounded-lg p-6">
                        <div className="flex items-center mb-4">
                          <Icon className="text-blue-400 mr-3" size={24} />
                          <h3 className="text-xl font-bold">{layer.category}</h3>
                        </div>
                        <div className="space-y-3">
                          {layer.components.map((comp) => (
                            <div key={comp.name} className="bg-slate-700/50 rounded-lg p-3">
                              <div className="flex justify-between items-start mb-1">
                                <span className="font-semibold text-blue-300">{comp.name}</span>
                                <span className="text-xs bg-purple-600 px-2 py-1 rounded">{comp.tech}</span>
                              </div>
                              <p className="text-sm text-gray-400">{comp.purpose}</p>
                            </div>
                          ))}
                        </div>
                      </div>
                    );
                  })}
                </div>
              </div>
            )}

            {/* Formulas View */}
            {selectedMetric === 'FORMULAS' && (
              <div>
                <h2 className="text-2xl font-bold mb-4">Advanced Mathematical Formulas</h2>
                <p className="text-gray-300 mb-6">
                  12 rigorously derived formulas from functional analysis, game theory, and topological data analysis
                </p>
                <div className="grid grid-cols-1 gap-4">
                  {formulas.map((formula) => (
                    <div key={formula.id} className="bg-gradient-to-r from-slate-800/50 to-blue-900/20 border border-blue-500/30 rounded-lg p-5">
                      <div className="flex items-start justify-between mb-3">
                        <div>
                          <h3 className="text-lg font-bold text-blue-300">#{formula.id}. {formula.name}</h3>
                          <p className="text-sm text-gray-400">Foundation: {formula.foundation}</p>
                        </div>
                      </div>
                      <div className="bg-slate-900/50 rounded p-3 mb-3 font-mono text-sm text-green-400">
                        {formula.formula}
                      </div>
                      <p className="text-gray-300 text-sm">
                        <span className="text-purple-400 font-semibold">Application:</span> {formula.application}
                      </p>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Footer */}
        <div className="bg-slate-800/50 backdrop-blur-sm rounded-lg border border-slate-700 p-6">
          <h3 className="text-xl font-bold mb-4">Platform Objectives</h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="bg-blue-900/20 border border-blue-500/30 rounded-lg p-4">
              <h4 className="font-semibold text-blue-400 mb-2">Clinical Impact</h4>
              <p className="text-sm text-gray-300">Transform static cancer staging into dynamic, real-time risk assessment using evolutionary game theory and AI agents</p>
            </div>
            <div className="bg-green-900/20 border border-green-500/30 rounded-lg p-4">
              <h4 className="font-semibold text-green-400 mb-2">Technical Innovation</h4>
              <p className="text-sm text-gray-300">First platform to integrate basketball analytics formulas (PER, Four Factors) with FHIR-compliant oncology data pipelines</p>
            </div>
            <div className="bg-purple-900/20 border border-purple-500/30 rounded-lg p-4">
              <h4 className="font-semibold text-purple-400 mb-2">Patient Engagement</h4>
              <p className="text-sm text-gray-300">Gamification with blockchain-verified rewards and wearable integration for continuous monitoring and adaptive therapy</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default OncologyAnalyticsPlatform;
