import graphene
from graphene import ObjectType, String, Float, List, Schema, Int

# Database
FOOD_LOOKUP_DB = {
    1: {"food_type": "apple", "unit_calorie_g": 0.52},
    2: {"food_type": "banana", "unit_calorie_g": 0.89},
    3: {"food_type": "orange", "unit_calorie_g": 0.47},
}

# FoodItem Type
class FoodItem(ObjectType):
    food_index = Int()
    food_type = String()
    unit_calorie_g = Float()

# Query Class
class Query(ObjectType):
    get_food_item = graphene.Field(FoodItem, food_index=Int())
    list_all_foods = List(FoodItem)

    def resolve_get_food_item(root, info, food_index):
        food_data = FOOD_LOOKUP_DB.get(food_index)
        if food_data:
            return FoodItem(food_index=food_index, **food_data)
        return None

    def resolve_list_all_foods(root, info):
        return [FoodItem(food_index=index, **data) for index, data in FOOD_LOOKUP_DB.items()]

# Mutation Class
class CreateFoodItem(graphene.Mutation):
    class Arguments:
        food_type = String(required=True)
        unit_calorie_g = Float(required=True)

    food_item = graphene.Field(FoodItem)

    def mutate(self, info, food_type, unit_calorie_g):
        new_index = max(FOOD_LOOKUP_DB.keys()) + 1
        FOOD_LOOKUP_DB[new_index] = {"food_type": food_type, "unit_calorie_g": unit_calorie_g}
        return CreateFoodItem(food_item=FoodItem(food_index=new_index, food_type=food_type, unit_calorie_g=unit_calorie_g))

# Mutation ObjectType
class Mutation(ObjectType):
    create_food_item = CreateFoodItem.Field()
# Schema
schema = Schema(query=Query, mutation=Mutation)

# Executing a Query to Get a Specific Food Item
query_string = '''
{
    getFoodItem(foodIndex: 1) {
        foodType
        unitCalorieG
    }
}
'''
result = schema.execute(query_string)
if result.errors:
    print("Errors:", result.errors)
else:
    print("Food item details:", result.data['getFoodItem'])

# Executing a Mutation to Add a New Food Item
mutation_string = '''
mutation {
    createFoodItem(foodType: "mango", unitCalorieG: 0.60) {
        foodItem {
            foodType
            unitCalorieG
        }
    }
}
'''
result = schema.execute(mutation_string)
if result.errors:
    print("Errors:", result.errors)
else:
    print("Added food item:", result.data['createFoodItem']['foodItem'])

# Executing a Query to List All Food Items
query_all_foods = '''
{
    listAllFoods {
        foodIndex
        foodType
        unitCalorieG
    }
}
'''
result = schema.execute(query_all_foods)
if result.errors:
    print("Errors:", result.errors)
else:
    print("All food items:")
    for item in result.data['listAllFoods']:
        print(f"Index {item['foodIndex']}: {item['foodType'].title()}, {item['unitCalorieG']} calories/g")

