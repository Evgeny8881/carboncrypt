#!/usr/bin/env python3

import os
import requests
import argparse
from tabulate import tabulate
from dotenv import load_dotenv

# Configuration per chain: API endpoint, env var for API key, average energy per tx (kWh)
CHAIN_CONFIG = {
    'ethereum': {
        'api_url': 'https://api.etherscan.io/api',
        'api_key_env': 'ETHERSCAN_API_KEY',
        'energy_per_tx_kwh': 71.0
    },
    'bsc': {
        'api_url': 'https://api.bscscan.com/api',
        'api_key_env': 'BSCSCAN_API_KEY',
        'energy_per_tx_kwh': 0.00051
    },
    'polygon': {
        'api_url': 'https://api.polygonscan.com/api',
        'api_key_env': 'POLYGONSCAN_API_KEY',
        'energy_per_tx_kwh': 0.00004
    }
}


def get_tx_count(address: str, chain: str) -> int:
    """Fetch transaction count for an address on the given chain."""
    cfg = CHAIN_CONFIG[chain]
    api_key = os.getenv(cfg['api_key_env'])
    if not api_key:
        raise ValueError(f"API key for {chain} not found. Set env var {cfg['api_key_env']}")
    params = {
        'module': 'account',
        'action': 'txlist',
        'address': address,
        'startblock': 0,
        'endblock': 99999999,
        'sort': 'asc',
        'apikey': api_key
    }
    resp = requests.get(cfg['api_url'], params=params)
    data = resp.json()
    if data.get('status') != '1':
        return 0
    return len(data.get('result', []))


def estimate_carbon(address: str, chain: str):
    """Estimate carbon footprint (kWh) given tx count and per-tx factor."""
    tx_count = get_tx_count(address, chain)
    energy = tx_count * CHAIN_CONFIG[chain]['energy_per_tx_kwh']
    return tx_count, energy


def main():
    load_dotenv()
    parser = argparse.ArgumentParser(
        description='Estimate carbon footprint of on-chain transactions.'
    )
    parser.add_argument(
        'address', help='Wallet address to analyze'
    )
    parser.add_argument(
        '-c', '--chains', nargs='+', choices=CHAIN_CONFIG.keys(),
        default=list(CHAIN_CONFIG.keys()),
        help='Blockchains to include in the analysis'
    )
    args = parser.parse_args()

    table = []
    for chain in args.chains:
        try:
            tx_count, energy = estimate_carbon(args.address, chain)
            table.append([chain, tx_count, f"{energy:.2f} kWh"])
        except Exception as e:
            table.append([chain, 'Error', str(e)])

    print(tabulate(table, headers=['Chain', 'TX Count', 'Energy (kWh)']))


if __name__ == '__main__':
    main()
