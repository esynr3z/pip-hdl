"""Tests of `graph` module."""
import random
from typing import List, Sequence

from pip_hdl.graph import DependencyGraph
from pip_hdl.metainfo import PackageDependency, PackageMetaInfo


class MockPackageMetaInfo(PackageMetaInfo):
    """Simplified version of class to mock dependencies resolution."""

    def __init__(self, name: str, dependencies: Sequence[PackageMetaInfo]) -> None:
        """Init object."""
        super().__init__(name)
        self._dependencies_meta = dependencies

    @property
    def dependencies(self) -> List[PackageDependency]:
        """Simplified dependencies."""
        return [PackageDependency(spec="", module=None, metainfo=d) for d in self._dependencies_meta]


def test_empty():
    """Test iterating empty graph."""
    graph = DependencyGraph([])
    assert list(graph) == []


def test_single_node():
    """Test iterating graph from a single package."""
    package = MockPackageMetaInfo("foo", [])
    graph = DependencyGraph([package])
    assert [node.id for node in graph] == [package.name]


def test_multi_node():
    """Test iterating graph from multiple packages."""
    packages = [MockPackageMetaInfo("foo", []), MockPackageMetaInfo("bar", []), MockPackageMetaInfo("baz", [])]
    graph = DependencyGraph(packages)
    assert set(node.id for node in graph) == set(p.name for p in packages)


def test_chain():
    """Test iterating graph in form of chain."""
    foo_pkg = MockPackageMetaInfo("foo", [])
    bar_pkg = MockPackageMetaInfo("bar", [foo_pkg])
    baz_pkg = MockPackageMetaInfo("baz", [bar_pkg])

    packages = [bar_pkg, foo_pkg, baz_pkg]
    random.shuffle(packages)
    graph = DependencyGraph(packages)

    assert list(node.id for node in graph) == ["foo", "bar", "baz"]


def test_triangle():
    """Test iterating graph in form of triangle."""
    foo_pkg = MockPackageMetaInfo("foo", [])
    bar_pkg = MockPackageMetaInfo("bar", [foo_pkg])
    baz_pkg = MockPackageMetaInfo("baz", [bar_pkg, foo_pkg])

    packages = [bar_pkg, foo_pkg, baz_pkg]
    random.shuffle(packages)
    graph = DependencyGraph(packages)

    assert list(node.id for node in graph) == ["foo", "bar", "baz"]


def test_diamond():
    """Test iterating graph in form of diamond."""
    foo_pkg = MockPackageMetaInfo("foo", [])
    bar_pkg = MockPackageMetaInfo("bar", [foo_pkg])
    baz_pkg = MockPackageMetaInfo("baz", [bar_pkg])
    ham_pkg = MockPackageMetaInfo("ham", [baz_pkg])

    packages = [ham_pkg, bar_pkg, foo_pkg, baz_pkg]
    random.shuffle(packages)
    graph = DependencyGraph(packages)

    assert list(node.id for node in graph) == ["foo", "bar", "baz", "ham"]


def test_tree():
    """Test iterating graph in form of tree."""
    a1_pkg = MockPackageMetaInfo("a1", [])
    a2_pkg = MockPackageMetaInfo("a2", [])
    b1_pkg = MockPackageMetaInfo("b1", [])
    b2_pkg = MockPackageMetaInfo("b2", [])
    c1_pkg = MockPackageMetaInfo("c1", [a1_pkg, a2_pkg])
    c2_pkg = MockPackageMetaInfo("c2", [b1_pkg, b2_pkg])
    d_pkg = MockPackageMetaInfo("d", [c1_pkg, c2_pkg])

    packages = [a1_pkg, a2_pkg, b1_pkg, b2_pkg, c1_pkg, c2_pkg, d_pkg]
    random.shuffle(packages)
    graph = DependencyGraph(packages)
    graph_nodes = list(node.id for node in graph)

    assert set(graph_nodes[:4]) == set(["a1", "a2", "b1", "b2"])
    assert set(graph_nodes[4:6]) == set(["c1", "c2"])
    assert graph_nodes[6] == "d"
