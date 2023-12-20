from graphene_pydantic import PydanticObjectType, PydanticInputObjectType

class FoodLookupGrapheneModel(PydanticObjectType):
    class Meta:
        model = FoodLookupModel

class FoodLookupGrapheneInputModel(PydanticInputObjectType):
    class Meta:
        model = FoodLookupModel
        exclude_fields = ("food_index",)
