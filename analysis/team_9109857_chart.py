#!/usr/bin/env python3
import json, sys
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import pandas as pd
import seaborn as sns

SCENARIOS = [
    ("all_anthropic_cost", "ALL Anthropic (+CTF)", "#C44E52"),
    ("status_quo_cost", "Status Quo (+CTF)", "#4C72B0"),
    ("optimized_cost", "Optimized (+CTF)", "#55A868"),
]
MONTH_LABELS = {"2026-02": "Feb 2026", "2026-03": "Mar 2026", "2026-04": "Apr 2026", "2026-05": "May 2026"}

def load_data(path):
    df = pd.DataFrame(json.loads(path.read_text()))
    df["month"] = pd.to_datetime(df["month_start"]).dt.strftime("%Y-%m")
    df["month_label"] = df["month"].map(MONTH_LABELS).fillna(df["month"])
    for col in ["status_quo_cost", "all_anthropic_cost", "optimized_cost"]:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0.0)
    df["user_short"] = df["email"].fillna(df["owninguser"].astype(str)).str.replace("@montran.com", "", regex=False)
    return df

def month_totals(df):
    totals = df.groupby("month_label", as_index=False)[["status_quo_cost", "all_anthropic_cost", "optimized_cost"]].sum()
    order = [MONTH_LABELS[m] for m in sorted(MONTH_LABELS) if MONTH_LABELS[m] in totals["month_label"].values]
    totals["month_label"] = pd.Categorical(totals["month_label"], categories=order, ordered=True)
    return totals.sort_values("month_label")

def top_users(df, n=25):
    return df.groupby("user_short")["status_quo_cost"].sum().sort_values(ascending=False).head(n).index.tolist()

def plot_faceted_bars(df, out_path, top_n=25):
    users = top_users(df, top_n)
    plot_df = df[df["user_short"].isin(users)].copy()
    long = plot_df.melt(id_vars=["month_label", "user_short"], value_vars=[s[0] for s in SCENARIOS], var_name="scenario_key", value_name="cost")
    scenario_map = {k: label for k, label, _ in SCENARIOS}
    color_map = {k: color for k, _, color in SCENARIOS}
    long["scenario"] = long["scenario_key"].map(scenario_map)
    months = [MONTH_LABELS[m] for m in sorted(MONTH_LABELS) if MONTH_LABELS[m] in plot_df["month_label"].unique()]
    long["month_label"] = pd.Categorical(long["month_label"], categories=months, ordered=True)
    sns.set_theme(style="whitegrid", context="talk", font_scale=0.85)
    g = sns.catplot(data=long, kind="bar", x="user_short", y="cost", hue="scenario", col="month_label", col_order=months,
        palette=[color_map[s[0]] for s in SCENARIOS], height=7, aspect=1.6, legend=False)
    g.set_axis_labels("", "Cost (USD)")
    g.set_titles("Month: {col_name}")
    for ax in g.axes.flat:
        ax.tick_params(axis="x", rotation=75, labelsize=8)
        ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
    g.fig.subplots_adjust(top=0.9, bottom=0.22)
    handles = [plt.Rectangle((0, 0), 1, 1, color=color_map[s[0]]) for s in SCENARIOS]
    g.fig.legend(handles, [s[1] for s in SCENARIOS], loc="upper center", ncol=3, frameon=False)
    g.fig.suptitle("Montran Corporation (Team 9109857)\nPer-User Monthly API + CTF Cost by Scenario", fontsize=16, y=0.98)
    g.savefig(out_path, dpi=160, bbox_inches="tight")
    plt.close(g.fig)

def plot_monthly_totals(totals, out_path):
    long = totals.melt(id_vars=["month_label"], value_vars=[s[0] for s in SCENARIOS], var_name="scenario_key", value_name="cost")
    scenario_map = {k: label for k, label, _ in SCENARIOS}
    color_map = {k: color for k, _, color in SCENARIOS}
    long["scenario"] = long["scenario_key"].map(scenario_map)
    sns.set_theme(style="whitegrid", context="talk")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(data=long, x="month_label", y="cost", hue="scenario", palette=[color_map[s[0]] for s in SCENARIOS], ax=ax)
    ax.set_xlabel("")
    ax.set_ylabel("Total Cost (USD)")
    ax.set_title("Team 9109857 Monthly Run-Rate by Scenario")
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
    ax.legend(title="", frameon=False)
    fig.tight_layout()
    fig.savefig(out_path, dpi=160, bbox_inches="tight")
    plt.close(fig)

def plot_savings_waterfall(totals, out_path):
    latest = totals.iloc[-1]
    labels = ["Status Quo", "ALL Anthropic", "Optimized"]
    values = [latest["status_quo_cost"], latest["all_anthropic_cost"], latest["optimized_cost"]]
    colors = ["#4C72B0", "#C44E52", "#55A868"]
    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.bar(labels, values, color=colors)
    ax.set_ylabel("Total Cost (USD)")
    ax.set_title(f"Latest Month ({latest['month_label']}) Team Cost Comparison")
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
    for bar, val in zip(bars, values):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), f"${val:,.0f}", ha="center", va="bottom", fontsize=10)
    fig.tight_layout()
    fig.savefig(out_path, dpi=160, bbox_inches="tight")
    plt.close(fig)

def print_summary(df, totals):
    print("=== Team 9109857 Run-Rate Scenario Analysis ===")
    print(f"Users with usage: {df['owninguser'].nunique()}")
    print(f"Months: {', '.join(totals['month_label'].astype(str).tolist())}\n")
    print("Monthly team totals (USD):")
    for _, row in totals.iterrows():
        sq, ant, opt = row["status_quo_cost"], row["all_anthropic_cost"], row["optimized_cost"]
        savings = sq - opt
        pct = (savings / sq * 100) if sq else 0
        print(f"  {row['month_label']}: Status Quo ${sq:,.0f} | ALL Anthropic ${ant:,.0f} | Optimized ${opt:,.0f} | saves ${savings:,.0f} ({pct:.1f}%)")
    latest = totals.iloc[-1]
    print(f"\nLatest-month annualized: Status Quo ${latest['status_quo_cost']*12:,.0f}/yr | Optimized ${latest['optimized_cost']*12:,.0f}/yr")

if __name__ == "__main__":
    data_path = Path(sys.argv[1] if len(sys.argv) > 1 else "team_9109857_costs.json")
    out_dir = Path(sys.argv[2] if len(sys.argv) > 2 else "output")
    out_dir.mkdir(parents=True, exist_ok=True)
    df = load_data(data_path)
    totals = month_totals(df)
    print_summary(df, totals)
    plot_faceted_bars(df, out_dir / "team_9109857_per_user_per_month.png")
    plot_monthly_totals(totals, out_dir / "team_9109857_monthly_totals.png")
    plot_savings_waterfall(totals, out_dir / "team_9109857_latest_month_comparison.png")
    print(f"\nCharts written to {out_dir}/")

