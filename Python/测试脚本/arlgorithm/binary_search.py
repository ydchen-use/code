

def binary_search(nums: list, num: int) -> int:
    """
    二分查找
    :param nums:
    :param num
    :return:
    """
    low = 0
    high = len(nums) - 1
    while low <= high:
        mid = (low + high) // 2
        if num == nums[mid]:
            return mid
        if num > nums[mid]:
            low = mid + 1
        else:
            high = mid - 1
    return -1

