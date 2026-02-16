Executive Summary
A single, executable pilot package that proves the NBA‑Analog Core Analytic Engine inside Bio‑OS Clinical Suite. Goal: validate decision‑ready BioBriefs with immutable provenance, demonstrate a measurable reduction in target selection time, and produce an investor‑grade ROI case. Duration 90 days. Primary outcomes: 3–5 validated BioBriefs, ledger audit trail for every computation, and a quantified time‑to‑decision improvement target of 25–35%.

---

Objectives and Success Metrics
Primary Objectives
- Validate the analytic engine on customer targets and seed entities.
- Demonstrate reproducible, auditable BioBrief generation.
- Tune scoring and simulation parameters to align with domain expert expectations.

Success Metrics
- Time to first BioBrief: median < 45 seconds.
- Trueness coverage: ≥ 90% of targets with Trueness ≥ 0.6.
- Ledger completeness: 100% of computations produce tx_hash.
- Prioritization speed improvement: 25–35% faster vs baseline.
- Stakeholder satisfaction: NPS ≥ 8/10 at pilot close.

---

90 Day Plan and Milestones

Phase 0 Prep Days 0–7
- Deliverables: Signed SOW and NDA; Supabase keys; seed executed.
- Actions: Run seed_supabase.py; verify endpoints; deploy UI to Cloudflare (optional).
- Acceptance: Successful KRAS G12C BioBrief generation.

Phase 1 Discovery Days 8–37
- Deliverables: Baseline report; 3 customer BioBriefs; ledger snapshot.
- Actions: Ingest 3 customer targets; run analytics; capture baseline compute times.
- Acceptance: Baseline metrics meet minimum thresholds and ledger entries exist.

Phase 2 Optimization Days 38–67
- Deliverables: Tuning log; simulation results; updated BioBrief templates.
- Actions: Tune weights via PATCH endpoints; run 10+ lineup simulations; validate SVI/R0 behavior with experts.
- Acceptance: Prioritization speed improvement ≥ 25% and ≥ 80% simulation agreement with experts.

Phase 3 Close Days 68–90
- Deliverables: Final pilot report; ROI estimate; production playbook; go/no‑go recommendation.
- Actions: Produce executive summary, deployment repo, and handoff materials.
- Acceptance: Stakeholder signoff and pilot ROI ≥ 3× investment.

---

Technical Runbook and Verification
Environment Setup
- Set GitHub secrets: CFPAGESAPITOKEN, CFACCOUNTID, CFZONEID, SUPABASEURL, SUPABASESERVICEROLEKEY, REGISTRY*, LEDGERPRIVATEKEY.
- Seed DB: python extensions/bio-os/scripts/seed_supabase.py.
- Deploy UI: wrangler publish or CI via GitHub Actions.
- Deploy API: Docker build + Railway/Render deploy.

Key Endpoints
- POST /api/analytics/compute → returns baseliner0, stresssvi, risktier, computetime_ms.
- POST /api/analytics/biobrief → returns biobriefid, ledgertx_hash.

Quick Verification Commands
- Compute
`bash
curl -s -X POST "https://api.example.com/api/analytics/compute" \
  -H "Content-Type: application/json" \
  -d '{"source":"seed","entityid":"krasg12c_mcrc","payload":{}}'
`
- BioBrief
`bash
curl -s -X POST "https://api.example.com/api/analytics/biobrief" \
  -H "Content-Type: application/json" \
  -d '{"entityid":"krasg12cmcrc","requester":"demouser"}'
`
- Ledger check
`bash
curl -s -X GET "${SUPABASEURL}/rest/v1/ledgers?select=txhash,payload,created_at&limit=5" \
  -H "apikey: ${SUPABASESERVICEROLE_KEY}" \
  -H "Authorization: Bearer ${SUPABASESERVICEROLE_KEY}"
`

Data and Schema Notes
- Store Arrow‑serialized payloads in bio_datasets JSONB.
- Use bio_overlays for computed metrics and quadrants.
- Ledger entries include txhash, payload, action, computetime_ms.

---

Team Roles Responsibilities and Communication
Core Team
- Pilot Lead (Overlay365): overall delivery, stakeholder liaison, weekly status.
- Data Engineer: seed ingestion, Supabase schema, Arrow integration.
- ML/Analytics Engineer: implement formulas, run simulations, tune weights.
- DevOps Engineer: CI/CD, Cloudflare, Railway deployment.
- Clinical Liaison (Partner): domain validation, expert review of BioBriefs.

Cadence
- Weekly 30‑minute sync: progress, blockers, demo.
- Ad hoc technical calls: as needed for ingestion or tuning.
- Final review: 60–90 minute closeout presentation.

---

Budget Payment and Legal
Pilot Cost
- Fixed fee: $45,000 (engineering + infra baseline).
- Optional public demo: $8,000 (3 months hosting + setup).
- Payment schedule: 30% signing, 40% end Phase 1, 30% final sign‑off.

Legal
- NDA required before data exchange.
- Data classification: de‑identified research use only.
- Termination: 14 days notice; data returned or deleted per NDA.

---

Risks Mitigation and Contingencies
Risk: Data quality prevents reliable metrics.  
Mitigation: Pre‑ingest validation pipeline; Trueness gating; fallbacks to manual review.

Risk: Ledger integration delays.  
Mitigation: Start with mock ledger entries and switch to Hyperledger once keys are provisioned; ensure auditability via Supabase export.

Risk: Domain expert disagreement on simulation outputs.  
Mitigation: Run A/B parameter sweeps, capture expert feedback, and lock tuned parameters in ledger for traceability.

---

Deliverables Handoff and Next Steps
Deliverables
- 3–5 validated BioBriefs with ledger proof.
- Baseline and tuned analytics dashboards.
- Final pilot report with ROI model and production playbook.
- Deployment repo and CI configuration.

Immediate Next Steps
- Confirm pilot partner and sign SOW.
- Provide Supabase service role key and 3 target datasets.
- Run seed script and push main to trigger CI.
- Schedule kickoff 15‑minute meeting and run KRAS G12C demo.

#!/usr/bin/env bash
set -euo pipefail

############################################
# NBA-Analog Bio-OS Verification Script
# Usage:
#   chmod +x verify_bio_os.sh
#   ./verify_bio_os.sh
#
# Required ENV:
#   API_BASE_URL        e.g. https://api.example.com
#   SUPABASE_URL        e.g. https://your-supabase-project.supabase.co
#   SUPABASE_SERVICE_ROLE_KEY
############################################

# ---- CONFIG / ENV CHECKS ----
: "${API_BASE_URL:?Must set API_BASE_URL, e.g. https://api.example.com}"
: "${SUPABASE_URL:?Must set SUPABASE_URL}"
: "${SUPABASE_SERVICE_ROLE_KEY:?Must set SUPABASE_SERVICE_ROLE_KEY}"

ENTITY_ID="krasg12c_mcrc"
REQUESTER="demo_user"

echo "=== NBA-Analog Bio-OS Verification ==="
echo "API_BASE_URL            = ${API_BASE_URL}"
echo "SUPABASE_URL           = ${SUPABASE_URL}"
echo "SUPABASE_SERVICE_ROLE_KEY = **** (hidden)"
echo "ENTITY_ID               = ${ENTITY_ID}"
echo

# ---- STEP 1: Verify compute endpoint ----
echo "1) Hitting /api/analytics/compute for ${ENTITY_ID} ..."
COMPUTE_RESP="$(curl -sS -X POST "${API_BASE_URL}/api/analytics/compute" \
  -H "Content-Type: application/json" \
  -d "{
    "source": "seed",
    "entityid": "${ENTITY_ID}",
    "payload": {}
  }")"

echo "Raw compute response:"
echo "${COMPUTE_RESP}" | jq .

BASELINE_R0="$(echo "${COMPUTE_RESP}" | jq -r '.baseliner0 // .baseline_r0 // empty')"
STRESS_SVI="$(echo "${COMPUTE_RESP}" | jq -r '.stresssvi // .stress_svi // empty')"
RISK_TIER="$(echo "${COMPUTE_RESP}" | jq -r '.risktier // .risk_tier // empty')"
COMPUTE_MS="$(echo "${COMPUTE_RESP}" | jq -r '.computetime_ms // empty')"

echo
echo "Parsed metrics:"
echo "  baseline R0  = ${BASELINE_R0:-N/A}"
echo "  stress SVI   = ${STRESS_SVI:-N/A}"
echo "  risk tier    = ${RISK_TIER:-N/A}"
echo "  compute time = ${COMPUTE_MS:-N/A} ms"
echo

# ---- STEP 2: Generate BioBrief and capture ledger tx ----
echo "2) Hitting /api/analytics/biobrief for ${ENTITY_ID} ..."
BIOBRIEF_RESP="$(curl -sS -X POST "${API_BASE_URL}/api/analytics/biobrief" \
  -H "Content-Type: application/json" \
  -d "{
    "entityid": "${ENTITY_ID}",
    "requester": "${REQUESTER}"
  }")"

echo "Raw biobrief response:"
echo "${BIOBRIEF_RESP}" | jq .

BIOBRIEF_ID="$(echo "${BIOBRIEF_RESP}" | jq -r '.biobriefid // .biobrief_id // empty')"
LEDGER_TX_HASH="$(echo "${BIOBRIEF_RESP}" | jq -r '.ledgertxhash // .ledger_tx_hash // empty')"

echo
echo "Parsed BioBrief info:"
echo "  biobrief id   = ${BIOBRIEF_ID:-N/A}"
echo "  ledger txhash = ${LEDGER_TX_HASH:-N/A}"
echo

# ---- STEP 3: Check Supabase ledgers for recent entries ----
echo "3) Checking Supabase ledgers (last 5 rows) ..."
curl -sS -X GET "${SUPABASE_URL}/rest/v1/ledgers?select=txhash,payload,created_at&order=created_at.desc&limit=5" \
  -H "apikey: ${SUPABASE_SERVICE_ROLE_KEY}" \
  -H "Authorization: Bearer ${SUPABASE_SERVICE_ROLE_KEY}" \
  | jq .

if [ -n "${LEDGER_TX_HASH:-}" ]; then
  echo
  echo "4) Verifying that txhash ${LEDGER_TX_HASH} exists in ledgers ..."
  MATCH="$(curl -sS -X GET "${SUPABASE_URL}/rest/v1/ledgers?txhash=eq.${LEDGER_TX_HASH}&select=txhash,payload,created_at" \
    -H "apikey: ${SUPABASE_SERVICE_ROLE_KEY}" \
    -H "Authorization: Bearer ${SUPABASE_SERVICE_ROLE_KEY}")"

  echo "${MATCH}" | jq .
else
  echo "No ledger txhash returned from BioBrief endpoint; skipping specific tx lookup."
fi

echo
echo "=== Verification complete ==="
