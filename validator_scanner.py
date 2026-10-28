import urllib.request
import json
import time

RPC_URL = "https://api.mainnet-beta.solana.com"

def rpc_call(method, params=[]):
    req = urllib.request.Request(RPC_URL, data=json.dumps({
        "jsonrpc": "2.0",
        "id": 1,
        "method": method,
        "params": params
    }).encode("utf-8"), headers={"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=10) as resp:
        return json.loads(resp.read().decode("utf-8")).get("result")

def find_target_validators():
    print("Fetching cluster nodes...")
    nodes = rpc_call("getClusterNodes")
    node_map = {n.get("pubkey"): n for n in nodes if n.get("pubkey")}
    
    print(f"Total cluster nodes indexed: {len(node_map)}")

    # Get recent finalized slot
    latest_slot = rpc_call("getSlot", [{"commitment": "finalized"}])
    print(f"Latest finalized slot: {latest_slot}")

    # Scan the last 300 blocks to identify block-producing validators
    print("Scanning recent blocks to map validators to their produced slots...")
    observed_producers = {}
    
    # We step backwards in blocks
    slot_cursor = latest_slot - 10
    scan_count = 0
    max_scan = 80
    
    while scan_count < max_scan and slot_cursor > latest_slot - 200:
        try:
            block = rpc_call("getBlock", [slot_cursor, {
                "encoding": "json",
                "transactionDetails": "signatures",
                "rewards": True,
                "maxSupportedTransactionVersion": 0
            }])
            if block:
                producer = None
                for r in block.get("rewards", []):
                    if r.get("rewardType") == "Fee":
                        producer = r.get("pubkey")
                        break
                if producer:
                    node_info = node_map.get(producer)
                    version = node_info.get("version", "unknown") if node_info else "unknown"
                    client_id = node_info.get("clientId", "unknown") if node_info else "unknown"
                    sigs = len(block.get("signatures", []))
                    
                    if producer not in observed_producers:
                        observed_producers[producer] = {
                            "pubkey": producer,
                            "version": version,
                            "clientId": client_id,
                            "slots": [],
                            "tx_counts": []
                        }
                    observed_producers[producer]["slots"].append(slot_cursor)
                    observed_producers[producer]["tx_counts"].append(sigs)
            scan_count += 1
            slot_cursor -= 1
        except Exception as e:
            slot_cursor -= 1
            time.sleep(0.1)

    print(f"\nScan completed! Identified {len(observed_producers)} active block-producing validators.")
    
    # Group by version
    by_version = {}
    for p, info in observed_producers.items():
        v = info["version"]
        by_version.setdefault(v, []).append(info)

    print("\nValidator breakdown by software version:")
    for v, val_list in by_version.items():
        print(f"--- Version {v} ({len(val_list)} active block producers) ---")
        for val in val_list[:3]:
            print(f"  * {val['pubkey']} (Client: {val['clientId']}) - Slots produced: {val['slots']}")

    # Save mapping to file
    with open("C:/Users/ovjup/Desktop/Code Bounties/solana-validator-ordering-research/observed_validators.json", "w", encoding="utf-8") as f:
        json.dump(observed_producers, f, indent=2)

    return observed_producers

if __name__ == "__main__":
    find_target_validators()
