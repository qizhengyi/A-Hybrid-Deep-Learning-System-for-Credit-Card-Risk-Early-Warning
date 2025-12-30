CREATE OR REPLACE VIEW v_features AS
SELECT
  -- identifiers: dataset has no customer_id, so we create a surrogate id
  row_number() over () AS customer_id,

  LIMIT_BAL,
  SEX,
  EDUCATION,
  MARRIAGE,
  AGE,

  -- delinquency features
  (PAY_0 > 0)::INT  AS delinquent_m1,
  (PAY_2 > 0)::INT  AS delinquent_m2,
  (PAY_3 > 0)::INT  AS delinquent_m3,
  (PAY_4 > 0)::INT  AS delinquent_m4,
  (PAY_5 > 0)::INT  AS delinquent_m5,
  (PAY_6 > 0)::INT  AS delinquent_m6,
  ((PAY_0 > 0)::INT + (PAY_2 > 0)::INT + (PAY_3 > 0)::INT + (PAY_4 > 0)::INT + (PAY_5 > 0)::INT + (PAY_6 > 0)::INT) AS delinquent_cnt_6m,
  GREATEST(PAY_0, PAY_2, PAY_3, PAY_4, PAY_5, PAY_6) AS max_dpd_bucket_6m,

  -- utilization
  BILL_AMT1 * 1.0 / NULLIF(LIMIT_BAL, 0) AS util_m1,
  BILL_AMT2 * 1.0 / NULLIF(LIMIT_BAL, 0) AS util_m2,
  BILL_AMT3 * 1.0 / NULLIF(LIMIT_BAL, 0) AS util_m3,

  -- payment ratio
  PAY_AMT1 * 1.0 / NULLIF(BILL_AMT1, 0) AS pay_ratio_m1,
  PAY_AMT2 * 1.0 / NULLIF(BILL_AMT2, 0) AS pay_ratio_m2,
  PAY_AMT3 * 1.0 / NULLIF(BILL_AMT3, 0) AS pay_ratio_m3,

  -- bill/payment trends (simple deltas)
  (BILL_AMT1 - BILL_AMT2) AS bill_delta_1,
  (BILL_AMT2 - BILL_AMT3) AS bill_delta_2,
  (PAY_AMT1  - PAY_AMT2)  AS pay_delta_1,
  (PAY_AMT2  - PAY_AMT3)  AS pay_delta_2,

  -- raw amounts (keep some)
  BILL_AMT1, BILL_AMT2, BILL_AMT3,
  PAY_AMT1,  PAY_AMT2,  PAY_AMT3,

  LABEL AS label
FROM credit_card_raw;
