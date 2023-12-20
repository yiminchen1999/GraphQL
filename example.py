import graphene
from graphene import ObjectType, String, Int, List, Schema

#
FOOD_LOOKUP_DB = {
    1: {"food_type": "apple", "unit_calorie_g": 0.52},
    2: {"food_type": "banana", "unit_calorie_g": 0.89},
    3: {"food_type": "orange", "unit_calorie_g": 0.47},
    #
}

class FoodItem(ObjectType):
    food_index = Int()
    food_type = graphene.String()
    unit_calorie_g = graphene.Float()

class Query(ObjectType):
    # Field to get food item by index
    get_food_item = graphene.Field(FoodItem, food_index=Int())
    list_all_foods = List(FoodItem)

    def resolve_get_food_item(root, info, food_index):
        food_data = FOOD_LOOKUP_DB.get(food_index)
        if food_data:
            return FoodItem(food_index=food_index, **food_data)
        return None

    def resolve_list_all_foods(root, info):
        return [FoodItem(food_index=index, **data) for index, data in FOOD_LOOKUP_DB.items()]

class CreateFoodItem(graphene.Mutation):
    class Arguments:
        food_type = graphene.String(required=True)
        unit_calorie_g = graphene.Float(required=True)

    food_item = graphene.Field(FoodItem)

    def mutate(self, info, food_type, unit_calorie_g):
        FOOD_LOOKUP_DB[food_type] = {"unit_calorie_g": unit_calorie_g}
        return CreateFoodItem(food_item=FoodItem(food_type=food_type, unit_calorie_g=unit_calorie_g))

class Mutation(graphene.ObjectType):
    create_food_item = CreateFoodItem.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
# Query for getting the calories of a specific food item
query_string = '''
{
    getCalories(foodType: "apple") {
        foodType
        unitCalorieG
    }
}
'''
result = schema.execute(query_string)
# Mutation for adding a new food item
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
print("Added food item:", result.data['createFoodItem']['foodItem'])
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
    # Access the correct field from result.data
    print("Calories in apple:", result.data)
# Corrected mutation
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

# List all foods
query_all_foods = '{ listAllFoods { foodIndex foodType unitCalorieG } }'
result = schema.execute(query_all_foods)
if result.errors:
    print("Errors:", result.errors)
else:
    print("All food items:")
    for item in result.data['listAllFoods']:
        print(f"Index {item['foodIndex']}: {item['foodType'].title()}, {item['unitCalorieG']} calories/g")
