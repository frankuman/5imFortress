from BS.backend.simulation import environment as env
class environment_manager:
    """
    Singleton class for sharing the environment with other modules

    How to get environment:  env_man = classes.EnvironmentManager().instance()
    then environment can be referenced as env_man.env1
    """
    _instance = None

    @classmethod
    def instance(cls):
        if cls._instance is None:
            print('Creating new instance')
            cls._instance = cls.__new__(cls)
            cls.env1 = env.wireless_environment(4000)
        return cls._instance
    