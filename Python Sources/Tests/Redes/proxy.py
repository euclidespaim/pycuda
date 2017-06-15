import winreg as winreg
import configparser
import ctypes
import os

WIN_PROXY = u'10.138.15.10:8080'
MERCURIAL_PROXY = u'http://87.254.212.121:8080'


class Registry(object):
    def __init__(self, key_location, key_path):
        self.reg_key = winreg.OpenKey(key_location, key_path, 0, winreg.KEY_ALL_ACCESS)

    def set_key(self, name, value):
        try:
            _, reg_type = winreg.QueryValueEx(self.reg_key, name)
        except WindowsError:
            # If the value does not exists yet, we guess use a string as the
            # reg_type
            reg_type = winreg.REG_SZ
        winreg.SetValueEx(self.reg_key, name, 0, reg_type, value)

    def delete_key(self, name):
        try:
            winreg.DeleteValue(self.reg_key, name)
        except WindowsError:
            # Ignores if the key value doesn't exists
            pass


class WindowsProxy(Registry):
    # See http://msdn.microsoft.com/en-us/library/aa385328(v=vs.85).aspx
    # Causes the proxy data to be reread from the registry for a handle. No buffer
    # is required. This option can be used on the HINTERNET handle returned by
    # InternetOpen. It is used by InternetSetOption.
    INTERNET_OPTION_REFRESH = 37

    # Notifies the system that the registry settings have been changed so that it
    # verifies the settings on the next call to InternetConnect. This is used by
    # InternetSetOption.
    INTERNET_OPTION_SETTINGS_CHANGED = 39

    def __init__(self):
        super(WindowsProxy, self).__init__(winreg.HKEY_CURRENT_USER,
                                           r'Software\Microsoft\Windows\CurrentVersion\Internet Settings')
        self.internet_set_option = ctypes.windll.Wininet.InternetSetOptionW

    def on(self):
        self.set_key('ProxyEnable', 1)
        self.set_key('ProxyOverride', u'*.local;<local>')  # Bypass the proxy for localhost
        self.set_key('ProxyServer', WIN_PROXY)

        self.refresh()

    def off(self):
        self.set_key('ProxyEnable', 0)

        self.refresh()

    def refresh(self):
        self.internet_set_option(0, self.INTERNET_OPTION_REFRESH, 0, 0)
        self.internet_set_option(0, self.INTERNET_OPTION_SETTINGS_CHANGED, 0, 0)


class MercurialProxy(object):
    def __init__(self):
        self.mercurial_ini = os.path.join(os.path.expanduser('~'), 'Mercurial.ini')

        self.config = ConfigParser.ConfigParser()
        self.config.read(self.mercurial_ini)

    def on(self):
        try:
            self.config.add_section('http_proxy')
        except ConfigParser.DuplicateSectionError:
            pass

        self.config.set('http_proxy', 'host', MERCURIAL_PROXY)
        self.save()

    def off(self):
        try:
            self.config.remove_section('http_proxy')
        except ConfigParser.NoSectionError:
            pass
        self.save()

    def save(self):
        with open(self.mercurial_ini, 'wb') as updated_config:
            self.config.write(updated_config)
