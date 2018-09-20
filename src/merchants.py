import collections          # namedtuple
import time
from typing import List     # List
from typing import Tuple    # Tuple
import sys  # argv is the 'argument vectors' on the command line.
import math

Merchant = collections.namedtuple('Merchant', ('name', 'location'))  # tuple

def read_people( filename: str ) -> List[ Merchant ]:
    """
    Read people from a file into a list of Merchant namedtuples.
    :param filename: The name of the file
    :return: A list of Person
    """
    people = list()
    with open(filename) as f:
        for line in f:
            fields = line.split()
            people.append(Merchant(
                name=str(fields[0]),
                location=int(fields[1])))
    return people

def _partition(data: List[Merchant], pivot: Merchant) \
      -> Tuple[List[Merchant], List[Merchant], List[Merchant]]:
    """
    Three way partition the data into smaller, equal and greater lists,
    in relationship to the pivot
    :param data: The data to be sorted (a list)
    :param pivot: The value to partition the data on
    :return: Three list: smaller, equal and greater
    """
    less, equal, greater = [], [], []
    for element in data:
        if element.location < pivot.location:
            less.append(element)
        elif element.location > pivot.location:
            greater.append(element)
        else:
            equal.append(element)
    return less, equal, greater

def quick_sort(lst: List[Merchant]) -> List[Merchant]:
    """
    Performs a quick sort and returns a newly sorted list
    :param lst: The data to be sorted (a list)
    :return: A sorted list
    """
    if len(lst) == 0:
        return []
    else:
        pivot = lst[0]
        less, equal, greater = _partition(lst, pivot)
        return quick_sort(less) + equal + quick_sort(greater)

def quick_select(lst, k):
    """
    Picks a median value from a list
    :param lst: The data (a list)
    :return: a median value (the pivot)
    """
    if len(lst) == 0:
        return []
    less, equal, greater = _partition(lst, lst[0])
    count = len(equal)
    m = len(less)
    if k >= m and k < m + count:
        return equal
    elif m > k:
        return quick_select(less, k)
    else:
        return quick_select(greater, k - m - count)

def main():
    """
    Deals with the timing that counts the start and end time.
    Checks from command line whether quick sort or quick select will be used.
    Calculates the sum of distance.
    Prints all the information.
    """
    start = time.clock()
    slow_or_fast = str(sys.argv[1])
    filename = str(sys.argv[2])
    lst = read_people(filename)
    sum = 0

    if slow_or_fast == "slow":
        slow_sort = quick_sort(lst)
        slow_median = len(slow_sort) // 2
        for i in lst:
            sum += abs(i[1] - slow_sort[slow_median].location)
    elif slow_or_fast == "fast":
        fast_median = quick_select(lst, len(lst) // 2)[0]
        for i in lst:
            sum += abs(i[1] - fast_median.location)
    print("$ python3 merchants.py " + str(sys.argv[1]) + " " + str(sys.argv[2]))
    print("Search type: " + str(sys.argv[1]))
    print("Number of merchants: " + str(len(read_people(filename))))
    time_took = time.clock() - start
    print("Elapsed time: " + str(time_took) + " seconds")
    if slow_or_fast == "slow":
        print("Optimal store location: " + str(slow_sort[slow_median]))
        print("Sum of distances: " + str(sum))
    elif slow_or_fast == "fast":
        print("Optimal store location: " + str(fast_median))
        print("Sum of distances: " + str(sum))

if __name__ == '__main__':
    main()