from PyQt5 import QtWidgets, QtCore, QtGui
import requests

import zipfile
import os
import sys

from Configure import Configure
from FilesListConfig import FileListCinfig
from update_window import Ui_Update

def download_file(url: str, path: str):
	try:
		resp = requests.get(url, stream=True)
		total = int(resp.headers.get('content-length', 0))
		progress = 0

		window.progressBarSignal.emit(0)

		with open(path, 'wb') as file:
			for data in resp.iter_content(chunk_size=1024):
				size = file.write(data)
				progress += size

				try:
					percent = int((progress/total)*100)

					window.progressBarSignal.emit(int(10 + (percent * 0.8)))
				except ZeroDivisionError:
					pass
		
	except (requests.Timeout, requests.HTTPError, requests.ConnectionError, requests.exceptions.ChunkedEncodingError):
		message_box('Нет подключения к сети', 'Проверьте ваше подключение к интернету')
		sys.exit(0)

def remove_files(path: str, files: list):
	dirs = []
	for filesI in range(len(files)):
		file_path = os.path.normpath(os.path.join(path, files[filesI]))
		
		if os.path.exists(file_path):
			if os.path.isfile(file_path):
				os.remove(file_path)
			elif os.path.isdir(file_path) and not(file_path in dirs):
				dirs.append(file_path)
				continue
			
			father_dir = '\\'.join(file_path.split('\\')[0:-1])
			
			if (not(father_dir in dirs)):
				dirs.append(father_dir)

		try:
			window.progressBarSignal.emit(int( (filesI / (len(files) - len(dirs))) * 10 ))
		except ZeroDivisionError:
			pass
	
	len_files = len(files)
	len_dirs = len(dirs)

	for dirsI in range(len(dirs)):
		dir_path = dirs[dirsI]
		
		if not os.listdir(dir_path):
			os.rmdir(dir_path)
		
		try:
			window.progressBarSignal.emit(int( (len_files / len_files - (len_dirs - dirsI))) * 10 )
		except ZeroDivisionError:
			pass
	


def message_box(title, text, action=None, action_arg=()):
	global msg
	msg = QtWidgets.QMessageBox()
	msg.setWindowTitle(title)
	msg.setText(text)
	msg.setIcon(QtWidgets.QMessageBox.Warning)

	msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
	if action != None:
		msg.buttonClicked.connect(lambda: action(action_arg))

	icon = QtGui.QIcon()
	icon.addPixmap(QtGui.QPixmap('./Resourses/icons/icon.png'), QtGui.QIcon.Selected, QtGui.QIcon.On)
	msg.setWindowIcon(icon)

	msg.exec_()
	if action != None:
		action(action_arg)

class ZipFileCustom(zipfile.ZipFile):
	""" Custom ZipFile class with a callback on extractall. """
	def extractall(self, path=None, members=None, pwd=None, fn_progress=None):
		if members is None:
			members = self.namelist()
		if path is None:
			path = os.getcwd()
		else:
			path = os.fspath(path)
		for index, member in enumerate(members):
			if fn_progress:
				fn_progress(len(members), index + 1)
			self._extract_member(member, path, pwd)
	
	def getFilesList(self):
		return self.namelist()

class Downloader(QtCore.QObject):
	endSignal = QtCore.pyqtSignal(bool)

	def __init__(self, url: str, path: str, zip_path: str) -> None:
		super().__init__()

		self.path = path
		self.zip_path = zip_path
		self.url = url
	
	def calculate_percentage_zip(self, total: int, current: int):
		try:
			percent = float(current) / total
			percent = int(percent * 9)
		except ZeroDivisionError:
			percent = 0
		return percent

	def start(self):
		self.endSignal.emit(0)
		file_list_config = FileListCinfig(os.path.normpath(self.path) + '\\TS2FilesListConfig.ini')
		remove_files(self.path, file_list_config.read('files'))
		file_list_config.update('files', [])
		
		download_file(self.url, self.zip_path)

		with ZipFileCustom(self.zip_path, 'r') as zip_ref:
			file_list_config.update('files', zip_ref.getFilesList())
			zip_ref.extractall(self.path, fn_progress=lambda total, current: window.progressBarSignal.emit(90 + self.calculate_percentage_zip(total, current)))
		
		os.remove(self.zip_path)
		window.progressBarSignal.emit(100)
		self.endSignal.emit(1)

class UpdateWindow(Ui_Update):
	modpacks = {}

	def __init__(self) -> None:
		super().__init__()

		if config.read('General', 'mods_folder') != '':
			self.folderEdit.setText(os.path.normpath(config.read('General', 'mods_folder')))
		else:
			self.folderEdit.setText(os.environ['APPDATA'] + '\\.minecraft\\mods')

		self.resize(int(config.read('Windows', 'settings_x')), int(config.read('Windows', 'settings_y')))

		try:
			response = requests.post(config.read('General', 'server'))
		except (requests.Timeout, requests.HTTPError, requests.ConnectionError):
			message_box('Нет подключения к сети', 'Проверьте ваше подключение к интернету', sys.exit, (0,))

		for modpack_name in response.json():
			self.modpacks[modpack_name] = response.json()[modpack_name]
			self.modpacksComboBox.addItem(modpack_name)
	
	def folderEditEvent(self):
		config.update('General', 'mods_folder', self.folderEdit.text())

	def updateButtonClicked(self):
		modpack_name = self.modpacksComboBox.currentText()
		if modpack_name != '':
			try:
				path = os.path.normpath(self.folderEdit.text())

				if not(os.path.exists(path)):
					os.mkdir(path)

				zip_path = path + '\\_ts2temp.zip'

				self.thread_downloader = QtCore.QThread()
				self.downloader = Downloader(self.modpacks[modpack_name], path, zip_path)

				self.downloader.moveToThread(self.thread_downloader)

				self.thread_downloader.started.connect(self.downloader.start)
				self.downloader.endSignal.connect(self.progressBarEnabling)

				self.thread_downloader.start()

			except FileNotFoundError:
				message_box("Указанный путь не найден", "Проверьте правильность пути или попробуйте указать новый. Желательно, чтобы символы были только из английского алфавита")

	def progressBarEnabling(self, value: bool):
		if value:
			self.progressBar.hide()
			self.thread_downloader.quit()
		else:
			self.progressBar.show()
		
	def resizeEvent(self, event):
		super().resizeEvent(event)
		config.update('Windows', 'settings_x', str(self.size().width()))
		config.update('Windows', 'settings_y', str(self.size().height()))

if __name__ == '__main__':
	directory = os.getcwd()
	
	global config
	config_path = os.environ['USERPROFILE'] + '\\Documents' + '\\TS2MinecraftModsUpdaterConfig.ini'
	config = Configure(config_path)
	
	app = QtWidgets.QApplication(sys.argv)

	window = UpdateWindow()
	window.show()

	sys.exit(app.exec_())