#!/usr/bin/env python3
"""Run-rate cost analysis for team 2354493 (Taboola) across three scenarios."""

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

CTF_PER_M = 0.25  # Teams plan Cursor Token Rate ($/M tokens), non-Auto only

# Public API rates from https://cursor.com/docs/models-and-pricing ($/M tokens)
PRICING = {
    "auto": {"input": 1.25, "cache_write": 1.25, "cache_read": 0.25, "output": 6.0, "ctf_exempt": True},
    "claude-4-6-sonnet": {"input": 3.0, "cache_write": 3.75, "cache_read": 0.3, "output": 15.0},
    "claude-4-7-opus": {"input": 5.0, "cache_write": 6.25, "cache_read": 0.5, "output": 25.0},
    # Opus Fast Mode (limited research preview) — 6x normal Opus rates
    "claude-4-7-opus-fast": {"input": 30.0, "cache_write": 37.5, "cache_read": 3.0, "output": 150.0},
    "claude-4-5-haiku": {"input": 1.0, "cache_write": 1.25, "cache_read": 0.1, "output": 5.0},
    "composer-2": {"input": 0.5, "cache_write": 0.5, "cache_read": 0.2, "output": 2.5},
    "composer-1.5": {"input": 3.5, "cache_write": 3.5, "cache_read": 0.35, "output": 17.5},
    "composer-1": {"input": 1.25, "cache_write": 1.25, "cache_read": 0.125, "output": 10.0},
    "gpt-5.5": {"input": 5.0, "cache_write": 5.0, "cache_read": 0.5, "output": 30.0},
    "gpt-5.4": {"input": 2.5, "cache_write": 2.5, "cache_read": 0.25, "output": 15.0},
    "gpt-5.3-codex": {"input": 1.75, "cache_write": 1.75, "cache_read": 0.175, "output": 14.0},
    "gpt-5.2": {"input": 1.75, "cache_write": 1.75, "cache_read": 0.175, "output": 14.0},
    "gpt-5.2-codex": {"input": 1.75, "cache_write": 1.75, "cache_read": 0.175, "output": 14.0},
    "gpt-5": {"input": 1.25, "cache_write": 1.25, "cache_read": 0.125, "output": 10.0},
    "gpt-5.1-codex-max": {"input": 1.25, "cache_write": 1.25, "cache_read": 0.125, "output": 10.0},
    "gpt-5.1-codex-mini": {"input": 0.25, "cache_write": 0.25, "cache_read": 0.025, "output": 2.0},
    "gemini-3-1-pro": {"input": 2.0, "cache_write": 2.0, "cache_read": 0.2, "output": 12.0},
    "gemini-3-pro": {"input": 2.0, "cache_write": 2.0, "cache_read": 0.2, "output": 12.0},
    "gemini-3-flash": {"input": 0.5, "cache_write": 0.5, "cache_read": 0.05, "output": 3.0},
    "grok-4": {"input": 2.0, "cache_write": 2.0, "cache_read": 0.2, "output": 6.0},
    "grok-code": {"input": 1.25, "cache_write": 1.25, "cache_read": 0.2, "output": 2.5},
    "kimi-k2": {"input": 0.6, "cache_write": 0.6, "cache_read": 0.1, "output": 3.0},
}

AUTO_MODELS = {"default", "auto", "premium"}  # premium = Premium routing (Auto-tier pool)


def _is_thinking_sonnet(m: str) -> bool:
    return "sonnet" in m and "thinking" in m


def _is_max_opus(m: str) -> bool:
    """Highest-reasoning Opus tiers — preserve in Optimized to avoid quality regression."""
    return ("opus" in m) and ("max" in m or "xhigh" in m)


def _is_fast_opus(m: str) -> bool:
    return "opus" in m and "fast" in m


def normalize_model(name: str) -> str:
    return (name or "").lower().strip()


def classify_actual_model(model_name: str) -> str:
    """Status quo: map raw model names to public pricing keys."""
    m = normalize_model(model_name)
    if m in AUTO_MODELS or m.startswith("premium"):
        return "auto"
    if m.startswith("composer-2"):
        return "composer-2"
    if m == "composer-1.5":
        return "composer-1.5"
    if m == "composer-1":
        return "composer-1"
    if m.startswith("gpt-5.5"):
        return "gpt-5.5"
    if m.startswith("gpt-5.4"):
        return "gpt-5.4"
    if m.startswith("gpt-5.3-codex"):
        return "gpt-5.3-codex"
    if m.startswith("gpt-5.2-codex"):
        return "gpt-5.2-codex"
    if m.startswith("gpt-5.2"):
        return "gpt-5.2"
    if m.startswith("gpt-5.1-codex-mini"):
        return "gpt-5.1-codex-mini"
    if m.startswith("gpt-5.1-codex"):
        return "gpt-5.1-codex-max"
    if m.startswith("gpt-5"):
        return "gpt-5"
    if "opus" in m and "fast" in m:
        return "claude-4-7-opus-fast"
    if "opus-4-7" in m or "opus-4.7" in m or "4-7-opus" in m:
        return "claude-4-7-opus"
    if "opus" in m:
        return "claude-4-7-opus"  # 4.6/4.5 opus → 4.7 rates (closest public)
    if "haiku" in m:
        return "claude-4-5-haiku"
    if "sonnet" in m:
        return "claude-4-6-sonnet"
    if m.startswith("gemini-3-1"):
        return "gemini-3-1-pro"
    if m.startswith("gemini-3"):
        return "gemini-3-pro" if "flash" not in m else "gemini-3-flash"
    if m.startswith("grok-code"):
        return "grok-code"
    if m.startswith("grok"):
        return "grok-4"
    if m.startswith("kimi") or "kimi" in m:
        return "kimi-k2"
    if m in {"agent_review", "github_bugbot"}:
        return "claude-4-6-sonnet"
    return "claude-4-6-sonnet"


def map_all_anthropic(model_name: str) -> str:
    """ALL Anthropic: Auto/Composer/intelligence → Sonnet; GPT/Codex → Opus 4.7.
    Opus Fast Mode users keep Opus Fast (top reasoning tier — credible peer would
    be Opus Fast itself, not a downgrade)."""
    m = normalize_model(model_name)
    if m in AUTO_MODELS or m.startswith("premium"):
        return "claude-4-6-sonnet"
    if m.startswith("composer"):
        return "claude-4-6-sonnet"
    if "opus" in m and "fast" in m:
        return "claude-4-7-opus-fast"
    if "opus" in m:
        return "claude-4-7-opus"
    if m.startswith("gpt-5.5") or m.startswith("gpt-5.3-codex") or m.startswith("gpt-5.4"):
        return "claude-4-7-opus"
    if m.startswith("gpt-5"):
        return "claude-4-7-opus"
    if "haiku" in m:
        return "claude-4-5-haiku"
    if m.startswith("gemini-3-1") or m.startswith("gemini-3-pro"):
        return "claude-4-7-opus"
    if m.startswith("gemini"):
        return "claude-4-6-sonnet"
    if m.startswith("grok") or m.startswith("kimi"):
        return "claude-4-6-sonnet"
    if "sonnet" in m:
        return "claude-4-6-sonnet"
    return "claude-4-6-sonnet"


def map_optimized(model_name: str) -> str:
    """Optimized (Aggressive) — biggest savings while keeping every swap defensible.

    Design principles:
      • Never demote `*-opus-max-*` — these users explicitly demanded peak reasoning.
        Keep them on Opus 4.7.
      • Opus Fast Mode (limited research preview at 6x rates) → standard Opus 4.7.
        Same model, normal Cursor pricing — zero quality regression.
      • Top-tier Opus thinking (`xhigh`) → GPT 5.5. OpenAI's peer top-reasoning
        model. Pricing is comparable per-token.
      • Workhorse high-thinking Opus (the bulk of the Opus pool) → GPT 5.4. Per
        Cursor docs GPT 5.4 is "agentic and reasoning capabilities" with Max Mode
        and 90% cache-input discount. For Cursor's core agentic coding workloads
        it's a credible peer at ~½ the rate of Opus and ~½ the rate of GPT 5.5.
      • Sonnet thinking variants stay on Sonnet — preserves reasoning depth.
      • Workhorse non-thinking Sonnet → Composer 2 (Cursor's Sonnet-class agent).
      • Composer 1 / Composer 1.5 → Composer 2 — strict newer-gen upgrade *and*
        cheaper. No-brainer.
      • Codex / Gemini / Grok / Kimi / Auto unchanged.
    """
    m = normalize_model(model_name)
    if m in AUTO_MODELS or m.startswith("premium"):
        return "auto"
    if "opus" in m:
        if _is_fast_opus(m):
            return "claude-4-7-opus"
        if "max" in m:
            return "claude-4-7-opus"
        if "xhigh" in m:
            return "gpt-5.5"
        return "gpt-5.4"
    if "sonnet" in m:
        if "thinking" in m:
            return "claude-4-6-sonnet"
        return "composer-2"
    if m.startswith("composer-1"):
        return "composer-2"
    if m.startswith("composer-2"):
        return "composer-2"
    return classify_actual_model(model_name)


def map_optimized_conservative(model_name: str) -> str:
    """Optimized (Conservative) — only swaps that preserve like-for-like quality.

    Differences from aggressive: all Opus thinking variants (high / xhigh / max)
    stay on Opus 4.7 — no OpenAI swap for any explicitly-thinking workload. Savings
    come only from Opus Fast Mode → Opus standard, Sonnet non-thinking → Composer 2,
    and Composer 1 / 1.5 → Composer 2. CTF still applies.
    """
    m = normalize_model(model_name)
    if m in AUTO_MODELS or m.startswith("premium"):
        return "auto"
    if "opus" in m:
        if _is_fast_opus(m):
            return "claude-4-7-opus"
        return "claude-4-7-opus"  # all Opus thinking stays on Opus
    if "sonnet" in m:
        if "thinking" in m:
            return "claude-4-6-sonnet"
        return "composer-2"
    if m.startswith("composer-1"):
        return "composer-2"
    if m.startswith("composer-2"):
        return "composer-2"
    return classify_actual_model(model_name)


def token_cost(row, price_key: str, apply_ctf: bool) -> float:
    rates = PRICING[price_key]
    inp = row["input_tokens"]
    out = row["output_tokens"]
    cw = row["cache_write_tokens"]
    cr = row["cache_read_tokens"]
    cost = (
        inp * rates["input"]
        + out * rates["output"]
        + cw * rates.get("cache_write", rates["input"])
        + cr * rates["cache_read"]
    ) / 1_000_000
    total_tokens = inp + out + cw + cr
    if apply_ctf and not rates.get("ctf_exempt", False):
        cost += total_tokens * CTF_PER_M / 1_000_000
    return cost


def scenario_cost(row, scenario: str) -> float:
    model = normalize_model(row["model_name"])
    if scenario == "status_quo":
        key = classify_actual_model(model)
        apply_ctf = key != "auto"
        return token_cost(row, key, apply_ctf)
    if scenario == "all_anthropic":
        key = map_all_anthropic(model)
        return token_cost(row, key, apply_ctf=False)
    if scenario == "optimized":
        key = map_optimized(model)
        apply_ctf = key != "auto"
        return token_cost(row, key, apply_ctf)
    if scenario == "optimized_conservative":
        key = map_optimized_conservative(model)
        apply_ctf = key != "auto"
        return token_cost(row, key, apply_ctf)
    raise ValueError(scenario)


def _parse_cell(v):
    if isinstance(v, dict):
        if "string_value" in v:
            return v["string_value"]
        if "str" in v:
            return v["str"]
        if "null_value" in v or v == {}:
            return None
        return next(iter(v.values()), None)
    return v


def load_usage(path: Path) -> pd.DataFrame:
    columns = [
        "owninguser",
        "month",
        "model_name",
        "input_tokens",
        "output_tokens",
        "cache_write_tokens",
        "cache_read_tokens",
        "email",
    ]
    if path.suffix == ".json":
        with open(path) as f:
            payload = json.load(f)
        rows = None
        if isinstance(payload, list) and payload:
            if isinstance(payload[0], dict):
                df = pd.DataFrame(payload)
            else:
                rows = payload
        elif "result" in payload:
            res = payload["result"]
            if "data_typed_array" in res:
                rows = [[_parse_cell(v) for v in item["values"]] for item in res["data_typed_array"]]
            elif "data_array" in res:
                rows = [[_parse_cell(v) for v in item["values"]] for item in res["data_array"]]
        else:
            df = pd.DataFrame(payload)
        if rows is not None:
            df = pd.DataFrame(rows, columns=columns)
    else:
        df = pd.read_csv(path)

    # Normalize column names from MCP / alternate exports
    rename_map = {
        "user_id": "owninguser",
        "requested_model": "model_name",
        "usage_month": "month",
    }
    df = df.rename(columns={k: v for k, v in rename_map.items() if k in df.columns})

    for col in ["input_tokens", "output_tokens", "cache_write_tokens", "cache_read_tokens"]:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0).astype(np.int64)
    # Normalize month to yyyy-MM
    df["month"] = pd.to_datetime(df["month"], errors="coerce").dt.strftime("%Y-%m")
    df["email"] = df["email"].fillna(df["owninguser"].astype(str))
    df["user"] = df["email"].apply(lambda x: x.split("@")[0] if isinstance(x, str) and "@" in x else str(x))
    return df


def short_label(email: str, max_len: int = 20) -> str:
    user = email.split("@")[0] if "@" in email else str(email)
    return user if len(user) <= max_len else user[: max_len - 1] + "…"


def main():
    data_path = Path(__file__).parent / "usage_data.json"
    out_dir = Path(__file__).parent
    df = load_usage(data_path)

    scenarios = {
        "status_quo": "Status Quo (+$0.25/M CTF)",
        "all_anthropic": "ALL Anthropic",
        "optimized_conservative": "Optimized — Conservative",
        "optimized": "Optimized — Aggressive",
    }
    colors = {
        "status_quo": "#4C78A8",
        "all_anthropic": "#F58518",
        "optimized_conservative": "#9ECAE1",
        "optimized": "#54A24B",
    }

    records = []
    for scenario in scenarios:
        tmp = df.copy()
        tmp["cost"] = tmp.apply(lambda r: scenario_cost(r, scenario), axis=1)
        agg = tmp.groupby(["month", "email", "user"], as_index=False)["cost"].sum()
        agg["scenario"] = scenario
        records.append(agg)
    costs = pd.concat(records, ignore_index=True)

    summary = costs.groupby(["month", "scenario"], as_index=False)["cost"].sum()
    summary_pivot = summary.pivot(index="month", columns="scenario", values="cost").fillna(0)

    print("\n=== Team monthly run-rate by scenario ===")
    print(summary_pivot.to_string(float_format=lambda x: f"${x:,.0f}"))

    months = sorted(costs["month"].unique())

    # Chart 1: Team monthly trend
    fig2, ax2 = plt.subplots(figsize=(11, 5))
    n = len(scenarios)
    x = np.arange(len(months))
    width = 0.8 / n
    for i, (scenario, label) in enumerate(scenarios.items()):
        vals = [summary[(summary.month == m) & (summary.scenario == scenario)]["cost"].sum() for m in months]
        offset = (i - (n - 1) / 2.0) * width
        ax2.bar(x + offset, vals, width=width, label=label, color=colors[scenario])
    ax2.set_xticks(x)
    ax2.set_xticklabels(months)
    ax2.set_ylabel("Team cost ($)")
    ax2.set_title("Team 2354493 (Taboola) — Monthly run-rate by scenario")
    ax2.legend()
    ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"${v:,.0f}"))
    plt.tight_layout()
    trend_path = out_dir / "team_2354493_monthly_trend.png"
    fig2.savefig(trend_path, dpi=160, bbox_inches="tight")
    print(f"Trend chart saved to {trend_path}")

    # Chart 2: Per-user per-month — top 20 users by 3-month status quo total
    user_sq = costs[costs["scenario"] == "status_quo"].groupby("email")["cost"].sum()
    top_users = user_sq.nlargest(20).index.tolist()
    top_labels = {e: short_label(e) for e in top_users}

    fig, axes = plt.subplots(1, len(months), figsize=(6 * len(months), 13), sharey=True)
    if len(months) == 1:
        axes = [axes]

    for ax, month in zip(axes, months):
        month_df = costs[(costs["month"] == month) & (costs["email"].isin(top_users))]
        pivot = month_df.pivot_table(index="email", columns="scenario", values="cost", aggfunc="sum").fillna(0)
        pivot = pivot.reindex(top_users).fillna(0)
        pivot.index = [top_labels[e] for e in pivot.index]

        n = len(scenarios)
        y = np.arange(len(pivot))
        height = 0.8 / n
        for i, scenario in enumerate(scenarios):
            if scenario in pivot.columns:
                vals = pivot[scenario].values
            else:
                vals = np.zeros(len(pivot))
            offset = (i - (n - 1) / 2.0) * height
            ax.barh(y + offset, vals, height=height, label=scenarios[scenario], color=colors[scenario])

        ax.set_yticks(y)
        ax.set_yticklabels(pivot.index, fontsize=7)
        ax.invert_yaxis()
        ax.set_title(month)
        ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"${v:,.0f}"))
        if month == months[0]:
            ax.set_ylabel("User")
        ax.set_xlabel("Cost ($)")

    fig.suptitle(
        "Team 2354493 — Per-user monthly cost by scenario (top 20 users by Status Quo spend)\n"
        "Rates: cursor.com/docs/models-and-pricing",
        fontsize=11,
        y=1.02,
    )
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="lower center", ncol=3, bbox_to_anchor=(0.5, -0.02))
    plt.tight_layout()
    chart_path = out_dir / "team_2354493_cost_scenarios.png"
    fig.savefig(chart_path, dpi=160, bbox_inches="tight")
    print(f"Per-user chart saved to {chart_path}")

    # Chart 3: Heatmap — all users with meaningful spend, per month (status quo vs optimized delta)
    user_month_pivot = costs.pivot_table(
        index=["email", "user"],
        columns=["month", "scenario"],
        values="cost",
        aggfunc="sum",
        fill_value=0,
    )
    active_users = costs.groupby("email")["cost"].sum()
    active_users = active_users[active_users > 50].index  # >$50 over period
    hm_users = user_sq.loc[user_sq.index.isin(active_users)].nlargest(40).index

    fig3, axes3 = plt.subplots(1, 3, figsize=(16, 14), sharey=True)
    for ax, (scenario, label) in zip(axes3, scenarios.items()):
        mat = []
        for email in hm_users:
            row = []
            for month in months:
                val = costs[(costs.email == email) & (costs.month == month) & (costs.scenario == scenario)][
                    "cost"
                ].sum()
                row.append(val)
            mat.append(row)
        mat = np.array(mat)
        im = ax.imshow(mat, aspect="auto", cmap="YlOrRd")
        ax.set_xticks(range(len(months)))
        ax.set_xticklabels(months)
        if scenario == "status_quo":
            ax.set_yticks(range(len(hm_users)))
            ax.set_yticklabels([short_label(e, 18) for e in hm_users], fontsize=6)
        ax.set_title(label)
        plt.colorbar(im, ax=ax, format=plt.FuncFormatter(lambda v, _: f"${v:,.0f}"))
    fig3.suptitle("Per-user per-month cost heatmap (top 40 users)", fontsize=12)
    plt.tight_layout()
    heatmap_path = out_dir / "team_2354493_user_month_heatmap.png"
    fig3.savefig(heatmap_path, dpi=160, bbox_inches="tight")
    print(f"Heatmap saved to {heatmap_path}")

    costs.to_csv(out_dir / "per_user_month_scenario_costs.csv", index=False)
    summary.to_csv(out_dir / "team_monthly_summary.csv", index=False)

    sq = summary[summary.scenario == "status_quo"]["cost"].sum()
    opt = summary[summary.scenario == "optimized"]["cost"].sum()
    opt_c = summary[summary.scenario == "optimized_conservative"]["cost"].sum()
    ant = summary[summary.scenario == "all_anthropic"]["cost"].sum()
    print("\n=== 3-month totals ===")
    print(f"Status Quo:                  ${sq:,.0f}")
    print(f"ALL Anthropic:               ${ant:,.0f} ({(ant/sq-1)*100:+.1f}% vs status quo)")
    print(f"Optimized (Conservative):    ${opt_c:,.0f} ({(opt_c/sq-1)*100:+.1f}% vs status quo)")
    print(f"Optimized (Aggressive):      ${opt:,.0f} ({(opt/sq-1)*100:+.1f}% vs status quo)")
    print(f"\nConservative savings: ${sq - opt_c:,.0f} ({(1-opt_c/sq)*100:.1f}%)")
    print(f"Aggressive savings:   ${sq - opt:,.0f}  ({(1-opt/sq)*100:.1f}%)")


if __name__ == "__main__":
    main()
