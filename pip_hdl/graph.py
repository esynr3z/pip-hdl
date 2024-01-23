"""Utilities to work with package dependencies.

All dependencies can be extracted to form a Directed Acyclic Graph,
which can be traversed in the correct (dependency-aware) order.
"""
from __future__ import annotations

from collections import deque
from pathlib import Path
from typing import Any, Deque, Iterable, Iterator, List, Sequence, Set

from .metainfo import PackageMetaInfo


class Node:
    """Graph node, which represents a package."""

    def __init__(self, metainfo: PackageMetaInfo) -> None:
        """Init node."""
        self.metainfo: PackageMetaInfo = metainfo
        self.upstreams: Set[Node] = set()  # aka requirements aka parents aka dependencies
        self.downstreams: Set[Node] = set()  # aka consumers ake childs aka dependants

    @property
    def id(self) -> str:
        """Node identifier."""
        return self.metainfo.name

    def add_upstreams(self, nodes: Iterable[Node]) -> None:
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

    def __iter__(self) -> Iterator[Node]:
        """Iterate through nodes in dependency-aware order."""
        # need to start from "roots" - nodes without dependecies
        initial_nodes = [node for node in self.nodes.values() if len(node.upstreams) == 0]

        if self.nodes and (len(initial_nodes) == 0):
            raise RuntimeError("Can't find packages without dependencies to start iteration. Circular dependency?")

        yield from self._traverse_from(initial_nodes)

    def _traverse_from(self, nodes: Iterable[Node]) -> Iterator[Node]:
        """Traverse through a DAG starting from provided `nodes` and visiting all their downstreams.

        Nodes are yielded in a dependency-aware manner - node is yielded only if it's dependencies were already yielded.
        Non-recursive BFS-like algorithm is used here.
        """
        visited: List[Node] = []
        planned: Deque[Node] = deque(nodes)

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

    def _packages_to_nodes(self, packages: Iterable[PackageMetaInfo]) -> Iterator[Node]:
        """Convert packages and all their dependencies to graph nodes recursivelly."""
        for pkg in packages:
            yield Node(pkg)
            yield from self._packages_to_nodes([d.metainfo for d in pkg.dependencies])

    def render_dag(self, **kwargs: Any) -> Path:
        """Represent current graph as directed acyclic graph using 'graphviz'.

        Arguments are the same as in 'graphviz.Digraph.render()'.
        May raise 'ModuleNotFoundError' if 'graphviz' is not installed.
        """
        import graphviz

        graph = graphviz.Digraph("Package Graph", graph_attr={"rankdir": "LR"})

        for node in self.nodes.values():
            for downstream in node.downstreams:
                graph.edge(node.id, downstream.id)

        return Path(graph.render(**kwargs))
