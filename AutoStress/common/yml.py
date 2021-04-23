import os
import yaml


def readYaml():
    path ="C:\\Users\\yinhang\\Desktop"
    #path = "/usr/local/prometheus"
    with open(os.path.join(path, "prometheus.yml"), 'r', encoding='utf-8') as file:
        yamlData = yaml.load(file, Loader=yaml.FullLoader)
    return yamlData

def writeYaml(ip):
    path = "C:\\Users\\yinhang\\Desktop"
    # path = "/usr/local/prometheus/prometheus.yml"
    # with open(path) as f:
    #     doc = yaml.safe_load(f)
    # doc['nc'] = state
    # with open(path, 'w') as f:
    #     yaml.safe_dump(doc, f, default_flow_style=False)

    with open(os.path.join(path, "prometheus.yml"), 'r', encoding='utf-8') as file:
        yamlData = yaml.load(file, Loader=yaml.FullLoader)
        print(yamlData["scrape_configs"][2]["static_configs"][0]["targets"])
    yamlData["scrape_configs"][2]["static_configs"][0]["targets"] = yamlData["scrape_configs"][2]["static_configs"][0]["targets"].append("177.168.1.125:9100")
    with open(os.path.join(path, "prometheus.yml"), 'w') as f:
        yaml.dump(yamlData, f)

