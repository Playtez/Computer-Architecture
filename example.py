"""
Given the following array of values, print out all the elements in reverse order, with each element on a new line.
For example, given the list
[10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
Your output should be
0
1
2
3
4
5
6
7
8
9
10
You may use whatever programming language you'd like.
Verbalize your thought process as much as possible before writing any code. Run through the UPER problem solving framework while going through your thought process.

1. loop through the array
2. print each num
range(starting_point, end_point'not included', what direction)

"""

array = [10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0]

for item in range(len(array)-1, -1, -1):
    print(array[item])

array = array[-1::-1]

for item in array:
    print(item)
