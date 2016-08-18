__author__ = 'shen'

import os
from ConfigParser import SafeConfigParser, NoSectionError

from test import sys_env

_config_files_paths = []


def _extract_conf_file_name(file_name):
    base_name = os.path.basename(file_name)
    if base_name.endswith(".conf"):
        return base_name[:-len(".conf")]
    else:
        return base_name


def _search_config_file(file_name):
    if not file_name.endswith(".conf"):
        full_file_name = file_name + ".conf"
    else:
        full_file_name = file_name

    for p in _config_files_paths:
        config_file_name = os.listdir(p)

        if full_file_name in config_file_name and os.path.isfile(p + os.sep + full_file_name):
            return p + os.sep + full_file_name
        elif file_name != full_file_name and file_name in config_file_name and os.path.isfile(p + os.sep + file_name):
            return p + os.sep + full_file_name

    return None


class ConfigParseError(Exception):
    pass


class ConfigMissingError(ConfigParseError):
    pass


class IntItemParser:
    @staticmethod
    def parse(value):
        try:
            return int(value)
        except:
            raise ConfigParseError(("Can't parse %s as integer" % str(value)))

    @staticmethod
    def get_type_str():
        return "int"

    @staticmethod
    def is_type(value):
        # Judge whether "value" is the type of "int" or not
        return isinstance(value, int)


class FloatItemParser:
    @staticmethod
    def parse(value):
        try:
            return float(value)
        except:
            raise ConfigParseError("Can't parse %s as float" % str(value))

    @staticmethod
    def get_type_str():
        return "float"

    @staticmethod
    def is_type(value):
        return isinstance(value, float)


class StrItemParser:
    def __init__(self, remove_quote=True):
        self._remove_quote = remove_quote

    def parse(self, value):
        str_value = str(value).strip()
        if self._remove_quote and \
                str_value.startswith("\"") and \
                str_value.endswith("\""):
            str_value = str_value[1:-1]
        return str_value

    @staticmethod
    def get_type_str():
        return "string"

    @staticmethod
    def is_type(value):
        # Note that we only support ASCII string. Unicode and
        # bytes object would not be considered as string
        return type(value) is str


class ListItemParser:
    def __init__(self, bracket="[]", element_parser=StrItemParser()):
        self._ele_parser = element_parser
        self._bracket = bracket

    def parse(self, value):
        value = str(value).strip()
        if not (value.startswith(self._bracket[0]) and
              value.endswith(self._bracket[1])):
            raise ConfigParseError("Can't parse %s as list" % value)

        return [self._ele_parser.parse(x.strip()) for x in value[1:-1].split(LIST_ELE_SEP)
                if len(x.strip()) > 0]

    @staticmethod
    def get_type_str():
        return "list"

    @staticmethod
    def is_type(value):
        return isinstance(value, list)


class TupleItemParser(ListItemParser):
    def __init__(self, element_parser=StrItemParser()):
        ListItemParser.__init__(self, "()", element_parser)

    @staticmethod
    def get_type_str():
        return "tuple"

    @staticmethod
    def is_type(value):
        return isinstance(value, tuple)

    def parse(self, value):
        return tuple(ListItemParser.parse(self, value))


class BooleanItemParser:
    @staticmethod
    def parse(value):
        value = value.strip().lower()
        if value == "true" or value == "1":
            return True
        elif value == "false" or value == "0":
            return False
        elif isinstance(value, int):
            return value != 0
        else:
            raise ConfigParseError("Can't parse %s as boolean" % value)

    @staticmethod
    def get_type_str():
        return "boolean"

    @staticmethod
    def is_type(value):
        return value in (True, False)


# An Configs object corresponds to a section in a .conf file.
# Configs should be instantiated by a module in meditator.
class Configs:
    # This buffer contains all the Configs object having been parsed
    # before. The key is like "conf_file_name.section_name". The value
    # is a Configs object.
    _configs_buffer = dict()

    # conf_file must be the refined version
    def __init__(self, conf_file, section, section_items):
        refined_items = [(x[0].strip(), x[1].strip()) for x in section_items]
        self._configs = dict(refined_items)
        self._conf_file = conf_file
        self._section = section
        self._updated = False

    def is_updated(self, set_false=True):
        return_val = self._updated
        if set_false:
            self._updated = False
        return return_val

    def set_updated(self, flag=True):
        self._updated = flag

    def get_absolute_name(self):
        return self.get_section() + "." + self.get_conf_file_name()

    def get_section(self):
        return self._section

    def get_conf_file_name(self):
        return self._conf_file

    def get_conf_items(self):
        return self._configs.items()

    def get_conf_keys(self):
        return self._configs.keys()

    def get_conf_values(self):
        return self._configs.values()

    def get_conf_except(self, exclude_keys):
        return {k: self._configs[k] for k in self._configs
                if k not in exclude_keys}

    @staticmethod
    def _try_use_default(default, has_default, err_msg):
        if default is not None or has_default:
            return default
        else:
            raise ConfigMissingError(err_msg)

    def set(self, name, value, set_update=True):
        self._configs[name] = value
        if set_update:
            self._updated = True

    def get(self, name, default=None, has_default=False, remove_quote=True):
        if name in self._configs:
            # Note that strip() is not needed. We have done this in
            # __init__ method.
            item = self._configs[name]
            if remove_quote and item.startswith("\"") and item.endswith("\""):
                item = item[1:-1]
            return item
        else:
            return Configs._try_use_default(default, has_default,
                                            "Can't find config:%s" % name)

    def get_int(self, name, default=None, has_default=False):
        item = ""
        try:
            item = self.get(name)
            return int(item)
        except ConfigMissingError as e:
            return Configs._try_use_default(default, has_default,
                                            e.message)
        except:
            raise ConfigParseError("Can't parse %s as integer" % str(item))

    def get_float(self, name, default=None, has_default=False):
        item = ""
        try:
            item = self.get(name)
            return float(item)
        except ConfigMissingError as e:
            return Configs._try_use_default(default, has_default,
                                            e.message)
        except:
            raise ConfigParseError("Can't parse %s as float" % str(item))

    def get_bool(self, name, default=None, has_default=False):
        try:
            item = self.get(name).strip().lower()
        except ConfigMissingError as e:
            return Configs._try_use_default(default, has_default,
                                            e.message)

        if item == "true" or item == "1":
            return True
        elif item == "false" or item == "0":
            return False
        else:
            raise ConfigParseError("Can't parse %s as boolean" % item)

    def get_tuple(self, name, ele_parser=StrItemParser(),
                  default=None, has_default=False, require_bracket=False):
        list_result = self.get_list(name, bracket="()",
                                   ele_parser=ele_parser,
                                   default=default, has_default=has_default,
                                   require_bracket=require_bracket)
        return tuple(list_result) if list_result is not None else list_result

    def get_list(self, name, bracket="[]", ele_parser=StrItemParser(),
                 default=None, has_default=False, require_bracket=False):
        try:
            item = self.get(name)
        except ConfigMissingError as e:
            return Configs._try_use_default(default, has_default, e.message)

        if require_bracket and \
                not (item.startswith(bracket[0]) and
                      item.endswith(bracket[1])):
            raise ConfigParseError("Can't parse %s as list" % item)

        if not item.startswith(bracket[0]):
            item = bracket[0] + item

        if not item.endswith(bracket[1]):
            item += bracket[1]

        try:
            return [ele_parser.parse(x.strip())
                    for x in item[1:-1].split(LIST_ELE_SEP)
                    if len(x.strip()) > 0]
        except:
            raise ConfigParseError("Elements in %s can't be parsed" % item)

    def get_configs(self, name, default=None, has_default=False):
        try:
            item = self.get(name)
        except ConfigMissingError as e:
            return Configs._try_use_default(default, has_default, e.message)

        return self.parse_refname(item)

    def parse_refname(self, refname):
        # !!!!!
        # The code may needed to be polished by using regular expression.
        if "." not in refname:
            return Configs.parse(self.get_conf_file_name(), refname)
        else:
            seps = [x.strip() for x in refname.split(".")]
            if len(seps) != 2 or any([len(x) == 0 for x in seps]):
                raise ConfigParseError("Can't parse %s as configs" % refname)

            return Configs.parse(seps[0], seps[1])

    @staticmethod
    def parse(conf_name, section):
        refined_conf_name = _extract_conf_file_name(conf_name)
        limited_conf_name = "".join([refined_conf_name, ".", section])
        if limited_conf_name in Configs._configs_buffer:
            return Configs._configs_buffer[limited_conf_name]

        conf_file_parser = ConfigFileParser.parse(conf_name)
        configs = Configs(refined_conf_name, section,
                          conf_file_parser.get_section(section))
        Configs._configs_buffer[limited_conf_name] = configs
        return configs


class ConfigFileParser(SafeConfigParser):
    # This buffer is used to avoid parsing a .conf file repeatedly.
    # The key is conf file name and the value is a ConfigFileParser
    # object.
    _file_parse_buffer = dict()

    def __init__(self):
        SafeConfigParser.__init__(self)

    def get_section(self, section):
        try:
            return self.items(section)
        except NoSectionError:
            raise ConfigMissingError("Can't find section %s" % section)

    @staticmethod
    def parse(conf_file_name):
        refined_conf_name = _extract_conf_file_name(conf_file_name)

        # If we have parsed this file, just return the result
        if refined_conf_name in ConfigFileParser._file_parse_buffer:
            return ConfigFileParser._file_parse_buffer[refined_conf_name]

        # Firstly, we search all possible paths to try to find out the
        # the path of conf_file_name
        if any([sep in conf_file_name for sep in "\\/"]):
            conf_file_path = conf_file_name.replace("$SYS_DIR",
                                                    sys_env.get_sys_dir())
        else:
            conf_file_path = _search_config_file(refined_conf_name)

        if conf_file_path is None:
            raise ConfigMissingError("Can't find configuration file:%s" %
                                     conf_file_name)

        # Then instantiate a ConfigFileParser and parse the file.
        cf_parser = ConfigFileParser()
        # set the optionxform function in order to be case-sensitive
        cf_parser.optionxform = str
        try:
            cf_parser.read(conf_file_path)
        except Exception as e:
            raise ConfigParseError("Can't parse configuration %s:%s" %
                                   (conf_file_name, e.message))

        # Lastly, buffer the parse result and return it
        ConfigFileParser._file_parse_buffer[refined_conf_name] = cf_parser
        return cf_parser


if __name__ == "__main__":
    # parser = SafeConfigParser()
    # parser.optionxform = str
    # parser.read("fra_conf.conf")
    # items = parser.items("random_forest_regressions", True)

    parser = ConfigFileParser()
    parser.optionxform = str
    parser.read("fra_conf.conf")
    items = parser.items("random_forest_regressions", True)
    list = ListItemParser()
    list.parse(items)
    print items
