"""Utilities to work with package dependencies.

All dependencies can be extracted to form a Directed Acyclic Graph,
which can be traversed in the correct (dependency-aware) order.
"""
from __future__ import annotations

from collections import deque
from pathlib import Path
from typing import Any, Deque, Iterable, Iterator, List, Sequence, Set

from .metainfo import PackageMetaInfo


class GraphNode:
    """Graph node, which represents a package."""

    def __init__(self, metainfo: PackageMetaInfo) -> None:
        """Init node."""
        self.metainfo: PackageMetaInfo = metainfo
        self.upstreams: Set[GraphNode] = set()  # aka requirements aka parents aka dependencies
        self.downstreams: Set[GraphNode] = set()  # aka consumers ake childs aka dependants

    @property
    def id(self) -> str:
        """Node identifier."""
        return self.metainfo.name

    def add_upstreams(self, nodes: Iterable[GraphNode]) -> None:
        """Link node with dependencies. Backlinks are created as well."""
        for node in nodes:
            self.upstreams.add(node)
            node.downstreams.add(self)


class DependencyGraph:
    """Directed Acyclic Graph to operate with package dependecies conveniently."""

    def __init__(self, packages: Sequence[PackageMetaInfo]) -> None:
        """Create dependecy DAG from provided packages."""
        # create nodes
        self.nodes = {n.id: n for n in self._packages_to_nodes(packages)}

        # link nodes
        for node in self.nodes.values():
            node.add_upstreams([self.nodes[d.metainfo.name] for d in node.metainfo.dependencies])

    def __iter__(self) -> Iterator[GraphNode]:
        """Iterate through nodes in dependency-aware order."""
        # need to start from "roots" - nodes without dependecies
        initial_nodes = [node for node in self.nodes.values() if len(node.upstreams) == 0]

        if self.nodes and (len(initial_nodes) == 0):
            raise RuntimeError("Can't find packages without dependencies to start iteration. Circular dependency?")

        yield from self._traverse_from(initial_nodes)

    def _traverse_from(self, nodes: Iterable[GraphNode]) -> Iterator[GraphNode]:
        """Traverse through a DAG starting from provided `nodes` and visiting all their downstreams.

        Nodes are yielded in a dependency-aware manner - node is yielded only if it's dependencies were already yielded.
        Non-recursive BFS-like algorithm is used here.
        """
        visited: List[GraphNode] = []
        planned: Deque[GraphNode] = deque(nodes)

        while len(planned):
            node = planned.popleft()

            if node in visited:
                continue
            if set(node.upstreams).intersection(set(planned)):
                # dependencies are not resolved yet, plan the job again
                planned.append(node)
                continue

            visited.append(node)
            yield node

            # plan all the following nodes
            for downstream in node.downstreams:
                planned.append(downstream)

    def _packages_to_nodes(self, packages: Iterable[PackageMetaInfo]) -> Iterator[GraphNode]:
        """Convert packages and all their dependencies to graph nodes recursivelly."""
        for pkg in packages:
            yield GraphNode(pkg)
            yield from self._packages_to_nodes([d.metainfo for d in pkg.dependencies])

    def render(self, **kwargs: Any) -> Path:
        """Render current graph using `graphviz`.

        Arguments are the same as in 'graphviz.Digraph.render()'.
        """
        # This minor feature requires rendering engine presence in a system, which might be not the case.
        # So do lazy import here only if rendering actually requested.
        import graphviz

        graph = graphviz.Digraph("graph", graph_attr={"rankdir": "RL"})

        for node in self.nodes.values():
            if len(node.upstreams) == 0:
                graph.node(node.id)
            else:
                for upstream in node.upstreams:
                    graph.edge(node.id, upstream.id)

        return Path(graph.render(**kwargs))
