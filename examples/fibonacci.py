# Author: Bishal Sarang

# Import Visualiser class from module visualiser
from visualiser import Visualiser as vs

# Add decorator
# Decorator accepts arguments: ignore_args and show_argument_name
@vs(ignore_args=['node_num'])
def fib(n, node_num):
    if n <= 1:
        return n
    vs.node_count += 1
    left = fib(n=n - 1, node_num=vs.node_count)

    vs.node_count += 1
    right = fib(n=n - 2, node_num=vs.node_count)
    return left + right

# Call function
print(fib(n=6, node_num=0))

# Save recursion tree to a file
vs.write_image("fibonacci.png")