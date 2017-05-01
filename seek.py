
import json

module_names = set() # Ensures that module names are unique.  "start" and "end" are reserved.
module_data = {}

class Module(object):
	"""
	Generic module object with a name and a target
	"""
	def __init__(self, name, link_to):
		if name not in module_names:
			self.name = name
		else:
			raise Exception("A module with this name already exists."\
				"Please use a unique name for the module")
		self.link_to = link_to

	def __repr__(self):
		return self.name + " page targeting: " + self.link_to

class ContentModule(Module):
	"""
	Creates a static page that displays html_body.  Meant to provide story or clues
	"""  

	def __init__(self, name, html_body, link_to):
		super(ContentModule, self).__init__(name, link_to)
		self.html_body = html_body
		self.url = "/content/" + self.name
		module_data[self.name] = {"url": self.url, "target": self.link_to, "data": {"html": html_body}}

class TextModule(ContentModule):
	"""
	Creates a simple static page with the text provided
	"""
	def __init__(self, name, link_to, text):
		html_body = "<p>" + text + "</p>"
		super(TextModule, self).__init__(name, html_body, link_to)

class StartModule(ContentModule):
	"""
	Creates a static page with html_body that acts as the start of the hunt
	"""
	def __init__(self, html_body, link_to):
		super(StartModule, self).__init__("start", html_body, link_to) #TODO switch to subclassing Module and change server code

class QRModule(Module):
	"""
	Creates a page with html_body.  The player has to scan a hidden qr code to progress.
	target_type is the module type of the next module root is the root url of your site
	"""
	def __init__(self, name, html_body, link_to,target_type, root):
		import qr
		super(QRModule, self).__init__(name, link_to)
                self.html_body = html_body
		self.url = r"/qr/" + self.name
		module_data[self.name] = {"url": self.url, "target": link_to, "data": {"html": html_body}}
        qr.make_qr("qr/" + self.name + "_qr.png", root + '/' + target_type + '/' + self.link_to + '/')

class InteractiveModule(Module):
	"""
	Parent class for all the interactive (non content) modules
	"""
	# TODO: Remove this class and integrate it into base Module class
	def __init__(self, name, link_to, module_type, extra_data_dict):
		super(InteractiveModule, self).__init__(name, link_to)
		self.url = "/" + module_type + "/" + self.name
		module_data[self.name] = {"url": self.url, "target": self.link_to, "data" : extra_data_dict}

class GPSModule(InteractiveModule):
	"""
	Creates a page that allows the user to progress once they reach the gps coordinates
	specified by x_coordinate, y_coordinate
	"""
	def __init__(self, name, link_to, x_coordinate, y_coordinate):
		super(GPSModule, self).__init__(name, link_to, "gps", {"x_coordinate": x_coordinate, "y_coordinate": y_coordinate})

class FindObjectModule(InteractiveModule):
	"""
	Creates a page that instructs users to take and upload a photo with object_name in it.
	Uses the google vision API to check if that object is in the picture
	"""
	def __init__(self, name, link_to, object_name):
		# assert(type(object_name) == type([1]))
                super(FindObjectModule, self).__init__(name, link_to, "find", {"object_name": object_name})

class ImageMatchModule(InteractiveModule):
	"""
	Creates a page that instructs the user to take and upload a photo that matches the image on the
	server at image_filename.  Allows the user to progress if the two photos are sufficiently similar
	"""
	def __init__(self, name, link_to, image_filename):
		super(ImageMatchModule, self).__init__(name, link_to, "match", {"image_filename": image_filename})

class TextInputModule(InteractiveModule):
	"""
	Creates a page with a text box that allows the user to progress if they enter correct_string
	"""

	def __init__(self, name, link_to, correct_string):
		super(TextInputModule, self).__init__(name, link_to, "text", {"correct_string": correct_string})

def save_module_data(filename = "modules.json"):
	"""
	Exports all of the modules created into a json file at filename which encodes all the details
	of the hunt
	"""
	url_module_data = {}
	for module_name in module_data:

		module_info = module_data[module_name]
		target_name = module_info["target"]
		if target_name == "end":
			target_url = "/end/"
		else:
			target_url = module_data[target_name]["url"]
		url_module_data[module_name] = {"url": module_info["url"], "target": target_url, "data": module_info["data"]}

	with open(filename, 'w') as fp:
		json.dump(url_module_data, fp)

