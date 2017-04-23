import json

module_names = set()
module_data = {}

class Module:

	def __init__(self, name, link_to):
		if name not in module_names:
			self.name = name
		else:
			raise Exception("A module with this name already exists."\
				"Please use a unique name for the module")
		self.link_to = link_to

	def __repr__(self):
		return self.name + " page targeting" + self.link_to

class ContentModule(Module):

	def __init__(self,name, html_body, link_to):
		super().__init__(name, link_to)
		self.html_body = html_body
		self.link_to = link_to
		self.url = "/content/" + self.name
		module_data[self.name] = (self.url, self.link_to, (html_body,))

class TextModule(ContentModule):
	def __init__(self, name, link_to, text):
		html_body = "<p>" + text + "</p>"
		super().__init__(name, html_body, link_to)

class StartModule(ContentModule):
	def __init__(self, html_body, link_to):
		super().__init__("start", html_body, link_to)


# def save_state_graph(filename = "state.json"):
# 	url_state_graph = {}
# 	for module_name in state_graph:

# 		module_url = module_data[module_name][0]
# 		target_module = state_graph[module_name]
# 		target_url = module_data[target_module][0]

# 		url_state_graph[module_url] = target_url		

# 	with open(filename, 'w') as fp:
# 		json.dump(url_state_graph, fp)

def save_module_data(filename = "modules.json"):
	url_module_data = {}
	for module_name in module_data:

		module_info = module_data[module_name]
		target_name = module_info[1]
		target_url = module_data[target_name][0]
		url_module_data[module_name] = (module_info[0], target_url, module_info[2])

	with open(filename, 'w') as fp:
		json.dump(url_module_data, fp)

