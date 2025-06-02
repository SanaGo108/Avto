from calculator import calculate_collateral

def test_calculate_collateral():
    prices = [1000000, 1500000, 2000000]
    average_price, collateral_value = calculate_collateral(prices)
    assert average_price == 1500000
    assert collateral_value == 1200000
