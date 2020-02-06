# Author: Bishal Sarang

# Import Visualiser class from module visualiser
from visualiser.visualiser import Visualiser as vs

# Add decorator
# Decorator accepts arguments: ignore_args and show_argument_name
@vs()
def fib(n):
    if n <= 1:
        return n
    return fib(n=n - 1) + fib(n=n - 2)


def main():
    # Call function
    print(fib(n=6))
    # Save recursion tree to a file
    vs.write_image("fibonacci.png")


if __name__ == "__main__":
    main()