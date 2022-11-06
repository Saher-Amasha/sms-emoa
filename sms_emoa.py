import random
import matplotlib.pyplot as plt


def f1(x):
    if len(x) > 0:
        t = x[0]
        return t ** 2


def f2(x):
    if len(x) > 0:
        t = x[0]
        return (t - 2) ** 2


def variate_2d(p_t):
    if len(p_t) > 0:
        r = [[(p_t[random.sample(range(0, len(p_t)), 1)[0]][0] * random.uniform(0, 1)) % 10]]
        return r


def fast_non_dominated_sort(population, function_1, function_2):
    fronts = [[]]
    points = {}
    for individual in population:
        domination_count = 0
        dominated_solutions = []

        points[individual[0]] = [domination_count, dominated_solutions, 0]
        for other_individual in population:
            if other_individual != individual:
                if dominates(individual, other_individual, function_1, function_2):
                    points[individual[0]][1].append(other_individual)
                elif dominates(other_individual, individual, function_1, function_2):
                    points[individual[0]][0] += 1
        if points[individual[0]][0] == 0:
            points[individual[0]][2] = 0
            fronts[0].append(individual)
    front_index = 0
    while len(fronts[front_index]) > 0:
        temp = []
        for individual in fronts[front_index]:
            for other_individual in points[individual[0]][1]:
                points[other_individual[0]][0] -= 1
                if points[other_individual[0]][0] == 0:
                    points[other_individual[0]][2] = front_index + 1
                    temp.append(other_individual)
        front_index = front_index + 1
        fronts.append(temp)
    return fronts


def dominates(p1, p2, function_1, function_2):
    if function_1(p1) <= function_1(p2) and function_2(p1) <= function_2(p2):
        if function_1(p1) < function_1(p2) or function_2(p1) < function_2(p2):
            return True

    return False


def init(num_samples, lower_bound=-10, upper_bound=10):
    t = []
    for i in range(0, num_samples):
        a = random.sample(range(lower_bound, upper_bound), 1)
        a[0] = a[0] * float(random.uniform(0, 1))
        t.append(a)
    return t


def reduce(q, function_1, function_2):
    fronts = fast_non_dominated_sort(q, function_1, function_2)

    while [] in fronts:
        fronts.remove([])
        most_dominated_front = fronts[len(fronts) - 1]
        res = sorted(most_dominated_front, key=lambda point: function_1(point), reverse=True)
        hv = {}
        if len(hv) > 1:
            for point_index in range(1, len(res)):
                hv[res[point_index][0][0]] = (function_1(res[point_index + 1]) - function_1(res[point_index])) * (
                        function_2(res[point_index - 1]) - function_2(res[point_index]))
            q.remove(min(hv, key=hv.get))
        else:
            q.remove(most_dominated_front[0])
        return q


def sms_emoa(max_iter, num_samples, offspring_generator, function_1, function_2):
    p = [init(num_samples)]
    q = []
    t = 0
    while t < max_iter:
        print(t)
        q.append(offspring_generator(p[t]))
        pUq = p[t] + q[t]

        p.append(reduce(pUq, function_1, function_2))

        t += 1

    return p


if __name__ == '__main__':
    max_iteration = 200
    number_of_samples = 200
    all_iterations = sms_emoa(max_iteration, number_of_samples, variate_2d, f1, f2)

    show_all_iterations = False
    X = []
    Y = []

    for iteration in all_iterations:
        for j in iteration:
            X.append(f1(j))
            Y.append(f2(j))
        if not show_all_iterations:
            if iteration == all_iterations[len(all_iterations) - 1]:
                plt.scatter(X, Y)
                plt.show()
                plt.close()
        else:
            plt.scatter(X, Y)
            plt.show()
            plt.close()
        X = []
        Y = []
