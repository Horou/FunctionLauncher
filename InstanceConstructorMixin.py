class InstanceConstructorMixin:

    @staticmethod
    def create_address(info):
        from client import Address
        obj = Address()
        obj.__dict__ = info
        return obj

    @staticmethod
    def create_personne(info):
        from client import Personne
        obj = Personne(info["name"], info["surname"])
        obj.__dict__ = info
        return obj

    @staticmethod
    def create_personne_mirror(info):
        from client import PersonneMirror
        obj = PersonneMirror(info["name"], info["surname"])
        obj.__dict__ = info
        return obj

    create_class = {
        "Address": create_address,
        "PersonneMirror": create_personne,
        "Personne": create_personne_mirror,
    }
