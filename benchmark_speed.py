import time
from universe.universe_loader import get_index_universe
import pandas as pd
import yfinance as yf
from strategy.signal_engine import generate_signal
from concurrent.futures import ThreadPoolExecutor, as_completed

def analyze_ticker(ticker):
    try:
        data = yf.download(
            ticker,
            period="2y",
            auto_adjust=True,
            progress=False
        )
        if data.empty:
            return None
        signal_data = generate_signal(data)
        if signal_data is None:
            return None
        return {"ticker": ticker, "final_score": signal_data["final_score"]}
    except:
        return None

def benchmark_sequential(tickers):
    start_time = time.time()
    results = []
    for ticker in tickers:
        res = analyze_ticker(ticker)
        if res:
            results.append(res)
    end_time = time.time()
    return end_time - start_time, len(results)

def benchmark_parallel(tickers, max_workers=10):
    start_time = time.time()
    results = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_ticker = {executor.submit(analyze_ticker, ticker): ticker for ticker in tickers}
        for future in as_completed(future_to_ticker):
            res = future.result()
            if res:
                results.append(res)
    end_time = time.time()
    return end_time - start_time, len(results)

if __name__ == "__main__":
    # Test with a small subset to avoid long wait
    tickers = get_index_universe("Dow Jones")[:10]
    # Filter out empty strings
    tickers = [t for t in tickers if t and t.strip()]

    print(f"Benchmarking sequential analysis for {len(tickers)} tickers...")
    duration_seq, count_seq = benchmark_sequential(tickers)
    print(f"Sequential took {duration_seq:.2f} seconds for {count_seq} results.")

    print(f"Benchmarking parallel analysis (10 workers) for {len(tickers)} tickers...")
    duration_par, count_par = benchmark_parallel(tickers, 10)
    print(f"Parallel took {duration_par:.2f} seconds for {count_par} results.")

    if duration_seq > 0:
        improvement = (duration_seq - duration_par) / duration_seq * 100
        print(f"Improvement: {improvement:.2f}%")
