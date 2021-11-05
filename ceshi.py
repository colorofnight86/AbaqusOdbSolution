import os


def refactor(list1):
    list1 = sorted(list1, key=lambda x: (x))


if __name__ == '__main__':
    lists = [0,1,2,3,4,5,6,7]
    # refactor(lists)
    str1 = ','.join(str(i) for i in lists)
    print(str1, lists)
