# Questrade Financial Group (Account 11954657) — Strategic Account Analysis

**Prepared:** April 15, 2026
**Renewal Date:** July 25, 2026 (~101 days out)
**Account Owner:** Alex DeMarco (Emerging Enterprise AE, US East)
**Subscription:** Enterprise Plan — Annual — $230,400 ARR (600 seats @ $32/seat/month)

---

## 1. Account Overview

| Attribute | Value |
|---|---|
| **SF Account ID** | 001Hr00002CQSRkIAP |
| **Cursor Team ID** | 11954657 |
| **Team Name** | QFG |
| **Industry** | Financial Services / Wealth & Asset Mgmt |
| **HQ** | Toronto, Ontario, Canada |
| **Employees** | ~1,766 (423 SWEs estimated) |
| **Customer Since** | July 25, 2025 |
| **Contract End Date** | July 24, 2026 |
| **Renewal Opp Stage** | 4 - Negotiation & Procurement |
| **Renewal Forecast** | Most Likely (80% probability) |
| **Segment** | Emerging Enterprise (EME) |
| **Payment Method** | Invoice (Net 30) |
| **Pricing Model** | Enterprise — $32/seat/mo, Usage via Requests, On-Demand +20% API, Unlimited BugBot |

---

## 2. Seat Utilization & User Activity

| Metric | Value |
|---|---|
| **Contracted Seats** | 600 |
| **Provisioned Seats** | 894 |
| **Total Team Members** | 896 (881 members + 14 owners + 1 free owner) |
| **Active Users (L30D)** | 591 |
| **Active Users (L7D)** | 441 |
| **Active Users (31-60D)** | 602 |
| **Active Users (8-14D)** | 471 |

### Key Insight — Massive Over-Deployment
Questrade has **896 members** provisioned against a **600-seat contract** — a 49% overage. Their 30-day active user count of 591 is very close to the contracted 600 seats, suggesting the contract size accurately reflects actual usage, but the provisioned headcount is significantly higher. This creates both a **risk** (they may feel they're overpaying per user if not all are active) and an **opportunity** (true-up / expansion).

### User Activity Trend (from Subscription Data)
- **L30D active users: 591** — essentially at contract capacity
- **L7D active users: 441** — ~74% weekly engagement of the L30D base
- **MAU MoM Change: -1.8%** — slight decline in monthly active users
- **WAU WoW Change: -6.4%** — notable weekly engagement softening

---

## 3. Usage Trends (Monthly Event Volume & Spend)

| Month | Events | Spend ($) | Input Tokens | Output Tokens | Cache Read Tokens |
|---|---|---|---|---|---|
| Apr 2026 (partial) | 74,076 | $171.98 | 225.6M | 45.5M | 5.47B |
| Mar 2026 | 114,157 | $1,495.02 | 261.3M | 50.2M | 5.79B |
| Feb 2026 | 55,734 | $1,537.68 | 48.5M | 8.6M | 1.34B |
| Jan 2026 | 50,205 | $1,278.80 | 47.0M | 10.7M | 1.51B |
| Dec 2025 | 47,881 | $810.28 | 22.0M | 12.4M | 2.41B |
| Nov 2025 | 31,329 | $629.36 | 29.7M | 9.6M | 1.58B |
| Oct 2025 | 31,149 | $831.48 | 26.4M | 7.0M | 1.22B |
| Sep 2025 | 24,120 | $505.32 | 39.6M | 6.4M | 1.46B |
| Aug 2025 | 36,857 | $458.40 | 92.1M | 15.6M | 2.17B |
| Jul 2025 | 99,096 | $868.72 | 42.3M | 48.9M | 6.39B |

### Key Usage Observations

1. **Strong upward trajectory in request volume:** From ~24K events/mo in Sep 2025 to 114K in Mar 2026 — a **4.7x increase** in 6 months. This is an exceptionally healthy adoption curve.

2. **March 2026 was a peak month** — 114K events, the highest since onboarding (even exceeding the initial Jul 2025 onboarding spike of 99K).

3. **Token consumption surging:** Input tokens jumped from ~47M in Jan to 261M in Mar — a **5.5x increase** driven by the shift to agentic workflows (more tool calls, longer contexts).

4. **Cache utilization is excellent:** 5.79B cache read tokens in Mar 2026 shows highly efficient codebase indexing and context reuse — this team knows how to use the product.

5. **April 2026 is on track:** With 74K events in only half the month, April is projecting ~148K+ events, which would set a new all-time high.

---

## 4. Feature Adoption Deep Dive

### 4.1 Models Used (Jan 2026 – Present)

| Model | Requests | % Share |
|---|---|---|
| default (auto-routing) | 125,479 | 35.3% |
| Claude 4.6 Opus Thinking | 41,765 | 11.7% |
| Claude 4.5 Opus Thinking | 39,866 | 11.2% |
| Claude 4.5 Sonnet Thinking | 31,484 | 8.9% |
| Composer-2 | 17,797 | 5.0% |
| Composer-1.5 | 14,443 | 4.1% |
| Claude 4.6 Sonnet Thinking | 10,063 | 2.8% |
| Composer-1 | 9,235 | 2.6% |
| Claude 4.5 Sonnet | 8,431 | 2.4% |
| GPT-5.3 Codex | 6,954 | 2.0% |
| GPT-5.2 Codex | 6,016 | 1.7% |
| Gemini 3.1 Pro Preview | 6,014 | 1.7% |
| Claude 4.6 Opus | 5,511 | 1.6% |
| Other models | ~9.0% | |

**Insight:** Questrade is a **power-user team** — they heavily leverage thinking models (Opus Thinking + Sonnet Thinking account for ~35% of named model usage). They are also multi-model consumers across Anthropic, OpenAI, and Google families. The `default` auto-routing at 35% indicates trust in the platform's model selection.

### 4.2 Agent Mode Adoption

| Month | Agent Mode | Requests | Unique Users |
|---|---|---|---|
| Jan 2026 | agent | 58,603 | 519 |
| Jan 2026 | non-agent | 31,341 | 408 |
| Jan 2026 | debug | 331 | 18 |
| Feb 2026 | agent | 8,478 | 153 |
| Feb 2026 | non-agent | 93,562 | 559 |
| Mar 2026 | non-agent | 116,300 | 593 |
| Apr 2026 (partial) | non-agent | 42,346 | 508 |

**Insight:** Agent mode saw a **massive spike in January** (58K requests, 519 users) but has since dropped off dramatically. The shift in data categorization may account for some of this (agent mode data may now be folded into the default mode tracking), but it's worth investigating whether agent mode adoption has genuinely stalled or if the measurement methodology changed.

### 4.3 Tool Calls & Agentic Depth

- **Mar 2026:** 88,020 of 116,300 requests (75.7%) included tool calls — avg 12.8 tool calls per request
- **Apr 2026:** 31,919 of 42,346 requests (75.4%) included tool calls — avg 13.9 tool calls per request
- **Feb 2026:** 27,807 of 93,562 requests (29.7%) included tool calls — avg 12.4 tool calls per request

**Insight:** The high tool-call rate (75%+ in recent months) with 13-14 avg tool calls per request signals **deep agentic usage**. This team is not just chatting — they're using the agent to read files, write code, run commands, and build substantial changes. This is a stickiness indicator.

### 4.4 Platform & Governance Features Enabled

| Feature | Status |
|---|---|
| **Privacy Mode** | Forced ON (NO_TRAINING) — no data used for training |
| **SSO** | Enabled |
| **SCIM** | Not connected |
| **BYOK Disabled** | Yes (using Cursor's keys) |
| **Usage-Based Pricing** | Enabled (admin-only controls) |
| **Auto-Run Controls** | Enabled with extensive allowlist (42 commands) |
| **Browser Features** | Enabled |
| **Extension Signing** | Verification enabled |
| **BugBot** | Plan ON, 0 licenses, globally not disabled, billing mode: seat |
| **Background Agents** | Enabled with ALLOWLIST config, private workers required |
| **Shared Conversations** | Enabled (team-only visibility) |
| **Repo Blocklist** | BLOCK mode enabled |
| **Network Allowlist** | `*.questrade.com`, `*.q3.questech.io` |
| **GitHub Installations** | 16 distinct installations |
| **GitHub App Repo Settings** | 21 repos configured |
| **Team Rules** | 1 rule configured |
| **Team Hooks** | 0 hooks |
| **Deepseek** | Blocked (model blocklist) |
| **MCP Controls** | Disabled at admin level |
| **Automations** | Enabled |
| **Cloud Agent Testing** | Enabled |
| **Long-Running Agent Mode** | Enabled |

### 4.5 Background Agent Configuration (Detail)

- **Allowlist config:** ALLOWLIST mode with 1 specific user/service allowed (ID: 195235063)
- **Auto-create PR:** Always
- **VM Sharing:** Allowed
- **Egress Protection:** Network settings only (locked)
- **GitHub Artifact Posting:** Link only
- **Private Workers:** Required
- **Team Followup:** Service accounts only
- **Automations:** Enabled

---

## 5. Opportunity History

| Opportunity | Type | Close Date | Stage | ARR | Notes |
|---|---|---|---|---|---|
| New Annual 7/2025 | New Business | Jul 25, 2025 | **Closed Won** | $230,400 | 600 seats, 12-mo term. Sourced via Contact Sales Form. |
| Exp (True Up #1) 10/2025 | True Up | Oct 25, 2025 | **Closed Lost** | $0 | No expansion captured |
| Exp (True Up #2) 1/2026 | True Up | Jan 25, 2026 | **Closed Lost** | $0 | No expansion captured |
| Exp (True Up #3) 4/2026 | True Up | Apr 25, 2026 | **Pending** | $0 | Currently open, 591 MAU vs 600 seats |
| **Renewal 7/2026** | Renewal | Jul 25, 2026 | **4 - Negotiation** | Baseline $230,400 | 80% probability, Most Likely forecast |

---

## 6. Risk Assessment

### HIGH RISKS

1. **Declining Weekly Engagement (-6.4% WoW):** While monthly volume is strong, weekly active users are softening. The WAU decline of 6.4% is a leading indicator that may signal fatigue, competing tool adoption, or seasonal effects. This needs to be monitored closely heading into the renewal.

2. **Three Consecutive Failed True-Ups:** True Up #1 and #2 both closed lost, and True Up #3 is pending at $0. Despite having 896 members (49% over the 600 contracted seats), Questrade has successfully resisted paying for overage. This suggests **strong procurement pushback** and sets a difficult precedent for the renewal — they may argue for fewer seats.

3. **Renewal Opportunity Shows Net New ARR of -$230,400:** The renewal opportunity currently shows a negative net new ARR equal to the full contract value, which could indicate the system is modeling a potential churn scenario or the renewal hasn't been properly configured. This needs immediate attention from the AE.

4. **Account Owner Recently Changed:** The original deal was closed by Max Kollmorgen, but the account and renewal are now owned by Alex DeMarco. True Ups #1 and #2 were owned by Joe Tucci. This means 3 different AEs have touched this account in under a year — relationship continuity risk.

5. **Known Product Issues from Deal History:** The original deal noted critical issues with C# extension functionality and Auto Mode inconsistencies. If these haven't been resolved, they could be leveraged as churn arguments during renewal.

6. **MAU Slightly Declining (-1.8% MoM):** Combined with the WAU decline, this could indicate early-stage disengagement.

### MODERATE RISKS

7. **Privacy/Security-First Buyer:** Privacy mode is forced ON, private workers are required, network allowlisting is strict, deepseek is blocked, and BYOK is disabled. This is a security-conscious financial services firm — any data handling incident or policy change could trigger churn.

8. **No Champion/Executive Sponsor on Renewal:** The renewal opportunity has no champion or executive sponsor assigned. The original deal had Anderson Luiz Mendes Matos as champion and Serena Kim (Vendor Management) as economic buyer — are these contacts still engaged?

9. **Competitor Presence:** OpenAI was listed as a competitor in the original deal. With GPT-5.x Codex usage visible in their model mix, they are clearly aware of alternatives.

---

## 7. Opportunities

### EXPANSION OPPORTUNITIES

1. **Seat True-Up:** 896 members are provisioned vs. 600 contracted. Even at the current 591 L30D active users, there's a case for right-sizing to at least 600 seats on renewal. But the real conversation should be around the 896 provisioned number — if they want to keep all those users, they should be paying for 900 seats. This represents a potential **$113,280 ARR expansion** (300 additional seats x $32/mo x 12).

2. **BugBot Activation:** BugBot is turned ON but has 0 licenses and hasn't been meaningfully adopted. With 21 GitHub repos configured and 16 installations, the infrastructure is there. BugBot could be a meaningful add-on for a team this size.

3. **Usage-Based Upsell:** Their usage spend is growing — from $458/mo in Aug 2025 to $1,495/mo in Mar 2026 (3.3x growth). As agentic usage deepens, their on-demand spending will increase. A pre-committed usage block could offer savings while locking in higher commit.

4. **MCP & Automations Expansion:** MCP controls are disabled at the admin level, but the background agent config has MCP tool allowlist set to `*:*` (all tools). Enabling MCP at the admin level and deploying team MCP servers could deepen integration and stickiness.

5. **Hooks Deployment:** Zero hooks configured. For a financial services team of this size, deployment hooks (pre-commit security scanning, compliance checks) could be a governance selling point.

### STRATEGIC OPPORTUNITIES

6. **Multi-Model Power Users:** Questrade uses models from Anthropic, OpenAI, and Google. Highlighting Cursor's model-agnostic advantage and ensuring they have access to the latest models keeps them engaged and prevents single-vendor lock-in concerns.

7. **Executive Engagement:** No executive meeting held, no executive sponsor on the account. For a $230K ARR customer, securing executive alignment before renewal is critical.

8. **SCIM Connection:** SSO is enabled but SCIM is not connected. Enabling SCIM would automate user provisioning/deprovisioning and deepen the platform's integration into their IT stack — increasing switching costs.

---

## 8. Interesting Trends

1. **Explosive Agentic Adoption:** The jump from 12.4 to 13.9 average tool calls per request (Feb to Apr) shows the team is doing increasingly complex work with the agent. This is the stickiest usage pattern.

2. **Cache Efficiency Leader:** 5.79B cache read tokens in March against 261M input tokens means a ~22:1 cache-to-input ratio — this team has heavily indexed their codebase and is getting enormous efficiency from caching. This is a power-user indicator.

3. **Thinking Model Preference:** Over 35% of their named model usage is "thinking" variants (Opus Thinking, Sonnet Thinking). This suggests they're working on complex, multi-step problems — not simple autocomplete tasks.

4. **Onboarding Velocity Was Exceptional:** They went from 0 to 99K events in July 2025 (onboarding month) — this indicates strong organizational buy-in from day one.

5. **Auto-Run Command Allowlist is Extensive:** 42 commands are approved for auto-run, including build tools (npm, dotnet, webpack, esbuild), testing (pytest, mocha, jest), and system tools. This shows trust in the platform and deep developer integration.

---

## 9. Recommended Actions for Renewal

| Priority | Action | Owner | Timeline |
|---|---|---|---|
| **P0** | Fix renewal opportunity showing -$230K net new ARR — ensure proper renewal baseline | AE/RevOps | Immediate |
| **P0** | Re-engage original champion (Anderson Mendes Matos) and economic buyer (Serena Kim) | AE | This week |
| **P0** | Schedule executive alignment meeting before renewal | AE + Leadership | Within 2 weeks |
| **P1** | Prepare seat true-up analysis: 896 provisioned vs 600 contracted | AE | Before renewal discussion |
| **P1** | Investigate the -6.4% WAU decline — is it seasonal or competitive? | TAM/AE | Within 1 week |
| **P1** | Check status of C# extension and Auto Mode issues flagged during original deal | TAM/Support | Within 1 week |
| **P2** | Pitch BugBot activation with pilot on their 21 configured repos | AE/SE | During renewal |
| **P2** | Propose pre-committed usage block to offset growing on-demand spend | AE | During renewal |
| **P2** | Recommend SCIM connection for automated provisioning | AE/TAM | During renewal |
| **P3** | Deploy team hooks for compliance/security workflows | SE/TAM | Post-renewal |

---

*This analysis was generated from Salesforce CRM data, product telemetry (Cursor team/usage data), and subscription records as of April 15, 2026.*
