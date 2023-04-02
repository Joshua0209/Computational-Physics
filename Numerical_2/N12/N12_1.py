def func(x, N):
    f_value = 0.
    ### START YOUR CODE HERE ###
    for n in range(1, N+1):
        f_value += x**n
    f_value -= N/2
    #### END YOUR CODE HERE ####
    return float(f_value)


def func_prime(x, N):
    fp_value = 0.
    ### START YOUR CODE HERE ###
    for n in range(1, N+1):
        fp_value += n*x**(n-1)
    #### END YOUR CODE HERE ####
    return float(fp_value)


def find_the_root(N):
    solution = 0.5

    ### START YOUR CODE HERE ###
    a, b, c = 0., 0.5, 1.
    fa, fb = func(a, N), func(b, N)
    d = b - fb/func_prime(b, N)
    while abs(fb) > 1E-11:
        d = b - fb/func_prime(b, N)
        # if (d-a)*(d-c) > 0.:
        #     if fa*fb > 0.:
        #         d = (b+c)*0.5
        #     else:
        #         d = (a+b)*0.5
        fd = func(d, N)
        b, fb = d, fd

    solution = b
    #### END YOUR CODE HERE ####
    return float(solution)
