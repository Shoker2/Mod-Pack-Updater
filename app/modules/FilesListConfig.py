import json
import os

class FileListCinfig:
	def __init__(self, config_path, create=True):
		self.config_path = config_path
		self.default_lists = ["files", "donotreplace"]

		if create and (not os.path.isfile(self.config_path)):
			self.file_data = json.loads("{}")
			self.write()
		
		self.file_data = self.open()
		self.selections_fix()
		
	def read(self, key):
		return self.file_data[key]
	
	def	update(self, key, arg):
		self.file_data[key] = arg
		self.write()

	def write(self):
		with open(self.config_path, 'w+', encoding='utf-8') as configfile:
			json.dump(self.file_data, configfile, ensure_ascii=False, indent=2)
	
	def open(self):
		with open(self.config_path, 'r', encoding='utf8') as f:
			return json.loads(f.read())
	
	def selections_fix(self):
		for i in self.default_lists:
			if not i in self.file_data:
				self.file_data[i] = []

if __name__ == '__main__':
	config = FileListCinfig('./testconfig.ini')