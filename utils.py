from configparser import ConfigParser


def parse_settings(filename):
    settings = dict()
    config = ConfigParser(allow_no_value=True)
    config.read(filename)

    for section in config.sections():
        settings[section] = dict()
        for option in config.options(section):
            settings[section][option] = config.get(section, option)

    return settings


def is_blacked(domain, blacklist):
    blacked = True

    for item in blacklist.keys():
        blacked = True if domain.matchSuffix(item) else False

    return blacked

