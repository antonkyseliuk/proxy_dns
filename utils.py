from configparser import ConfigParser


def parse_settings(filename):
    """
        Function to parse settings from configuration file
    """
    settings = dict()
    config = ConfigParser(allow_no_value=True)
    config.read(filename)

    for section in config.sections():
        settings[section] = dict()
        for option in config.options(section):
            settings[section][option] = config.get(section, option)

    return settings


def is_blacked(domain, blacklist):
    """
        Function returns True if domain in the blacklist
    """
    for item in blacklist:
        if domain.matchSuffix(item):
            return True

    return False
