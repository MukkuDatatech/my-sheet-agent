import google.ads.google_ads.client
import pandas as pd
from datetime import datetime, timedelta

# Authentication
def initialize_client():
    client = google.ads.google_ads.client.GoogleAdsClient.load_from_storage('path/to/google-ads.yaml')
    return client

# Fetch campaign metrics
def fetch_campaign_metrics(client, customer_id):
    query = """
    SELECT campaign.id, campaign.name, metrics.impressions, metrics.clicks, metrics.cost_micros
    FROM campaign
    WHERE segments.date DURING LAST_30_DAYS
    """
    response = client.service.google_ads.search(customer_id=customer_id, query=query)
    return response

# Parsing metrics
def parse_metrics(response):
    metrics_list = []
    for row in response:
        campaign = row.campaign
        metrics = row.metrics
        metrics_list.append({
            "Campaign ID": campaign.id,
            "Campaign Name": campaign.name,
            "Impressions": metrics.impressions,
            "Clicks": metrics.clicks,
            "Cost (USD)": metrics.cost_micros / 1_000_000
        })
    return pd.DataFrame(metrics_list)

# Generating daily summaries
def generate_daily_summaries(metrics_df):
    summary = metrics_df.groupby('Campaign Name').agg(
        Total_Clicks=('Clicks', 'sum'),
        Total_Impressions=('Impressions', 'sum'),
        Total_Cost=('Cost (USD)', 'sum')
    ).reset_index()
    return summary

if __name__ == "__main__":
    client = initialize_client()
    customer_id = 'INSERT_CUSTOMER_ID_HERE'
    response = fetch_campaign_metrics(client, customer_id)
    metrics_df = parse_metrics(response)
    daily_summary = generate_daily_summaries(metrics_df)
    print(daily_summary)