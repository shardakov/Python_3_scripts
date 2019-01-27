#!/usr/bin/env python3

from xml.dom import minidom
from yaml import load
import argparse


class TestClass(object):

    _args = {}
    _config = {}
    _name_base = {}

    def __init__(self):
        self.parse_args()
        self.parse_config()
        self.input_in_xml_file()

    def parse_args(self):
        parser = argparse.ArgumentParser(description='Generate clickhous dictionary from template')
        parser.add_argument('--config', '-c', default='tmp', type=str, nargs='?')
        parser.add_argument('--name_base', '-n', default='tmp', type=str, nargs='?')
        self._args = parser.parse_args()

    def parse_config(self):
        config = self._args.config
        try:
            with open(config) as c:
                self._config = load(c)
            # print(self._config)
        except Exception as e:
            print('Config file "{}" invalid!\n{}'.format(config, str(e)))
            exit(1)

    def input_in_xml_file(self):
        tmp_dict = self._config.copy()

        dict_name = self._args.name_base

        doc = minidom.Document()

        dictionaries = doc.createElement('dictionaries')
        doc.appendChild(dictionaries)

        comment = doc.createElement('comment')
        text = doc.createTextNode('Local File dictionary with company device_network_generation list details')
        comment.appendChild(text)
        dictionaries.appendChild(comment)

        dictionary = doc.createElement('dictionary')

        name = doc.createElement('name')
        text_name = doc.createTextNode(dict_name)
        name.appendChild(text_name)
        dictionary.appendChild(name)

        source = doc.createElement('source')

        if tmp_dict[dict_name]['source'] == 'file':
            file = doc.createElement('file')

            file_path = doc.createElement('path')
            file_path_text = doc.createTextNode(str(tmp_dict[dict_name]['file_path']))
            file_path.appendChild(file_path_text)
            file.appendChild(file_path)

            file_format = doc.createElement('format')
            file_format_text = doc.createTextNode(str(tmp_dict[dict_name]['file_format']))
            file_format.appendChild(file_format_text)
            file.appendChild(file_format)

            source.appendChild(file)

        elif tmp_dict[dict_name]['source'] == 'sql':
            sql = doc.createElement('mysql')

            sql_port = doc.createElement('port')
            sql_port_text = doc.createTextNode(str(tmp_dict[dict_name]['sql_port']))
            sql_port.appendChild(sql_port_text)
            sql.appendChild(sql_port)

            sql_user = doc.createElement('user')
            sql_user_text = doc.createTextNode(str(tmp_dict[dict_name]['sql_user']))
            sql_user.appendChild(sql_user_text)
            sql.appendChild(sql_user)

            sql_password = doc.createElement('password')
            sql_password_text = doc.createTextNode(str(tmp_dict[dict_name]['sql_password']))
            sql_password.appendChild(sql_password_text)
            sql.appendChild(sql_password)

            if tmp_dict[dict_name]['replica']:
                for key in tmp_dict[dict_name]['replica']:

                    replica = doc.createElement('replica')

                    host = doc.createElement('host')
                    host_text = doc.createTextNode(str(tmp_dict[dict_name]['replica'][key]['host']))
                    host.appendChild(host_text)
                    replica.appendChild(host)

                    priority = doc.createElement('priority')
                    priority_text = doc.createTextNode(str(tmp_dict[dict_name]['replica'][key]['priority']))
                    priority.appendChild(priority_text)
                    replica.appendChild(priority)

                    sql.appendChild(replica)

            db = doc.createElement('db')
            db_text = doc.createTextNode(str(tmp_dict[dict_name]['db']))
            db.appendChild(db_text)
            sql.appendChild(db)

            table = doc.createElement('table')
            table_text = doc.createTextNode(str(tmp_dict[dict_name]['table']))
            table.appendChild(table_text)
            sql.appendChild(table)

            source.appendChild(sql)
        dictionary.appendChild(source)

        layout = doc.createElement('layout')
        if tmp_dict[dict_name]['layout'] == 'hashed':
            hashed = doc.createElement('hashed')
            layout.appendChild(hashed)
        elif tmp_dict[dict_name]['layout'] == 'flat':
            flat = doc.createElement('flat')
            layout.appendChild(flat)
        dictionary.appendChild(layout)

        structure = doc.createElement('structure')

        structure_id = doc.createElement('id')

        name_id = doc.createElement('name')
        name_id_text = doc.createTextNode('browser_id')
        name_id.appendChild(name_id_text)
        structure_id.appendChild(name_id)

        type_id = doc.createElement('type')
        type_id_text = doc.createTextNode('UInt64')
        type_id.appendChild(type_id_text)
        structure_id.appendChild(type_id)

        structure.appendChild(structure_id)

        for keys in tmp_dict[dict_name]['attribute']:
            attribute = doc.createElement('attribute')

            name = doc.createElement('name')
            name_text = doc.createTextNode(str(tmp_dict[dict_name]['attribute'][keys]['name']))
            name.appendChild(name_text)
            attribute.appendChild(name)

            type = doc.createElement('type')
            type_text = doc.createTextNode(str(tmp_dict[dict_name]['attribute'][keys]['type']))
            type.appendChild(type_text)
            attribute.appendChild(type)

            null_value = doc.createElement('null_value')
            null_value_text = doc.createTextNode(str(tmp_dict[dict_name]['attribute'][keys]['null_value']))
            null_value.appendChild(null_value_text)
            attribute.appendChild(null_value)

            structure.appendChild(attribute)

        dictionary.appendChild(structure)

        lifetime = doc.createElement('lifetime')

        lifetime_min = doc.createElement('min')
        lifetime_min_text = doc.createTextNode(str(tmp_dict[dict_name]['lifetime_min']))
        lifetime_min.appendChild(lifetime_min_text)
        lifetime.appendChild(lifetime_min)

        lifetime_max = doc.createElement('max')
        lifetime_max_text = doc.createTextNode(str(tmp_dict[dict_name]['lifetime_max']))
        lifetime_max.appendChild(lifetime_max_text)
        lifetime.appendChild(lifetime_max)

        dictionary.appendChild(lifetime)

        dictionaries.appendChild(dictionary)

        xml_str = doc.toprettyxml(indent="  ")
        with open(dict_name + '.xml', "w") as f:
            f.write(xml_str)


if __name__ == '__main__':
    t = TestClass()
    t.parse_args()
    t.parse_config()
    t.input_in_xml_file()
