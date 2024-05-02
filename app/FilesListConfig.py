import json
import os

class FileListCinfig:
	def __init__(self, config_path, create=True):
		self.config_path = config_path

		if create and (not os.path.isfile(self.config_path)):
			self.file_data = json.loads('{"files": []}')
			self.write()
		
		self.file_data = self.open()
		
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

if __name__ == '__main__':
	config = FileListCinfig('./testconfig.ini')