def nodef(tree):
	pk = tree.attrib['id']
	label = ""
	shape = ""
	for item in tree.iterfind("data/ShapeNode"):
		for child in item:
			if child.tag == "NodeLabel":
				label = child.text
			elif child.tag == "Shape":
				shape = child.attrib["type"]
			else:
				pass
	return {"id": pk, "label": label, "shape": shape}

def edgef(tree):
	pk = tree.attrib['id']
	label = ""
	source = tree.attrib['source']
	target = tree.attrib['target']
	for item in tree.iterfind("data/PolyLineEdge"):
		for child in item:
			if child.tag == "EdgeLabel":
				label = child.text
			else:
				pass

	for item in tree.iterfind("data/ArcEdge"):
		for child in item:
			if child.tag == "EdgeLabel":
				label = child.text
			else:
				pass

	return {"id": pk, "label": label, "source": source, "target": target}

class Node:
	def __init__(self, id, label, shape):
		self.id = str(id)
		self.label = label
		self.shape = shape
		self.in_edges = []
		self.out_edges = []

	def add_in_edges(self, edge):
		edge.set_target(self)

	def remove_in_edges(self, edge):
		edge.set_target(None)

	def add_out_edges(self, edge):
		edge.set_source(self)

	def remove_out_edges(self, edge):
		edge.set_source(None)

class Edge:
	def __init__(self, id, label):
		self.id = id
		self.label = label
		self.source = None
		self.target = None

	def set_source(self, node):
		if self.source:
			self.source.out_edges.remove(self)
		self.source = node
		if self.source:
			self.source.out_edges.append(self)

	def set_target(self, node):
		if self.target:
			self.target.in_edges.remove(self)
		self.target = node
		if self.target:
			self.target.in_edges.append(self)

class Graph:
	def __init__(self):
		self.clear()

	def clear(self):
		self.step = 0
		self.history = []
		self.node_list = []
		self.edge_list = []
		self.node_max = 0
		self.edge_max = 0
		self.node_map = {}
		self.edge_map = {}

		self._node_pointer = None
		self._edge_pointer = None
		self.pointer_mode = "node" # node or edge

		self.point_in_edge = None
		self.point_out_edge = None

	@property
	def pointer(self):
		if self.pointer_mode == 'node':
			return self._node_pointer
		elif self.pointer_mode == 'edge':
			return self._edge_pointer

	@property
	def node_pointer(self):
		return self._node_pointer

	@node_pointer.setter
	def node_pointer(self, value):
		self._node_pointer = value
		try:
			self.point_in_edge = self.node_pointer.in_edges[0]
		except BaseException as e:
			self.point_in_edge = None
		try:
			self.point_out_edge = self.node_pointer.out_edges[0]
		except BaseException as e:
			self.point_out_edge = None

	@property
	def edge_pointer(self):
		return self._edge_pointer

	@edge_pointer.setter
	def edge_pointer(self, value):
		self._edge_pointer = value

	@property
	def history_pointer(self):
		pointer = None
		if self.step-1 >= 0:
			pointer = self.history[self.step-1]
		return pointer

	def next_node(self):
		if not self.pointer_mode == 'node':
			self.pointer_mode = 'node'
			return True
		index = (self.node_list.index(self.node_pointer) + 1)
		if index < len(self.node_list):
			self.node_pointer = self.node_list[index]
			return True
		else:
			return False

	def previous_node(self):
		if not self.pointer_mode == 'node':
			self.pointer_mode = 'node'
			return True
		index = (self.node_list.index(self.node_pointer) - 1)
		if index >= 0:
			self.node_pointer = self.node_list[index]
			return True
		else:
			return False

	def next_edge(self):
		if not self.pointer_mode == 'edge':
			self.pointer_mode = 'edge'
			return True
		try:
			index = (self.edge_list.index(self.edge_pointer) + 1)
		except ValueError:
			return False
		if index < len(self.edge_list):
			self.edge_pointer = self.edge_list[index]
			return True
		else:
			return False

	def previous_edge(self):
		if not self.pointer_mode == 'edge':
			self.pointer_mode = 'edge'
			return True
		try:
			index = (self.edge_list.index(self.edge_pointer) - 1)
		except ValueError:
			return False
		if index >= 0:
			self.edge_pointer = self.edge_list[index]
			return True
		else:
			return False

	def next_in(self):
		if self.point_in_edge:
			index = (self.node_pointer.in_edges.index(self.point_in_edge) + 1)
			if index < len(self.node_pointer.in_edges):
				self.point_in_edge = self.node_pointer.in_edges[index]
				self.edge_pointer = self.point_in_edge
				return True
			else:
				self.edge_pointer = self.point_in_edge
				return False
		else:
			return False

	def current_in(self):
		if self.point_in_edge:
			self.edge_pointer = self.point_in_edge
			return True
		else:
			return False

	def previous_in(self):
		if self.point_in_edge:
			index = (self.node_pointer.in_edges.index(self.point_in_edge) - 1)
			if index >= 0:
				self.point_in_edge = self.node_pointer.in_edges[index]
				self.edge_pointer = self.point_in_edge
				return True
			else:
				self.edge_pointer = self.point_in_edge
				return False
		else:
			return False

	def next_out(self):
		if self.point_out_edge:
			index = (self.node_pointer.out_edges.index(self.point_out_edge) + 1)
			if index < len(self.node_pointer.out_edges):
				self.point_out_edge = self.node_pointer.out_edges[index]
				self.edge_pointer = self.point_out_edge
				return True
			else:
				self.edge_pointer = self.point_out_edge
				return False
		else:
			return False

	def current_out(self):
		if self.point_out_edge:
			self.edge_pointer = self.point_out_edge
			return True
		else:
			return False

	def previous_out(self):
		if self.point_out_edge:
			index = (self.node_pointer.out_edges.index(self.point_out_edge) - 1)
			if index >= 0:
				self.point_out_edge = self.node_pointer.out_edges[index]
				self.edge_pointer = self.point_out_edge
				return True
			else:
				self.edge_pointer = self.point_out_edge
				return False
		else:
			return False

	def forward_walk(self):
		if self.point_out_edge and self.point_out_edge.target:
			if self.step > 0:
				if not self.history[self.step-1].target == self.point_out_edge.source:
					self.step = 0
			self.history = self.history[:self.step] + [self.point_out_edge]
			self.node_pointer = self.point_out_edge.target
			self.step += 1
			return True
		else:
			return False

	def reverse_walk(self):
		if self.point_in_edge and self.point_in_edge.source:
			self.node_pointer = self.point_in_edge.source
			self.step = 0 if self.step <= 0 else self.step-1
			return True
		else:
			return False

	def forward_history(self):
		pointer = None
		if self.step < len(self.history):
			self.step += 1
			pointer = self.history_pointer
			self.node_pointer = pointer.target
			self.edge_pointer = pointer

		return pointer

	def reverse_history(self):
		pointer = None
		if self.step-1 >= 0:
			pointer = self.history_pointer
			self.node_pointer = pointer.source
			self.edge_pointer = pointer
			self.step -= 1

		return pointer

class DirectedGraph(Graph):
	def __init__(self, path=None, ET=None):
		super().__init__()
		data = {
			'nodes': [
				{
					'id': 'n1',
					'label': 'source',
					'shape': 'rectangle',
				},
				{
					'id': 'n2',
					'label': 'target',
					'shape': 'rectangle',
				}
			],
			'edges': [
				{
					'id': 'e1',
					'label': 'path',
					'source': 'n1',
					'target': 'n2'
				}
			]
		}

		for node in data["nodes"]:
			node_instance = Node(id=node["id"], label=node["label"], shape=node["shape"])
			self.node_list.append(node_instance)
			self.node_map[node["id"]] = node_instance
			self.node_max += 1

		for edge in data["edges"]:
			edge_instance = Edge(id=edge["id"], label=edge["label"])
			self.edge_list.append(edge_instance)
			self.edge_map[edge["id"]] = edge_instance
			self.edge_max += 1
			edge_instance.set_source(self.node_map[edge["source"]])
			edge_instance.set_target(self.node_map[edge["target"]])

		self.node_pointer = list(self.node_map.values())[0]
		self.edge_pointer = list(self.edge_map.values())[0]

		if path:
			self.load(path, ET)

	def load(self, path, ET):
		self.clear()
		with open(path, "r", encoding="utf8") as f:
			content = f.read()
		parser = ET.XMLParser()
		try:
			tree = ET.fromstring(content.encode('utf-8'), parser=parser)
		except BaseException as e:
			print(e)
			return

		for item in tree.iter():
			prefix, has_namespace, postfix = item.tag.partition('}')
			item.tag = postfix

		global nodef, edgef
		nodes = [nodef(item) for item in tree.iterfind("graph/node")]
		edges = [edgef(item) for item in tree.iterfind("graph/edge")]
		data = {
			"nodes": nodes,
			"edges": edges,
		}

		for node in data["nodes"]:
			node_instance = Node(id=node["id"], label=node["label"], shape=node["shape"])
			self.node_list.append(node_instance)
			self.node_map[node["id"]] = node_instance
			self.node_max += 1

		for edge in data["edges"]:
			edge_instance = Edge(id=edge["id"], label=edge["label"])
			self.edge_list.append(edge_instance)
			self.edge_map[edge["id"]] = edge_instance
			self.edge_max += 1
			edge_instance.set_source(self.node_map[edge["source"]])
			edge_instance.set_target(self.node_map[edge["target"]])

		self.node_pointer = list(self.node_map.values())[0]
		self.edge_pointer = list(self.edge_map.values())[0]

	def add_node(self, label):
		pk = "n{}a".format(self.node_max)
		node_instance = Node(id=pk, label=label, shape="rectangle")
		self.node_list.append(node_instance)
		self.node_map[pk] = node_instance
		self.node_max += 1

	def add_edge(self, source, label, target):
		pk = "e{}a".format(self.edge_max)
		edge_instance = Edge(id=pk, label=label)
		self.edge_list.append(edge_instance)
		self.edge_map[pk] = edge_instance
		self.edge_max += 1
		edge_instance.set_source(self.node_map[source])
		edge_instance.set_target(self.node_map[target])

class Tree(Graph):
	def __init__(self, count):
		super().__init__()
		self.roots = []

		if count <= 0:
			node = Node(id=1, label="tree 1", shape="c")
			self.roots.append(node)
			self.node_map[node.id] = node
			self.node_max += 1
		else:
			for c in range(count):
				node = Node(id=str(c+1), label="tree {}".format(c+1), shape="c")
				self.roots.append(node)
				self.node_map["n{}".format(node.id)] = node
				self.node_max += 1

		self.node_pointer = self.roots[-1]
		self.add_child()
		self.add_child()
		self.add_child()

	def add_child(self):
		child_count = len(self.node_pointer.out_edges) + 1
		node = Node(id=self.node_max, label="node {}".format(self.node_max), shape="c")
		self.node_map["n{}".format(node.id)] = node
		self.node_max += 1
		edge = Edge(id=self.edge_max, label="edge {}".format(self.edge_max))
		edge.set_source(self.node_pointer)
		edge.set_target(node)
		self.edge_map[edge.id] = edge
		self.edge_max += 1
		self.node_pointer = self.node_pointer

	def remove_child(self):
		pass
