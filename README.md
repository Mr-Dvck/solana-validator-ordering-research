# Inside the Block: How Solana Validators Order Transactions

An empirical investigation into transaction sequencing, account write-lock contention, and scheduler divergence across Solana validator clients (**FireBAM**, **Rakurai**, **HarmonicAgave**, and **AgaveBam**).

**Author:** Tim BC (`Mr-Dvck`) — BC Research  
**Target:** Superteam Ukraine Research Bounty ($2,500 USDC)  
**Publication Date:** October 28, 2026 (Post-Alpenglow Upgrade)  
**Mainnet Live Verification:** 100% Reproducible via Docker / CLI  

---

## 1. Quick Start & One-Command Reproducibility

### Option A: Docker Compose (Recommended)
Reproduce the analysis matrix with zero local dependencies:
```bash
docker-compose up --build
```

### Option B: Local Python Execution
```bash
# Verification & Dry-run mode (Default, zero funds spent)
python order_analyzer.py --dry-run

# Re-scan live mainnet validators
python validator_scanner.py
python order_analyzer.py --recompute
```

---

## 2. Bounty Compliance Matrix

| Requirement | Implementation Details | Status |
| :--- | :--- | :--- |
| **Solana Mainnet-Beta** | All data sampled from live Mainnet-Beta slots (462,604,339 - 462,604,568). | ✅ Complete |
| **>= 6 Validators & >= 3 Clients** | 6 production validators across 3 architectures: **FireBAM** (v26.10.5), **Rakurai** (v4.3.2), **HarmonicAgave** (v4.3.2), **AgaveBam** (v4.3.2). | ✅ Complete |
| **Post-Alpenglow Upgrade** | All measurements conducted on October 28, 2026 (after the Oct 21 Alpenglow boundary). | ✅ Complete |
| **One-Command Reproducibility** | Full Dockerfile & `docker-compose.yml` included. | ✅ Complete |
| **Key Safety & Spend Cap** | Dry-run by default. Keys injected strictly via `SOLANA_PRIVATE_KEY` env var; hard spend cap enforced at `<= 0.05 SOL`. | ✅ Complete |
| **Raw Data & Verification** | Full, un-truncated 88-character base58 signatures provided in `analysis_results.json` for independent `getBlock` verification. | ✅ Complete |
| **"What Went Wrong" Section** | Documented in Section 9 of the whitepaper covering RPC 429 cascades, CPI wrapper fees, and scheduler non-determinism. | ✅ Complete |

---

## 3. Key Findings Summary

1. **Streaming Arrival Trumps Priority Fees**: Transactions cannot be sorted globally before execution because blocks are emitted continuously over a 400ms leader window.
2. **Account Write-Lock Contention Forces Serialization**: High-fee transactions contending for identical write locks (e.g. popular DEX pools) are held back by the scheduler, appearing in the 50%-75% block quartiles rather than index 0.
3. **FireBAM Deterministic Inception**: FireBAM validators enforce a deterministic consensus initialization anchor at index 0 (consistently `5,131 lamports` and `2,363 CUs`).
4. **Conclusion on "The Rule"**: Within standard TPU lanes, there is **no strict priority fee ordering rule**—multi-threaded banking stage execution introduces structural non-determinism. Guaranteed head-of-block sequencing only exists within atomic Jito bundles.

---

## 4. Full Research Whitepaper

Read the complete peer-review research paper:
📄 [INSIDE_THE_BLOCK_RESEARCH_REPORT.md](INSIDE_THE_BLOCK_RESEARCH_REPORT.md)

---

## 5. Raw Data Verification Commands

Anyone can verify our empirical dataset directly against Solana Mainnet RPC:
```bash
# Verify Slot 462604343 (FireBAM v26.10.5) Index 0 Deterministic Anchor
curl -X POST https://api.mainnet-beta.solana.com -H "Content-Type: application/json" -d '{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "getTransaction",
  "params": ["3VMRxfXXGXnLZiKrcFh5tPnmrLJrxaEMipwEfcXg3BEHaurezoDAd2PXhdJGPi7eeJqXR7YLtq9WLZrZmJYapzm4", {"encoding": "jsonParsed", "maxSupportedTransactionVersion": 0}]
}'
```

---
*Certified by BC Research.*
