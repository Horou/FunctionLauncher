import json
from InstanceConstructorMixin import InstanceConstructorMixin


class JsonObjectEncoder(json.JSONEncoder):
    create_class = InstanceConstructorMixin.create_class

    #####################################################################

    @staticmethod
    def dumps(obj, indent=None):
        return json.dumps(obj, cls=JsonObjectEncoder, indent=indent)

    @staticmethod
    def loads(obj: str):
        return json.loads(obj, object_hook=JsonObjectEncoder.hook)

    #####################################################################

    def default(self, obj):
        if obj.__class__.__name__ in self.create_class:
            result = obj.to_representation() if hasattr(obj, 'to_representation') else self.cleaner(obj.__dict__)
            result["__class__"] = obj.__class__.__name__
            return result
        return str(obj)

    @staticmethod
    def hook(obj: dict):
        if "__class__" in obj:
            class_name = obj.pop("__class__")
            return JsonObjectEncoder.create_class[class_name](obj)
        return {
            (JsonObjectEncoder.str_to_type(k) if isinstance(k, str) else k):
                (JsonObjectEncoder.str_to_type(v) if isinstance(v, str) else v)
            for k, v in obj.items()
        }

    #####################################################################

    @staticmethod
    def cleaner(obj):
        if isinstance(obj, dict):
            return {(str(k) if isinstance(k, tuple) else k): JsonObjectEncoder.cleaner(v) for k, v in obj.items()}
        if isinstance(obj, (list, tuple)):
            return [JsonObjectEncoder.cleaner(x) for x in obj]
        return obj

    @staticmethod
    def str_to_type(obj: str):
        if obj.startswith("'") and obj.endswith("'"):
            return obj[1:-1]
        if obj.startswith("(") and obj.endswith(")"):
            return tuple(JsonObjectEncoder.str_to_type(x) for x in obj[1: -1].split(", "))
        try:
            if "." in obj:
                return float(obj)
            return int(obj)
        except:
            return obj
