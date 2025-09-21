import numpy as np
import pandas as pd
import matplotlib.pyplot as pl

class ReportGeneration:
    def __init__(self, equity_curve, periods_per_year=252, risk_free_rate=0.0):
        self._equity_curve = equity_curve
        self._periods_per_year = periods_per_year
        self._risk_free_rate = risk_free_rate

    def generate_report(self):
        # Turn into pandas dataframe for easier calculations
        df = pd.DataFrame(self._equity_curve, columns=["timestamp", "equity value"])
        #Calculate total return
        initial_equity_value = df["equity value"].iloc[0]
        final_equity_value = float(df["equity value"].iloc[-1])
        total_return = final_equity_value / initial_equity_value - 1.0

        # Calculate series of periodic returns
        df["periodic returns"] = df["equity value"].pct_change()

        # Calculate sharpe ratio

        sharpe_ratio_annual = self.sharpe_using_average_time_interval(df, risk_free_annual=0.0)

        # Calculate max drawdown
        running_peak = df["equity value"].cummax()
        drawdown = df["equity value"] / running_peak - 1.0   # series of values ≤ 0
        max_drawdown = float(drawdown.min())            # most negative number
        max_drawdown_pct = abs(max_drawdown)    # report as positive percent
        
        # plot PNG chart
        pl.figure(figsize=(8, 4))
        pl.plot(df["timestamp"], df["equity value"], label="Equity")
        pl.title("Equity Curve")
        pl.xlabel("Time")
        pl.ylabel("Equity Value")
        pl.legend()
        pl.tight_layout()
        img_path = "equity_curve.png"
        pl.savefig(img_path, dpi=150)
        pl.close()

        # Write Markdown file
        with open("performance.md", "w", encoding="utf-8") as f:
            f.write("# Performance Report\n\n")

            f.write("## Summary metrics\n\n")
            f.write("| Metric | Value |\n")
            f.write("|:--|--:|\n")
            f.write(f"| Total return | {total_return:.2%} |\n")
            f.write(f"| Sharpe ratio (annualized) | {(f'{sharpe_ratio_annual:.3f}')} |\n")
            f.write(f"| Max drawdown | {max_drawdown_pct:.2%} |\n")
            f.write(f"| Observations | {len(df)} |\n")
            f.write(f"| Start | {df['timestamp'].iloc[0]} |\n")
            f.write(f"| End | {df['timestamp'].iloc[-1]} |\n")

            f.write("\n## Equity curve (Embedded PNG)\n\n")
            f.write(f"![Equity Curve]({img_path})\n")

        print('Performance report is available in performance.md.')

    def sharpe_using_average_time_interval(self, df, risk_free_annual=0.0):
        timestamp = pd.to_datetime(df["timestamp"])
        equity_value = df["equity value"] 
        rets = equity_value.pct_change().dropna()

        elapsed_micro_s = (timestamp.iloc[-1] - timestamp.iloc[0]).value / 1000  # nanoseconds to microseconds
        micro_s_per_year = 251 * 24 * 60 * 60 * 1e6  # trading-year in microseconds

        steps_per_year = micro_s_per_year / (elapsed_micro_s / len(rets))
        annual_vol = rets.std() * np.sqrt(steps_per_year)
        annual_returns = (equity_value.iloc[-1] / equity_value.iloc[0]) ** (micro_s_per_year / elapsed_micro_s) - 1

        return (annual_returns - risk_free_annual) / annual_vol

