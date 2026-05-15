
WITH base AS (
  SELECT DATE_TRUNC('month', timestamp) AS month_start, owninguser, model_name,
    SUM(input_tokens) AS input_tokens, SUM(output_tokens) AS output_tokens,
    SUM(cache_write_tokens) AS cache_write_tokens, SUM(cache_read_tokens) AS cache_read_tokens
  FROM main.dbt.stg_usage_events_tokens_per_model
  WHERE owningteam = 9109857 AND timestamp >= DATE_TRUNC('month', CURRENT_DATE()) - INTERVAL 3 MONTH
  GROUP BY 1,2,3
),
with_tokens AS (
  SELECT *, input_tokens + output_tokens + cache_write_tokens + cache_read_tokens AS total_tokens FROM base
),
scenario_models AS (
  SELECT *, model_name AS sq_model,
    CASE WHEN model_name IN ('default') THEN 'default'
      WHEN model_name IN ('composer-2','composer-1','composer-1.5') OR model_name LIKE 'composer%' THEN '4-6-sonnet'
      WHEN model_name LIKE '%sonnet%' OR model_name IN ('3-7-sonnet','4-sonnet') THEN '4-6-sonnet'
      WHEN model_name LIKE '%opus%' THEN '4-7-opus'
      WHEN model_name LIKE 'gpt-5.5%' OR model_name LIKE 'gpt-5.3-codex%' OR model_name LIKE 'gpt-5.3-codex-fast%'
        OR model_name LIKE 'gpt-5.2-codex%' OR model_name LIKE 'gpt-5.4%' OR model_name LIKE 'gpt-5.4-mini%'
        OR model_name LIKE 'gpt-5.2%' OR model_name LIKE 'gpt-5.1%' OR model_name LIKE 'gpt-5-mini%'
        OR model_name = 'gpt-5' THEN '4-7-opus'
      WHEN model_name LIKE 'gemini%' OR model_name LIKE 'kimi%' OR model_name LIKE 'grok%' THEN '4-6-sonnet'
      WHEN model_name = 'agent_review' THEN '4-6-sonnet' ELSE '4-6-sonnet' END AS ant_model,
    CASE WHEN model_name IN ('default') THEN 'default'
      WHEN model_name LIKE '%opus%' THEN 'gpt-5.5'
      WHEN model_name LIKE '%sonnet%' OR model_name IN ('3-7-sonnet','4-sonnet') THEN 'composer-2'
      WHEN model_name IN ('composer-2','composer-1','composer-1.5') OR model_name LIKE 'composer%' THEN 'composer-2'
      WHEN model_name LIKE 'gpt-5.5%' THEN 'gpt-5.5'
      WHEN model_name LIKE 'gpt-5.3-codex%' OR model_name LIKE 'gpt-5.3-codex-fast%' THEN 'gpt-5.3-codex'
      WHEN model_name LIKE 'gpt-5.2-codex%' THEN 'gpt-5.2-codex'
      WHEN model_name LIKE 'gpt-5.4-mini%' THEN 'gpt-5.4-mini'
      WHEN model_name LIKE 'gpt-5.4%' THEN 'gpt-5.4'
      WHEN model_name LIKE 'gpt-5.2%' THEN 'gpt-5.2'
      WHEN model_name LIKE 'gpt-5.1-codex-max%' THEN 'gpt-5.1-codex-max'
      WHEN model_name LIKE 'gpt-5.1-codex-mini%' THEN 'gpt-5.1-codex-mini'
      WHEN model_name LIKE 'gpt-5.1%' THEN 'gpt-5.1'
      WHEN model_name LIKE 'gpt-5-mini%' THEN 'gpt-5-mini'
      WHEN model_name = 'gpt-5' THEN 'gpt-5'
      WHEN model_name LIKE 'gemini-3-flash%' OR model_name LIKE 'gemini-2-5-flash%'
        OR model_name LIKE 'kimi%' OR model_name LIKE 'grok%' THEN 'composer-2'
      WHEN model_name LIKE 'gemini%' THEN 'gpt-5.5'
      WHEN model_name = 'agent_review' THEN 'composer-2' ELSE 'composer-2' END AS opt_model
  FROM with_tokens
),
price AS (
  SELECT *,
    CASE sq_model WHEN 'default' THEN (input_tokens + cache_write_tokens) * 1.25e-6 + cache_read_tokens * 0.25e-6 + output_tokens * 6.0e-6
      WHEN 'composer-2' THEN input_tokens * 0.5e-6 + cache_read_tokens * 0.2e-6 + output_tokens * 2.5e-6
      WHEN 'composer-1' THEN input_tokens * 1.25e-6 + cache_read_tokens * 0.125e-6 + output_tokens * 10.0e-6
      WHEN 'composer-1.5' THEN input_tokens * 3.5e-6 + cache_read_tokens * 0.35e-6 + output_tokens * 17.5e-6
      WHEN 'gpt-5.5' THEN input_tokens * 5.0e-6 + cache_read_tokens * 0.5e-6 + output_tokens * 30.0e-6
      WHEN 'gpt-5.4' THEN input_tokens * 2.5e-6 + cache_read_tokens * 0.25e-6 + output_tokens * 15.0e-6
      WHEN 'gpt-5.4-mini' THEN input_tokens * 0.75e-6 + cache_read_tokens * 0.075e-6 + output_tokens * 4.5e-6
      WHEN 'gpt-5.3-codex' THEN input_tokens * 1.75e-6 + cache_read_tokens * 0.175e-6 + output_tokens * 14.0e-6
      WHEN 'gpt-5.3-codex-fast' THEN input_tokens * 1.75e-6 + cache_read_tokens * 0.175e-6 + output_tokens * 14.0e-6
      WHEN 'gpt-5.2-codex' THEN input_tokens * 1.75e-6 + cache_read_tokens * 0.175e-6 + output_tokens * 14.0e-6
      WHEN 'gpt-5.2' THEN input_tokens * 1.75e-6 + cache_read_tokens * 0.175e-6 + output_tokens * 14.0e-6
      WHEN 'gpt-5.1-codex-max' THEN input_tokens * 1.25e-6 + cache_read_tokens * 0.125e-6 + output_tokens * 10.0e-6
      WHEN 'gpt-5.1-codex-mini' THEN input_tokens * 0.25e-6 + cache_read_tokens * 0.025e-6 + output_tokens * 2.0e-6
      WHEN 'gpt-5-mini' THEN input_tokens * 0.25e-6 + cache_read_tokens * 0.025e-6 + output_tokens * 2.0e-6
      WHEN 'gpt-5' THEN input_tokens * 1.25e-6 + cache_read_tokens * 0.125e-6 + output_tokens * 10.0e-6
      WHEN 'gpt-5.1' THEN input_tokens * 1.25e-6 + cache_read_tokens * 0.125e-6 + output_tokens * 10.0e-6
      WHEN 'kimik2.5' THEN input_tokens * 0.6e-6 + cache_read_tokens * 0.1e-6 + output_tokens * 3.0e-6
      WHEN 'kimi-k2' THEN input_tokens * 0.6e-6 + cache_read_tokens * 0.1e-6 + output_tokens * 3.0e-6
      WHEN 'gemini-3-flash' THEN input_tokens * 0.5e-6 + cache_read_tokens * 0.05e-6 + output_tokens * 3.0e-6
      WHEN 'gemini-2-5-flash' THEN input_tokens * 0.3e-6 + cache_read_tokens * 0.03e-6 + output_tokens * 2.5e-6
      WHEN 'gemini-3-pro-preview' THEN input_tokens * 2.0e-6 + cache_read_tokens * 0.2e-6 + output_tokens * 12.0e-6
      WHEN 'gemini-3-1-pro-preview' THEN input_tokens * 2.0e-6 + cache_read_tokens * 0.2e-6 + output_tokens * 12.0e-6
      WHEN 'grok-code' THEN input_tokens * 1.25e-6 + cache_read_tokens * 0.2e-6 + output_tokens * 2.5e-6
      WHEN '4-5-haiku' THEN input_tokens * 1.0e-6 + cache_write_tokens * 1.25e-6 + cache_read_tokens * 0.1e-6 + output_tokens * 5.0e-6
      ELSE input_tokens * CASE WHEN sq_model LIKE '%opus%' THEN 5.0 WHEN sq_model LIKE '%haiku%' THEN 1.0 ELSE 3.0 END * 1e-6
        + cache_write_tokens * CASE WHEN sq_model LIKE '%opus%' THEN 6.25 WHEN sq_model LIKE '%haiku%' THEN 1.25 ELSE 3.75 END * 1e-6
        + cache_read_tokens * CASE WHEN sq_model LIKE '%opus%' THEN 0.5 WHEN sq_model LIKE '%haiku%' THEN 0.1 ELSE 0.3 END * 1e-6
        + output_tokens * CASE WHEN sq_model LIKE '%opus%' THEN 25.0 WHEN sq_model LIKE '%haiku%' THEN 5.0 ELSE 15.0 END * 1e-6
      END AS sq_api_cost,
    CASE WHEN sq_model IN ('default','composer-2','composer-1','composer-1.5') THEN 0 ELSE total_tokens * 0.25e-6 END AS sq_ctf_cost,
    CASE ant_model WHEN '4-6-sonnet' THEN input_tokens * 3.0e-6 + cache_write_tokens * 3.75e-6 + cache_read_tokens * 0.3e-6 + output_tokens * 15.0e-6
      WHEN '4-7-opus' THEN input_tokens * 5.0e-6 + cache_write_tokens * 6.25e-6 + cache_read_tokens * 0.5e-6 + output_tokens * 25.0e-6
      ELSE input_tokens * 3.0e-6 + cache_write_tokens * 3.75e-6 + cache_read_tokens * 0.3e-6 + output_tokens * 15.0e-6 END AS ant_api_cost,
    total_tokens * 0.25e-6 AS ant_ctf_cost,
    CASE opt_model WHEN 'default' THEN (input_tokens + cache_write_tokens) * 1.25e-6 + cache_read_tokens * 0.25e-6 + output_tokens * 6.0e-6
      WHEN 'composer-2' THEN input_tokens * 0.5e-6 + cache_read_tokens * 0.2e-6 + output_tokens * 2.5e-6
      WHEN 'gpt-5.5' THEN input_tokens * 5.0e-6 + cache_read_tokens * 0.5e-6 + output_tokens * 30.0e-6
      WHEN 'gpt-5.4' THEN input_tokens * 2.5e-6 + cache_read_tokens * 0.25e-6 + output_tokens * 15.0e-6
      WHEN 'gpt-5.4-mini' THEN input_tokens * 0.75e-6 + cache_read_tokens * 0.075e-6 + output_tokens * 4.5e-6
      WHEN 'gpt-5.3-codex' THEN input_tokens * 1.75e-6 + cache_read_tokens * 0.175e-6 + output_tokens * 14.0e-6
      WHEN 'gpt-5.3-codex-fast' THEN input_tokens * 1.75e-6 + cache_read_tokens * 0.175e-6 + output_tokens * 14.0e-6
      WHEN 'gpt-5.2-codex' THEN input_tokens * 1.75e-6 + cache_read_tokens * 0.175e-6 + output_tokens * 14.0e-6
      WHEN 'gpt-5.2' THEN input_tokens * 1.75e-6 + cache_read_tokens * 0.175e-6 + output_tokens * 14.0e-6
      WHEN 'gpt-5.1-codex-max' THEN input_tokens * 1.25e-6 + cache_read_tokens * 0.125e-6 + output_tokens * 10.0e-6
      WHEN 'gpt-5.1-codex-mini' THEN input_tokens * 0.25e-6 + cache_read_tokens * 0.025e-6 + output_tokens * 2.0e-6
      WHEN 'gpt-5-mini' THEN input_tokens * 0.25e-6 + cache_read_tokens * 0.025e-6 + output_tokens * 2.0e-6
      WHEN 'gpt-5' THEN input_tokens * 1.25e-6 + cache_read_tokens * 0.125e-6 + output_tokens * 10.0e-6
      WHEN 'gpt-5.1' THEN input_tokens * 1.25e-6 + cache_read_tokens * 0.125e-6 + output_tokens * 10.0e-6
      ELSE input_tokens * 0.5e-6 + cache_read_tokens * 0.2e-6 + output_tokens * 2.5e-6 END AS opt_api_cost,
    CASE WHEN opt_model IN ('default','composer-2') THEN 0 ELSE total_tokens * 0.25e-6 END AS opt_ctf_cost
  FROM scenario_models
),
user_month AS (
  SELECT month_start, owninguser,
    SUM(sq_api_cost + sq_ctf_cost) AS status_quo_cost,
    SUM(ant_api_cost + ant_ctf_cost) AS all_anthropic_cost,
    SUM(opt_api_cost + opt_ctf_cost) AS optimized_cost
  FROM price GROUP BY 1,2
)
SELECT um.month_start, um.owninguser, u.email,
  ROUND(um.status_quo_cost, 2) AS status_quo_cost,
  ROUND(um.all_anthropic_cost, 2) AS all_anthropic_cost,
  ROUND(um.optimized_cost, 2) AS optimized_cost
FROM user_month um
LEFT JOIN main.cln_maindb.user u ON u.id = um.owninguser
WHERE um.status_quo_cost > 0 OR um.all_anthropic_cost > 0 OR um.optimized_cost > 0
ORDER BY um.month_start, um.status_quo_cost DESC

