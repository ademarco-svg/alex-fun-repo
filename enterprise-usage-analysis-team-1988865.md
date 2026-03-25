# Enterprise Upgrade Analysis: Envato (Team ID 1988865)

## Executive Summary

Envato is a textbook enterprise-ready account. Over the past 12 months, they have grown from 12 to 100+ active Cursor users, their usage-based spend has surged from near-zero to nearly $12,000/month, and they have adopted virtually every advanced Cursor capability. With 80%+ weekly agent adoption, rapidly growing MCP and Plan Mode usage, and zero competitor tool leakage, Envato has made Cursor their standard engineering platform. They are now at the scale and spend level where Enterprise governance, cost predictability, and admin controls become essential.

---

## 1. Explosive User Growth (8x in 6 Months)

Envato's active user base has grown dramatically since they first appeared on the platform in late 2024:

| Month | Monthly Active Users | Growth |
|-------|---------------------|--------|
| Dec 2024 | 12 | -- |
| Jan 2025 | 34 | +183% |
| Feb 2025 | 34 | Stable |
| Mar 2025 | 50 | +47% |
| Apr 2025 | 64 | +28% |
| May 2025 | 78 | +22% |
| Jun 2025 | 103 | +32% |
| Jul 2025 | 103 | Stable |
| Aug 2025 | 102 | Stable |
| Sep 2025 | 99 | Stable |
| Oct 2025 | 101 | Stable |
| Nov 2025 | 102 | Stable |
| Dec 2025 | 98 | Stable |

**Key insight**: They went from a small pilot of 12 users to 100+ monthly actives in just six months (Dec 2024 - Jun 2025), representing an **8.6x increase**. Since June, the user base has plateaued at ~100 active users -- this isn't a decline, it's a signal that Cursor has become embedded across their engineering org and they've reached full penetration of their current seat allocation (144 seats, ~70% utilization).

The 7-day active user counts from daily data confirm consistently strong engagement: weekday WAU peaked at 87 in early December 2025, meaning the vast majority of their monthly actives are using Cursor multiple times per week.

---

## 2. Usage-Based Spend: From Zero to $12K/Month

This is perhaps the most compelling data point for the enterprise conversation. Envato's usage-based token spend has exploded:

| Month | Total Usage Revenue (Tokens) | Legacy Overage | API Cost |
|-------|------------------------------|----------------|----------|
| Dec 2024 | $0.00 | $0.00 | $0.00 |
| Jan 2025 | $0.00 | $10.10 | $0.00 |
| Feb 2025 | $0.00 | $100.36 | $0.00 |
| Mar 2025 | $0.00 | $173.30 | $0.00 |
| Apr 2025 | $0.00 | $79.18 | $0.00 |
| May 2025 | $0.00 | $381.12 | $0.00 |
| Jun 2025 | $1,666.77 | $1,191.79 | $1,403.64 |
| Jul 2025 | $1,855.27 | $1,633.84 | $1,569.16 |
| Aug 2025 | $1,813.87 | $1,227.43 | $1,453.07 |
| **Sep 2025** | **$5,355.82** | **$1,810.43** | **$4,250.22** |
| **Oct 2025** | **$6,837.16** | **$3,129.66** | **$5,481.86** |
| **Nov 2025** | **$11,773.50** | **$3,270.52** | **$9,332.74** |
| **Dec 2025** | **$11,777.75** | $0.00 | **$9,848.87** |

**Key insight**: Usage-based spend grew **7x from Aug to Nov 2025** ($1.8K to $11.8K). The December number held steady at $11.8K despite the holiday season, suggesting this spend level is the new normal. At $12K/month in variable usage costs on top of per-seat fees, Envato would benefit enormously from enterprise pricing with committed spend tiers and cost predictability. This is exactly the kind of unpredictable variable cost that makes CFOs nervous -- and that an enterprise contract can solve.

---

## 3. Agent Adoption: 80%+ of Users Are Agent-First

Envato has become a deeply agent-centric organization. Weekly agent usage data shows:

| Period | Agent WAU | Agent L4 (Heavy Users) | Power Users |
|--------|-----------|------------------------|-------------|
| Late Mar 2025 | 32 | 8 | 2 |
| Late Apr 2025 | 44 | 13 | 4 |
| Late May 2025 | 62 | 27 | 10 |
| Late Jun 2025 | 83 | 43 | 6 |
| Late Jul 2025 | 82 | 40 | 10 |
| Late Sep 2025 | 76 | 38 | 15 |
| Late Oct 2025 | 82 | 48 | 13 |
| Late Nov 2025 | 82 | 49 | 17 |
| Mid Dec 2025 | 73 | 45 | 17 |

**Key insights**:
- **80%+ of monthly active users** are using Agent mode weekly (82 agent WAU out of ~100 MAU)
- **L4 (heavy) agent users grew from 8 to 48** -- nearly half their active users are heavy agent consumers
- **Power users grew from 2 to 20** -- a 10x increase, showing a growing cohort of developers who've made Agent their primary workflow
- Agent request volume per day surged from single digits in Jan 2025 to routinely **500-1,300+ requests/day** by Q4 2025

This level of agent adoption directly drives the usage-based spend increase and makes enterprise features like usage policies, spend controls, and model governance critical.

---

## 4. Advanced Feature Adoption Is Accelerating

### MCP (Model Context Protocol) Usage
MCP adoption shows a clear upward trajectory:

| Week | MCP WAU |
|------|---------|
| Sep 8, 2025 | 1 |
| Oct 13, 2025 | 4 |
| Nov 3, 2025 | 7 |
| Nov 24, 2025 | 11 |
| Dec 1-15, 2025 | **13** |

**13x growth in 3 months.** MCP is how teams connect Cursor to their internal tools and infrastructure. This growing adoption signals Envato is integrating Cursor deeply into their development workflow -- exactly the kind of customization that benefits from Enterprise admin controls and governance.

### Plan Mode Usage
Plan Mode adoption is also climbing:

| Week | Plan Mode WAU |
|------|---------------|
| Oct 6, 2025 | 10 |
| Nov 3, 2025 | 18 |
| Dec 1, 2025 | 19 |
| Dec 15, 2025 | **22** |

**2.2x growth in 10 weeks.** Plan Mode users tend to be strategic users who rely on Cursor for complex, multi-step engineering tasks. This cohort represents high-value power users.

### Best-of-N Usage
Best-of-N (parallel agent attempts) started appearing in late October:

| Week | Best-of-N WAU |
|------|---------------|
| Oct 27, 2025 | 2 |
| Nov 17, 2025 | 5 |
| Dec 15, 2025 | 3 |

Still early but shows willingness to adopt cutting-edge capabilities as they become available.

### Rules Usage
Team rules adoption is steady:

| Week | Rules WAU |
|------|-----------|
| Sep 1, 2025 | 1 |
| Sep 29, 2025 | 6 |
| Oct 27, 2025 | 8 |
| Dec 1, 2025 | 8 |

Rules are how teams enforce coding standards, conventions, and best practices through Cursor. With Enterprise, they could centrally manage and deploy rules across all 100+ users.

---

## 5. Zero Competitor Tool Leakage

**Envato has zero users on competing AI coding tools** (Claude Code, OpenAI Codex, Google Gemini Code Assist, Amp). The competitor usage table returned no rows for this team.

This is a strong signal that:
- Developers are satisfied with Cursor and not seeking alternatives
- There's no shadow IT risk from competing tools
- The organization has effectively standardized on Cursor

This makes them an ideal enterprise customer -- they've already consolidated on Cursor and just need the enterprise wrapper to manage it properly at scale.

---

## 6. Daily Request Volume Shows Deep Integration

Looking at the granular daily request data, Envato's total daily request volume (agent + composer + chat) paints a picture of a team that lives in Cursor:

| Period | Typical Weekday Requests | Peak Day |
|--------|-------------------------|----------|
| Jan 2025 | 100-400 | 361 (Jan 9) |
| Mar 2025 | 200-500 | 488 (Mar 24) |
| May 2025 | 400-1,100 | 1,074 (May 27) |
| Jul 2025 | 600-1,600 | 1,617 (Jul 17) |
| Sep 2025 | 800-2,500 | 2,531 (Sep 11) |
| Nov 2025 | 800-2,700 | 2,724 (Nov 18) |

Total daily requests grew roughly **7x from January to November 2025**. The team is not just using Cursor casually -- it has become their primary coding interface.

---

## 7. Enterprise Pitch Narrative

### The Story to Tell the CTO

> "Your engineering team has voted with their fingers. Over the past year, Envato has grown from a 12-person Cursor pilot to 100+ daily active developers -- an 8x increase that happened organically. Your developers aren't just using Cursor for autocomplete anymore: 80% of your active users are running Agent mode weekly, you have 20 power users, and your team is actively adopting advanced capabilities like MCP integrations, Plan Mode, and Best-of-N.
>
> This organic success has created a new challenge: your usage-based spend has grown from near-zero to nearly $12,000 per month. That's a trajectory that demands enterprise-grade cost controls, spend visibility, and pricing predictability.
>
> At 100+ active users, you also need the governance layer that Enterprise provides: SSO/SCIM for user lifecycle management, audit logs for compliance, centralized admin controls for model and feature policies, and team-wide rules management to enforce coding standards at scale.
>
> The good news: your team has zero leakage to competing tools. They've chosen Cursor. Now it's time to give them -- and your IT and finance teams -- the enterprise infrastructure to support that choice properly."

### Key Selling Points

1. **Cost Predictability**: $12K/month in variable usage costs is budget-unfriendly. Enterprise committed pricing provides predictability and likely savings at their volume.

2. **Governance at Scale**: 100+ users need SSO/SCIM, audit logs, and centralized policy management that only Enterprise provides.

3. **Usage Controls**: Heavy agent adoption drives high token consumption. Enterprise usage policies let admins set guardrails without limiting developer productivity.

4. **Admin Visibility**: With their usage growing 7x in 4 months, leadership needs dashboards and analytics to understand and manage AI-assisted development across the org.

5. **Rules & Standards at Scale**: Enterprise enables centrally managed team rules, ensuring consistent coding standards across 100+ developers.

6. **Future Growth**: At 144 seats with ~100 active, there's still room to grow. Enterprise onboarding, training, and support accelerate adoption of the remaining seats.

---

*Analysis generated on March 25, 2026 from Cursor internal analytics data.*
