# Venture Portfolio State Matrix — Required for Jarvis Mode

**Purpose:** Give Hermes complete context so it can operate autonomously across all 7 ventures without blocking.

**Time to Complete:** 20-30 minutes. One-time investment.

**Format:** Fill in each row. Be honest about state (POC, revenue-generating, stuck, etc.). That's how Hermes prioritizes.

---

## Template

| **Venture** | **Current State** | **Phase** | **Revenue/Status** | **Blocker #1** | **Blocker #2** | **Blocker #3** | **Timeline to Exit** | **Owner / Partner** | **Dice/Metrics** |
|---|---|---|---|---|---|---|---|---|---|
| **Echo Oncology** | EagleEye POC live, 15 BraTS cases, real data | Phase 1: Algorithm validation | Validation (no revenue yet) | Dice validation on 15 cases | 3D/4D enhancement (tumor click, layer peeling, cardiac 4D) | Helen Wheeler partnership formalization | 18-24 mo (FDA) / 12-18 mo (TGA) | You + Helen Wheeler | ? |
| **ElectraScan** | v1.1.1.0 live on Vercel, 4.8K LOC, React 19 + Supabase + DocuSign | Production (generating revenue?) | ??? | Vision detection unreliability (same PDF → diff results) | Phase 1 Polish (5d, 40% visual uplift) | Phase 2 Data Viz (10d) + Phase 3 Mobile (12d) | 12 mo | You | Vision accuracy baseline? |
| **Ember** | 40% MVP scaffold, API built, segmentation folder exists | Early development | Validation (no revenue) | Synthetic ECG generation | 4D heart mesh animation (2-3 wks) | Risk scoring model training | TBD | You | Cardiac dataset progress? |
| **Ember Echo** | ??? | ??? | ??? | ??? | ??? | ??? | ??? | ??? | ??? |
| **PLÉO** | Premium dance athlete recovery kits | ??? | ??? | ??? | ??? | ??? | ??? | ??? | ??? |
| **Eka Noe** | Investment intelligence | ??? | ??? | ??? | ??? | ??? | ??? | ??? | ??? |
| **Claude Ares** | Hermes infrastructure / AI backbone | ??? | ??? | ??? | ??? | ??? | ??? | ??? | ??? |

---

## What Each Column Means

### Current State
Exact status. Examples:
- "Live on Vercel with 15 real BraTS cases"
- "MVP 40% complete, missing X and Y"
- "Concept stage, no code yet"
- "Prototype works but untested on real data"

### Phase
Where in the product lifecycle:
- **Concept** — idea only, no code
- **Early Dev** — code started, <40% complete
- **MVP** — 40-70%, core features work
- **Prototype/POC** — working demo, not production
- **Production** — live, customers using it
- **Phase 1** — research/validation phase
- **Phase 2** — commercialization phase

### Revenue/Status
Be specific:
- "No revenue, validation stage"
- "€50K MRR, growing 20% MoM"
- "$0, blocked on X"
- "Pre-revenue, negotiations with Y hospital"
- "Generating user traction, no monetization yet"

### Blockers #1, #2, #3
What stops progress **right now**. Ranked by impact:
1. **Blocker #1** = Most critical, unblocks everything else
2. **Blocker #2** = Medium priority, needed for next phase
3. **Blocker #3** = Lower priority but still on roadmap

Examples:
- "Vision model hallucination (same input → diff outputs)"
- "Hospital partnership not formalized"
- "Dataset too small for training"
- "Missing clinical advisor"
- "No regulatory strategy"

### Timeline to Exit
How long until you want to exit this venture or reach profitability:
- "12 months"
- "6 months (TGA approval)"
- "24 months (FDA → US expansion)"
- "Indefinite (building for revenue, not exit)"

### Owner / Partner
Who owns this venture:
- "You (Damien)"
- "You + Helen Wheeler (clinical advisor)"
- "You + TLE (TLE Electrical partnership)"
- "Partner name"

### Dice / Metrics
Current KPIs or validation metrics:
- For Echo: "Dice scores on 15 cases = ???"
- For ElectraScan: "Vision accuracy baseline = ???"
- For Ember: "Cardiac segmentation Dice = ???"
- For others: "Revenue MRR = $X" or "User count = Y"

---

## Example (Filled In — Not Your Data)

| **Venture** | **Current State** | **Phase** | **Revenue/Status** | **Blocker #1** | **Blocker #2** | **Blocker #3** | **Timeline to Exit** | **Owner / Partner** | **Metrics** |
|---|---|---|---|---|---|---|---|---|---|
| **Echo Oncology** | EagleEye POC, 15 BraTS cases, nnU-Net integrated | Phase 1 validation | $0, research stage | Dice validation: are 15 cases ≥95%? | 3D enhancement (tumor click, layer peeling) | Helen Wheeler partnership letter signed? | 18 mo TGA / 24 mo FDA | You + Helen Wheeler | Dice = 0.927 (mean, 15 cases) |
| **ElectraScan** | v1.1.1.0 live, revenue-generating | Production | $8K MRR, growing | Vision detection: 15% of PDFs fail, no confidence thresholding | Phase 1 Polish (5d effort) | TLE Electrical integration (7d effort) | 12 mo (exit or acq.) | You + TLE partner | Vision accuracy: 85% (need ≥95%) |
| **Ember** | 40% complete, cardiac MRI segmentation | MVP validation | $0 | Synthetic ECG generation (3d effort) | 4D animation implementation (2 wks) | Risk scoring model (1 wk training) | Depends on Echo success | You | ACDC dataset: 100 cases available |
| **Ember Echo** | Unknown, possibly Echo+Ember combo | TBD | TBD | Clarification: is this separate product? | Requirements from Helen Wheeler | Integration with Foundry OSDK | TBD | TBD | TBD |
| **PLÉO** | Prototype kits, dance athlete partnerships | Validation | $0, pre-revenue | Athlete feedback on kit efficacy | Manufacturing cost/unit | Market validation (how many athletes?) | 12 mo (series A or exit) | You + partner | NPS = ? (need to track) |
| **Eka Noe** | Live investment intelligence tool | Production | $12K MRR (est.) | Scale to 100 users | ML model improvements | Regulatory (if needed?) | Revenue-focused, no hard exit | You | DAU = 45, retention = 62% |
| **Claude Ares** | Hermes AI backbone, running this system | Infrastructure | $0 (cost, no revenue) | Stability/uptime (99.9% SLA needed?) | Model inference speed (sub-100ms needed?) | Cost optimization (running $X/mo?) | Indefinite (support all ventures) | You + Claude team | Uptime = 99.7%, cost = $X/mo |

---

## Send This Back to Hermes

Once filled in, send to this thread. Hermes will:

1. ✅ Load into permanent memory (never forgotten)
2. ✅ Identify dependencies (what unblocks what)
3. ✅ Sequence work (critical path to exit)
4. ✅ Parallelize (run non-blocking work simultaneously)
5. ✅ Flag conflicts (if two ventures compete for resources)
6. ✅ Create weekly execution plan (which venture gets how much effort)

---

**Deadline:** This week, before Monday sync.  
**Format:** Copy template, fill in, send back.  
**Effort:** 20-30 min per venture.

Once I have this, I operate in **true Jarvis mode** — autonomous, coordinated, no blockages.

