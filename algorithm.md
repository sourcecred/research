# SourceCred Algorithm

SourceCred is a system for assigning 'cred' to contributors, in proportion
to the value they've contributed to the project.

SourceCred does this by creating a 'Contribution Graph', a [graph]
containing all of the contributions and contributors to a project, as well as how
they are inter-related. It then assigns cred to every node in the graph,
with [PageRank]-esque semantics such that cred flows along edges, accumulating
at nodes that are connected to other high-cred nodes. Intuitively,
contributions are important if they are depended on by other important
contributions, and users are important if they are connected to important
contributions.

The intention of this document is to rigorously describe the SourceCred algorithm,
so that we can use it as a basis for discussing improvements and open issues with the system.
This is a living document, and we intend to keep it up-to-date so as to describe the
present operation of SourceCred's algorithm.

Pull requests welcome!

[graph]: https://en.wikipedia.org/wiki/Graph_(abstract_data_type)
[PageRank]: https://en.wikipedia.org/wiki/PageRank


# Contribution Graphs
The core data structure in SourceCred is the [contribution graph]. Strictly
speaking, it's actually a [quiver] as the edges are directed, multiple edges
are allowed between a given pair of nodes, and loop edges are permitted.

[contribution graph]: https://github.com/sourcecred/sourcecred/blob/master/src/core/graph.js
[quiver]: https://en.wikipedia.org/wiki/Quiver_(mathematics)

## Nodes
Every contribution or contributor to a project is represented by a node in a graph.
For example, GitHub pull requests, user accounts, comments, and repositories are all
represented as nodes. Every node is assigned *cred* based on how it's connected to
other nodes.

It can be counter-intuitive that users get the same "kind" of cred as issues
and pull requests, but handling things this way makes the algorithm nicely
simple and consistent.

Every node is given a unique address, which is represented by an array of
strings. The graph does not store any metadata with nodes. Because addresses
are unique, the addresses can be used as an index into other databases.

## Edges
Every relationship between contributions or contributors is represented by an
edge in the graph. For example, a GitHub pull request may have some of the
following edges:
- an *authored by* edge, connecting it with a user that authored the pull
- a *has child* edge, connecting it with its comments or reviews
- a *has parent* edge, connecting it with the repository that contains it
- a *references* edge, connecting it with an issue or pull it textually references

By convention, we name edges with verb phrases, so that the `src` is the
subject and the `dst` is the object of the verb phrase. Thus, an edge
connecting a GitHub user with a post they wrote would be an *authors* edge.

### Edge Bidirectionality

In practice, we often want to flow cred along both directions of an edge. For
example, if a user authors a post, that user should earn some cred from the
post (cred flows along the *authored by* edge). However, we may also want cred
to flow from the user to the post, with the intuition that posts authored by
important contributors are likely more important than posts authored by someone
who has no history in the project. Then, cred should flow along the *authors*
edge.

These situations come up pretty often, so by default, we treat every edge as
potentially bidirectional. When we assign weights to edges, we give every edge
a `toWeight` and `froWeight`. The `toWeight` configures how much cred flows
from the `src` to the `dst`, and the `froWeight` configures how much cred flows
from the `dst` to the `src`. This way, we don't need to add backwards edges to
the graph to enable these flows. If an edge really should be uni-directional,
we can just set one of the weights to 0.

## Plugin Graphs

A core goal for SourceCred is configurability and extensibility. That
extensibility starts with the graph. The SourceCred core doesn't create any
graphs itself; it just defines the semantics for graphs. Graphs are actually
created by plugins. SourceCred currently includes two initial plugins: one for
Git, another for GitHub. In the future, we imagine having plugins for other
tools, like Twitter, StackOverflow, Google Docs, npm, and so forth.

### Plugin Namespacing

As mentioned above, we require that node and edge addresses be unique within a
graph. That means that they need to be unique across plugins. To ensure this
property, plugins are expected to define their own namespaces within address
space, by making all of their node and edge addresses start with a unique
two-part plugin prefix. The first element of the prefix should be the name of
the owner of the plugin, and the second part should be the name of the plugin
itself.

For example, every node and edge address created by SourceCred's GitHub plugin
starts with the prefix `["sourcecred", "github"]`.

## Node and Edge Types

Nodes and edges organized into meaningful "types" or "kinds" which share common
semantics. For example, some kinds of nodes include issues, pull requests, and
user accounts; kinds of edges include authors, references, and merges.

To support this, SourceCred has a concept of [types]. Type membership is
determined by a shared address prefix.

[types]: https://github.com/sourcecred/sourcecred/blob/master/src/analysis/types.js

For example, every node whose address starts with `["sourcecred", "git",
"commit"]` is considered a member of the commit type defined by SourceCred's
Git plugin.

A node or edge may be a member of multiple types (and every node and edge is
considered a member of the empty type).


## Weights

SourceCred allows the assignment of weights to nodes and edges. A weight is a
non-negative floating point number, i.e. in the range `[0, Infinity)`. Nodes
have a single weight, and edges have two weights, a `toWeight` and `froWeight`.
At present, weights may only be set at the type level, but our intention is to
allow arbitrarily customized weights that are modified by user provided
*heuristics*.

# Attribution

Attribution is the process by which we assign a score ('cred') to every node in
a contribution graph. It uses a PageRank-based algorithm, although in contrast
to [canonical PageRank], there is no random teleportation vector. (Due to the
lack of a teleportation vector, it's possible that the chain is not ergodic,
and that the algorithm will fail to converge. There's no particular reason we
don't have a teleportation vector, and may choose to add one in the future.)

[canonical PageRank]: http://ilpubs.stanford.edu:8090/422/1/1999-66.pdf

## Creating the Markov Chain

We convert the contribution graph into a [Markov Chain]. For every node in the
graph, we create a self-loop connection with a small 'synthetic loop weight'
(usually 1E-3). This ensures that every node has at least some outbound
connections (in lieu of a teleportation vector). Without such a loop, the Graph
might not correspond to a valid Markov Chain.

We then add connections corresponding to edges in the graph. Specifically, for
every edge, we add a connection from its `src` to `dst` with a weight
`edge.toWeight * dst.weight`, and we create a connection from its `dst` to
`src` with weight `edge.froWeight * src.weight`.

Finally, we normalize the weights so that the outbound connections for each
node sum to 1 (i.e. it's a valid Markov Chain).

[Markov Chain]: https://brilliant.org/wiki/markov-chains/

## Assigning Raw Cred

Once the Markov chain is created, we are ready to assign cred. We start with a
uniform distribution over over every node in the graph. Then, we successively
update that distribution with Markov chain actions, until we find a stationary
distribution. We measure how well converged a distribution is by looking at the
infinity-norm difference between that distribution and the distribution with
one more Markov action applied. Concretely, if `A` is the transition matrix
corresponding to the chain, then:

`convergenceDelta(x: Distribution) = infinityNorm(x - A * x)`

We keep iterating until the convergence delta is sufficiently small, or until a
max number of iterations is reached.

## Normalizing Cred Scores

The raw cred scores generalized by this algorithm form a probability
distribution. This means that most users will have tiny scores like 0.00363,
which is aesthetically unappealing for human consumption, and hard to compare
across projects. To make the scores easier for humans to remember and
interpret, we re-normalize the scores so that all GitHub user accounts, in
aggregate, share 1000 cred. The normalization algorithm is linear, i.e. every
score is multiplied by the same constant.
