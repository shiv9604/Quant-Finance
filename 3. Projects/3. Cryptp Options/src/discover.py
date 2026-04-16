"""Run once to find the correct BTC perpetual/spot symbol on your environment."""

import os

from dotenv import load_dotenv

load_dotenv()

from src.execution.broker import DeltaBroker

broker = DeltaBroker(
    api_key=os.getenv("DELTA_API_KEY", ""),
    api_secret=os.getenv("DELTA_API_SECRET", ""),
    base_url=os.getenv("DELTA_BASE_URL", "https://cdn-ind.testnet.deltaex.org"),
)

products = broker.list_products("BTC")
print(f"Found {len(products)} BTC products:\n")
for p in products:
    print(f"  symbol={p.get('symbol'):<30}  type={p.get('contract_type')}")
