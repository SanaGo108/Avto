import statistics

def calculate_collateral(prices):
    if not prices:
        logging.warning("No prices available for calculation.")
        return 0, 0  # Возвращаем 0, если цен нет

    average_price = statistics.mean(prices)
    collateral_value = average_price * 0.8
    return average_price, collateral_value
