# File containing functions used for data analysis

def get_average(data: list[int | float]) -> float:
    return sum(data) / len(data)


def get_deviation(data: list[int | float]):
    S2 = 0

    avg = get_average(data)
    n = len(data)

    for point in data:
        S2 += (point - avg)**2
    
    return (S2 / (n - 1))**0.5


def get_low(data):
    return min(data)

def get_high(data):
    return max(data)
