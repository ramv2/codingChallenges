import json
from ast import literal_eval

class RootReachability:
    """Class to identify the group of nodes that cannot reach the root node
    in a directed graph.
    """

    def __init__(self):
        """
        Constructor to initialize the graph variables.
        """
        self.vertices = []
        self.adj = {}
        self.root = ""
        self.non_orphan_nodes = []
        self.orphan_nodes = []
        self.done = False

    def construct_adjacency_lists(self, json_input):
        """
        Function to construct the adjacency lists associated with this
        directed graph.

        Parameters
        ----------
        json_input : str
            String containing the structure of the graph.

        Raises
        ------
        ValueError
            If the JSON string couldn't be parsed properly.
        """

        # Try parsing the string.
        try:
            data = json.loads(json_input)
        except ValueError:
            raise ValueError("Couldn't parse input properly. Please check "
                             "input and try again.")



        self.root = data["root"]
        self.vertices = [node["id"] for node in data["nodes"]]

        for edge in data["edges"]:
            _from = edge["from"]
            _to = edge["to"]

            if _from not in self.adj:
                self.adj[_from] = []

            self.adj[_from].append(_to)


    def get_orphan_nodes(self):
        """
        Function to get the list of orphan nodes that cannot reach the root.

        Returns
        -------
        orphan_nodes : array-like
            List of nodes that cannot reach the root.
        """

        # Loop through the vertices and perform dfs to see if the root can be
        # reached from the current vertex. If yes, add it to the list of
        # non-orphan nodes and continue.
        for v in self.vertices:
            # We are not interested in the vertices that we can reach from
            # the root. We are also not interested in performing dfs from
            # vertices that have already been shown to connect to the root
            # a.k.a. non-orphan nodes.
            if v == self.root or v in self.non_orphan_nodes:
                continue
            marked = [False] * len(self.vertices)
            self.done = False
            self.dfs(v, marked)
            # If we are able to reach the root as part of this dfs call,
            # albeit indirectly, that means the root can be reached from this
            # vertex. If it is not already in the list of non-orphan nodes,
            # add it.
            if self.done and v not in self.non_orphan_nodes:
                self.non_orphan_nodes.append(v)

        # Compute the list of orphan nodes.
        self.orphan_nodes = [x for x in self.vertices if x not in
                             self.non_orphan_nodes and x != self.root]
        return self.orphan_nodes

    def dfs(self, v, marked):
        """
        Function to perform depth-first search from a given vertex v.

        Parameters
        ----------
        v : str
            String denoting the vertex id.
        marked : array-like
            List of booleans to ensure we are not visiting the same vertex
            twice. Helpful in avoiding cycles.

        Returns
        -------

        """
        if not self.done:
            # Mark vertex as visited.
            marked[self.vertices.index(v)] = True

            # Check if the vertex has any edges that it points to.
            if v in self.adj:
                for w in self.adj[v]:
                    # We are not interested in the vertices that we can reach
                    # from the root. We are also not interested in performing
                    # dfs from vertices that have already been shown to
                    # connect to the root a.k.a. non-orphan nodes.
                    if not self.done and (w == self.root or w in
                        self.non_orphan_nodes):
                        self.done = True
                        self.non_orphan_nodes.append(v)
                        break

                    # If it is already marked as part of the current dfs
                    # call, we don't need to visit it. Otherwise, perform a
                    # dfs starting from the vertex w.
                    if not marked[self.vertices.index(w)]:
                        self.dfs(w, marked)

    def delete_edge(self):
        """
        Function to delete the edge (or perform the user action) specified by
        the user.

        Returns
        -------

        Raises
        ------
        TypeError
            If input is not a dictionary.
        ValueError
            If edge to be deleted doesn't exist in the graph.
            If dictionary format is invalid.

        """
        text = """"Please input the edge to be deleted in the form of a 
        dictionary. For example: {"from": "M01", "to": "M02"}\nEnter input: """

        deleted_edge = literal_eval(input(text))
        if not isinstance(deleted_edge, dict):
            raise TypeError("Expected input is a dictionary!")
        if "from" in deleted_edge and "to" in deleted_edge and len(
                deleted_edge) == 2:
            deleted_from = deleted_edge["from"]
            deleted_to = deleted_edge["to"]
            if deleted_from in self.adj and deleted_to in self.adj[
                deleted_from]:
                self.adj[deleted_from].remove(deleted_to)
            else:
                raise ValueError("Edge from {} to {} doesn't exist in the "
                                 "input structure. Please correct input and "
                                 "try again.".format(deleted_from, deleted_to))
        else:
            raise ValueError("Dictionary representing edge to be deleted is "
                             "in an invalid format.")
if __name__ == "__main__":
    rr = RootReachability()
    inp = """
            {
                "nodes": [{
                            "id": "M00"
                        }, {
                            "id": "M01"
                        }, {
                            "id": "M02"
                        }
                        ],
                "edges": [{
                            "from": "M01",
                            "to": "M02"
                            }, {
                            "from": "M00",
                            "to": "M02"
                            }, {
                            "from": "M01",
                            "to": "M00"
                            }
                        ],
                "root": "M00"
            }
            """
    rr.construct_adjacency_lists(inp)
    rr.delete_edge()
    print(rr.get_orphan_nodes())