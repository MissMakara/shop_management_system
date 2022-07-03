import configparser
import os


class ConfigsParser(object):
    DEVELOPMENT_ENV_CONFIG = None
    PRODUCTION_ENV_CONFIG = None

    @staticmethod
    def parse_configs(csection='DEFAULT'):
        try:
            cur_dir = os.path.dirname(os.path.realpath(__file__))
            '''if local config exists switch to developent and set git ignore dev configs'''
            ConfigsParser.DEVELOPMENT_ENV_CONFIG = os.path.join(cur_dir, '../configs/configs_local.ini')
            ConfigsParser.PRODUCTION_ENV_CONFIG = os.path.join(cur_dir, '../configs/configs.ini')

            filename = ConfigsParser.PRODUCTION_ENV_CONFIG

            if os.path.exists(ConfigsParser.DEVELOPMENT_ENV_CONFIG):
                ''' switched env loading development environment configs'''
                filename = ConfigsParser.DEVELOPMENT_ENV_CONFIG

            cparser = configparser.ConfigParser()
            sects1 = cparser.sections()
            if os.path.isfile(filename):
                cparser.read(filename)
            else:
                print(filename, " does not exist...")

            config_dic = {}

            sects = cparser.sections()
            list_len = len(sects)
            s = 0
            for s in range(list_len):
                cdata = {}
                for key, val in cparser[sects[s]].items():
                    cdata[key] = val

                config_dic[sects[s]] = cdata

            if csection:
                return config_dic.get(csection)
            return config_dic
        except Exception as e:
            return {}
