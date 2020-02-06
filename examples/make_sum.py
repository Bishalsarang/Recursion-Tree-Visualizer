# Author: Bishal Sarang
from visualiser.visualiser import Visualiser as vs

"""
    Problemm Link: https://qr.ae/TltTCV
    Find all permutations of 2, 3, and 7 that can add up to make 10. (Ex: 2,2,2,2,2; or 3,7)
    Output:
        [2, 2, 2, 2, 2]
        [2, 2, 3, 3]
        [2, 3, 2, 3]
        [2, 3, 3, 2]
        [3, 2, 2, 3]
        [3, 2, 3, 2]
        [3, 3, 2, 2]
        [3, 7]
        [7, 3]
"""


@vs(ignore_args=['node_num'], show_argument_name=False, show_return_value=False)
def f(sum, ans):
    # If sum becoms 0 we have found the required list
    if sum == 0:
        print(ans)

    # Include every other element to make the sum
    # Number that is included also can be included
    for elem in nums:
        if sum - elem >= 0:
            f(sum=sum - elem, ans=ans + [elem])


# We want to make the sum from list nums
nums = [2, 3, 7]
sum = 10

# Call solve with sum and an empty list
f(sum=sum, ans=[])
vs.write_image("make_sum.png")