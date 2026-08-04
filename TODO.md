# TODO

- [ ] Try to understand IPO dates why 06-02
- [ ] Circuit Breaker for your Buy Engine (Price drops >50% FORBIDEN TO BUY)
- [ ] generate HTML
- [ ] push on github
- [ ] plot crypto like etf
- [ ] refine crypto invest
- [ ] adapt etf invest (maybe 45% xtrackers is too much?)
- [ ] entry-point signal in conviction score — the score ranks conviction (own it?)
      but not timing (buy now?). A ~30% drop (e.g. ALNY) barely moves CONV because
      falling price only lifts VAL. `portfolio/signals.py` HAS an entry engine
      (dynamic buy target from 50/200-SMA + RSI + drawdown → BUY NOW/DIP/WAIT via
      `evaluate_buy`) but it runs on the OLD sector `ASSET_META` (24 names, ALNY not
      in it), not the AI book. Fix: add a deterministic `[DIP]`/`[ENTRY]` flag to
      `score_holdings.py` computed from CSV columns already present
      (`pct_above_200dma`, `pct_below_52w_high`) — flag when a high-CONV name sits
      well below its 200DMA. Snapshot-driven = reproducible, no live yfinance fetch
      (feed is date-corrupted here). Ties into the existing Circuit Breaker TODO
      (>50% drop = FORBIDDEN to buy) as the buy-side counterpart.
