# encoding: utf-8
class CreateInstanceMixin:
    @staticmethod
    def update_instance(instance, update):
        for key, value in update.items():
            setattr(instance, key, value)

    @staticmethod
    def create_address(info):
        from client import Address
        instance = Address()
        CreateInstanceMixin.update_instance(instance, info)
        return instance

    @staticmethod
    def create_personne(info):
        from client import Personne
        instance = Personne(info["name"], info["surname"])
        CreateInstanceMixin.update_instance(instance, info)
        return instance

    @staticmethod
    def create_personne_mirror(info):
        from client import PersonneMirror
        instance = PersonneMirror(info["name"], info["surname"])
        CreateInstanceMixin.update_instance(instance, info)
        return instance


CREATE_CLASS = {
    "Address": CreateInstanceMixin.create_address,
    "PersonneMirror": CreateInstanceMixin.create_personne,
    "Personne": CreateInstanceMixin.create_personne_mirror,
}
