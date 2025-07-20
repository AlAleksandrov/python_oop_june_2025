def solution():
    def integers():
        count = 1
        while True:
            yield count
            count += 1

    def halves():
        for i in integers():
            yield i / 2

    def take(n, seq):
        result = []
        for i in range(n):
            result.append(next(seq))
        return result


    return (take, halves, integers)


take = solution()[0]
halves = solution()[1]
print(take(5, halves()))

print('\n---------------------')
take = solution()[0]
halves = solution()[1]
print(take(0, halves()))
