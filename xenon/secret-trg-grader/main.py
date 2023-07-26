import os

from collections import defaultdict
from flask import Flask, request


app = Flask(__name__)
graders = {}


def fixed_grader(a, case=True):
    if case:
        return lambda s: '1' if s == a else '0'
    else:
        b = a.casefold()
        return lambda s: '1' if s.casefold() == b else '0'


def grader_str_weave(ans):
    f = ''
    ss = ['auspicium melioris aevi', '077146317705149305190', 'teddy world domination', '<html>woo css!</html>', '+++++ moor tarbet +++++', 'haerzbugpnmysargcojhnmmrbyipwiyqbsascu', 'rgs celebrates 143 years', 'random stuff', 'ri debate', 'lookie it’s a fishie <><']
    sel = ''
    t = 0

    for c in ans:
        match c:
            case '0' | '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9':
                t += 27
                sel = ss[int(c)]
            case 'T':
                t += 3
                sel = sel[1:]
            case 'F':
                t += 4
                sel = sel[:-2]
            case 'M':
                t += 5
                sel = sel[1:-1]
            case 'S':
                t += 2
                if len(sel) > 1:
                    sel = sel[-1] + sel[1:-1] + sel[0]
            case 'A':
                t += 38
                f += sel
                sel = ''

    if f == 'raffles <3 computer science':
        return f'{t}'
    return '-1'


def grader_scrambled_gryphon_eggs(ans):
    s = 'LESLESLESLESLESIFFIFFIFFIFFIFFGRGRGRGRGR'

    for c in ans:
        match c:
            case '1':
                s = s.replace('IFFGR', 'GRIFF', 1)
            case '2':
                s = s.replace('LESGR', 'GRLES', 1)
            case '3':
                s = s.replace('LESIFF', 'IFFLES', 1)

    return '1' if s == 'GRIFFLESGRIFFLESGRIFFLESGRIFFLESGRIFFLES' else '0'


def grader_sched(ans):
    ans = [c for c in ans if c in 'qwertyuiopasdfghjklzxcvbnm']
    if len(ans) != 26:
        return '-1'

    ds = { 'v': 0, 'l': 1, 'u': 2, 'h': 3, 'c': 4, 'j': 5, 'a': 6, 'b': 7, 'n': 8, 'f': 9, 'm': 10, 't': 11, 's': 12, 'o': 13, 'z': 14, 'q': 15, 'i': 16, 'y': 17, 'r': 18, 'e': 19, 'g': 20, 'x': 21, 'p': 22, 'd': 23, 'w': 24, 'k': 25 }
    _rs = [('a', 'ch'), ('b', 'a'), ('d', 'c'), ('g', 'z'), ('i', 'jnq'), ('k', 'di'), ('l', 'hm'), ('m', 'nr'), ('o', 'km'), ('s', 'l'), ('t', 'ay'), ('u', 'y'), ('v', 'i'), ('x', 'dqvy'), ('z', 'j')]
    rs = defaultdict(str)
    for k, v in _rs:
        rs[k] = v
    done = defaultdict(bool)
    happy = 0

    for i, c in enumerate(ans):
        happy += abs(ds[c] - i)

        if done[c]:
            return '-1'
        done[c] = True

        for r in rs[c]:
            if not done[r]:
                return '-1'

    assert len(rs) == 26

    return f'{happy}'


def grader_nat_weri_sekure(ans):
    def g(s):
        def h(s):
            return s[::-1] if s.count('1') == 1 else s
        s1, s2 = s[:24], s[24:]
        s1, s2 = [('0' if c == '1' else '1') for c in s1], s2[::-1]
        s3 = ''.join(c1 + c2 for c1, c2 in zip(s1, s2))
        l = []
        for i in range(0, 45, 5):
            l.append(h(s3[i:i+3]))
            l.append(s3[i+4:i+2:-1])
        l.append(h(s3[45:]))
        return ''.join(l)

    try:
        n, bs, *_ = ans.split(' ')
        n = int(n)
    except ValueError:
        return '-1'
    if len(bs) != 48:
        return '-1'
    if not 4 <= n <= 128:
        return '-1'
    for c in bs:
        if c not in '01':
            return '-1'

    proc = bs
    for _ in range(n):
        proc = g(proc)

    dist = 0
    for x, y in zip(bs, proc):
        if x != y:
            dist += 1

    if dist <= 12:
        return f'{dist}'
    return '-1'


@app.route('/', methods=['GET'])
def endpoint():
    if 's' not in request.args or request.args['s'] != graders['__secret__']:
        return 'go away!'

    qn = request.args['q'].strip()
    ans = request.args['a'].strip()

    return str(graders[qn](ans))


if __name__ == '__main__':
    exec(f'graders = {os.environ["GRADERS"]}')
    app.run(host='0.0.0.0', port=5000)
