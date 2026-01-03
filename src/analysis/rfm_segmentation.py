import polars as pl
from datetime import datetime


def calculate_rfm(transactions_path):
    """Calculate RFM scores for each customer"""

    # Load transactions
    df = pl.read_csv(transactions_path)

    # Convert date column
    df = df.with_columns(pl.col('transaction_date').str.to_date())

    # Reference date (today)
    reference_date = df['transaction_date'].max()

    # Calculate RFM metrics
    rfm = df.group_by('customer_id').agg([
        ((reference_date - pl.col('transaction_date').max()).dt.total_days()).alias('recency'),
        pl.len().alias('frequency'),
        pl.col('total_amount').sum().alias('monetary')
    ])

    # Create quintile-based scores (1-5)
    rfm = rfm.with_columns([
        pl.col('recency').qcut(5, labels=None).rank().alias('R_score'),
        pl.col('frequency').qcut(5, labels=None).rank().alias('F_score'),
        pl.col('monetary').qcut(5, labels=None).rank().alias('M_score')
    ])

    # Total RFM score
    rfm = rfm.with_columns(
        (pl.col('R_score') + pl.col('F_score') + pl.col('M_score')).alias('RFM_score')
    )

    print(f"✅ RFM calculated for {len(rfm)} customers")
    return rfm


# Test it
if __name__ == "__main__":
    rfm_data = calculate_rfm('data/raw/transactions.csv')
    print(rfm_data.head(10))
    rfm_data.write_csv('data/processed/rfm_scores.csv')