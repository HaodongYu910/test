import os
import yaml


def readYaml():
    path = "/usr/local/prometheus/prometheus.yml"
    with open(path, "r") as yaml_file:
        yaml_obj = yaml.load(yaml_file.read())

def writeYaml():
    path = "/usr/local/prometheus/prometheus.yml"
    with open(path, "r") as yaml_file:
        yaml_obj = yaml.load(yaml_file.read())

        main_yaml = open(path, 'w')
        yaml.dump(yaml_obj, main_yaml)
        main_yaml.close()
