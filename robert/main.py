from data_loader import read_csv_to_immutable_list
from engine import ExecutionEngine
from reporting import ReportGeneration


if __name__ == "__main__":
    price_history = read_csv_to_immutable_list('csv_file_name')
    strat_names = ['MovingAverageStrategy']
    windows ={'MovingAverageStrategy' : 5}
    test1 = ExecutionEngine(100000, strat_names, price_history, windows)
    test1.execute_strategies()
    equity_curve = test1._equity_curve
    print(equity_curve)
    report = ReportGeneration(equity_curve)
    report.generate_report()

    # strat_names = ['MovingAverageStrategy', 'MovingAverageCrossoverStrategy']
    # windows ={'MovingAverageStrategy' : 5, 'MovingAverageCrossoverStrategy' : [10, 30]}
    
    
