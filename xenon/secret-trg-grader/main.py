import os

from flask import Flask, request


app = Flask(__name__)
graders = {}


def fixed_grader(a, case=True):
    if case:
        return lambda s: '1' if s == a else '0'
    else:
        b = a.casefold()
        return lambda s: '1' if s.casefold() == b else '0'


def startswith_grader(a, case=True):
    if case:
        return lambda s: '1' if s.startswith(a) else '0'
    else:
        b = a.casefold()
        return lambda s: '1' if s.casefold().startswith(b) else '0'


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
            case 'C':
                x1 = f(p)
                y1 = f(p + 8)
                x2 = f(p + 4)
                y2 = f(p + 12)
                s[x1], s[y1] = s[y1], s[x1]
                s[x2], s[y2] = s[y2], s[x2]
                p = y1

    if ''.join(s) == 'painted jezebel ':
        return len(ans)
    return 0


def grader_insurrection_interception(ans):
    def f(s):
        return sum(vals[c] * (i + 1) for i, c in enumerate(s)) % 4000

    if len(ans) != 12:
        return '0'

    vals = dict((' ABCDEFGHIJKLMNOPQRSTUVWXYZ '[i], i) for i in range(1,28))
    expected = f('STRIKE AT EIGHT ON THE NINTH OF MAY')
    actual = f(f'ALL HAIL EMPEROR TEDDY {ans.upper()}')

    if expected == actual:
        return '1'
    return '0'


def grader_eruces_yrev_ton(ans):
    def vignere(s, k):
        c = []
        for i in range(len(s)):
            x = (ord(s[i]) +
                 ord(k[i % len(k)])) % 26
            x += ord('A')
            c.append(chr(x))
        return c
    def rail_fence(s):
        rail = [['\n' for _ in range(len(s))]
                    for _ in range(3)]
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

    if not 16 <= len(ans) <= 32:
        return '0'

    if not ans.isalpha():
        return '0'

    ans = ans.upper()
    cc = rail_fence(vignere(ans, 'GVSOIQMCA'))
    cc = rail_fence(vignere(ans, 'OFEJI'))
    cc = rail_fence(vignere(ans, 'MVAQEIQRTG'))
    l = lcs(ans[::-1], cc)

    if l >= 8:
        return f'{l}'
    return '0'


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
