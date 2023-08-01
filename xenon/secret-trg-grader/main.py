import os
import re

from flask import Flask, request


app = Flask(__name__)
graders = {}


def fixed_grader(a, case=True):
    if case:
        return lambda s: 1 if s == a else 0
    else:
        b = a.casefold()
        return lambda s: 1 if s.casefold() == b else 0


def startswith_grader(a, case=True):
    if case:
        return lambda s: 1 if s.startswith(a) else 0
    else:
        b = a.casefold()
        return lambda s: 1 if s.casefold().startswith(b) else 0


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
        if t <= 1250:
            return 1
        return max(0.2, 3 - 0.0016 * t)
    return 0


def grader_2048(ans):
    size = 6

    def create_null(row, col):
        return [[0 for i in range(col)] for j in range(row)]
    def move(state, direction):
        done = create_null(size,size)
        if direction == 'u':
            for times in range(10):
                for j in range(size):
                    for i in range(1,size):
                        if done[i][j]:
                            continue
                        elif state[i][j] == 0:
                            continue
                        elif state[i-1][j] == 0:
                            state[i-1][j] = state[i][j]
                            state[i][j] = 0
                        elif state[i-1][j] == state[i][j] and done[i-1][j] == 0:
                            state[i-1][j] += state[i][j]
                            state[i][j] = 0
                            done[i-1][j] = 1
        elif direction == 'l':
            for times in range(10):
                for i in range(size):
                    for j in range(1,size):
                        if done[i][j]:
                            continue
                        elif state[i][j] == 0:
                            continue
                        elif state[i][j-1] == 0:
                            state[i][j-1] = state[i][j]
                            state[i][j] = 0
                        elif state[i][j-1] == state[i][j] and done[i][j-1] == 0:
                            state[i][j-1] += state[i][j]
                            state[i][j] = 0
                            done[i][j-1] = 1
        elif direction == 'r':
            for times in range(10):
                for i in range(size):
                    for j in range(size-2,-1,-1):
                        if done[i][j]:
                            continue
                        elif state[i][j] == 0:
                            continue
                        elif state[i][j+1] == 0:
                            state[i][j+1] = state[i][j]
                            state[i][j] = 0
                        elif state[i][j+1] == state[i][j] and done[i][j+1] == 0:
                            state[i][j+1] += state[i][j]
                            state[i][j] = 0
                            done[i][j+1] = 1
        elif direction == 'd':
            for times in range(10):
                for j in range(size):
                    for i in range(size-2,-1,-1):
                        if done[i][j]:
                            continue
                        elif state[i][j] == 0:
                            continue
                        elif state[i+1][j] == 0:
                            state[i+1][j] = state[i][j]
                            state[i][j] = 0
                        elif state[i+1][j] == state[i][j] and done[i+1][j] == 0:
                            state[i+1][j] += state[i][j]
                            state[i][j] = 0
                            done[i+1][j] = 1
        return state
    def genrand(state):
        if (state[size-1][0] != 0):
            return False
        state[size-1][0] = 2
        return state
    def win(state):
        for i in range(size):
            for j in range(size):
                if state[i][j] == 2048:
                    return True
        return False

    state = create_null(size,size)
    state = genrand(state)
    moves = [(m.group(1), int(m.group(2) or 1)) for m in re.finditer(r'([uldr])(\d*)',ans)]
    total = 0

    for (where, times) in moves:
        total += times
        for _ in range(times):
            state = move(state, where)
            state = genrand(state)
            if state is False:
                return 0
    for i in range(size):
        for j in range(size):
            if state[i][j] == 2048:
                if total <= 1050:
                    return 1
                return max(0.2, 3.1 - 0.002 * total)
    return 0


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

    count = s.count('GRIFFLES')

    if count > 0:
        if count == 5:
            return 1
        return 0.2 * count
    return 0


def grader_painted_jezebel(ans):
    def f(x):
        return (x + 16) % 16

    s = list('p ajienzteebde l')
    p = 0

    for c in ans.upper():
        match c:
            case 'R':
                x = f(p)
                y = f(p + 1)
                s[x], s[y] = s[y], s[x]
                p = y
            case 'L':
                x = f(p)
                y = f(p - 1)
                s[x], s[y] = s[y], s[x]
                p = y
            case 'S':
                x = f(p - 1)
                y = f(p + 1)
                s[x], s[y] = s[y], s[x]

    if ''.join(s) == 'painted jezebel ':
        if len(ans) <= 60:
            return 1
        return max(0.2, 2.2 - 0.02 * len(ans))
    return 0


def grader_insurrection_interception(ans):
    def f(s):
        return sum(vals[c] * (i + 1) for i, c in enumerate(s)) % 4000

    if len(ans) != 12:
        return 0

    vals = dict((' ABCDEFGHIJKLMNOPQRSTUVWXYZ '[i], i) for i in range(1,28))
    expected = f('STRIKE AT EIGHT ON THE NINTH OF MAY')
    actual = f(f'ALL HAIL EMPEROR TEDDY {ans.upper()}')

    if expected == actual:
        return 1
    return 0


def grader_eruces_yrev_ton(ans):
    def vignere(s, k):
        c = []
        for i in range(len(s)):
            x = (ord(s[i]) + ord(k[i % len(k)])) % 26
            x += ord('A')
            c.append(chr(x))
        return c
    def rail_fence(s):
        rail = [['\n' for _ in range(len(s))] for _ in range(3)]
        dir_down = False
        row, col = 0, 0
        for i in range(len(s)):
            if (row == 0) or (row == 2):
                dir_down = not dir_down
            rail[row][col] = s[i]
            col += 1
            if dir_down:
                row += 1
            else:
                row -= 1
        c = []
        for i in range(3):
            for j in range(len(s)):
                if rail[i][j] != '\n':
                    c.append(rail[i][j])
        return c
    def lcs(x, y):
        m, n = len(x), len(y)
        dp = [[-1] * (n+1) for _ in range(m+1)]
        for i in range(m+1):
            for j in range(n+1):
                if i == 0 or j == 0:
                    dp[i][j] = 0
                elif x[i-1] == y[j-1]:
                    dp[i][j] = dp[i-1][j-1]+1
                else:
                    dp[i][j] = max(dp[i-1][j], dp[i][j-1])
        return dp[m][n]

    if len(ans) != 32:
        return 0

    if not ans.isalpha():
        return 0

    ans = ans.upper()
    cc = rail_fence(vignere(ans, 'GVSOIQMCA'))
    cc = rail_fence(vignere(cc, 'OFEJI'))
    cc = rail_fence(vignere(cc, 'MVAQEIQRTG'))
    l = lcs(ans[::-1], cc)

    if l >= 16:
        return 1
    return 0


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
