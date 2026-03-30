-- AppDirect (Team 5764393) On-Demand Usage Analysis - March 2026
-- Enterprise contract: $56,640 committed usage, Sept 15 2025 - Sept 15 2026

-- 1. Monthly usage breakdown across the contract period
SELECT
  DATE_TRUNC('month', timestamp) AS usage_month,
  SUM(cursor_token_fee) / 1000000.0 / 100.0 AS monthly_usage_usd,
  COUNT(*) AS events
FROM main.analyticsdbpublic.usageevent
WHERE owningTeam = 5764393
  AND timestamp >= '2025-09-15'
  AND timestamp < '2026-04-01'
GROUP BY DATE_TRUNC('month', timestamp)
ORDER BY usage_month;

-- 2. March 2026 on-demand usage calculation
WITH monthly_usage AS (
  SELECT
    DATE_TRUNC('month', timestamp) AS usage_month,
    SUM(cursor_token_fee) / 1000000.0 / 100.0 AS monthly_usage_usd
  FROM main.analyticsdbpublic.usageevent
  WHERE owningTeam = 5764393
    AND timestamp >= '2025-09-15'
    AND timestamp < '2026-04-01'
  GROUP BY DATE_TRUNC('month', timestamp)
),
cumulative AS (
  SELECT
    usage_month,
    monthly_usage_usd,
    SUM(monthly_usage_usd) OVER (ORDER BY usage_month) AS cumulative_usage_usd
  FROM monthly_usage
)
SELECT
  usage_month,
  monthly_usage_usd,
  cumulative_usage_usd,
  56640.00 AS committed_usage_usd,
  GREATEST(0, cumulative_usage_usd - 56640.00) AS on_demand_usd
FROM cumulative
ORDER BY usage_month;

-- Results as of 2026-03-30:
-- Pre-March cumulative usage: ~$35,800.71
-- March 2026 MTD usage: ~$22,257.68
-- Total cumulative: ~$58,058.39
-- On-demand this month: ~$1,418 ($58,058.39 - $56,640 committed)
