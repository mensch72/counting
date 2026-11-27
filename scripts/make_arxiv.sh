#!/bin/bash
# Build the arXiv submission bundle arxiv/arxiv.tar.gz:
#   paper.tex (with paper/tables.tex inlined), anc/ (data tables and programs as ancillary files)
# and arxiv/abstract.txt (plain-text abstract for the submission form).  Test-compiles the bundle.
set -e
cd "$(dirname "$0")/.."
python3 scripts/make_tables.py
rm -rf arxiv/build && mkdir -p arxiv/build/anc
python3 - <<'P'
s = open('paper/paper.tex').read()
t = open('paper/tables.tex').read()
s = s.replace(r'\input{tables.tex}', '% ---- generated tables (scripts/make_tables.py) ----\n' + t + '% ----\n')
open('arxiv/build/paper.tex', 'w').write(s)
# plain-text abstract for the arXiv form
import re
a = s[s.index(r'\begin{abstract}') + len(r'\begin{abstract}'):s.index(r'\end{abstract}')]
macros = dict(re.findall(r'\\newcommand\{\\(\w+)\}\{([^{}]*)\}', t))
for k, v in macros.items(): a = a.replace('\\' + k + '$', v + '$').replace('\\' + k + ' ', v + ' ')
a = re.sub(r'\$([^$]*)\$', r'\1', a)
a = a.replace(r'\emph{', '').replace('}', '').replace('{', '').replace('\\,', ' ').replace('~', ' ')
a = re.sub(r'\\[a-zA-Z]+', '', a)
a = ' '.join(a.split())
assert len(a) <= 1920, len(a)
open('arxiv/abstract.txt', 'w').write(a + '\n')
P
cp data/b006982.txt data/b072361.txt data/b229202.txt data/b072407.txt data/b186808.txt \
   data/b006981.txt data/b342132.txt data/bounded_growth.txt data/bounded_growth_modular.txt \
   data/bounded_certificates.txt data/bounded_certificates_modular.txt arxiv/build/anc/
mkdir -p arxiv/build/anc/src arxiv/build/anc/scripts
cp src/frontier.cpp src/frontier2.cpp src/modular.cpp src/layers.cpp src/layers2.cpp src/bounded.cpp \
   src/brute_rank.cpp src/brute_layers.cpp arxiv/build/anc/src/
cp scripts/assemble.py scripts/assemble_mod.py scripts/assemble_layers.py scripts/check_dual.py \
   scripts/planar_check.py scripts/bounded_growth.py scripts/bounded_certificate.py scripts/run_bounded.sh \
   scripts/derived.py arxiv/build/anc/scripts/
cat > arxiv/build/anc/README.txt <<'R'
Ancillary files for "Counting distributive and modular lattices with a frontier transfer matrix".
b006982.txt  distributive lattices d(n), n <= 160          b072361.txt  vertically indecomposable ones
b006981.txt  modular lattices m(n)                          b342132.txt  vertically indecomposable ones
b229202.txt  semimodular lattices                           b072407.txt, b186808.txt  derived sequences
bounded_*.txt  growth rates of the bounded-layer automata and the exact certificates
src/, scripts/  the programs (C++, needs nauty) and the checking scripts; see
https://github.com/mensch72/counting for instructions, logs and the full history.
R
# test compile in a clean copy
T=$(mktemp -d); cp -r arxiv/build/* $T/; (cd $T && pdflatex -interaction=nonstopmode paper.tex >/dev/null && pdflatex -interaction=nonstopmode paper.tex >/dev/null; grep -E "^!|undefined" paper.log && exit 1; grep -o "Output written.*" paper.log); rm -rf $T
tar -czf arxiv/arxiv.tar.gz -C arxiv/build .
echo "bundle: arxiv/arxiv.tar.gz ($(du -k arxiv/arxiv.tar.gz | cut -f1) KB); abstract: $(wc -c < arxiv/abstract.txt) characters"
