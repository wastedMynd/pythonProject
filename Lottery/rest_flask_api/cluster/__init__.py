# read cluster setup properties
import os
from Lottery.rest_flask_api.__init__ import Logging
import yaml

logger = Logging().get_logger()


@Logging
def get_cluster_properties(cluster_properties_file_yaml=None):
    if cluster_properties_file_yaml is None:
        cluster_properties_file_yaml = os.path.join(
            "/home/sizwe/PycharmProjects/pythonProject/Lottery/rest_flask_api/cluster/",
            'cluster_properties.yaml'
        )

    if not os.path.exists(cluster_properties_file_yaml):
        logger.critical(f"Settings yaml file {cluster_properties_file_yaml} does not exist!!!")
        return None

    try:
        with open(cluster_properties_file_yaml, 'r') as yaml_stream:
            return yaml.load(yaml_stream, Loader=yaml.SafeLoader)
    except:
        logger.critical(f"Cannot read yaml config file {cluster_properties_file_yaml}, check formatting.")
        return None


@Logging
def get_cluster_url(cluster_properties_file_yaml=None) -> str:
    # get cluster properties
    properties = get_cluster_properties(cluster_properties_file_yaml)
    return str(properties.get("cluster")["url"]).format(
        properties.get("user")["name"],
        properties.get("user")["password"],
        properties.get("cluster")["database"]
    )


if __name__ == '__main__':
    print(get_cluster_url())
