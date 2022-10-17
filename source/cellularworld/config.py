import yaml
import box
import pprint


config = box.Box()


def initialise(yaml_path='config.yaml'):
    global config
    with open(yaml_path) as file:
        config.update(yaml.safe_load(file))
    pprint.pprint(config)
