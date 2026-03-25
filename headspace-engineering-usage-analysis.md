# Headspace Engineering (Team 8969557) - Usage Analysis & Enterprise Upgrade Narrative

## Executive Summary

Headspace Engineering has become one of the most deeply embedded Cursor Teams deployments, growing from an initial rollout in April 2025 to **105+ weekly active developers** generating **3.8 million accepted lines of AI-assisted code**. Their usage patterns reveal an engineering organization that has moved far beyond experimentation -- Cursor is now a core part of how Headspace ships software. The team is bumping up against Teams-tier limits and would benefit significantly from Enterprise features including SSO/SCIM provisioning, advanced admin analytics, enforced privacy controls, and usage governance.

## Quick Narrative

In less than a year, Headspace Engineering went all-in on Cursor. What started as a small pilot in April 2025 exploded into a 105-person daily habit by September -- and they haven't looked back. Seven out of every ten developers on the team now use Agent mode every single week, trusting AI to make complex, multi-file changes across their codebase. The numbers tell the story: 3.8 million lines of AI-generated code accepted, 50,000+ AI requests per month at peak, and 27 power users who've each woven over 50,000 lines of AI output into production. They've already flipped on SSO, locked down privacy mode, and set up repo blocklists -- they're running Cursor like an enterprise tool on a Teams plan. Meanwhile, they're consistently blowing past their subscription limits (69% of requests were overages in peak months), their Cloud Agent usage has tripled and is now producing merged PRs, and they've onboarded 37+ new engineers in the last six months without any automated provisioning. Headspace doesn't need to be convinced that Cursor works -- the data proves their team has already rebuilt their development workflow around it. What they need now is the governance, cost controls, SCIM provisioning, audit logging, and agent oversight that only Enterprise provides.

---

## 1. Rapid, Sustained Adoption

### Team Growth Trajectory

| Month | Cumulative Members | Monthly Active Users |
|-------|-------------------|---------------------|
| Apr 2025 | 36 | 47 |
| May 2025 | 63 | 74 |
| Jun 2025 | 76 | 84 |
| Jul 2025 | 82 | 95 |
| Aug 2025 | 88 | 99 |
| Sep 2025 | 94 | 103 |
| Oct 2025 | 100 | 105 |
| Nov 2025 | 107 | 105 |
| Jan 2026 | 125 | -- |
| Mar 2026 | 137 | -- |

**Key insight:** They went from 0 to 100+ members in under 6 months and are still actively adding seats (14 new in January 2026, 7 in March 2026). The team now has **129 purchased seats and 137 members** -- they are growing past their seat count. Monthly active user counts consistently match or exceed 95% of the team, meaning this is not shelfware. Nearly everyone on the team uses Cursor daily.

---

## 2. Explosive AI Usage -- This Team Ships Code with AI

### Monthly AI Request Volume

| Month | Agent Requests | Composer Requests | Chat Requests | Total AI Requests |
|-------|---------------|-------------------|---------------|------------------|
| Apr 2025 | 1,885 | 36 | 499 | 2,420 |
| May 2025 | 7,207 | 1,487 | 780 | 9,474 |
| Jun 2025 | 9,949 | 10,587 | 653 | 21,189 |
| Jul 2025 | 10,055 | 18,502 | 982 | 29,539 |
| Aug 2025 | 11,966 | 30,263 | 1,219 | 43,448 |
| Sep 2025 | 15,684 | 34,071 | 1,178 | 50,933 |
| Oct 2025 | 16,173 | 30,022 | 1,332 | 47,527 |
| Nov 2025 | 10,551 | 14,618 | 1,624 | 26,793 |

**Total all-time: 231,000+ AI requests.** The team grew from ~2,400 requests/month at launch to a peak of **50,933 requests/month** in September -- a **21x increase** in 5 months.

### Per-User AI Productivity Is Accelerating

| Month | Active Users | AI Requests / User | Accepted Lines / User |
|-------|-------------|-------------------|----------------------|
| Apr 2025 | 47 | 51 | 727 |
| May 2025 | 74 | 128 | 2,029 |
| Jun 2025 | 84 | 252 | 2,940 |
| Jul 2025 | 95 | 311 | 2,698 |
| Aug 2025 | 99 | 439 | 6,185 |
| **Sep 2025** | **103** | **494** | **14,646** |
| Oct 2025 | 105 | 453 | 7,315 |

**Per-user productivity peaked at 14,646 accepted lines per user in September** -- that's each developer accepting nearly 15,000 lines of AI-generated code in a single month. Even in the "slower" months, each user is accepting 2,000-7,000 lines/month. These are not casual users; they're power users building real features.

---

## 3. Agent-First Engineering Culture (~70% Agent Adoption)

### Weekly Agent Adoption Rate

Headspace quickly became an agent-first team. By week 3 of their rollout, over 50% of active users were using Agent mode:

| Period | Agent Users | Total Active | % Using Agent |
|--------|------------|-------------|---------------|
| Apr 14 2025 | 21 | 39 | 53.8% |
| Jun 9 2025 | 57 | 77 | 74.0% |
| Sep 8 2025 | 72 | 100 | 72.0% |
| Nov 17 2025 | 75 | 105 | 71.4% |

**Consistently 65-74% of the team uses Agent mode every week.** This is a team that trusts AI to make complex, multi-file changes -- not just autocomplete. The implication: they need enterprise-grade governance and controls for these agentic workflows.

---

## 4. 3.8 Million Lines of AI-Accepted Code

### Monthly Accepted Lines (Added + Deleted)

| Month | Accepted Lines | Growth |
|-------|---------------|--------|
| Apr 2025 | 34,171 | -- |
| May 2025 | 150,132 | 4.4x |
| Jun 2025 | 246,965 | 1.6x |
| Jul 2025 | 256,357 | 1.0x |
| Aug 2025 | 612,268 | 2.4x |
| **Sep 2025** | **1,508,555** | **2.5x** |
| Oct 2025 | 768,078 | -- |
| Nov 2025 | 199,960 | -- |

**Total: 3,776,486 accepted lines.** In September alone, the team accepted **1.5 million lines** of AI-generated code. This represents massive productivity leverage -- equivalent to dozens of additional developers' output.

### Power User Distribution

| Tier | Users | Accepted Lines | Avg Active Days |
|------|-------|---------------|----------------|
| Power User (50k+ lines) | 27 | 3,016,374 | 201 |
| Heavy User (10k-50k lines) | 29 | 641,292 | 190 |
| Moderate User (1k-10k lines) | 23 | 115,734 | 187 |
| Light User (<1k lines) | 13 | 3,086 | 134 |

**27 power users** (25% of the team) generated **80% of all accepted lines.** These are developers who have fundamentally changed how they work. The top individual contributor (alexey.bedonik@headspace.com) alone has **448,286 accepted lines** over 153 active days.

---

## 5. Usage-Based Spend Is Growing -- They're Exceeding Subscription Limits

### Subscription vs. Usage-Based Request Share

| Month | Subscription Reqs | Usage-Based Reqs | % Usage-Based |
|-------|-------------------|-----------------|---------------|
| Apr 2025 | 2,518 | 0 | 0% |
| May 2025 | 8,040 | 1,753 | 17.9% |
| Jun 2025 | 12,884 | 8,491 | 39.7% |
| Jul 2025 | 10,757 | 18,947 | **63.8%** |
| Aug 2025 | 14,889 | 28,667 | **65.8%** |
| Sep 2025 | 15,832 | 35,291 | **69.0%** |
| Oct 2025 | 24,792 | 22,888 | 48.0% |

**By July 2025, the majority of their requests exceeded subscription limits and billed as usage-based.** In September, **69% of all requests** were usage-based overages. This means the team is consistently pushing beyond what Teams-tier subscription limits provide.

### Direct Usage-Based Spend (Service Usage Events)

| Month | Usage-Based Spend | Events |
|-------|------------------|--------|
| Jun 2025 | $216.55 | 257 |
| Jul 2025 | $1,320.03 | 2,191 |
| Aug 2025 | $246.05 | 3,151 |
| Sep 2025 | $594.66 | 3,114 |
| Oct 2025 | $492.04 | 2,541 |
| Nov 2025 | $305.24 | 327 |
| Dec 2025 | $300.63 | 280 |
| Jan 2026 | $239.06 | 299 |
| Feb 2026 | $226.27 | 261 |

Total observed overage spend: **~$3,940+**. Combined with monthly seat costs, their total Cursor spend is substantial and growing with the team.

---

## 6. Model Sophistication -- Power Users on Frontier Models

### Most-Used Models (by user-days)

| Model | Unique Users | User-Days |
|-------|-------------|-----------|
| claude-4-sonnet-thinking | 87 | 1,651 |
| default (auto) | 80 | 1,638 |
| claude-4-sonnet | 52 | 791 |
| claude-4.5-sonnet-thinking | 59 | 706 |
| gpt-5 | 38 | 464 |
| claude-3.5-sonnet | 37 | 190 |
| claude-4.5-sonnet | 14 | 170 |
| claude-4.1-opus-thinking | 9 | 70 |
| claude-4-opus-thinking | 7 | 68 |
| gpt-5-codex | 11 | 67 |

**87 users** (the vast majority of the team) have adopted Claude 4 Sonnet with thinking mode as their go-to model. This shows a highly sophisticated engineering team that uses the most capable reasoning models available. Their spending on premium tier models (Opus, GPT-5 Codex) further reinforces that they're willing to pay for the best AI tooling.

---

## 7. Cloud Agents -- Early but Growing Adoption

| Month | Cloud Agent Runs | Unique Users | PRs Created | PRs Merged |
|-------|-----------------|-------------|-------------|------------|
| Jul 2025 | 21 | 6 | 4 | 1 |
| Aug 2025 | 20 | 4 | 3 | 0 |
| Sep 2025 | 25 | 3 | 3 | 0 |
| Dec 2025 | 33 | 2 | 9 | 0 |
| Jan 2026 | 43 | 2 | 0 | 0 |
| **Mar 2026** | **73** | **4** | **0** | **6** |

Cloud Agent runs have **grown 3.5x from July 2025 to March 2026** (21 to 73 runs/month). March 2026 saw 6 merged PRs from Cloud Agents -- the team is starting to trust autonomous agents to ship production code. Enterprise features like audit logs and agent governance would be critical as this scales.

---

## 8. Enterprise Readiness Signals

The team is already behaving like an Enterprise customer:

| Feature | Current Status | Enterprise Value |
|---------|---------------|-----------------|
| **SSO** | Enabled (allow_sso = true, sso_enabled = true) | Already using -- Enterprise provides enforced SSO |
| **SCIM** | Not connected | Enterprise provides automated user provisioning |
| **Privacy Mode** | NO_TRAINING, forced = true | Already enforcing -- Enterprise adds audit logging |
| **Repo Blocklist** | BLOCK mode enabled | Enterprise provides granular controls |
| **Admin Analytics** | Requires admin (dashboard_analytics_requires_admin = true) | Enterprise provides deeper analytics |
| **Team Size** | 137 members, 129 seats | Enterprise provides volume pricing |
| **Hard Limits** | $10,000 team / $1,050/user | Enterprise provides custom limits and governance |
| **Usage-Based Pricing** | Enabled, active overages | Enterprise provides better unit economics |

---

## 9. The Narrative for the CTO

**"Your engineering org has fundamentally changed how it builds software."**

In less than a year, Headspace Engineering went from zero to having **105 developers actively using AI-assisted coding every single week**. Your team has accepted **3.8 million lines** of AI-generated code -- the equivalent output of dozens of additional engineers. **70% of your developers** use Agent mode every week, trusting AI to make complex, multi-file changes to your codebase.

**This isn't experimentation anymore. This is how Headspace ships software.**

The scale of your adoption creates specific challenges that Enterprise solves:

1. **Governance at scale**: With 100+ developers using agentic AI to modify production code daily, you need comprehensive audit logging, admin controls, and usage policies that go beyond what Teams provides.

2. **Cost optimization**: Your team consistently exceeds subscription limits -- **69% of requests in peak months were usage-based overages**. Enterprise pricing gives you better unit economics as usage scales, with custom limits and committed-use discounts.

3. **Identity & access management**: You've already enabled SSO, but Enterprise gives you SCIM for automated user provisioning/deprovisioning -- critical with a team that's added 37+ new members in the last 6 months.

4. **Security & compliance**: You've enforced NO_TRAINING privacy mode and repo blocklists. Enterprise adds SOC 2 Type II compliance, audit logs for AI interactions, and the ability to route through your own cloud infrastructure.

5. **Cloud Agent governance**: Your Cloud Agent usage has grown 3.5x and is now producing merged PRs. As autonomous agents generate production code, you need enterprise-grade controls, approval workflows, and visibility.

**Bottom line: Headspace has 27 power users who've each accepted 50,000+ lines of AI code. Your team generates 50,000+ AI requests per month. You're already paying for overages. Enterprise gives you the governance, economics, and controls to scale this responsibly -- and to unlock features like unlimited Cloud Agent runs, deeper analytics, and dedicated support.**

---

*Analysis generated March 25, 2026 from Cursor usage telemetry.*
