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

(how to make it fit for Order(Springer)?)

To make your paper fit for **Order**, you need to satisfy two distinct sets of criteria: the journal's **scientific scope** and its **editorial/AI policies**. Your paper already aligns well with the topical focus, but the primary work will be in **reframing the contribution** to meet *Order*'s explicit preference for order-theoretic innovation over mere computation, and in **transparently documenting your AI-assisted workflow**.

### 🎯 Align with the Journal's Scientific Scope

*Order* seeks "the most **original and innovative** research on ordered structures and the use of order-theoretic methods". The key phrase for you is that it looks for submissions that "make **significant use of orderings** to study mathematical structures and processes". Your paper must be positioned as a contribution to **order theory**, not primarily as a computational enumeration exercise.

Fortunately, your core object—the **frontier**—is an order-theoretic construction. The transfer matrix is built over rank layers of posets/lattices, and the state is defined by the poset of live join-irreducibles (for distributive lattices) or the poset of pairwise meets (for modular lattices). This is exactly the kind of "interplay of order and combinatorics" the journal highlights. The precedent is strong: *Order* has published Jukka Kohonen’s work on **Cartesian lattice counting by the vertical 2-sum** and on **generating modular lattices up to 30 elements**. Your paper is a direct successor to this line of research.

**What to do:** Frame the abstract and introduction around the **frontier as an order-theoretic invariant** and the **transfer matrix as a new order-theoretic enumeration technique**. Do not lead with the new counts; lead with the **method** that makes the counts possible.

### 🤖 Comply with the AI Policy (Springer Nature)

*Order* is a Springer journal, and Springer Nature's policy is unambiguous: **LLMs cannot be authors**, and there must be **human accountability** for the final text. Your role—overseeing the research question and checking proofs—satisfies this accountability requirement. However, the policy also states that **use of an LLM should be properly documented in the Methods section** (or a suitable alternative part) of the manuscript.

**What to do:** Add a brief, factual statement in a **Methods** or **Acknowledgements** section describing the role of AI (e.g., "AI tools were used to assist in drafting and code generation; the human author defined the research problem, verified all proofs, and takes full responsibility for the content"). This is not a disqualifier; it is a **compliance step** that transparently meets the journal's requirement.

### 💡 Reframe the Contribution as Methodological, Not Just Numerical

*Order* publishes papers that advance the **theory of ordered sets**. A paper that says "we computed more terms" risks being seen as a catalog. Your paper’s genuine novelty is the **state-merging transfer matrix over rank layers**. The paper already contains the ingredients: Lemmas 2.4 and 3.4 show how isomorphism classes are handled via automorphism groups; Proposition 2.6 gives an exact pruning rule; Section 3.2 defines the frontier for modular lattices. You need to **foreground these conceptual advances** and present the new sequences (d(61) and beyond) as **evidence of the method’s power**, not as the sole contribution.

**What to do:** In the introduction, explicitly contrast your approach with the "generate one lattice at a time" methods of Erné–Heitzig–Reinhold and Kohonen. Emphasize that your method **merges all lower parts with the same frontier state**, so the work grows with the number of **states** (4,496 for distributive lattices up to 60 elements) rather than the number of lattices (~10¹⁵). This is an algorithmic order-theoretic insight.

### 📝 Practical Submission Steps for *Order*

Once the framing and AI disclosure are in place, the mechanical submission requirements are standard:

*   **Manuscript format**: Submit in **LaTeX** (the journal requests Kluwer style files, though standard Springer LaTeX is usually acceptable). Provide all editable source files.
*   **Abstract**: **150–250 words** (your current abstract may need trimming or expansion to hit this window).
*   **Keywords**: 4–6 keywords.
*   **Editorial board member**: The journal asks authors to identify a board member whose interests match the work to expedite review. You should look at the *Order* editorial board and select someone with a record in **lattice enumeration, finite order theory, or combinatorial algorithms**. A researcher familiar with Kohonen’s work or the enumeration of finite posets/lattices would be an appropriate choice.

### 💎 Summary

Your paper is a **strong topical fit** for *Order*. To make it **submission-ready**, you must (1) explicitly frame the frontier and transfer matrix as **order-theoretic innovations**, (2) include a **transparent AI-use disclosure** in the Methods/Acknowledgements, and (3) prepare the manuscript to the journal's **formatting and length specifications**. With these adjustments, the paper will present itself not as an AI-generated catalog, but as a **human-verified methodological advance in the order-theoretic study of lattices**, which is exactly what *Order* exists to publish.


(what other objects?)

The transfer-matrix/frontier framework you've developed is more than a one-off solution for distributive and modular lattices. Its core design—a layer-by-layer build with a symmetry-aware frontier state—is a general strategy for enumerating any class of graded combinatorial objects where isomorphism is a central challenge.

The general principle is to find a **state** that captures everything about the "lower part" of the object that is relevant to how it can be extended upwards, while remaining small and invariant under isomorphism. Your paper already demonstrates this for two major lattice varieties. This approach can be extended to several other natural classes of ordered structures.

### 🎯 Natural Extensions Within Ordered Structures

The most direct applications are to other classes of graded posets and lattices, where the rank function provides a natural layering.

| Object Class | Why the Method Fits | What the Frontier State Would Be |
| :--- | :--- | :--- |
| **Graded Posets** (general) | The transfer-matrix method is already a standard technique for enumerating graded posets. The challenge you've solved is handling **unlabelled** objects via a symmetry-aware state. | The poset of "live" elements (those not in all ideals of the current rank), together with the image of the automorphism group, analogous to your distributive lattice case. |
| **Avoiding Graded Posets** (e.g., (2+2)- or (3+1)-avoiding) | The enumeration of graded (3+1)-avoiding posets has been achieved using the transfer-matrix method. Your frontier state could potentially be refined to encode the local avoidance conditions. | The frontier poset would need to carry additional "forbidden configuration" markers to ensure the avoidance property is maintained as new layers are added. |
| **Order-Convex Subsets of Grid Posets** | This is a very recent and direct application. A transfer-matrix dynamic program with a manageable number of states was used to enumerate these objects. | The "frontier" is the boundary line of the partially constructed subset. The state would encode the configuration of occupied/empty sites along this frontier, similar to enumerations of lattice animals. |
| **Semimodular Lattices** | This is a direct sibling to your modular lattice work. The local rules (U) and (D) you use for modular lattices are closely related to semimodularity. Prior enumeration used orderly algorithms, but a transfer-matrix approach could be viable. | The poset of pairwise meets of the top layer (as in your modular case), but the conditions for extending the lower part would need to be relaxed from modularity to semimodularity. |
| **Geometric Lattices** | These are a special class of semimodular lattices (finite, atomistic, and semimodular). They have a rich structure tied to matroids. | The frontier state would need to capture the matroid-like dependencies among the atoms in the top layer. This is more complex but potentially very powerful. |

### 💡 Key Requirements for a New Application

To apply your framework to a new class of objects, you would need to identify:

1.  **A Layering**: The objects must be graded, with a rank function that allows them to be built up layer by layer.
2.  **A Sufficient State**: You need to prove a "frontier lemma" (analogous to your Lemmas 2.2/2.3 and 3.3) stating that the possible extensions of a lower part depend only on a well-defined frontier.
3.  **Symmetry Handling**: The state must include the image of the automorphism group of the lower part, as you've done with Lemmas 2.4 and 3.4. This is the crucial ingredient for counting **unlabelled** objects.

### 💎 Summary

Your method is a powerful template. Beyond distributive and modular lattices, it is most naturally suited for other **graded** ordered structures. The most promising immediate extensions would be to **graded posets with avoidance conditions** and **semimodular/geometric lattices**, as these share the closest structural DNA with the objects you've already successfully tackled. The core insight—using a symmetry-aware frontier state to merge lower parts—is portable to any graded class where isomorphism is the primary obstacle to efficient enumeration.

(what is provable for the asymptotics?)



Some progress, and a useful reduction. I haven't proved the full conjecture, but I have identified precisely what is missing and found an existing theorem that establishes part of the asymptotics.

## **1. A result that is already provable: the exponential growth constant exists**

Write

\\[ v_n=d\_{\rm vi}(n),\qquad d_n=d(n). \\]

The vertical-decomposition recurrence is

\\[ d_n=\sum\_{k=2}^{n}v_kd\_{n-k+1}. \\]

Now define

\\[ a_j=v\_{j+1},\qquad s_j=d\_{j+1}. \\]

Then

\\[ s_0=1,\qquad s_n=\sum\_{j=1}^n a_js\_{n-j}. \\]

This is precisely the type of *summatorial sequence* studied by Erné, Heitzig and Reinhold (2002).

Their Corollary 11 proves that, provided the gcd of the support of \\(a\\) is one,

\\[ \lim\_{n\to\infty}s_n^{1/n} \\]

exists.

Here this condition is immediate: \\(a_1=v_2=1\\).

Consequently, we already have the rigorous result

\\[ \boxed{\lambda_d:=\lim\_{n\to\infty}d_n^{1/n} \quad\text{exists}.} \\]

This is stronger than merely having a limsup or liminf. It establishes a well-defined exponential growth rate, although not its numerical value or a constant-factor asymptotic.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://www.combinatorics.org\&sz=32)

combinatorics.org



Interestingly, the same theorem also applies to the vertically indecomposable counts. In their canonical 2-decomposition, Erné et al. obtain

\\[ v(x)=\frac{1}{1-W(x)}, \\]

where \\(W\\) counts canonically 2-indecomposable posets. Their sequence has \\(w_2=w_9=1\\), so the support has gcd one. Thus

\\[ \boxed{\lambda_v:=\lim\_{n\to\infty}v_n^{1/n} \quad\text{also exists}.} \\]

[image](https://www.google.com/s2/favicons?domain=https://www.combinatorics.org\&sz=32)

combinatorics.org+1

This gives us two well-defined growth constants to compare.

## **2. A sufficient condition for the conjectured asymptotic**

Define

\\[ V(z)=\sum\_{k\ge2}v_kz^{k-1}, \qquad D(z)=\sum\_{n\ge1}d_nz^{n-1}. \\]

The recurrence gives

\\[ D(z)=\frac{1}{1-V(z)}. \\]

Here is a useful theorem for your problem.

**Proposition.** Suppose that

\\[ \lambda_v<\lambda_d. \\]

Then there exists \\(C>0\\) such that

\\[ \boxed{d_n\sim C\lambda_d^n.} \\]

*Proof.*

Put \\(r=1/\lambda_d\\).

Since \\(\lambda_v<\lambda_d\\), the radius of convergence of \\(V\\) is strictly greater than \\(r\\). Thus \\(V\\) is analytic in a neighbourhood of the closed disk \\(|z|\le r\\).

Since \\(d_n^{1/n}\to\lambda_d\\), the radius of convergence of \\(D\\) is exactly \\(r\\).

For \\(0\le x\<r\\), we have \\(V(x)<1\\). By continuity, \\(V(r)\le1\\).

But \\(D\\) has a singularity at the positive real point \\(r\\), by Pringsheim's theorem. Since \\(V\\) is analytic there, the identity \\(D=1/(1-V)\\) implies

\\[ V(r)=1. \\]

Furthermore,

\\[ V'(r)>0, \\]

because \\(v_2=1\\).

Therefore \\(D\\) has a simple pole at \\(r\\).

There cannot be another pole on \\(|z|=r\\): equality in

\\[ |V(z)|\le V(|z|)=1 \\]

would require all nonzero terms to have the same argument. Since the coefficient of \\(z\\) is positive, this requires \\(z=r\\).

Analyticity beyond the circle and uniqueness of the dominant pole now give

\\[ d_n\sim \frac{1}{V'(r)}r^{-n}. \\]

Hence

\\[ \boxed{C=\frac{1}{V'(1/\lambda_d)}.} \\]

\\(\square\\)

This is exactly the simple-pole argument suggested in Section 2.4 of your paper, but now with its missing hypothesis made explicit.

paper.pdf

## **3. What is actually missing?**

It is the strict inequality

\\[ \boxed{\lambda_v<\lambda_d.} \\]

The available bounds are unfortunately insufficient:

| Quantity                                                         | Rigorous bound                  |
| ---------------------------------------------------------------- | ------------------------------- |
| \\(\lambda_v\\), vertically indecomposable distributive lattices | \\(1.7250\le\lambda_v\le2.33\\) |
| \\(\lambda_d\\), all distributive lattices                       | \\(1.84\le\lambda_d\le2.39\\)   |

The lower bound for \\(\lambda_v\\) is improved by Kohonen; the upper bound comes from the coding argument of Erné et al.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://d-nb.info\&sz=32)

d-nb.info+2



The intervals overlap substantially.

Your new computations suggest

\\[ \lambda_v\approx1.7265,\qquad \lambda_d\approx1.84337, \\]

but the finite computations through 160 cannot establish the strict inequality.

There is also a more elementary way of expressing the missing condition. We need to establish that

\\[ \sum\_{k\ge2} v_k\lambda_d^{-(k-1)}=1 \\]

with sufficient convergence control, and preferably that the corresponding first moment is finite. The strict growth-rate inequality supplies both automatically.

## **4. Can the existing frontier method help?**

I think this is where the most promising new work lies.

Your frontier algorithm does something the earlier enumeration approaches did not: it merges partial constructions according to a finite mathematical summary of what remains possible above them.

The empirical state growth is remarkably slow compared with the growth of the number of lattices. At \\(N=160\\), you have 17.5 million states, against approximately \\(10^{36}\\) vertically indecomposable lattices.

There may be an opportunity to turn this into a rigorous asymptotic argument.

One possible strategy:

1. Partition the distributive lattices according to frontier size and structure.
2. Prove an exponential upper bound for the contribution of large frontiers.
3. Show that the remaining small-frontier contribution can be bounded using a finite transfer system.
4. Establish an upper bound \\(\lambda_v<1.84\\), or at least \\(\lambda_v<\lambda_d\\).

The difficulty is step 2. The observed state counts do not themselves establish a uniform bound on the number of paths through those states.

Nevertheless, this is a more concrete programme than trying to infer convergence of ratios from increasingly large tables.

## **5. What about modular lattices?**

The analogous vertical-decomposition recurrence also holds:

\\[ M(z)=\frac{1}{1-W(z)}, \\]

where \\(W\\) is the generating function of vertically indecomposable modular lattices.

But the paper's observations of increasing successive ratios at \\(n=35,36\\) are not enough to establish an asymptotic regime. There is not yet an equivalent useful strict-growth-separation result for that problem.

paper.pdf

## **My recommendation**

I would add the root-limit theorem to your paper's discussion, cite Erné et al., and explicitly state the following hierarchy of results:

- **Proved:** Both \\(d_n^{1/n}\\) and \\(v_n^{1/n}\\) converge.
- **Numerically strongly supported:** Their limits are approximately 1.84337 and 1.7265, respectively.
- **Still open:** Proving that the two limits are strictly different.
- **Consequence:** That strict inequality would establish the conjectured simple-pole asymptotic \\(d_n\sim C\beta^n\\).

This also gives a particularly clean mathematical research question:

**Prove that the number of vertically indecomposable distributive lattices grows strictly more slowly, exponentially, than the number of all distributive lattices.**

That is the real missing theorem. And it is considerably more interesting than proving that a sequence of numerical ratios happens to settle down.
