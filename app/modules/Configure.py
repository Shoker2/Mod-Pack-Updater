import configparser
import os

class Configure:
	config_general = {
				'mods_folder': '',
				'server': 'http://themallist.temp.swtest.ru/'
			}

	config_windows = {
			'main_x': '520',
			'main_y': '140',
			'settings_x': '500',
			'settings_y': '100'
		}
	
	def __init__(self, config_path, create=True):
		self.config_path = config_path
		self.config = configparser.ConfigParser()

		if create and (not os.path.isfile(self.config_path)):
			self.config['General'] = self.config_general
			self.config['Windows'] = self.config_windows
			
			self.write()
					
		self.config.read(self.config_path, encoding='utf-8')

		self.repair_selections('General', self.config_general)
		self.repair_selections('Windows', self.config_windows)
	
	def repair_selections(self, selection, dic: dict):
		for subselection in dic.keys():
			try:
				self.read(selection, subselection)

			except KeyError:
				try:
					self.update(selection, subselection, dic[subselection])
				except KeyError:
					self.config[selection] = dic
					self.write()
					return
		
	def read(self, section, key):
		self.config.read(self.config_path, encoding='utf-8')
		return self.config[section][key]
	
	def	update(self, section, key, arg):
		self.config[section][key] = arg
		self.write()

	def write(self):
		with open(self.config_path, 'w+', encoding='utf-8') as configfile:
			self.config.write(configfile)

# if __name__ == '__main__':
# 	config = Configure('./config.ini')