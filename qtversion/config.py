import json
import os

class Config:
    def __init__(self):
        self.config_file = 'config.json'
        self.load_config()

    def load_config(self):
        try:
            with open(self.config_file, 'r') as f:
                self.config = json.load(f)
        except:
            self.config = {
                'database': {
                    'host': 'localhost',
                    'port': 3306,
                    'user': 'root',
                    'password': 'root',
                    'database': 'mangos'
                },
                'preferences': {
                    'theme': 'light',
                    'font_size': 12,
                    'table_row_height': 30,
                    'window_geometry': {
                        'x': 100,
                        'y': 100, 
                        'width': 1920,
                        'height': 1000
                    },
                    'splitter_sizes': [[200, 800], [300, 700]], # 添加分隔条尺寸
                    'column_widths': {}, # 添加列宽记忆
                    'expanded_nodes': [] # 添加展开节点记忆
                },
                'shortcuts': {
                    'search': 'Ctrl+F',
                    'save': 'Ctrl+S',
                    'export': 'Ctrl+E'
                },
                'paths': {
                    'dbc_output_path': '',
                    'patch_path': '',
                    'mpq_output_path': ''
                }
            }

    def save_config(self):
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=4)

    def get_database_config(self):
        return self.config['database']

    def set_database_config(self, config):
        self.config['database'] = config
        self.save_config()

    def get_preferences(self):
        return self.config['preferences']

    def set_preferences(self, preferences):
        self.config['preferences'] = preferences
        self.save_config()

    def get_shortcuts(self):
        return self.config['shortcuts']

    def set_shortcuts(self, shortcuts):
        self.config['shortcuts'] = shortcuts
        self.save_config()

    def get_paths(self):
        return self.config.get('paths', {})

    def set_paths(self, paths):
        self.config['paths'] = paths
        self.save_config() 