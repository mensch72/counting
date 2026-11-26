#!/usr/bin/env python3
"""Generate paper/tables.tex from the b-files, so that no number in the paper is typed by hand."""
import os
here = os.path.dirname(os.path.abspath(__file__)); D = os.path.join(here, '..', 'data')
def rb(name):
    d = {}
    for l in open(os.path.join(D, name)):
        if l.strip() and l[0] != '#':
            a, b = l.split(); d[int(a)] = int(b)
    return d
def num(x):  # thin-space digit grouping
    s = str(x); g = []
    while s: g.append(s[-3:]); s = s[:-3]
    return r'\,'.join(reversed(g))
f, v = rb('b006982.txt'), rb('b072361.txt'); m, mv = rb('b006981.txt'), rb('b342132.txt')
N = max(f); NM = max(m)
o = []
o.append(r'\newcommand{\Ndist}{%d}' % N)
o.append(r'\newcommand{\Nmod}{%d}' % NM)
o.append(r'\newcommand{\Nmodprev}{%d}' % (NM-1))
o.append(r'\newcommand{\Ndistprev}{%d}' % (N-1))
o.append(r'\newcommand{\dlast}{%s}' % num(f[N]))
o.append(r'\newcommand{\ratiod}{%.11f}' % (f[N] / f[N - 1]))
o.append(r'\newcommand{\ratiov}{%.5f}' % (v[N] / v[N - 1]))
o.append(r'\newcommand{\ratiom}{%.4f}' % (m[NM] / m[NM - 1]))
o.append(r'\newcommand{\ratiomv}{%.4f}' % (mv[NM] / mv[NM - 1]))
rows = list(range(61, 81)) + list(range(90, N + 1, 10))
o.append(r'\newcommand{\tabledist}{\begin{tabular}{rrr}\toprule $n$ & $d(n)$ & $d_{\mathrm{vi}}(n)$\\\midrule')
for n in rows: o.append(r'%d & {\footnotesize $%s$} & {\footnotesize $%s$}\\' % (n, num(f[n]), num(v[n])))
o.append(r'\bottomrule\end{tabular}}')
o.append(r'\newcommand{\tablemod}{\begin{tabular}{rrr}\toprule $n$ & $m(n)$ & $m_{\mathrm{vi}}(n)$\\\midrule')
for n in range(33, NM + 1):
    if n == 36: o.append(r'\midrule')
    o.append(r'%d & $%s$ & $%s$\\' % (n, num(m[n]), num(mv[n])))
o.append(r'\bottomrule\end{tabular}}')
# semimodular / geometric results (optional)
def opt(name):
    q = os.path.join(D, name)
    return rb(name) if os.path.exists(q) else {}
sm, ge = opt('b229202.txt'), opt('b281574.txt')
txt = []
if sm or ge:
    txt.append(r'\begin{table}[ht]')
    if sm:
        txt.append(r'\begin{tabular}{rr}\toprule $n$ & semimodular\\\midrule')
        for n in range(23, max(sm) + 1):
            if n == 26: txt.append(r'\midrule')
            txt.append(r'%d & $%s$\\' % (n, num(sm[n])))
        txt.append(r'\bottomrule\end{tabular}\qquad')
    if ge:
        txt.append(r'\begin{tabular}{rr}\toprule $n$ & geometric\\\midrule')
        for n in range(35, max(ge) + 1):
            if n == 38: txt.append(r'\midrule')
            txt.append(r'%d & $%s$\\' % (n, num(ge[n])))
        txt.append(r'\bottomrule\end{tabular}')
    txt.append(r'\caption{Numbers of semimodular lattices (A229202) and of geometric lattices (A281574) with $n$ elements.  Values above the rules agree with~\cite{Koh19} and the OEIS; those below are new.}\label{tab:other}')
    txt.append(r'\end{table}')
o.append(r'\newcommand{\resultsother}{' + '\n'.join(txt) + '}')
bt = [r'\begin{table}[ht]', r'\begin{tabular}{rrrll}\toprule $W$ & states & edges & growth rate, v.i. & growth rate, all\\\midrule']
for l in open(os.path.join(D, 'bounded_growth.txt')):
    w, st, tr, gall, gvi = l.split()
    bt.append(r'%s & $%s$ & $%s$ & $%s$ & $%s$\\' % (w, num(int(st)), num(int(tr)), gvi, gall))
bt += [r'\bottomrule\end{tabular}', r'\caption{The automata $\mathcal{A}_W$ and the exponential growth rates of the distributive lattices all of whose layers have at most $W$ elements (floating point values; the certified bounds are in Theorem~\ref{thm:growth}).}\label{tab:bounded}', r'\end{table}']
o.append(r'\newcommand{\boundedtable}{' + '\n'.join(bt) + '}')
o.append(r'\newcommand{\Nsemi}{%d}' % (max(sm) if sm else 0))
o.append(r'\newcommand{\Ngeo}{%d}' % (max(ge) if ge else 0))
open(os.path.join(here, '..', 'paper', 'tables.tex'), 'w').write('\n'.join(o) + '\n')
print('wrote paper/tables.tex; distributive to', N, 'modular to', NM)
