# Author: Bishal Sarang
from visualiser.visualiser import  Visualiser as vs

"""
    Number of ways to make change:
"""
@vs(ignore_args=["coins"], show_argument_name=False)
def f(coins, amount, n):
    if amount == 0:
        return 1

    if amount < 0:
        return 0

    if n <= 0 and amount >= 1:
        return 0

    include = f(coins=coins, amount=amount - coins[n - 1], n=n)
    exclude = f(coins=coins, amount=amount, n=n-1)

    return include + exclude

def main():
    amount = 5
    coins = [1, 2, 5]
    print(f(coins=coins, amount=amount, n=len(coins)))
    vs.make_animation("coin_change.gif", delay=3)

if __name__ == "__main__":
    main()