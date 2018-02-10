import json
from ast import literal_eval

class RootReachability:
    """Class to identify the group of nodes that cannot reach the root node
    in a directed graph.

    Attributes
    ----------
    data : dict
        Dictionary containing the strucutre.
    vertices : array-like
        List of vertex ids.
    adj : dict
        Dictionary containing vertices as keys and the list of vertices to
        which they point as the values. Edge list.
    root : str
        Root node.
    non_orphan_nodes : array-like
        List of nodes that have a path to the root.
    orphan_nodes : array-like
        List of nodes that do not have a path to the root.
    done : bool
        Whether the root can be reached from a single vertex.
    """

    def __init__(self, input_from_user=True, json_input=None,
                 edge_to_delete=None):
        """
        Constructor to initialize the graph variables.

        Parameters
        ----------
        input_from_user : bool
            Whether to take input from user or not. Set flag to False for
            unit tests.
        json_input : str
            Input JSON string containing a list of components.
        edge_to_delete : dict
            Dictionary containing the from and to vertices of the edge to be
            deleted.
        """

        self.data = {}
        self.vertices = []
        self.adj = {}
        self.root = ""
        self.non_orphan_nodes = []
        self.orphan_nodes = []
        self.done = False

        if input_from_user:
            self.get_data()
        elif json_input is not None and edge_to_delete is not None:
            self.get_data(json_input, edge_to_delete)
        else:
            raise ValueError("No input provided. Initialize class to either "
                             "accept input from user to provide a JSON "
                             "string.")

    def get_data(self, json_input=None, edge_to_delete=None):
        """Function to get data from the user.

        Parameters
        ----------
        json_input : str
            Input JSON string containing a list of components.
        edge_to_delete : dict
            Dictionary containing the from and to vertices of the edge to be
            deleted.

        Returns
        -------

        Raises
        ------
        TypeError
            If input is not a dictionary.
        ValueError
            If the JSON string couldn't be parsed properly.
            If edge to be deleted doesn't exist in the graph.
            If dictionary format is invalid.
        """
        if json_input is None:
            text = """Please input the list of components as a dictionary in 
            a SINGLE LINE.\nFor example:\n
            {"nodes": [{"id": "M00"}, {"id": "M01"}, {"id": "M02"}],"edges": [{"from": "M01","to": "M02"}, {"from": "M00","to": "M02"}, {"from": "M01","to": "M00"}],"root": "M00"}
            Enter input: 
            """
            data = literal_eval(input(text))
        else:
            # Try parsing the string.
            try:
                data = json.loads(json_input)
            except ValueError:
                raise ValueError("Couldn't parse input properly. Please check "
                                 "input and try again.")

        self.data = data
        self.construct_adjacency_lists()
        if edge_to_delete is None:
            text = """"Please input the edge to be deleted in the form of a 
                    dictionary in a SINGLE LINE.\n For example: {"from": "M01","to": "M02"}\nEnter input: """

            deleted_edge = literal_eval(input(text))
        else:
            deleted_edge = literal_eval(edge_to_delete)

        if not isinstance(deleted_edge, dict):
            raise TypeError("Expected input is a dictionary!")

        if "from" in deleted_edge and "to" in deleted_edge and len(
                deleted_edge) == 2:
            deleted_from = deleted_edge["from"]
            deleted_to = deleted_edge["to"]
        else:
            raise ValueError(
                "Dictionary representing edge to be deleted is "
                "in an invalid format.")
        if deleted_from in self.adj and deleted_to in self.adj[
            deleted_from]:
            self.adj[deleted_from].remove(deleted_to)
        else:
            raise ValueError("Edge from {} to {} doesn't exist in the "
                             "input structure. Please correct input and "
                             "try again.".format(deleted_from,
                                                 deleted_to))

    def construct_adjacency_lists(self):
        """
        Function to construct the adjacency lists associated with this
        directed graph.

        Raises
        ------
        ValueError
            If the JSON string couldn't be parsed properly.
        """

        self.root = self.data["root"]
        self.vertices = [node["id"] for node in self.data["nodes"]]

        for edge in self.data["edges"]:
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

if __name__ == "__main__":
    rr = RootReachability()
    print("Deleted array: ", rr.get_orphan_nodes())