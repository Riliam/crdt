class CvRDTBase:
    replicas_count = 0
    replicas = []

    def __new__(cls, *args, **kwargs):
        instance = super(CvRDTBase, cls).__new__(cls, *args, **kwargs)
        instance.id = cls.replicas_count
        cls.replicas.append(instance)
        cls.replicas_count += 1
        for r in cls.replicas:
            r.reinitialize()
        return instance

    def __repr__(self):
        return '<{0} replica; ID: {1}>'.format(self.__class__.__name__, self.id)

    def __eq__(self, other):
        return self.id == other.id

    def __ne__(self, other):
        return not self.__eq__(other)

    @classmethod
    def send_state_to_other_replicas(cls, func):
        """ Decorates operation.
        Calls .merge on every replica other than self
        after performing operation.
        """

        def wrapper(instance, *args, **kwargs):
            result = func(instance, *args, **kwargs)
            for replica in cls.replicas:
                if replica != instance:
                    replica.merge(instance)
            return result

        return wrapper

    def reinitialize(self):
        """ Updates initial state of instance, e.g. if it depends on
        replicas_count.
        If initial state is independent of replicase_count,
        use __init__ instead.
        """
        pass

    def merge(self, other):
        """ Merges state of `other` instance into self """
        raise NotImplementedError
