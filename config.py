import configparser

ENCODING_INI = 'utf-8'


class Config:

    def __init__(self, ini: str):
        self.ini = ini
        self.config = configparser.ConfigParser()
        self.pathFolder: str = './'
        self.extensionFile: str = ''
        self.levelDir: int = 1

    def getstring(self, section, option, fallback):
        string = self.config.get(section, option, fallback=fallback)
        if string:
            return string
        else:
            return fallback

    def getfloat(self, section, option, fallback):
        try:
            return self.config.getfloat(section, option, fallback=fallback)
        except ValueError:
            return fallback

    def getint(self, section, option, fallback):
        try:
            return self.config.getint(section, option, fallback=fallback)
        except ValueError:
            return fallback

    def getboolean(self, section, option, fallback):
        try:
            return self.config.getboolean(section, option, fallback=fallback)
        except ValueError:
            return fallback

    def load(self):
        self.config.read(self.ini, encoding=ENCODING_INI)
        self.pathFolder = self.getstring('Options',
                                         'path_folder',
                                         fallback=self.pathFolder)
        self.extensionFile = self.getfloat('Options',
                                           'extension_file',
                                           fallback=self.extensionFile)
        self.levelDir = self.getint('Options',
                                    'level_dir',
                                    fallback=self.levelDir)

    def save(self) -> str:
        self.config['Options'] = {
            'path_folder': self.pathFolder,
            'extension_file': self.extensionFile,
            'level_dir': self.levelDir
        }
        try:
            with open(self.ini, 'w', encoding=ENCODING_INI) as configfile:
                self.config.write(configfile)
                return 'Building configuration file completed successfully.'
        except Exception as exc:
            return f'Error building configuration file "{exc}": {self.ini}'
