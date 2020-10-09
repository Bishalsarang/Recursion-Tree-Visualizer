from visualiser.visualiser import Visualiser as vs

"""
    Given an array of numbers, find all the subsets:
    eg: nums = [1, 2, 3]
    Output:
        [[], [1], [2], [2, 1], [3], [3, 1], [3, 2], [3, 2 , 1]]
    You can find my explanation here: https://qr.ae/TWHmsi 
"""

subsets = []


@vs(ignore_args=["nums"], show_return_value=False, show_argument_name=False)
def f(nums, i, current_subset):
    # If no more elements left
    if i == 0:
        subsets.append(current_subset)
        return
    # Exclude Current element
    f(nums=nums, i=i - 1, current_subset=current_subset)

    # Include current element
    f(nums=nums, i=i - 1, current_subset=current_subset + [nums[i - 1]])


if __name__ == "__main__":
    nums = [1, 2, 3]
    f(nums=nums, i=len(nums), current_subset=[])
    # Save recursion tree to a file
    vs.make_animation("subset.gif", delay=3)
