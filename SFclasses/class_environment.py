from WNS import environment as env

class EnvironmentManager:
    """
    Singleton class for sharing the enviroment with other modules

    How to get environment:  env_man = classes.EnvironmentManager().instance()
    then environment can be referenced as env_man.env1
    """
    _instance = None

    @classmethod
    def instance(cls):
        if cls._instance is None:
            print('Creating new instance')
            cls._instance = cls.__new__(cls)
            cls.env1 = env.wireless_environment(4000, sampling_time = 0.1)
        return cls._instance
    