import pytest

numpy = pytest.importorskip("numpy")
scipy = pytest.importorskip("scipy")


import networkx as nx
from networkx.algorithms import node_classification


class TestLocalAndGlobalConsistency:
    def test_path_graph(self):
        G = nx.path_graph(4)
        label_name = "label"
        G.nodes[0][label_name] = "A"
        G.nodes[3][label_name] = "B"
        predicted = node_classification.local_and_global_consistency(
            G, label_name=label_name
        )
        assert predicted[0] == "A"
        assert predicted[1] == "A"
        assert predicted[2] == "B"
        assert predicted[3] == "B"

    def test_no_labels(self):
        with pytest.raises(nx.NetworkXError):
            G = nx.path_graph(4)
            node_classification.local_and_global_consistency(G)

    def test_no_nodes(self):
        with pytest.raises(nx.NetworkXError):
            G = nx.Graph()
            node_classification.local_and_global_consistency(G)

    def test_no_edges(self):
        with pytest.raises(nx.NetworkXError):
            G = nx.Graph()
            G.add_node(1)
            G.add_node(2)
            node_classification.local_and_global_consistency(G)

    def test_digraph(self):
        with pytest.raises(nx.NetworkXNotImplemented):
            G = nx.DiGraph()
            G.add_edge(0, 1)
            G.add_edge(1, 2)
            G.add_edge(2, 3)
            label_name = "label"
            G.nodes[0][label_name] = "A"
            G.nodes[3][label_name] = "B"
            node_classification.harmonic_function(G)

    def test_one_labeled_node(self):
        G = nx.path_graph(4)
        label_name = "label"
        G.nodes[0][label_name] = "A"
        predicted = node_classification.local_and_global_consistency(
            G, label_name=label_name
        )
        assert predicted[0] == "A"
        assert predicted[1] == "A"
        assert predicted[2] == "A"
        assert predicted[3] == "A"

    def test_nodes_all_labeled(self):
        G = nx.karate_club_graph()
        label_name = "club"
        predicted = node_classification.local_and_global_consistency(
            G, alpha=0, label_name=label_name
        )
        for i in range(len(G)):
            assert predicted[i] == G.nodes[i][label_name]
