class LazyLoadingRegister:
    """Lazily instantiates controllers on first access for improved startup performance."""

    def __init__(self, controller_map):
        """
        Args:
            controller_map: Dict mapping routes to controller classes (not instances).
        """
        self._controller_classes = controller_map
        self._instances = {}

    def get(self, route, default=None):
        """Get controller instance, instantiating on first access."""
        if route not in self._controller_classes:
            return default

        if route not in self._instances:
            controller_class = self._controller_classes[route]
            self._instances[route] = controller_class()

        return self._instances[route]

    def __getitem__(self, route):
        """Support dict-style access."""
        return self.get(route)
