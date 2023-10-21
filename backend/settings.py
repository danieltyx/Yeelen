import toml
import copy
import hashlib
from pathlib import Path

CONFIG_FILE_PATH = Path(__file__).parent / 'config/'

class Settings:
	def checksum(self, filename, hash_factory=hashlib.md5, chunk_num_blocks=128):
		h = hash_factory()
		with open(filename,'rb') as f: 
			while chunk := f.read(chunk_num_blocks*h.block_size): 
				h.update(chunk)
		return h.digest()

	def reload_file(self, file):
		file_hash = self.checksum(file)

		if file in self.files_to_hash and self.files_to_hash[file] == file_hash:
			return

		self.files_to_hash[file] = file_hash
		
		config_settings = toml.load(file)
		self.toml_data.update(config_settings)

		for config_setting in config_settings:
			self.config_to_file[config_setting] = file

	def reload_files(self):
		for config_file in Path(CONFIG_FILE_PATH).iterdir():
			if not config_file.is_file():
				continue
			
			config_str = str(config_file)

			if config_str[-5:] != ".toml":
				continue

			self.reload_file(config_str)

	def __init__(self, dev=False):
		self.toml_data = {}
		self.files_to_hash = {}
		self.config_to_file = {}

		self.dev = dev

		self.reload_files()

	def get_config(self, config):
		config_data = self.toml_data
		config_keys = config.split('.')
		self.reload_file(self.config_to_file[config_keys[0]])

		for key in config_keys:
			config_data = config_data[key]

		config_type = type(config_data)

		if config_type == list or config_type == dict:
			return copy.deepcopy(config_data)

		return config_data
	
	def __getitem__(self, key):
		return self.get_config(key)