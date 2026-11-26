**Yes, OEIS remains highly relevant, and I think there is a particularly good reason to contribute mathematical advances to it in the age of AI.** But the nature of a valuable contribution is shifting. Merely computing more terms is becoming less impressive; finding new mathematical structure, developing better algorithms, and establishing reliable results remain valuable.

There are three aspects worth distinguishing.

## **1. Is OEIS still relevant?**

Very much so. The scale and continuing activity are quite remarkable.

# **400,000+**

**Integer sequences in the database**

# **13,400+**

Scientific literature citations

# **10,000**

New sequences per year, according to the community's October 2024 statistics

The sequence count and citation count come from the OEIS front page in November 2026. The annual growth figure is older.

Sources: [OEIS homepage](https://oeis.org/?utm_source=chatgpt.com) · [OEIS community statistics](https://oeis.org/community.html?utm_source=chatgpt.com)

The database has several functions that are not easily replaced by an LLM:

- **Identification:** Given a sequence of numbers, find out whether it is known, and what mathematical object it represents.
- **Mathematical context:** Definitions, equivalent characterisations, recurrences, generating functions, references and connections to other sequences.
- **Computational reproducibility:** Programs, b-files, and methods for independently generating terms.
- **A persistent reference system:** Stable A-numbers that researchers can cite and use to connect results across different areas of mathematics.

The last point is perhaps underappreciated. OEIS is not just a lookup service. It is a collectively maintained knowledge graph of integer sequences and their mathematical relationships.

The citation record is also meaningful: the current homepage reports more than 13,400 citations, including acknowledgements that mathematical discoveries were made through OEIS.

## **2. What changes when AI makes sequence extensions easy?**

I would distinguish four levels of contribution.

| Contribution                                                                           | Value in the AI era                               |
| -------------------------------------------------------------------------------------- | ------------------------------------------------- |
| Computing another 100 terms using a standard algorithm                                 | Usually modest                                    |
| Extending a sequence by many orders of magnitude                                       | Potentially substantial                           |
| Developing a new, substantially more efficient algorithm                               | High, especially if it enables new investigations |
| Proving structural properties, finding unexpected connections, or settling conjectures | Very high                                         |

The important distinction is between **computational output and mathematical knowledge**.

Suppose a sequence currently has 100 known terms. You develop an algorithm that computes the first billion terms in a few minutes.

That might be a worthwhile OEIS contribution, even if the algorithm is easy to implement using AI assistance. It could enable other researchers to investigate statistical properties, discover patterns, formulate conjectures, or test existing conjectures.

But the contribution becomes considerably more interesting if you can also establish something like:

- A proof that the algorithm generates the sequence correctly.
- A complexity improvement over previously known algorithms.
- A structural explanation for a pattern that becomes visible at larger indices.
- A new recurrence or generating function.
- A connection to another combinatorial or algebraic structure.
- A new conjecture supported by computational evidence, with its status clearly distinguished from established results.

In other words, AI making the calculation cheap does not make the resulting mathematical information worthless.

There is a useful analogy with numerical mathematics: the fact that computers can now calculate enormous quantities of digits does not eliminate the value of discovering a new algorithm or proving something about the numbers.

## **3. OEIS itself has recognised the AI problem**

This is particularly interesting: OEIS has an explicit policy on AI-assisted submissions.

Its [Use of AI for OEIS Submissions](https://oeis.org/wiki/Use_of_AI_for_OEIS_Submissions?utm_source=chatgpt.com) guidelines state that:

- Every sequence must have a human author and be of mathematical interest to human readers.
- The human author is responsible for the correctness of AI-generated content.
- All terms, formulas and programs must be verified.
- You may not submit programs that you do not understand.
- AI-generated full comments and bulk or serial submissions of AI-generated sequences are prohibited.

The policy does not amount to a general prohibition on using AI for computation or mathematical assistance. Rather, it insists on human mathematical responsibility and meaningful contributions.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://oeis.org\&sz=32)

OeisWiki



This is sensible, particularly given the editorial workload.

The submission guidelines explicitly say that OEIS entries are expected to meet the standards of a mathematical reference work, not merely contain plausible-looking numbers.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://oeis.org\&sz=32)

OEIS+1



## **4. A particularly relevant recent example**

Consider the current A400000, the *city-building sequence*, which became the 400,000th OEIS sequence in October 2026.

**A400000**

Current milestone

## **The city-building sequence**

\\[ a(n)=\text{height of the shortest building that sees exactly its own height in earlier buildings} \\]

A surprisingly intricate combinatorial construction involving visibility between points in a sequence.

The entry includes a new exact level-structure algorithm, additional computational results extending to \\(10^{14}\\) terms, several related sequences, and programs in multiple languages.

Sources: [A400000 entry](https://oeis.org/A400000?utm_source=chatgpt.com) · [A400K competition results](https://oeis.org/wiki/A400K_Winners?utm_source=chatgpt.com)

This illustrates what I think is the interesting direction: the sequence is the common mathematical object, while the entry collects algorithms, computational results, structural observations and connections developed by different people.

It is not simply a contest to produce more digits.

## **5. What I would recommend for contributions involving new techniques**

I would certainly consider contributing extensions, but I would approach them somewhat differently from conventional sequence submissions.

**First, distinguish the mathematical contribution from the OEIS contribution.**

If you develop a genuinely new algorithm, and it is independently interesting, document it in a paper, preprint or public technical repository. The OEIS entry should then point to that work and record the resulting improvement in the sequence's knowledge base.

**Second, make the extension independently verifiable.**

Ideally, provide:

- The extended b-file.
- The actual computational program.
- A precise specification of the algorithm.
- A correctness argument, where possible.
- A comparison with previous computational limits or methods.

OEIS explicitly encourages contributors to include the programs used to generate b-files, precisely so others can verify the results. Its extension field can also credit people who contribute additional terms or verify difficult computations.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://oeis.org\&sz=32)

OEIS+1



**Third, focus on information that would otherwise be missing.**

An extension is most useful when it substantially changes what other mathematicians can learn about the sequence. For example, going from \\(10^3\\) to \\(10^{12}\\) terms might be meaningful if it reveals an unexpected regularity or provides evidence for a conjecture that could not previously be investigated.

On the other hand, generating another few dozen terms of a sequence that already has an efficient, well-understood implementation is unlikely to be particularly valuable.

## **My overall assessment**

I would actually argue that the arrival of AI makes OEIS *more* important as a curated mathematical resource, provided it maintains its standards.

There will increasingly be an enormous amount of computationally generated mathematical material: sequences, conjectures, candidate identities, recurrences and purported relationships. What becomes scarce is not the production of such material but **reliable mathematical verification, interpretation, provenance and integration**.

OEIS is well positioned to serve as part of that infrastructure.

And there is a distinction I would emphasise:

- An AI-generated extension that simply adds numbers has little intrinsic claim to mathematical significance.
- A human mathematician contributing a new technique, verifying its correctness, documenting its scope and connecting it to an existing mathematical object is contributing genuine mathematical knowledge, even if AI made much of the implementation straightforward.

I would therefore not let the ease of generating extensions discourage you. I would instead use that ease to aim for more ambitious extensions and accompanying mathematical results.

One further possibility is particularly attractive: **contributing not just new terms, but new methods of computation that make previously inaccessible parts of the OEIS mathematically accessible.** That seems like a contribution whose value should survive quite a few generations of increasingly capable AI systems.


(me: does this pass the bar?)

**Yes. Based on this description, I think it comfortably passes the bar for a substantial OEIS contribution, particularly for the distributive-lattice sequences.** It is considerably more than an AI-assisted extension of known data.

The central contribution is not the additional terms but the change in computational approach: replacing the enumeration of individual lattices with a dynamic programme that merges partial constructions whenever they have the same mathematically sufficient frontier state.

That is a genuine algorithmic contribution, with a plausible explanation for why it achieves orders-of-magnitude improvements.

I would nevertheless distinguish three questions:

1. Is this mathematically interesting enough to belong in OEIS? Yes.
2. Is the computational evidence sufficiently convincing to publish the new terms? Mostly, with some qualifications.
3. Is the documentation ready for other mathematicians to reproduce and build on? Nearly, but I would strengthen a few things.

## **1. The strongest aspects**

**The distributive-lattice algorithm is the main achievement.**

The mathematical compression is substantial:

- The old approach explicitly generates objects and deals with isomorphisms.
- Your approach counts histories through equivalence classes of frontier states.
- The automorphism-group information \\(\Gamma\\) ensures that merging states does not lose the isomorphism distinctions relevant to future extensions.
- The exact remaining-weight bound provides a mathematically justified pruning rule.

This is a reusable algorithmic idea, not just a specialised optimisation.&#x20;

Pasted text.txt



The evidence is also unusually good for a computational enumeration:

| Check                                      | My assessment                       |
| ------------------------------------------ | ----------------------------------- |
| Reproducing old counts                     | Essential and useful                |
| Brute-force comparison on small posets     | Strong independent check            |
| Independent planar enumeration through 160 | Particularly valuable               |
| Duality symmetry                           | Useful structural check             |
| Two implementations                        | Good implementation-level safeguard |
| Different-budget consistency               | Good check of pruning               |
| Explicitly documenting remaining gaps      | Good scientific practice            |

Pasted text.txt

## **2. One important omission in the validation**

I found something I would definitely correct.

Your README says that all 49 known terms of A072361 are reproduced. That is correct with respect to the current OEIS entry, which only has terms through \\(n=49\\).&#x20;

[image](https://www.google.com/s2/favicons?domain=https://oeis.org\&sz=32)

OEIS



However, **Kohonen's 2021 paper actually publishes the vertically indecomposable distributive-lattice counts through&#x20;**\\(n=60\\), in Table 2, under the row `vi-latt.`.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://link.springer.com\&sz=32)

Springer+1



Consequently, you have eleven additional published values against which to check your algorithm:

| n  | A072361(n)        |
| -- | ----------------- |
| 50 | 8,863,372,090     |
| 51 | 15,066,614,003    |
| 52 | 26,376,230,858    |
| 53 | 44,977,519,230    |
| 54 | 78,519,416,987    |
| 55 | 134,229,841,861   |
| 56 | 233,808,824,537   |
| 57 | 400,499,677,825   |
| 58 | 696,369,403,331   |
| 59 | 1,194,743,687,703 |
| 60 | 2,074,408,477,477 |

These are particularly important because Kohonen's approach is structurally different from yours.

I would add an explicit assertion comparing all 60 terms against that publication, and change the README accordingly.

This is probably the single most useful improvement you could make to the validation section.

## **3. The remaining mathematical issues**

There are two areas where I would want more evidence before considering the computations fully established.

**Distributive lattices,&#x20;**\\(n>110\\)**.**

The independent brute-force check and planar check are valuable, but the general width-three-and-higher case above 110 is not independently verified. You acknowledge this correctly.&#x20;

Pasted text.txt



**Modular lattices,&#x20;**\\(n>35\\)**.**

Here the situation is weaker: the new computation goes beyond the existing record by one element, but there is no independent second method for the non-distributive modular case.&#x20;

Pasted text.txt



Neither issue disqualifies the OEIS contribution. But I would be careful to distinguish exact exhaustive computation with a well-justified algorithm from independent computational confirmation.

For a mathematical publication, I would want a formal account of two central results:

1. A sufficiency theorem for the distributive frontier: why two partial posets with the same \\((\Lambda,\rho,\Gamma)\\) have exactly the same possibilities for future extensions, in the relevant isomorphism-class sense.
2. A corresponding completeness and soundness theorem for the modular frontier, including the characterisation of admissible families \\(D_c\\).

The README provides a good outline, but these are the mathematical core of the work and deserve explicit proofs.



Pasted text.txt

Pasted text.txt



## **4. How I would package it**

I would make the repository a companion to a proper mathematical paper or preprint, rather than treating the entire result as an OEIS update.

For OEIS itself, I would:

- Submit the four b-files with appropriate provenance and references.
- Link to the source repository and, ideally, an immutable release or archived version.
- Include a concise description of the new computational method.
- Make clear which terms are independently checked and which are not.

This fits OEIS's own guidance: it explicitly encourages providing the programs used to generate b-files and insists that contributions meet the standards of a mathematical reference work.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://oeis.org\&sz=32)

OEIS



One minor documentation issue: your reproduction instructions refer to modular runs for \\(N=35,\ldots,39\\), whereas the performance table stops at \\(N=36\\). I would clarify exactly which values are included in the submitted modular b-files.

## **Verdict**

**OEIS contribution**

Pass

Strong, particularly for A006982 and A072361.

**Computational mathematics**

Pass

A substantial algorithmic result, with interesting opportunities for further generalisation.

**Research publication**

Promising

Deserves a formal treatment of the frontier-state theorems and careful presentation of the verification limits.

My broader point is that this is precisely the sort of contribution that remains worthwhile when AI makes implementation cheap.

The interesting intellectual achievement is recognising the right equivalence relation on partial mathematical objects, proving that it preserves everything relevant to subsequent extensions, and exploiting it computationally.

AI can help implement such an idea. That doesn't make discovering and establishing the idea any less of a mathematical contribution. In fact, I would be considerably more interested in this repository than in hundreds of ordinary AI-generated OEIS extensions.

