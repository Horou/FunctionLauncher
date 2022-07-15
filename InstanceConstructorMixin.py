class CreateInstanceMixin:
    @staticmethod
    def update_instance(instance, update):
        for key, value in update.items():
            setattr(instance, key, value)

    @staticmethod
    def create_address(info):
        from client import Address
        obj = Address()
        CreateInstanceMixin.update_instance(obj, info)
        return obj

    @staticmethod
    def create_personne(info):
        from client import Personne
        obj = Personne(info["name"], info["surname"])
        CreateInstanceMixin.update_instance(obj, info)
        return obj

    @staticmethod
    def create_personne_mirror(info):
        from client import PersonneMirror
        obj = PersonneMirror(info["name"], info["surname"])
        CreateInstanceMixin.update_instance(obj, info)
        return obj


CREATE_CLASS = {
    "Address": CreateInstanceMixin.create_address,
    "PersonneMirror": CreateInstanceMixin.create_personne,
    "Personne": CreateInstanceMixin.create_personne_mirror,
}
