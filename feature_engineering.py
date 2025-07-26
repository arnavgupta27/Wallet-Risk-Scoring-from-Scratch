import pandas as pd
import numpy as np

def robust_divide(numerator, denominator):
    if pd.isna(denominator) or denominator == 0:
        return 0.0
    return numerator / denominator

def engineer_features(input_csv_path, output_csv_path):
    try:
        df = pd.read_csv(input_csv_path)
    except Exception as e:
        print(f"Error reading input CSV file: {e}")
        return

    features = pd.DataFrame()
    features['wallet_id'] = df['wallet_id']

    # 1. Total Supplied Value (USD)
    features['total_supplied_usd'] = df.get('v2_totalDepositUSD', 0).fillna(0)

    # 2. Total Borrowed Value (USD)
    features['total_borrowed_usd'] = df.get('v2_totalBorrowUSD', 0).fillna(0)

    # Additional useful totals for ratios
    features['total_withdrawn_usd'] = df.get('v2_totalWithdrawUSD', 0).fillna(0)
    features['total_repaid_usd'] = df.get('v2_totalRepayUSD', 0).fillna(0)

    # 3. Collateralization Ratio = total_supplied_usd / total_borrowed_usd (no div-by-zero)
    features['collateralization_ratio'] = [
        robust_divide(sup, bor) for sup, bor in zip(features['total_supplied_usd'], features['total_borrowed_usd'])
    ]

    # 4. Number of Entered Markets (unique asset markets engaged)
    features['number_markets_used'] = df.get('v2_uniqueMarketsCount', 0).fillna(0).astype(int)

    # Dropped largest_single_deposit_usd and largest_single_borrow_usd (no per-event data)

    # 5. Number of Borrow Events
    features['num_borrow_events'] = df.get('v2_borrows_count', 0).fillna(0).astype(int)

    # 6. Number of Supply Events (deposit count proxy)
    features['num_deposit_events'] = df.get('v2_deposits_count', 0).fillna(0).astype(int)

    # 7. Average Borrow Amount per Event USD
    features['avg_borrow_amount_usd'] = [
        robust_divide(borrowed, count) for borrowed, count in 
        zip(features['total_borrowed_usd'], features['num_borrow_events'])
    ]

    # 8. Average Deposit Amount per Event USD
    features['avg_deposit_amount_usd'] = [
        robust_divide(supplied, count) for supplied, count in 
        zip(features['total_supplied_usd'], features['num_deposit_events'])
    ]

    # 9. Repayment Rate = total repaid USD / total borrowed USD (filled with 0)
    features['repayment_rate'] = [
        robust_divide(repaid, borrowed) for repaid, borrowed in 
        zip(features['total_repaid_usd'], features['total_borrowed_usd'])
    ]

    # 10. Number of Liquidations Suffered
    features['liquidations_suffered'] = df.get('v2_liquidationCount', 0).fillna(0).astype(int)

    # 11. Number of Times Acting as Liquidator
    features['liquidations_as_liquidator'] = df.get('v2_liquidateCount', 0).fillna(0).astype(int)

    # 12. Has Been Liquidated Flag (binary)
    features['has_been_liquidated'] = (features['liquidations_suffered'] > 0).astype(int)

    # 13. Total Number of Protocol Transactions (sum of supply, withdraw, borrow, repay counts)
    tx_counts = (
        df.get('v2_depositCount', 0).fillna(0)
        + df.get('v2_withdrawCount', 0).fillna(0)
        + df.get('v2_borrowCount', 0).fillna(0)
        + df.get('v2_repayCount', 0).fillna(0)
    )
    features['total_protocol_tx'] = tx_counts.astype(int)

    # 14. Lifetime Interest Accrued Approximation = max(borrowed - repaid, 0)
    features['lifetime_interest_accrued'] = [
        max(borrowed - repaid, 0) for borrowed, repaid in 
        zip(features['total_borrowed_usd'], features['total_repaid_usd'])
    ]

    # Dropped:
    # deposit_volatility_usd, borrow_volatility_usd - per-event amounts unavailable in current CSV
    # last_activity_days_ago, first_activity_days_ago - lacking timestamps in current CSV
    # min_collateralization_ratio - needs time-series or oracle pricing, unavailable

    # Additional feature: 
    # Withdraw to Supply ratio (risk flag if close to 1)
    features['withdraw_to_supply_ratio'] = [
        robust_divide(wd, sup) for wd, sup in zip(features['total_withdrawn_usd'], features['total_supplied_usd'])
    ]
    features['high_withdraw_flag'] = (features['withdraw_to_supply_ratio'] > 0.9).astype(int)

    # Final cleanup: fill remaining NaNs (should be none now)
    features.fillna(0, inplace=True)

    try:
        features.to_csv(output_csv_path, index=False)
        print(f"Engineered features successfully saved to {output_csv_path}")
    except Exception as e:
        print(f"Failed to save engineered features: {e}")

if __name__ == "__main__":
    engineer_features("compound_wallets_raw_data.csv", "engineered_feature_data.csv")
