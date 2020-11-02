nums = [3,5,1,2,9,4,12,6]

for x in range(0, len(nums)):
    minIndex = x

    for y in range(x, len(nums)):
        if nums[y] < nums[minIndex]:
            minIndex = y
    
    temp = nums[minIndex]
    nums[minIndex] = nums[x]
    nums[x] = temp

print(nums)
