# Author: Bishal Sarang

# Import Visualiser class from module visualiser
from visualiser.visualiser import Visualiser as vs

"""
    Given an array of numbers, find all the subsets:
    eg: nums = [1, 2, 3]
    Output:
        [[], [1], [2], [2, 1], [3], [3, 1], [3, 2], [3, 2 , 1]]
    You can find my explanation here: https://qr.ae/TWHmsi 
"""

subsets = []
@vs(ignore_args=["node_num", "nums"], show_return_value=False, show_argument_name=False)
def f(nums, i, current_subset, node_num):
    # If no more elements left
    if i == 0:
        subsets.append(current_subset)
        return
    # Exclude Current element
    vs.node_count += 1
    f(nums=nums, i=i - 1, current_subset=current_subset, node_num=vs.node_count)

    # Include current element
    vs.node_count += 1
    f(nums=nums, i=i - 1, current_subset=current_subset + [nums[i - 1]], node_num=vs.node_count)

if __name__ == "__main__":
    nums = [1, 2, 3]
    f(nums=nums, i = len(nums), current_subset=[], node_num=0)
    vs.write_image("subset.png")