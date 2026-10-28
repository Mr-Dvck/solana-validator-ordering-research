# Superteam Earn Submission Brief

**Listing**: [Inside the Block: How Solana Validators Order Transactions](https://earn.superteam.fun/listings/bounties/inside-the-block-how-solana-validators-order-transactions)  
**Sponsor**: Superteam Ukraine  
**Prize Pool**: **$2,500 USDC** ($1,200 1st / $800 2nd / $500 3rd)  
**Submission Title**: *Inside the Block: How Solana Validators Order Transactions (Empirical Multi-Client Mainnet Analysis)*  
**Author**: Tim BC (`Mr-Dvck`) — BC Research  
**Payout Address**: `0x0190C582b0eF8a4D27aaDbf73FEFc1f389bd1f5C` / Solana: `Mr-Dvck`  

---

### Deliverables Included:
1. **Full Research Report**: [`INSIDE_THE_BLOCK_RESEARCH_REPORT.md`](file:///C:/Users/ovjup/Desktop/Code%20Bounties/solana-validator-ordering-research/INSIDE_THE_BLOCK_RESEARCH_REPORT.md)
   - Architectural breakdown of the TPU, SWQoS, Banking Stage, Unified Scheduler, and PoH Recorder.
   - Empirical mainnet analysis across **6 active validators** and **3 distinct client software versions**:
     - **FireBAM (`v26.10.5`)** (Firedancer AVX-512 hybrid)
     - **Rakurai (`v4.3.2`)** (Low-latency custom Jito fork)
     - **HarmonicAgave (`v4.3.2`)** (Harmonic institutional Agave client)
     - **AgaveBam (`v4.3.2`)** (Standard Agave Jito architecture)
   - Quantile ordering matrix demonstrating why priority fees do not sort blocks monotonically due to streaming arrival time and write-lock account contention.
2. **Empirical Dataset**: [`analysis_results.json`](file:///C:/Users/ovjup/Desktop/Code%20Bounties/solana-validator-ordering-research/analysis_results.json)
3. **Data Collection & Analysis Code**:
   - [`validator_scanner.py`](file:///C:/Users/ovjup/Desktop/Code%20Bounties/solana-validator-ordering-research/validator_scanner.py)
   - [`order_analyzer.py`](file:///C:/Users/ovjup/Desktop/Code%20Bounties/solana-validator-ordering-research/order_analyzer.py)
