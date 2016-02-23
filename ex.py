def move(n, frm=0, to=1, via=2, total=[]):
    if (n == 1):
        total.append((frm,to))
    else:
        (move(n-1, frm, via, to, total))
        (move(1, frm, to, via, total))
        (move(n-1, via, to, frm, total))
    return total
