# encoding: utf-8
import json
from InstanceConstructorMixin import CREATE_CLASS


class JsonObjectEncoder(json.JSONEncoder):

    @staticmethod
    def dumps(obj, indent=None):
        return json.dumps(obj, cls=JsonObjectEncoder, indent=indent)

    @staticmethod
    def loads(obj):
        return json.loads(obj, object_hook=JsonObjectEncoder.hook)

    #####################################################################

    def default(self, obj):
        if obj.__class__.__name__ in CREATE_CLASS:
            result = obj.to_representation() if hasattr(obj, 'to_representation') else self.cleaner(obj.__dict__)
            result["__class__"] = obj.__class__.__name__
            return result
        return str(obj)

    @staticmethod
    def hook(obj):
        class_name = obj.pop("__class__", None)
        clean_dict = {
            (JsonObjectEncoder.str_to_type(k) if isinstance(k, str) else k):
                (JsonObjectEncoder.str_to_type(v) if isinstance(v, str) else v)
            for k, v in obj.items()
            if not (isinstance(v, str) and v.startswith("<") and v.endswith(">"))
        }
        return CREATE_CLASS[class_name](clean_dict) if class_name else clean_dict

    #####################################################################

    @staticmethod
    def cleaner(obj):
        if isinstance(obj, dict):
            return {(str(k) if isinstance(k, tuple) else k): JsonObjectEncoder.cleaner(v) for k, v in obj.items()}
        if isinstance(obj, (list, tuple)):
            return [JsonObjectEncoder.cleaner(x) for x in obj]
        return obj

    @staticmethod
    def str_to_type(obj):
        if obj.startswith("'") and obj.endswith("'"):
            return obj[1:-1]
        if obj.startswith("(") and obj.endswith(")"):
            return tuple(JsonObjectEncoder.str_to_type(x) for x in obj[1: -1].split(", "))
        try:
            return float(obj)
        except ValueError:
            return obj
