import os
import helpers.config as config


def get_env_var(var_name):
    """Fetch and validate an environment variable"""
    var_value = os.getenv(var_name)
    if var_value is None:
        # check if the var_name exists inside config, if so, use that value
        if var_name in config:
            var_value = config[var_name]
        else:
            raise EnvironmentError(f"{var_name} is not set")
    return var_value
