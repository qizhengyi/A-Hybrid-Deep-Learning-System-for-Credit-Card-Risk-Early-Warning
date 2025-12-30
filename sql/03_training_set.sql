CREATE OR REPLACE TABLE training_set AS
SELECT
  customer_id,
  -- features
  LIMIT_BAL, SEX, EDUCATION, MARRIAGE, AGE,
  delinquent_m1, delinquent_m2, delinquent_m3, delinquent_m4, delinquent_m5, delinquent_m6,
  delinquent_cnt_6m, max_dpd_bucket_6m,
  util_m1, util_m2, util_m3,
  pay_ratio_m1, pay_ratio_m2, pay_ratio_m3,
  bill_delta_1, bill_delta_2, pay_delta_1, pay_delta_2,
  BILL_AMT1, BILL_AMT2, BILL_AMT3,
  PAY_AMT1, PAY_AMT2, PAY_AMT3,
  label
FROM v_features;
