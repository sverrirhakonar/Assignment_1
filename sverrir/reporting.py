
import statistics
import math

def calculate_total_return(equity_curve):
    start_value = equity_curve[0]
    end_value = equity_curve[-1]
    return end_value / start_value -1


def calculate_periodic_return(equity_curve):
    periodic_returns = []
    for i in range(1, len(equity_curve)):
        if equity_curve[i-1] == 0:
            p_return = 0
        else:
            p_return = equity_curve[i] / equity_curve[i-1] -1
        periodic_returns.append(p_return)
    return periodic_returns

def calculate_sharpe_ratio(periodic_rerturns):
    average_return = statistics.mean(periodic_rerturns)
    standard_deviation = statistics.stdev(periodic_rerturns)
    if standard_deviation == 0:
        return 0.0
    else:
        simplified_sharpe = average_return / standard_deviation
        sharpe = simplified_sharpe * math.sqrt(252)
        return sharpe

def calculate_max_drawdown(equity_curve):
    peak = equity_curve[0]
    max_drawdown = 0
    for value in equity_curve:
        if value > peak:
            peak = value
        if peak != 0:
            drawdown = (peak - value) / peak
            if drawdown > max_drawdown:
                max_drawdown = drawdown
    return max_drawdown
        
