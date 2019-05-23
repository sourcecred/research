Contextualizing Cred
=
**SourceCred Research Status Report**
*Michael Zargham*
5/13/2019

see hackmd for version with rendered math
- https://hackmd.io/s/SkY7VvQnV

see medium for distilled versions of the sections with computational experiments:
- https://medium.com/sourcecred/exploring-subjectivity-in-algorithms-5d8bf1c91714
- https://medium.com/sourcecred/network-formation-games-7a74491abf0e

Next steps
- break this file out into individual files for each section so that its easier to work with/learn from

## Introduction

**Replace intro with references to the Introductory Medium Article.**
https://medium.com/sourcecred/introduction-to-sourcecred-7665297af715

The primary goal of the research outlined below is to leverage experience and knowledge [DFS - *Leverage whose experience and knowledge and for what purpose?*] of network science and socio-technical systems in the context of SourceCred. SourceCred's prototypical use case is an open source development project, but its potential scope extends beyond software development labor to research, design, narrative, logistics, and even emotional labor. This document will use the term "co-creative community" to name the abstraction that encompasses the prototpical and the extension use cases. The goal of SourceCred is to provide a utility for quantifying relative contributions of individuals to the goals of co-creative communities.

Such a broad goal creates product design and development challenges because the defining properties must be characterized for abstractions, and yet implemented and tested for specific cases. SourceCred bootstraps this abstraction challenge by leveraging a mature yet very general theory of credit attribution, using graph data structures and the PageRank class of algorithms. SourceCred solves the implementation challenge by leveraging a plugin architecture which allows any particular instance of SourceCred to be defined with data sources specific to the community using it, rather than presuppose the space of all possible contributions.

As part of this research document, an abstract formalism for a credit attribution network with minimal assumptions on the nature of those contributions is presented in the Preliminaries section. Then building upon this abstraction, the PageRank Algorithm section will explore the PageRank algorithm itself as a tool for providing "spatial-context" dependent scores using Personalized PageRank. Experiments that explore the sensitivity of this algorithm to its parameters are also presented in this section. Next in the Temporal Context section, this model will be extended to include temporal dyanmics. Various methods of interpreting the evolution and accumulation of Cred will also be discussed. The Sociotechnical Feedback Loops section discusses the feedback effects that Cred may have on co-creative community contributor behavior. In the final Conclusions and Next Steps section, future work focused on exploring the co-creative process as a network formation game will be introduced.

The reference post for motivating Cred as a context dependent measure of credit and or credibility in a co-creative community is:
[Contextual Cred;
Dandelion Man&eacute;](https://discourse.sourcecred.io/t/contextual-cred/99)

## Preliminaries

Consider an attribution graph according to convention in the network science literature: let $\mathcal{G}=\left(\mathcal{V},\mathcal{E}\right)$ denote an directed graph with $n$ vertices and $m$ edges. We
denote by
$\mathcal{V}=\left\{ 1,\dots,n\right\}$
the set of vertices and by
$\mathcal{E}\subseteq\mathcal{V}\times\mathcal{V}$
the set of directed edges of $\mathcal{G}$. Any node pair (i,j) is an edge 
$e=(i,j) \iff \left( i,j\right) \in\mathcal{E}$
and we call vertex $i$ *child* of *parent* vertex $j$, with the child-parent link
additionally denoted as $i\rightarrow j$.

### Graph Evolution

The contributions of a co-creative project evolve in time, thus it is necessary to characterize notion for a time varying attribution network. Time from the perspective of attribution network is event based: there is a new $\mathcal{G}$ when new nodes and/or edges are added by some action. 

Index events by $k$, where $k=0$ is the event that generated the initial attribution network. Then the graph update for any event $k$ is defined as
$\mathcal{G}_{k} = \mathcal{G}_{k-1} \oplus \Delta \mathcal{G}_k = (\mathcal{V}_{k-1} \oplus\Delta \mathcal{V}_k,\, \mathcal{E}_{k-1} \oplus\Delta \mathcal{E}_k)$
which is specically the addition of a new set of nodes $\Delta \mathcal{V}_k$ and a new set of edges $\Delta \mathcal{E}_k$ associated with event $k$.

For notational simplicity, the event index subscript $k$ will be neglected for the parts of this report where the evolution of the network is need directly under consideration. One can interpret this as $\mathcal{G} = \mathcal{G}_k$ for some $k$ representing a current snapshot. 

### Graph MetaData

Since every node in our attribution network is meant to be interpretable, there is going to be metadata that describes it. For the purpose of this general analysis, the abstract space of this metadata will simply be denoted $\mathcal{X(\mathcal{G})}$, but one can refer to the data about a node as $x_i$ for any $i \in \mathcal{V}$ and data about an edge as $x_e$ and any $e\in \mathcal{E}$.

Note that SourceCred graphs are multi digraphs. This means, in general, we can have more than one edge $i\rightarrow j$ for any pair of nodes $i,j\in \mathcal{V}$. For notational simplicity, and without loss of generality, assume this additional level detail about the relationship $e=(i,j)$ is stored in the data $x_e$. This further implies that $x_e$ may change during graph update $\mathcal{G}_{k} \leftarrow \mathcal{G}_{k-1}$.

### Weighted Graphs

The network defined so far only contains the relationships' information and metadata. In SourceCred, nodes and edges have weights which are determined by *heuristics*. The choice of weight heuristic encodes a perspective on the importance of different kinds of contributions. These heurisitcs may have default settings, but they are configurable by the user to ensure that the software does not take too heavy a hand in defining how contributions are valued by the co-creating community.

Define the set of weight-generating rules for nodes $h$ and set of weight-generating rules for edges $H$; then the weight of any particular node

$w_i= w_{(i,i)} = h(x_i) \ge 0$ given that $i \in \mathcal{V}$
where $w_i$ is interpreted as a self-loop $i\rightarrow i$. (In graph theory, self-loops are edges that connect a node to itself. In SourceCred, a self-loop is a mechanism for ensuring the 'stickiness' of the cred for a particular node in the attribution network.)

Note that in SourceCred graphs Cred may flow both up and down a directed edge:

$w^{down}_{(i,j)} = H(x_e, x_i, x_j)>0$ given that $e=(i,j) \in\mathcal{E}$
$w^{down}_{(i,j)} = 0$ that $e=(i,j) \not\in\mathcal{E}$

$w^{up}_{(i,j)} = H(x_e, x_i, x_j)>0$ given that $e=(i,j) \in\mathcal{E}$
$w^{up}_{(i,j)} = 0$ that $e=(i,j) \not\in\mathcal{E}$

$w_{(i,j)} = w^{down}_{(i,j)} + w^{up}_{(j,i)}$


If a heuristic choice $H$ maps an edge weight $w_e=0$, that heuristic can be said to be filtered out by the Heuristic[DFS - *Confusing nomenclature, heuristic vs Heuristic. Also, not a sentence.*]. That is to say the edge is not present in the weighted graph, even if it was present in the unweighted graph. Further note that in SourceCred graphs Cred may flow both up and down a directed edge. Therefore the total weight associated with a link $i \rightarrow j$ is the downstream weight assigned to edge $(i,j)$

In the current implementation of SourceCred, the self-loops [DFS - *Self loops popped out of nowhere. What are they, and whay are they important?*] are uniform for all nodes and the edge weights are determined by the edge type and destination node type.


### Markov Chains

A weight graph can be interpreted as having a mixing process if one normalizes each flow by weighted outdegree of its source node. This is generally specificied using an $n \times n$ dimensional sparse matrix $W$ where the elements are the weights
$W_{ij} = w_{(i,j)}$ for all $i,j\in\mathcal{V}$
which by our definitions in the previous section results in a matrix sharing the sparsity pattern of the graph; also called a weighted adjacency matrix. The outdegree is given by
$d_i = \sum_{j\in \mathcal{V}} W_{ij}$
Normalize to get the Markov chain matrix $M$ where
$M_{ij} = \frac{W_{ij}}{d_i}$
which is a row stochastic matrix. The initial implementation of SourceCred uses the stationary distribution of the Markov chain $M$ created by applying a heuristic $H$ to a graph $\mathcal{G}$ to assign Cred to each node in the network. The distribution is the eigenvector of $M$, associated with the eigenvalue 1.

A recommended reference for computing Markov Chain stationary distributions locally is:
[Computing the Stationary Distribution, Locally;
Christina E. Lee, Asuman Ozdaglar, Devavrat Shah](https://github.com/sourcecred/research/blob/master/references/StationaryDistribution.pdf)

### Example

The SourceCred prototype, prior to the Odyssey Hackathon and subsequent updates to be discussed in the next section, uses the git and github plugins to build a data set containing actions from the git workflow. A stylized representation of the data in a git workflow is the following:

> ![gitflow](https://i.imgur.com/Nki8Cxr.jpg)
> Figure from [Multiclass PageRank](https://github.com/sourcecred/research/blob/master/references/multiclassPageRank.md) in SourceCred/Research

> ![sourcecred](https://i.imgur.com/9ZgZd5s.jpg)
> A zoomed out view the SourceCred/SourceCred repo's actual network. Plot Courtesy of Ryan Morton

Note the full network visualization is difficult to parse. The large purple circle is the SourceCred repo itself. The smaller pink circles are the core developers Dandelion and William. All of the other contributions are essentially in orbit around these three large masses of Cred.

> These scores were computed using the default heuristic configuration shown below.
> 
> ![](https://i.imgur.com/4TOaHoC.png)
> 
> and a (truncated) leaderboard for Cred (with contributions aggregated by Issue) helps clarify the results.
> 
> ![](https://i.imgur.com/LKLES41.png)
> Prototype is hosted at [https://sourcecred.io/prototypes/sourcecred/sourcecred/](https://sourcecred.io/prototypes/sourcecred/sourcecred/)

### Limitations

At this stage, the SourceCred codebase is high quality and functionally capable of generating valid scores. As a baseline the technical implementation is successfully deployed, but the user experience, social science, and algorithm design questions are still open. 

The simplest experimentation shows that the results are relatively insensitive to changes in weighting heuristics. More importantly however, it is hard to tell if cred beyond the top contributors is a meaningful metric. Issues or pull requests that have been given large amounts of cred are not obviously important contributions. One would hope to empirically, albeit anecdotally, confirm that high cred contributions had some structural or functional importance to the project.

On the other hand, it may be that looking at the Markov process's stationary distribution simply doesn't provide enough control of the algorithm's perspective to select a metric that reflects Cred. In the next section, PageRank and Personalized PageRank will be discussed as means of providing spatial context for cred scores. Care also has to be taken to prevent overcontrol of the algorithm's perspective such that arbitrary results can result such as favoring pet contributors.

## Spatial Context

Using the stationary distribution of Markov Chain as a measure of importance of nodes in a graph is a global metric without mechanism for specifying a measure relative to a particular node or set of nodes which are of interest to the observer[DFS - *Confusing. Should be more than one sentence.*].

As part of our explorations into the values and goals of SourceCred, we determined that a project using SourceCred should be able to define values and goals for itself and, in turn, award cred relative to any of these goals. We made two important advancements out of this discussion:
 1. It is necessary to be able to manually add nodes and edges in order to make goals and values explicit parts of the network, and to connect these nodes to other contributions.
 2. It is necessary to be able to compute Cred scores which are defined relative to the goals and values in order to identify not just contributions, but also meaningful feedback on the impact of those contributions.

The manual mode capability was protyped as part of the Odyssey Hackathon project and is currently being merged into the SourceCred/SourceCred code base.  For this researh report, the focus will be on item 2: extending the ranking algorithm from Markov Chain Stationary distributions to Personalized PageRank vectors, and the implications thereof.

For details on variations and applications of PageRank as a statistical ranking algorithm see:
[PageRank Beyond the Web;
David F. Gleich](https://github.com/sourcecred/research/blob/master/references/pagerank_surveypaper.pdf)

### PageRank Algorithm

The PageRank algorithm is defined by combining a Markov Mixing process with a linear driving function. The Markov Mixing process described as a dynamical system is
$\pi^+ = M \pi$
and its stationary distribution $\pi^*$ is precisely the fixed point of this system. A PageRank vector $r_{\vec{s},\alpha}$ is computed as
$r_{\vec{s},\alpha}^+ = (1-\alpha)M r_{\vec{s},\alpha}+ \alpha \vec{s}$
where $\vec{s}$ is a node dimensional seed vector and $\alpha\in (0,1)$ is the 'teleportation' probability which encodes how long diffusion process propogates through the network before it restarts from the seed again. The fixed point is given by
$r^*_{\vec{s},\alpha} = \alpha \big(I-(1-\alpha) M\big)^{-1}\vec{s}$
where $I$ is the identity matrix. While $\pi^*$ was an eigenvalue of the Markov Chain Matrix $M$, $r^*_{\vec{s},\alpha}$ has nuanced dependence on our choices of $\alpha$ and $\vec{s}$ which will be explored in the parameter sensitivity analysis subsection.

The fixed point of this process is called the Personalized PageRank when $\vec{s}$ is the indicator vector $\mathbb{1}(i)$ for a specific node $i$, then $\vec{s} =  \mathbb{1}(i)$ implies
$\vec{s}_i=1$ for node $i$ and 
$\vec{s}_j=0$ for all $i \not = j$.

This formulation is sufficiently general that one can use any stochastic vector $\vec{s}$ and get a score; however, the PageRank is a linear operator in the vector $\vec{s}$ so it is common practice to reason about the algorithm one source node at a time. This fits with our SourceCred use case because when adding nodes that represent specific goals or values, one can directly compute the distribution of cred to all other nodes relative to the goal or value node. This provides a mechanism to control the algorithm’s perspective without introducing arbitrary cred distributions. 

For simplicity, set $\alpha=.01$ and suppose node $v\in \mathcal{V}$ is a manually added node representing a design goal. If the maintainer wishes to assign 1000 Design Cred for accomplishing this design goal then the design Cred assigned to each other node is
$C_i = \vec{C}_i$ where
$C = 1000*\alpha \big(I-(1-\alpha) M\big)^{-1}\mathbb{1}(v)$.
Thus, each node in the network gets a share of the Cred as defined by row $v$ of the matrix 
$\alpha \big(I-(1-\alpha) M\big)^{-1}$.

First point of nuance, this distribution will allocate a potentially large proportion of the cred to the source node $v$. This is handled by computing the Cred distribution, and then dropping the value for node $v$ and renormalizing to sum to one.

Second point of nuance, the smaller the value of $\alpha$ the slower the simple local mixing process algorithm will converge. There are multiple approaches to accelerate convergence, some of which will be reviewed in the next subsection.

###
The convergence rate of a mixing process is bounded by the spectral gap of the matrix $M$. Recall that $M$ is a stochastic matrix with maximum eigenvalue equal to $\lambda_1=1$. Ordering the eigenvalues from from largest to smallest, denote the second largest eigenvalue $\lambda_2$. The convergence rate bound for the Markov Mixing process is $\lambda_2$. 

However for the PageRank iteration it gets slower as you decrease $\alpha$. This can be problematic as small $\alpha$ is desireable to allow cred to spread widely through network and to accumulate in pockets revealing critical path contributions.  In this section, the lazy random walk methods for accelerating conververgance will be introduced.

The lazy random walk perserves the resulting stationary distribution while accelerating convergence. In place of the PageRank iteration in the previous section, substitute:
$r_{\vec{s},\alpha}^+ = (1-\alpha)\frac{I+M}{2}r_{\vec{s},\alpha}+ \alpha \vec{s}$

This algorithm is Lazy in the sense that it adds strong self loops, which provide momementum and prevent oscillatory dyamics which slow convergence, especially near the beginning of the iteration. 


Let's first inspect a case where $\alpha =1$ and the seed vector is the SourceCred repo to see the oscillations.
```
iterations = 150

alpha = .01
seed = {n:0.0 for n in G.nodes}
seed[4392]=1.0 #4392 is the repo itself
self_loop_wt = 1/1000
```
Then we compute the PageRank using the research implementation with the Lazy Random walk turned off
```
r, df, g = pr.pageRanker(G,
                         alpha,
                         iterations,
                         seed=seed,
                         initial_value = seed,
                         lazy=False,
                         self_loop_wt=self_loop_wt)
```
I can plot the worst case differential for each iteration to see the convergence rate
```
df.diff().T.max().plot(logy=True)
plt.title('Convergence of PageRank Iteration')
plt.xlabel('iteration')
plt.ylabel("$\max_i\, c_i^{t+1}-c_i^t$")
```
![](https://i.imgur.com/9li42UV.png)


If we repeat the same experiment with the lazy random walk
```
r, df, g = pr.pageRanker(G,
                         alpha,
                         iterations,
                         seed=seed,
                         initial_value = seed,
                         lazy=True,
                         self_loop_wt=self_loop_wt)
```
the oscillations are smoothed out and the simulation actually reaches machine precision before the 150 iterations are up.
```
df.diff().T.max().plot(logy=True)
plt.title('Convergence of PageRank Iteration')
plt.xlabel('iteration')
plt.ylabel("$\max_i\, c_i^{t+1}-c_i^t$")
```
![](https://i.imgur.com/RefImyO.png)

It is important to note that the SourceCred/SourceCred network is still relatively small compared to SourceCred graphs that may exist in the future. As there is a need to further decrease $\alpha$ or as the graphs themselves get much larger, it may be necessary to use more advance acceleration methods. These methods leverage the a priori knowledge of the analytical exact solution and use iterative sparse matrix inverse approximations to achieve superlinear convergece rates. See the below for details:

[Fast Distributed Optimization Strategies for Resource Allocation in Networks;
Michael C. Zargham](https://github.com/sourcecred/research/blob/master/references/dissertation_final.pdf)

### Sensitivity to Subjective Parameters

*This subsection is [published](https://medium.com/sourcecred/exploring-subjectivity-in-algorithms-5d8bf1c91714) as a medium article on the SourceCred Medium page*


The vector called the PageRank is the stationary distribution of the random walks assuming those random walks start at a particular seed vector and that any particular random walk ends and new one is started with probability alpha, also known as the teleportation rate. It uses additional link metadata to give the links different weights, the resulting ranking could differ significantly.

Algorithm decomposition: the Graph G encodes relationships and potentially metadata for a set of nodes and edges, the heuristic h maps that data into weights for a mixing process W(G), and a metric is a mapping which uniquely defines a vector of rankings over the nodes in graph G.

Changing the seed vector will also significantly change the algorithms results; the canonical PageRank algorithm uses a uniform distribution over the nodes as the seed vector. The algorithm is referred to as Personalized PageRank when using a single node or a subset of nodes as the seed. The results can be interpreted as the importance of each node relative to the seed, in this case often referred to as the personalization vector. We have introduced our first notion of subjectivity. Even if we all agree on one heuristic for applying weights to the mixing process, we can arrive at different rankings simply by acknowledging a position in the network implies a unique perspective, and thus a unique ranking. I will demonstrate this affect using a simple reference case, a circle graph. This directed circle graph has a uniform canonical PageRank because it is symmetric.
> ![](https://i.imgur.com/rQiCNGG.png)
> ![](https://i.imgur.com/Ap5sydm.png )
>  Canonical PageRank for Directed Cycle with Uniform seed and alpha=0.1
> 
When the seed is changed from the uniform distribution to the Personalization vector for node 3, the symmetry is broken and the direction of the cycle is immediately apparent.

> ![](https://i.imgur.com/72cfKDI.png)
> ![](https://i.imgur.com/lhDur0Q.png)
> Node 3's personalized PageRank with alpha = 0.1


So for this is still pretty basic, selecting personalization vectors gives context dependent rankings but it doesn't yet scratch the surface of the family of mixing process based ranking algorithms, and the more subjective choices an algorithm designer makes (intentionally or unintentionally) affecting the outcome of the metric.

In order to examine these questions, let's expand our interpretation of the underlying network being hyperlinks and webpages to a more general attribution network. In this article, an *attribution network* is any directed graph where a link assigns credit (or credibility) from the source to the destination. Examples of such networks include academic citations, software dependencies and twitter style social networks (following assigns credibility). In introducing this form, we further parameterize our algorithm to allow our mixing process to flow both up and down a directed edge, albeit with different weights.

Using the the academic citations reference case, this assumption acknowledges that citing a well known reference my paper gains credibility, albeit not to the same degree it confers it. We will not require that the edges flow more weight downstream than upstream but it is a good convention to follow.

#### Why do we need a convention?
Because this a *subjective choice*, motivated by an intuition that when work A cites work B, A lends more credibility to B than B being cited lends to A. Now let's look at what happens to personalized PageRank in our circle graph when upstream downstream credit is conferred, but upstream flows have half the weight.

> ![](https://i.imgur.com/sv3e6OP.png)
> ![](https://i.imgur.com/y2pMAOc.png)
> Node 3's Personalized PageRank with upstream weights 1/2 power of downstream weights and alpha=0.1

A great deal more weight is capture by nodes 1 and 2which have the closest upstream links from node 3, but somewhat counter-intuitively the ranking of the nodes a but further downstream like 17 and 18, lost a lot of ground. This occurs because the ranking algorithm is stochastic vector, that is, it has a conserved sum of 1. In giving upstream nodes credit, nodes immediately downstream of the seed gained importance through the creation of short cycles, and the nodes further downstream lost out proportionally. An important message here is that even a well intentioned alteration to a simple algorithm can have unintended and undesirable consequences.

With this in mind, I would like to pose some simple reference cases with no 'right answer' per se. For purpose of this discussion let us suppose the links represent academic citations, and for plotting purposes, I will retain the assumption that credit flows upstream at half weight.

#### How should credit be distributed over a sequence of dependent papers?
(As represented by a line graph of 20 nodes)

If we simply take the canonical PageRank algorithm with no personalization something very strange happens. The algorithm considers the second from the end (node 18), not the end (node 19), interpreted as the first paper to the most important.

> ![](https://i.imgur.com/mgASoKG.png)
> ![](https://i.imgur.com/8UnqxmL.png)
> Canonical PageRank with uniform seed and upstream weights 1/2 power of downstream weights and alpha=0.1

Why does this happen? The mathematical answer is node 19 is disadvantaged by the fact that it sits on the boundary and receives no upstream credit. Most of us would intuitively prefer to node 19 at or above node 18, because it feels more consistent. However, others might argue that we could not have appreciated the work in node 19 without corroboration by node 18; in practice, there are a lot of cases where an early paper exists in near obscurity until other begin to build on it. Who is to say that node 19 should be more important than node 18.

Let's suppose we wish to rectified this perceived slight of the root node. I can do so with a simple change to the algorithm: introducing self loops at weight equal to the downstream citations.

> ![](https://i.imgur.com/7ojeEb9.png)
> ![](https://i.imgur.com/c2qZOiy.png)
> Canonical PageRank with uniform seed, self loop weights equal to downstream weights, and upstream weights 1/2 power of downstream weights, and alpha=0.1

Do the self loops make the algorithm better? It depends on who you ask. These algorithms are equally 'objective' in that they represent mathematical properties of a mixing process on the same graph. If you look carefully, our addition of self loops also improve node 0's score. Where the mixing model without self loops disadvantaged nodes on the edges, the self loops favor them.

Another salient feature of the line graph reference case is the rate the PageRank falls off. The uniform seed vector drives some base level of credit into every node and the mixing process allows it to diffuse throughout the network; the coefficient alpha can interpreted as the rate at which this credit is injected: larger alpha will drive the solution closer and closure to uniform PageRank and smaller alpha will allow the credit to diffuse much further resulting in more accumulation in pockets and thus a much wider spread between the largest and smallest values. Here is what happens when I set alpha = 0.001.

> ![](https://i.imgur.com/29RJDu6.png)
> ![](https://i.imgur.com/tTxQBlZ.png)
> Canonical PageRank with uniform seed, self loop weights equal to downstream weights, and upstream weights 1/2 power of downstream weights, and alpha=0.001

What happens in the case that node 0 is deemed to be an important discovery and the community is instead interested in how prior work deserves credit in making this possible? This context calls for a personalized PageRank, but does not indicate whether to keep the self loops, the upstream links or how to set alpha. I will demonstrate the result with self loops and half power upstream links, but acknowledge this choice is discretionary.

> ![](https://i.imgur.com/UEasz2D.png)
> ![](https://i.imgur.com/VE08Qg0.png)
> Personalized PageRank with node 0 as the seed, self loop weights equal to downstream weights, and upstream weights 1/2 power of downstream weights, and alpha=0.01

Since we are using a personalized PageRank the scores are very sensitive to our choice of alpha, so I have computed the results for a range of alpha values.

> ![](https://i.imgur.com/1qIfeRS.png)
> Personalized PageRank on Directed Line Graph with edges pointed in descending order, self loops weigth of 1 and upstream weight of 1/2, the seed is node 0

What stands out is that decreasing alpha shifts the credit from the most immediate dependencies to the earlier dependencies. If one believe the most foundational work was the most important, then a small alpha is required. On the other hand, if one believes that the most recent work leading up to the discovery deserves more credit, then a larger alpha is required. Personally, I like the result from alpha = 0.03 because allows value to accrue for foundational results while still heavily weighting work closer to the discovery.

That is however not something I plan for directly. The moment we change the network, the alpha that "feels right" or even an alpha optimized for a particular characteristic for one graph, will not necessarily have that characteristic on another graph. Let's examine a few more reference cases.

#### How should credit be distributed for Star Graph?
As one might expect the credit accumulates at the shared dependency.

> ![](https://i.imgur.com/e9Hzd77.png)
> ![](https://i.imgur.com/owL2jXC.png)
> Canonical PageRank with uniform seed, self loop weights equal to downstream weights, and upstream weights 1/2 power of downstream weights, and alpha=0.1

It is interesting to note that changing alpha has almost no affect at all on this reference case.

> ![](https://i.imgur.com/y2JjUXu.png)
> Canonical PageRank with uniform seed, self loop weights equal to downstream weights, and upstream weights 1/2 power of downstream weights, parameter sweep of alpha

A more interesting case arises when the direction of the star is flipped and a large number of unconnected references are used are referenced by one paper. Now the focus is on the relative power of the upstream weights. When the upstream weights are small as in the case below, the outer nodes all get more credit than the hub.

> ![](https://i.imgur.com/dz9deTT.png)
> ![](https://i.imgur.com/AnVPZpl.png)
> Canonical PageRank with uniform seed, self loop weights equal to downstream weights, and upstream weights 0.001 power of downstream weights, and alpha=0.1

However, as the upstream weights are increase this is reversed and the hub captures the lion share of the credit because it draws on the credibility of all of the references none of which have any other links from which to accrue credit.

> ![](https://i.imgur.com/pwUoqIx.png)
> ![](https://i.imgur.com/cxhTOnv.png)
> Canonical PageRank with uniform seed, self loop weights equal to downstream weights, and upstream weights 0.1 power of downstream weights, and alpha=0.1

This flip in importance can be examined by repeating experiments over a range of relative values for the upstream weights (relative to the weight of 1 assigned to downstream edges and self loops).

> ![](https://i.imgur.com/Sv3UmgW.png)
> Canonical PageRank with uniform seed, self loop weights equal to downstream weights, and alpha=.1, with parameter sweep of upstream weights

This change happens much more quickly than one might expect; the influence of the central node referencing all the others surpasses the referenced nodes in the periphery with less than 1% upstream weight. This brings to our attention an important fact about upstream weights; if they are even within an order of magnitude as downstream weights, a contributor wishing to pad their own ranking might spam references to elevate themselves in appropriately. However, one should also note that this reference case is hyper sensitive to upstream weights. We should examine a reference case where the dependencies are more spread out.

#### How should credit be distributed for Tree Graph?
In this reference case the network is directed binary tree of depth 4. The directed tree graph shares properties of both our line graph and our star graph. As was the case with the line graph, without self loops, the node with the root node actually receives less credit than its immediate predecessors.

> ![](https://i.imgur.com/eS9PeyP.png)
> ![](https://i.imgur.com/zjWWGoV.png)
> Canonical PageRank with uniform seed and upstream weights 1/2 power of downstream weights, zero self loops, and alpha=0.1

As was the case with the line graph, the inclusion of self loops with weight equal to the downstream links corrects for this effect.

> ![](https://i.imgur.com/zpZfcdt.png)
> ![](https://i.imgur.com/zd6Gzbp.png)
> Canonical PageRank with uniform seed and upstream weights 1/2 power of downstream weights, self loops weight equal to downstream weight, and alpha=0.1

As was the case with the star graph, switching the direction of the reference to fan out, rather than converge, highlights the effect of the upstream weights.

> ![](https://i.imgur.com/web2PFk.png)
> ![](https://i.imgur.com/vcxKBCT.png)
> Canonical PageRank with uniform seed and upstream weights 1/2 power of downstream weights, self loops weight equal to downstream weight, and alpha=0.1

Unlike the case of the star graph the node without only outbound reference does not accumulate a significant amount of credit. There is still however an interesting phenomena: the second to last layer accumulates the most credit per node in that layer. Further exploring how the credit accumulates in the layers it is clear that the depth 4, the last layer does still accumulate the most credit but it is spread out over more nodes.

> ![](https://i.imgur.com/Nlgz1zr.png)
> ![](https://i.imgur.com/EfKlta3.png)
> Canonical PageRank with uniform seed and upstream weights 1/2 power of downstream weights, self loops weight equal to downstream weight, and alpha=0.1

It is yet again not clear whether this is the behavior we want for a credit attribution algorithm. Choosing the strength of the of the upstream weights can significantly affect these credit distributions.

> ![](https://i.imgur.com/2BAjGMM.png)
> Canonical PageRank with uniform seed, self loop weights equal to downstream weights, and alpha=.1, with parameter sweep of upstream weights

Similar to the case of the star network, larger upstream weights drive credit to the node with no inbound links, but unlike the star network, those weight must be quite large the PageRank rises significantly.

Now, let's repeat experiment run on the line graph; suppose that the node that doesn't have any references to it yet is new breakthrough and we want to decide to allocate credit to prior work. Our personalized PageRank version of the above analysis will show us.

> ![](https://i.imgur.com/ZFIUpLi.png)
> ![](https://i.imgur.com/vty7oJW.png)
> PageRank with node 0 as the seed, self loop weights equal to downstream weights, and upstream weights 1/2 power of downstream weights, and alpha=0.01

Results indicate value still accumulates in the last two layers with the penultimate layer capturing the most per capita influence and the last layer capturing the most total influence.

> ![](https://i.imgur.com/F6EUGA3.png)
> ![](https://i.imgur.com/kbkq810.png)
> Personal PageRank with uniform seed and upstream weights 1/2 power of downstream weights, self loops weight equal to downstream weight, and alpha=0.1

Again, these results are very dependent on parameter choices. When sweeping the upstream weights parameter lower upstream weights shift the importance to nodes which come much further down the dependency graph. When sweeping the alpha parameter, smaller alpha shifts the credit further down the dependency graph.

> Personal PageRank with seed node 0 and self loops weight equal to downstream weight. 
> ![](https://i.imgur.com/i2oXqja.png)
> top: alpha=0.01 with parameter sweep upstream weights. 
> ![](https://i.imgur.com/O8KnIhs.png)
> bottom:upstream weights are 1/2 power of downstream weights, with parameter sweep on alpha

These two parameters have notably different effects on nodes in the intermediate depths; decreasing the upstream weights has a significant adverse affect on the nodes in the penultimate layer, whereas changing alpha causes little to no change on the credit attributed to these nodes.

#### I will conclude with one of my favorite experiments: 
What happens when a group of attackers contribute bogus content to the network, but start creating interconnected references among themselves?

In this reference case my project is made up of contributions in nodes 7 to 13, and my attack has submitted contributions 0 through 6 with one link to the rest of the project and a lot of internal links amongst their own contributions.

> ![](https://i.imgur.com/ODsXYfw.png)
> ![](https://i.imgur.com/abxpz3t.png)
> Canonical PageRank with uniform seed and upstream weights 1/2 power of downstream weights, self loops weight equal to downstream weight, and alpha=0.1

Well at first it doesn't look great. Due to the absence of links from the legitimate work clique to the bogus work clique the legitimate work has marginally higher PageRank, but not enough to be a meaningful defense from this kind of attack.

This is where seed vectors can be used as a form of trust anchoring. In an environment where some activity might be falsified in order to artificially inflate the credit of certain contributions, it is best to avoid the uniform seed which rewards sybil attackers and instead leverage a human knowledge to determine a seed comprised on human verified content.

Supposing instead of using the uniform seed, the same experiment is repeated with nodes 9 and 13 set as trusted seeds. The results are very different.

> ![](https://i.imgur.com/Iy154Jv.png)
> ![](https://i.imgur.com/bMbLA78.png)
> Personal PageRank with seeds 9 and 13, and upstream weights 1/2 power of downstream weights, self loops weight equal to downstream weight, and alpha=0.1

One might argue that these choices of trusted seeds are arbitrary and subjective! To which I will say of course they are, but what the person making this argument often fails to acknowledge was how much subjectivity was in the algorithm even before we allow human experts to decide the trusted seed.

Who decided whether and two what extend credit can flow upstream on links? Who decided whether there would be self-loops and how strong they are? Who decided what the alpha parameter should be? All of these are subjective choices and they have non-trivial ramifications on how credit is assigned, and once put into practice such a measure will have equally non-trivial affects on the behavior of participants seeking credit or compensation for their contributions.

To be clear, this isn't a statement about the PageRank algorithm, it is a statement about algorithms, and in particular algorithms used to reduce complex human efforts into quantitive boxes so we can compare them. There is no absolute objective measure of value. Every metric is objective conditioned on subjective choices of what to value. 

We make these subjective value judgements everyday, and there is nothing wrong with that, but when it comes to encoded our subjective value judgements into code, and implicitly or explicitly imposing them on others, it is our obligation as algorithm designs to be mindful of those subjective choices, and the impacts they can and will have on others.

### Odyssey Prototype

During the Odyssey Hackathon the SourceCred/SourceCred repo was forked and the Markov mixing process was changed into a Personalized PageRank iteration. The hack team constructed a manual data set representing the collaborative labor of a group of hackers and support team members to show how the outcome of that labor was a combined effort, and to highlight that SourceCred manual mode with Value and Goal nodes allows a creative team to value heterogenous contributions.

> ![](https://i.imgur.com/1oiBbkx.png)
> Odyssey Hackathon Prototype published [here](https://sourcecred.io/odyssey-hackathon/); created by *Dandelion Man&eacute;*.

In this example below, the Personalized PageRank seed vector is the project value "Narrative" and I've highlighted Abbey Titcombe who spent much the Hackathon working with various teams crafting an over-arching narrative about commons and community co-creation. One should also note that this cred graph includes valuing "emotional labor" and "logistics" which are forms of support labor than often go systematically undervalued due to low visibility, especially in highly technical domain.

The strength of encorporating spatial context in our thinking about SourceCred is that one can traverse the contribution graph (space) to to see what others are creating, which helps to reduce the observation bias where everyone thinks that their contributions and the contributions of those closest to them, or closest to the deliverables in the graph (space) are the most important.

### Limitations

The additional generality of personalized PageRank means that there is not a specific set of opimal parameters, the analysis above uses the some intuitive reference graphs to help reason about upstream weights as part of the heursistic choice $H$, personalization vectors $\vec{s}$ and the $\alpha$ parameter.

The intent of going through such a broad range of experiments on simple graphs is to equip a mainter or contributor to make informed decisions about the SourceCred parameters when choosing a perspective from which to view the data.

It is important note that this analysis still works within the paradigm of a single snapshot of Cred. Since the SourceCred is intended to help steward a dynamic collaborative effort, it is insufficient to restrict the analysis to snapshots. 

It is certainly the case that thinking spatially about Cred has helped us undestand a wider range of contributions, it also opens new challenges. What happens when connections are formed for support during one period of time, during an event or a deliverable. Do those links persist? How should the graph changing in time be related to how Cred is changing in time?

In the next section, the focus is understanding how to interpret the network changing over time.

## Temporal Context

In the preminaries section, the graph evolution process was introduced allowing to define a sequence of attribution networks:
$\mathcal{G_0}, \mathcal{G_1}, \mathcal{G_2}, \ldots$
where the $\mathcal{G_k}=\{\mathcal{V_k},\mathcal{E_k} \}$ is a snapshot of the sequence at a particular state in its evolution. In this section, Cred's dynamics in time as denoted by $k=0,1,2,\ldots$ will be discussed. 

As the material moves into temporal dynamics it is important to note that we're stepping away from a place where orthodox economic canon is directly applicable. The mathematical assumptions used in economic decision theory are based on utilities which collapse or ignore the temoral dynamics. A particular, domain of heterodox economics called ergodocity economics is focused on deriving and rederiving economic theories with temporal dynamics and stochastic process; this textbook is considered foundational material for any economic research involving stochastic dynamic process.
[Ergodicity Economics;
Ole Peters and Alexander Adamou](https://ergodicityeconomics.files.wordpress.com/2018/06/ergodicity_economics.pdf)



### Snapshots of Cred over time

Up until this point, all mappings defined where applied to a snapshot simply denoted $\mathcal{G}$.  Recalling that that our Cred metric is characterized first by a weighting heuristic $W=H(\mathcal{G})$ and then computing Personalized PageRank with teleportation parameter $\alpha$ and seed vector $\vec{s}$. To simplify notation, used $R_{\alpha,\vec{s}}(W)$ to denote the mapping from the weighted Adjacency matrix to the PageRank vector. 

Therefore, given $H$, $\vec{s}$ and $\alpha$ our ranking is:

$\mathcal{G_k} \rightarrow W(\mathcal{G_k}) \rightarrow R_{\alpha,\vec{s}}(W)$

Initially, assume that $H$, $\vec{s}$ and $\alpha$ are fixed with respect to time and the Cred sequence over time is characterized as $\vec{r}_k = R(W(\mathcal{G_k}))$ bearing in mind that since the network is growing the dimensionality of both $\vec{r}$ and $\vec{s}$ is actually growing. The assumption that $\vec{s}$ remains constant is appropriate because $\vec{s}= \mathbb{1}(i)$ for a goal or value node $i\in\mathcal{V}_0$.

Thus the sequence of cred rankings
$\vec{r_0},\vec{r_1},\vec{r_2} \ldots$
is well defined even though the dimension of the vectors is expanding. For additional considerations for expanding statespace dynamical systems see:
[A State-Space Modeling Framework for Engineering Blockchain-Enabled
Economic Systems;
Michael Zargham, Zixuan Zhang, Victor Preciado](https://arxiv.org/pdf/1807.00955.pdf)

This framing of cred covers the basic case in its entirety by observing that selection of $\vec{s}$ defines the type of cred, for example "design cred" comes from setting $\vec{s}=  \mathbb{1}(i)$ where $i$ is the goal node "design" and we can get "users design cred" by selecting from $[\vec{r}_k]_j$ only the values where node $j$ is type 'user'.

It is important to note that these selections operations occur at different points in the calculation. The selection of $\vec{s}=  \mathbb{1}(i)$ occurs before the ranking and $[\vec{r}_k]_j$ occurs after. Filtering to 'users' before the ranking would break the graph and render the ranking useless. 

### Cumulative and Smoothed Cred

Even in the case where the parameters $H$, $\vec{s}$ and $\alpha$ the evolution of the underlying graph $\mathcal{G_k}$ leads to rather jerky variations of the ranking $\vec{r_k}$. Furthermore, the PageRank operation produces stochastic vectors so users may see their cred fall as an effect of the ongoing contributions of others in a manner that could undermine the desired cooperative behavior.

In order to address the jerky behavoir of the signal $\vec{r_k}$ one can introduce smoothed weighted average as a low pass filter, Smoothed Cred with memory $\gamma$ is given as

$\bar r_k = \gamma\bar r_{k-1}+(1-\gamma) \vec{r}_k$

noting that newly added nodes $j$ at time $k$ have their smoothed cred initialized as $[\bar{r}_k]_j = [\vec{r}_k]_j$. The effect of this smoothing will be further discussed in the section on computational experiments.

Cumulative Cred forgoes the smoothed averaging for a simple sum over time.

$\tilde{r}_k = \tilde{r}_{k-1}+\vec{r}_k$

noting that newly added nodes $j$ at time $k$ have their cumulative cred initialized as $[\tilde{r}_k]_j = [\vec{r}_k]_j$. The cumulative cred addresses the question of users cred going down in time by accumulating it. A user whose contributions are decreasing in PageRank will experience a slowing growth rate in cred. 

### Dynamic Release Cred

The cumulative cred concept is particularly useful if it is combined with a dynamic release of time varying volume $\vec{v_t}$ cred from the source nodes where

$[\vec{v_t}]_i\ge 0$ for some goal or value node $i$

then the dynamic release cred is cumulative cred associated with $i$ with a total volume in time

$V_i=\sum_{\tau=0}^t[\vec{v_\tau}]_i$

and for a group of value and goal 'source' nodes $\mathcal{S} \subset \mathcal{V_0}$, define the vector of total cred volumes

$\vec{V}=\sum_{\tau=0}^t\vec{v}_\tau$

this results in the metric dynamic cumulative cred matrix 
$\mathbf{C}_t \in \mathbb{R}_+^{|\mathcal{V}_k|} \times \mathbb{R}_+^{|\mathcal{S}|}$
which depends on the sequences $[\vec{v_t}]$ where $|\mathcal{V}_k|$ is the number of nodes in the network $\mathcal{G}_k$ and $|\mathcal{S}|$ is the set of cred source nodes:

$\mathbf{C}_t=\mathbf{C}_{k-1}+\big[\cdots\big|\,[\vec{v_t}]_i\cdot\vec{r}^{[\vec{s}=\mathbb{1}(i)]}_k\,\big| \cdots\big]$

where $\vec{r}^{[\vec{s}=\mathbb{1}(i)]}_k$ is the Personalized Pagerank of network $\mathcal{G}_k$ with seed vector $\vec{s}=\mathbb{1}(i)$ where $i \in \mathcal{S}$. Note the switch from the $k$ index to $t$. It is not assumed that cred is released at every graph mutation event $k$ but every cred release event $t$ must occur at some point between graph mutuations $k$ so the computation of $\mathbf{C}_t$ always occurs on network $\mathcal{G}_k$ where $k$ was the most recent graph mutation event. As with the cumulative and smoothed cred, the statespace is expanding so nodes $j$ which appear for the first in some $\mathcal{G_k}$ that falls between $t-1$ and $t$ initialize as

$[\mathbf{C}_t]_j= Row_j\big[\cdots\big|\,[\vec{v_t}]_i\cdot\vec{r}^{[\vec{s}=\mathbb{1}(i)]}_k\,\big| \cdots\big]$.

To wrap up this subsection, note that this collection of cumulative dynamic cred scores combined with a maintainer defining the goals and values $\mathcal{S}$, the sequence of volumes of cred released $\vec{v_t}$, and the links to the value nodes $\mathcal{S} \times \mathcal{V_k} \subset \mathcal{E}_k$ provides an sufficient degrees of freedom to shift new cred accumulations to more recent work while still continuing to reward older contributions to the extent that they are still heavily relied upon by the newer contributions.

### Time Varying Heuristics

The maximum degrees of freedom are realized if the parameter $\alpha$ and the weighting heuristic $H$ are allowed to vary in time. As a user of SourceCred exploring the data, one should be free to adjust the weighting Heuristic as one sees fit in order to see the current ranking snapshot $\vec{r_k}$ from any perspectives. However, leaderboards containing smoothed and cumulative Cred scores depend on history and it infeasible to maintain the whole historical trajectory of the network $\mathcal{G_k}$ for $k=0,1,2,\ldots$ in order to compute these metrics for any $H$.

A specific suggestion from Denis Kudinov is to define a small set $\mathcal{H}$ of heurstics which are designed to capture unique perspectives of a set of user personas. This is a good middle ground, for maintaining flexibility while avoid storage and computation explosions. This would extend our matrix $\mathbf{C}_t \in \mathbb{R}_+^{|\mathcal{V}_k|} \times \mathbb{R}_+^{|\mathcal{S}|}$ to a tensor  $\mathbf{C}_t \in \mathbb{R}_+^{|\mathcal{V}_k|} \times \mathbb{R}_+^{|\mathcal{S}|}\times \mathbb{R}_+^{|\mathcal{H}|}$. This is relatively straightforward as it is just $|\mathcal{H}|$ copies of the same computations in previous subspection; it is recommended that $|\mathcal{H}|<=3$.

Tuning the $\alpha$ parameter should be under taken with care but as long as it is not changed too much too quickly this is a modest adjustment which can help keep the dynamic release cumulative cred from being seriously gamed by parties attempting to maximize their credit without care for the real value of their contributions.

As with $\alpha$, making the weighting heuristics $H\in \mathcal{H}$ time dependent is an intuitive approach to counter gaming; as with $\alpha$ changing it slowly is suggested. Especially, if there is financial reward associated with Cred generated through this process, it may be important the bound the rate that $H$ or $\alpha$ can be changed in time to establish trust in the community that the rewards are not being manipulated, even as adaptability is retained. An important concept here is seperation of time scales; for more on this topic see:

[MULTISCALE INFORMATION AND UNIVERSALITY;
Yaneer Bar-Yam](https://necsi.edu/multiscale-information-and-universality)
### Computational Experiments

An initial framework for analyzing various measures associated with evolving attribution networks was created using scientific python. This experimental appartus was created leveraging the complex adaptive system modeling framework developed internally at BlockScience in addition to the networkx package form managing graph data structures. In the interest of making research progress this code is in pre-infra state and requires engineering rather than research bandwidth in order to refactor and source control for use as infra. Given that SourceCred provides users choices over how to configure the algorithm parameters in their own instances, this research infra code may serve as thebasis for tooling allowing maintainers to analyze their attribution graphs more deeply to make decisions about parameter governance and monitor the network for gaming behavior.

> Examine the existing SourceCred/Research repo's attribution network as a starting point:
> ![](https://i.imgur.com/LTuMyUE.png)
> networkx plots will eventually be replaced with easier to read d3 plots based on the ongoing work of Ryan Morton

In order to do time analysis of Cred metrics for time varying networks, we first reduce the network to a subgraph containing the repo itself, three issues, the users, and few comments to keep the network connected.

> ![](https://i.imgur.com/qvdAzNB.png)
> The choice of $\mathcal{G}_0$ for our dynamic graph Cred Analysis

Let's examine the initial Snapshot PageRank scores using the Research Repo itself as the source of Cred, which then flows to the users and comments through the issues.
```python=
#set up the pagerank algorithm params
iterations = 25

alpha = .01
seed = {n:0.0 for n in base_graph.nodes}
source_id = get_nodes_by_type(smaller_base_graph, 'github/repo')[0]
seed[source_id]=1.0 #source_id is the repo itself
self_loop_wt = 1/1000

_,_, network= pr.pageRanker(smaller_base_graph,
                         alpha,
                         iterations,
                         seed=seed,
                         initial_value = seed,
                         lazy=True,
                         self_loop_wt=self_loop_wt)
```

> The code above plotted using networkx built-in functions and node size proportional to pagerank. The seed denoted in red.
> ![](https://i.imgur.com/Wu2lTNd.png)

The default SourceCred heuristics where used:
```python=
#tuples are (to_weight, from_weight)
default_edge_wt_by_type = {
    'github/authors': (0.5,1),
    'github/hasParent':(1,1/4),
    'git/hasParent':(1,1/4),
    'github/mentionsAuthor': (1,1/32),
    'github/mergedAs':(.5,1),
    'github/references':(1,1/16),
    'github/reactsHeart':(2,1/32),
    'github/reactsHooray':(4,1/32),
    'github/reactsRocket':(1,0),
    'github/reactsThumbsUp':(1,1/32)
    }

default_node_wt_by_type = {
    'github/issue':2.0, 
    'github/repo':4.0, 
    'github/comment': 1.0, 
    'git/commit':2.0, 
    'github/user':1.0,
    'github/bot':1.0,
    'github/review': 1.0, 
    'github/pull': 4.0
    }
```

Having already extensively explored the Personalized PageRank parameter sensitivity in the previous section, we will move on to  demontrating a graph evolution $\mathcal{G}_0$ to $\mathcal{G}_1$ where a new user joins the network by making adding a comment.

```python=
def synthetic_new_user(g, include_comment= True):
    graph=g.copy()
    new_node_id = len(graph.nodes)
    graph.add_node(new_node_id)
    graph.nodes[new_node_id]["type"] = 'github/user'
    graph.nodes[new_node_id]["address"] = ('sythethic','','','','SyntheticUser'+str(new_node_id))
    
    if include_comment:
        graph = synthetic_random_comment(graph, author_input=new_node_id)
    
    return graph
```
Generating synthetic randomized attribution networks for repeating experiments is accomplished through focusing on how comments reference each other, the authors and the issues. 
```python=
def synthetic_random_comment(g, author_input='random'):
    graph=g.copy()
    
    new_node_id = len(graph.nodes)
    graph.add_node(new_node_id)
    graph.nodes[new_node_id]["type"] = 'github/comment'
    graph.nodes[new_node_id]["address"] = ('sythethic')
    
    #pick an author
    author_candidates = get_nodes_by_type(graph, 'github/user')
    if author_input in author_candidates:
        author = author_input
    else:
        author = np.random.choice(author_candidates)
    
    author_edge_id = (author, new_node_id, edge_count(graph,author,new_node_id))
    graph.add_edge(author, new_node_id)
    graph.edges[author_edge_id]['type'] = 'github/authors'
    graph.edges[author_edge_id]['address'] = ('sythethic')
    
    #pick the thing being commented on
    commented_on_candidates = get_nodes_by_type(graph, 'github/comment') \
        + get_nodes_by_type(graph, 'github/review')\
        + get_nodes_by_type(graph, 'github/issue')  
    
    commented_on =  np.random.choice(commented_on_candidates)
    commented_on_edge_id = (new_node_id, commented_on, edge_count(graph,new_node_id, commented_on))
    graph.add_edge(new_node_id,commented_on)
    graph.edges[commented_on_edge_id]['type'] = 'github/hasParent'
    graph.edges[commented_on_edge_id]['address'] = ('sythethic')
    
    
    #pick some references
    refs_candidates =  get_nodes_by_type(graph, 'github/issue') \
        + get_nodes_by_type(graph, 'github/user') \
        + get_nodes_by_type(graph, 'github/review')
    
    #number of references
    mu = 2 #expected number of references
    num_refs = sts.poisson.rvs(mu)
    
    refs = np.random.choice(refs_candidates,2, replace=False)
    for ref in refs:
        if graph.nodes[ref]["type"] == 'github/user':
            ref_type = 'github/mentionsAuthor'
        else :
            ref_type ='github/references'
        
        ref_edge_id = (new_node_id, ref, edge_count(graph,new_node_id, ref))
        graph.add_edge(new_node_id,ref)
        graph.edges[ref_edge_id]['type'] = ref_type
        graph.edges[ref_edge_id]['address'] = ('sythethic')
    
    return graph
```

> ![](https://i.imgur.com/uSh8j8f.png)
> Shows the subgraph of $\mathcal{G_1}$ that is connected to the new new nodes in $\Delta \mathcal{V}_1$. 

For the purpose of computational experiments the network update is packaged up into a dynamical system with the graph itself embedded in the system state:
```python=
initial_conditions = {'cred':cred,
                      'cumulative_cred':cred,
                      'time_weighted_cred':cred,
                      'network':network}
```
At each timestep, randomly determine whether the contribution comes from an existing user or a new user
```python=
def random_contribution(params, step, sL, s):
    
    network = s['network']
    users = get_nodes_by_type(network, 'github/user')
    num_users = len(users)
    
    rv = np.random.uniform(0,1)
    #probability of new user ~ .2
    thresh = .2
    new_user = bool(rv<thresh)

    return({'new_user':new_user})
```
Then the network is updated with a random comment, and a set of metrics are computed and stored in the networkx object in the dynamical system state

```python=
def update_network(params, step, sL, s, _input):
    
    prior_network = s['network']
    
    if _input['new_user']:
        new_network = synthetic_new_user(prior_network)
    else:
        new_network = synthetic_random_comment(prior_network)
    
    _,_,new_network = pr.pageRanker(new_network,
                         alpha,
                         iterations,
                         seed=indicator_of(new_network,source_id),
                         initial_value = indicator_of(new_network,source_id),
                         lazy=True,
                         self_loop_wt=self_loop_wt)
    
    for node in new_network.nodes:
        if node in prior_network.nodes:
            new_network.nodes[node]['cumulative']=prior_network.nodes[node]['cumulative']\
                +new_network.nodes[node]['score']
            new_network.nodes[node]['time_weighted']=gamma*prior_network.nodes[node]['time_weighted']\
                +(1-gamma)*new_network.nodes[node]['score']
        else:
            new_network.nodes[node]['cumulative']= new_network.nodes[node]['score']
            new_network.nodes[node]['time_weighted']=new_network.nodes[node]['score']
    
    key = 'network'
    value = new_network 
    
    return (key, value)
```
All of the data collected about the evolution of the graph is stored in the network state trajectory but since the implementation of this system will not preserve the trajectory of the network, state variables encoding the values of each metric at each timestep are stored as top level state variables as well (but these update functions are not shown here). 

The partial state update blocks are wired together to create a dynamical system using the cadcad engine api:
```python=
partial_state_update_blocks = [
    { 
        'policies': { # The following policy functions will be evaluated and their returns will be passed to the state update functions
            'random': random_contribution
        },
        'variables': { # The following state variables will be updated simultaneously
            'network': update_network
            
        }
    },
    {
      'policies': { # The following policy functions will be evaluated and their returns will be passed to the state update functions 
        },
        'variables': { # The following state variables will be updated simultaneously
            'cred': update_cred,
            'cumulative_cred': update_cumulative,
            'time_weighted_cred':update_time_weighted
        }
    }
]
```
To generate a system trajectory we set the simulation parameters and use the cadcad engine
```python=
simulation_parameters = {
    'T': range(T), #length of one experiment
    'N': 1, #number of monte carlo experiments
    'M': {} #additional arguments for parameter sensitivity analysis
}

# The configurations above are then packaged into a `Configuration` object
config = Configuration(initial_state=initial_conditions, #dict containing variable names and initial values
                       partial_state_update_blocks=partial_state_update_blocks, #dict containing state update functions
                       sim_config=simulation_parameters #dict containing simulation parameters
                      )
                      
exec_mode = ExecutionMode()
exec_context = ExecutionContext(exec_mode.single_proc)
executor = Executor(exec_context, [config]) # Pass the configuration object inside an array
raw_result, tensor = executor.main() # The `main()` method returns a tuple; its first elements contains the raw results

df = pd.DataFrame(raw_result)
```
> Despite the complexity of the highy heterogenous state: multiple expanding vectors and a graph object which varying nodes and edges the system output is well conformed:
> ![](https://i.imgur.com/K3KFGvU.png)
> Note that in this set of experiments the variable 'time_weighted_cred' is mapped to the algorithm defined as $\vec{\bar{r}}_t$ in this document, but the code is factored in such a way that this need only be modified in place to change the experiment.

The dataframe object simply reports the list of nodes under the 'network' column but in fact the whole graph trajector is stored. Plot of the sequence of $\mathcal{G}_{t}=\mathcal{G}_{t-1} + \Delta \mathcal{G}_t$:
```python=
nets = df[df.substep==1].network.values
pos = nx.kamada_kawai_layout(nets[-1])

#note that the alpha kwarg in the draw method is transparency
#not the pagerank parameter alpha
for i in range(len(nets)-1):
    nx.draw(nets[i],pos=pos, alpha=.5, node_color='b')
    nx.draw(nets[i+1],pos=pos,  alpha=.5, node_color='g')
    plt.show()
```
> **t=1**
> ![t=1](https://i.imgur.com/0kGaLJJ.png)
> **t=2**
> ![t=2](https://i.imgur.com/CAPEMNg.png)
> **t=3**
> **$\vdots$**
> **t=48**
> ![](https://i.imgur.com/88tp0Rv.png)
> **t=49**
> ![](https://i.imgur.com/BXugtuJ.png)

Rather than try to pack two much information in the network evolution plots, the network description are plotted in time here:
> ![](https://i.imgur.com/dUjG8bT.png)


> ![](https://i.imgur.com/1U4Cigo.png)

Looking at the snapshot Personalized PageRank scores one can see the jerkiness discussed earlier in this section. Given that graph formation processes have intrinsic preferential attachment dynamics it is unsuprising that the oldest contributions tend to retain the highest scores. 

For more on preferential attachment dynamics see:
[NETWORK SCIENCE;
ALBERT-LÁSZLÓ BARABÁSI](http://barabasi.com/f/622.pdf)

The reason for initially simply using the smoothed average as the time weighted cred was in order to more clearly interpret the trends in cred over time without all the jerky changes
> ![](https://i.imgur.com/tCOvLAT.png)
> 
One can clearly observe the advantage of early contributions but the highest cred contributions are losing ground and there are some later contributions that jump up to at least the middle of the pack.

As discussed in the theory section, this metric suffers from a zero sum scenario where the cred for new contributions is being 'taken' in a sense away from the existing items. Our simulations also include the cumulative cred case to compare. 
> ![](https://i.imgur.com/0LPJbeM.png)

Here one observes that the new contributions enter the network and then accumulate cred over time allowing each contribution to have a monotonically increasing score. The main feature of this metric is to help the users feel good about collaborating rather than competing so it makes sense to zoom in on the 'user' nodes in the network.

> ![](https://i.imgur.com/I7oLQ8m.png)

Reviewing the same set of plots put limiting the analysis to just the users in the network, it is clear that the snapshot pagerank is still a very jerky measure as the graph evolves.

> ![](https://i.imgur.com/gN3GTnj.png)

The exponential smoothing does a good job cleaning up the noisy results but we still observe the zero sum game scenario.

> ![](https://i.imgur.com/ITHwGfb.png)

Using the cumulative cred metric results in monotonically increasing cred, though it remains to be see just how much or how little this might exacerbate the advantages of the early contributors under different cred injection signals $\vec{v}_t$.

### Limitations

Thus far this analysis only scratches the surface of the computational experimentation enabled by the networkx+cadCAD simulation configuration; and our cred source has been a fixed single node seed with a 'steady drip' of cred in the sense that $[\vec{v}_t]_i=1$ at each iteration of the network. 

> ![](https://i.imgur.com/IA0jbDq.jpg)
> A system Map of the simulations in this section shows that there is not yet any strategic or intelligent behavior wired into the computational experiments.

It is likely that steady flows of cred make sense for source nodes which represent project 'Values', but that batch releasing cred from source nodes representing 'Goals' will make more sense.

An important next step in analyzing algorithms for time weighted cred would be to explore variable cred volumes, in particular releasing cred upon deeming a goal or milestone achieved would be considered strategic behavior. 

In addition to working with cumulative cred, it would make sense to continue to experiment with new ideas about how to compute time varying cred as they come up. The cadCAD engine has A/B testing capabilities which can be leveraged when we're ready.

The example in this document is also a single realization of a random process. To better understand the properties of this stochastic dynamic process, one should run Monte Carlo analysis, repeating the same experiments many times are observing what aspects vary widely and which are more consistent.

In the next section of this document, the topic of Socio-Technical Feedback Loops will be address. These loops account for both strategic behavior on the part of the contributing agents, as well as adjustments to the cred metrics, source nodes and cred release volumes on the part of the maintainers. These closed loops dynamics can be introduced into our stochastic dynamical system through the addition of states and partial state update blocks with policies encoding the strategic behavoir on the part of both the participants (where and what they contribute to evolve the network) and the maintainers (adjusting the metrics or releasing cred for hitting goals). This will require the construction of additional formalisms, which are under development.

## Socio-technical Feedback Loops

Socio-Technical Feedback Loops are interactions between intelligent agents and a system they are part of which is made up of a set of mechanisms or state updates rules and a system state which is evolving in time. It is assumed that agents know the mechanisms, can observe some or all of the system states, and that their behavior is driven by some potentially private goals, and additional private signals

> ![](https://i.imgur.com/UXdxpTn.jpg)
> This is generic model of a discrete dynamic game with private information and private objectives. Our term 'SocioTechnical Feedback loop' refers to the interaction effects between how the human agents behave and how the mechanisms are designed.

More details and updated notation for formal feedback system models for use with cryptographically secured computation see:
[Statespace Framework;
MICHAEL ZARGHAM](https://github.com/sourcecred/research/blob/master/references/State_Model_V3.pdf)

A broader basis for dynamic decision systems and optimization can be obtained from this [Stanford Course](https://stanford.edu/class/ee363/courseinfo.html), the textbooks for which are (unfortunately not available in public pdf):
- Dynamic Programming and Optimal Control, vol. 1;
Bertsekas
- Optimal Filtering and Optimal Control: Linear Quadratic Methods;
Anderson & Moore
- Nonlinear systems: Analysis, Stability, and Control; 
Sastry

Additionally, I recommend the following text which is available in public pdf:
 - [Game Theory and Control;
Jason R. Marden and Jeff S. Shamma](https://www.ece.ucsb.edu/~jrmarden/files/marsha2017.pdf)

The system level goal of a SourceCred instance is to enable efficient and enjoyable co-creation on the part of a community. This end is accomplished through transparency and social incentives. This means that the observable system state, denoted $Y$ in the diagram above should aim to encourage collaboration through present co-creation as a positive sum game, and allowing users to explore the data in a manner fitting their private objectives or preferences even when those things are not known a priori by the system designers or project maintainers. Due to the social nature of the co-creation this is largely a task of User Experience focused product research.

### Role of the graph visualizer & importance of graph mappings

*This section is notes still as we (Z, Dandelion and Evan) decided to backburner the graph mappings specification and prototyping tasks to focus on time weighted cred results* 


##### Graph Visualizer
- Enagement: observation of others work motivates contributions
- Leaderboard is great but it espouses competition vibe, graph visualizer allows contributors to see/feel the positive impact of contributions on each other

##### Graph Mappings 
 - High degree nodes are an issue for UX (visualization & reporting)
 - High degree nodes are mathematically/structurally important
 - Need to preserve correct structure "under the hood"
 - Need to make it easy to make meaningful reductions for UX

### Gaming Cred: Dynamic Network Formation Games

In the future, SourceCred may be combined with explicit financial incentives so exploring its mechanisms robustness to gaming in a valuable undertaking. For now, it will suffice to observe that the goal of robust mechanism design is bound the the reachable space, as derived from the mechanism's action space as opposed to rely on rationality assumptions regarding agent behavior.
> ![](https://i.imgur.com/vu9A6o4.png)
> System requirements are formal statements about the Reachable space, and nice to have features are error metrics applied over the course of a realiztion, or trajectory of states an actions as the system evolves through time.

A concrete example of how Cred may be used to allocate financial assets on a small scale is by integrating with a bounty platform such as [GitCoin](https://gitcoin.co/bounties/funder) and by computing a Personalized PageRank relative to a the issue that is bountied, incentivize and reward a more robust solution than might be engineered if only the party committing the solution recieved a reward. It is however, still the case that one might contribute strategically to maximize their share of a bounty while minimizing effort; such a case may be studied as a dynamic game, with the intent to select mechanism parameters that mitigate the benefits of such behavior. 

The computational experiments undertaken in the Section on Temporal Context provide the initial system testing framework for analyzing SourceCred as a class of dynamic game called a network formation game. A wide range of formalizations and analysis of Network formation games exisit in the network science literature; the critical reference texts are:
- [Social and Economic Networks;
Matthew O. Jackson](https://github.com/sourcecred/research/blob/master/references/netbook-jackson.pdf)

- [Algorithmic Game Theory;
Noam Nisan, Tim Roughgarden, Eva Tardos, Vijay V. Vazirani](https://github.com/sourcecred/research/blob/master/references/Algorithmic_Game_Theory.pdf)

- [Networks, Crowds, and Markets: Reasoning about a Highly Connected World;
David Easley and Jon Kleinberg](https://github.com/sourcecred/research/blob/master/references/networks-book.pdf)

As an initial formulation the figure below extends the system configuration map from our Temporal Context computional experiments to include strategic behavoir of three types: agents making strategic decisions about their contributions, maintainers making strategic decisions regarding when to release cred, and maintainers tweaking system paramters to mitigate the effectiveness of gaming by contributors.

> ![](https://i.imgur.com/2SuxI5w.jpg)
> A system Map of the simulations extended to include strategic  behavior for both contributors and maintainers, including parameter governance.

In practice one would not layer in all three strategic behaviors at once, instead the system would be incrementally extended and studied as deemed appropriate. At this stage, analyzing a study of either strategic contributor behavior is the next step.



Such analysis becomes increasingly critical the larger scale the collaboration, and the larger the financial incentives are. The long term vision for SourceCred would support such large scale coordination efforts via an economic asset called Grain; for further details see:
[SourceCred and the Quest to Outcompete Capitalism;
Dandelion Man&eacute;](https://discourse.sourcecred.io/t/draft-sourcecred-and-the-quest-to-outcompete-capitalism/64)

## Next Steps

The primary body of code that was used to generate this document is in pre-infra state and needs to be oranized into the SourceCred/Research repo in order to make the work accessable to others. Due to the specialized tools in my local python environment, it may be necessary to create a container with an appropriately configured environment for others to use the networkx+cadCAD SourceCred simulator, as well as future monte carlo and A/B testing notebooks.

Should the research project have renewed funding, a reallocation of resources will be made to prioritize engineering bandwidth and project management. More detailed ongoing goals may be established in subsequent discussions.

## Acknowledgements

- *David F. Sisson* for broad and deep background research on frameworks and data models for attribution networks, regular discussions and reviewing my work.

- *Markus Koch* and *Joshua Jodesty* for collaboration and support on computational experiments, especially the networkx in cadCAD configurations enabling the experiments in the temporal context section.

- *Matthew Stephenson* for the ongoing value of the output of our collaborative research on incentives and behavior in network formation games.

- *Ryan Morton* for helping map out and develop exploratory data analysis tools for attribution networks.

- *Maksim and Denis Kudinov* for extensive discussions on co-creative workflows and user experience for community self-reflection analytics.

- *Charlie Rice* for past and future editing of the technical writing throughout the doc.

- Huge thanks to the SourceCred creator and project lead *Dandelion Man&eacute;*, as well as all of the other contributors to this amazing project.
