from collections.abc import MutableMapping
class LayeredDict(MutableMapping):
    def __init__(self, data=None):
        """
        Initialize the LayeredDict with an optional dictionary.
        
        :param data: The initial dictionary to wrap (default: None).
        """
        super().__setattr__("_data", self._convert_to_layered_dict(data or {}))

    def _convert_to_layered_dict(self, obj):
        """
        Recursively convert nested dictionaries to LayeredDict instances.

        :param obj: The object to convert.
        :return: The converted object.
        """
        if isinstance(obj, dict):
            return {k: self._convert_to_layered_dict(v) for k, v in obj.items()}
        return obj

    def _get_nested(self, key, create_missing=False):
        """
        Traverse or create nested dictionaries based on a dot-separated key.

        :param key: Dot-separated key string (e.g., "key1.key2.key3").
        :param create_missing: Whether to create missing intermediate dictionaries.
        :return: A tuple of (final dictionary, last key).
        """
        keys = key.split(".")
        current = self._data
        for k in keys[:-1]:
            if k not in current:
                if create_missing:
                    current[k] = {}
                else:
                    raise KeyError(f"Key '{k}' not found.")
            current = current[k]
        return current, keys[-1]

    def get(self, key, default=None):
        """
        Retrieve a value from the nested dictionary using a dot-separated key.

        :param key: Dot-separated key string (e.g., "key1.key2.key3").
        :param default: Value to return if the key is not found (default: None).
        :return: The value if found, else the default.
        """
        try:
            current, last_key = self._get_nested(key)
            return current[last_key]
        except KeyError:
            return default

    def set(self, key, value):
        """
        Set a value in the nested dictionary using a dot-separated key.

        :param key: Dot-separated key string (e.g., "key1.key2.key3").
        :param value: The value to set.
        """
        current, last_key = self._get_nested(key, create_missing=True)
        current[last_key] = self._convert_to_layered_dict(value)

    def delete(self, key):
        """
        Delete a key from the nested dictionary using a dot-separated key.

        :param key: Dot-separated key string (e.g., "key1.key2.key3").
        """
        current, last_key = self._get_nested(key)
        if last_key in current:
            del current[last_key]
        else:
            raise KeyError(f"Key '{last_key}' not found.")

    def to_dict(self):
        """
        Get the underlying dictionary.

        :return: The wrapped dictionary.
        """
        def unwrap(obj):
            if isinstance(obj, dict):
                return {k: unwrap(v) for k, v in obj.items()}
            return obj

        return unwrap(self._data)

    def __getitem__(self, key):
        """
        Enable dictionary-like access using bracket notation.

        :param key: Dot-separated key string (e.g., "key1.key2.key3").
        :return: The value if found.
        """
        return self.get(key)

    def __setitem__(self, key, value):
        """
        Enable dictionary-like setting using bracket notation.

        :param key: Dot-separated key string (e.g., "key1.key2.key3").
        :param value: The value to set.
        """
        self.set(key, value)

    def __delitem__(self, key):
        """
        Enable dictionary-like deletion using bracket notation.

        :param key: Dot-separated key string (e.g., "key1.key2.key3").
        """
        self.delete(key)

    def __iter__(self):
        """
        Return an iterator over the top-level keys of the dictionary.
        """
        return iter(self._data)

    def __len__(self):
        """
        Return the number of top-level keys in the dictionary.
        """
        return len(self._data)

    def __contains__(self, key):
        """
        Check if a dot-separated key exists in the dictionary.
        """
        try:
            self.get(key)
            return True
        except KeyError:
            return False

    def __getattr__(self, name):
        """
        Enable attribute-like access for top-level keys.
        
        :param name: The attribute name.
        :return: The value associated with the key.
        """
        try:
            return self._data[name]
        except KeyError:
            raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")

    def __setattr__(self, name, value):
        """
        Enable attribute-like setting for top-level keys.

        :param name: The attribute name.
        :param value: The value to set.
        """
        if name == "_data":
            super().__setattr__(name, value)
        else:
            self._data[name] = self._convert_to_layered_dict(value)