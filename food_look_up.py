import graphene
from graphene import ObjectType, String, Float, List, Schema

#ref: https://us.myprotein.com/thezone/nutrition/food-calories-chart-whats-in-your-fruit-veg-meat-and-other-daily-produce/
FOOD_LOOKUP_DB = {
    "apple": {"unit_calorie_g": 0.37},  # 37 kcal per 100g
    "banana": {"unit_calorie_g": 0.51},  # 51 kcal per 100g
    "orange": {"unit_calorie_g": 0.39},  # Approximate value
    "rice_brown": {"unit_calorie_g": 1.32},  # 132 kcal per 100g (cooked)
    "chicken_breast": {"unit_calorie_g": 1.48},  # 148 kcal per 100g
    "broccoli": {"unit_calorie_g": 0.35},  # 35 kcal per 100g
    "carrot": {"unit_calorie_g": 0.10},  # 10 kcal per 100g
    "cheddar_cheese": {"unit_calorie_g": 4.03},  # 403 kcal per 100g
    "salmon_raw": {"unit_calorie_g": 1.83},  # 183 kcal per 100g
    "egg_whole": {"unit_calorie_g": 1.55},  # 155 kcal per 100g
    "almonds": {"unit_calorie_g": 5.75},  # 575 kcal per 100g
    "pasta_cooked": {"unit_calorie_g": 1.58},
    "spinach": {"unit_calorie_g": 0.24},  # 24 kcal per 100g
    "avocado": {"unit_calorie_g": 1.34},  # 134 kcal per 100g
    "tofu": {"unit_calorie_g": 0.76},  # 76 kcal per 100g
    "potato": {"unit_calorie_g": 0.97},  # 97 kcal per 100g
    "beef_steak": {"unit_calorie_g": 2.52},  # 252 kcal per 100g
    "whole_milk": {"unit_calorie_g": 0.62},  # 62 kcal per 100mL
    "oats": {"unit_calorie_g": 3.81},  # 381 kcal per 100g (rolled oats)
    "peanut_butter": {"unit_calorie_g": 5.94},
    "quinoa": {"unit_calorie_g": 1.11},  # 111 kcal per 100g (cooked)
    "lentils": {"unit_calorie_g": 1.16},  # 116 kcal per 100g (cooked)
    "chickpeas": {"unit_calorie_g": 1.64},  # 164 kcal per 100g (cooked)
    "turkey_breast": {"unit_calorie_g": 1.04},  # 104 kcal per 100g
    "salmon": {"unit_calorie_g": 2.08},  # 208 kcal per 100g
    "sweet_potato": {"unit_calorie_g": 0.86},  # 86 kcal per 100g
    "blueberries": {"unit_calorie_g": 0.57},  # 57 kcal per 100g
    "almond_milk": {"unit_calorie_g": 0.17},
    "blackberries": {"unit_calorie_g": 0.21},  # 21 kcal per 100g
    "cucumber": {"unit_calorie_g": 0.15},  # 15 kcal per 100g
    "tomato": {"unit_calorie_g": 0.18},  # 18 kcal per 100g
    "mushroom": {"unit_calorie_g": 0.08},  # 8 kcal per 100g
    "cauliflower": {"unit_calorie_g": 0.30},  # 30 kcal per 100g
    "green_peas": {"unit_calorie_g": 0.70},  # 70 kcal per 100g
    "pumpkin": {"unit_calorie_g": 0.13},
    "strawberries": {"unit_calorie_g": 0.32},  # 32 kcal per 100g
    "spinach": {"unit_calorie_g": 0.23},  # 23 kcal per 100g
    "walnuts": {"unit_calorie_g": 6.54},  # 654 kcal per 100g
    "cod": {"unit_calorie_g": 0.82},  # 82 kcal per 100g
    "shrimp": {"unit_calorie_g": 0.99},  # 99 kcal per 100g
    "beef": {"unit_calorie_g": 2.50},  # 250 kcal per 100g
    "pork": {"unit_calorie_g": 2.42},
    "olive_oil": {"unit_calorie_g": 8.80},  # 880 kcal per 100g
    "bread_whole_grain": {"unit_calorie_g": 2.66},  # 266 kcal per 100g
    "yogurt_plain": {"unit_calorie_g": 0.59},  # 59 kcal per 100g
    "lamb": {"unit_calorie_g": 2.94},  # 294 kcal per 100g
    "honey": {"unit_calorie_g": 3.04},  # 304 kcal per 100g
    "cheddar_cheese": {"unit_calorie_g": 4.03}
}

# FoodItem Type
class FoodItem(ObjectType):
    food_type = String()
    unit_calorie_g = Float()

# Query Class
class Query(ObjectType):
    list_all_foods = List(String)
    get_unit_calories = graphene.Field(Float, food_type=String())

    def resolve_list_all_foods(root, info):
        return list(FOOD_LOOKUP_DB.keys())

    def resolve_get_unit_calories(root, info, food_type):
        food_data = FOOD_LOOKUP_DB.get(food_type)
        if food_data:
            return food_data['unit_calorie_g']
        return None

# Mutation Class
class CreateFoodItem(graphene.Mutation):
    class Arguments:
        food_type = String(required=True)
        unit_calorie_g = Float(required=True)

    food_item = graphene.Field(FoodItem)

    def mutate(self, info, food_type, unit_calorie_g):
        FOOD_LOOKUP_DB[food_type] = {"unit_calorie_g": unit_calorie_g}
        return CreateFoodItem(food_item=FoodItem(food_type=food_type, unit_calorie_g=unit_calorie_g))

# Mutation ObjectType
class Mutation(ObjectType):
    create_food_item = CreateFoodItem.Field()

# Schema
schema = Schema(query=Query, mutation=Mutation)

# Executing Queries
# Query to List All Food Names
query_all_foods = '{ listAllFoods }'
result = schema.execute(query_all_foods)
if result.errors:
    print("Errors:", result.errors)
else:
    print("All food types:", result.data['listAllFoods'])

# Schema
schema = Schema(query=Query, mutation=Mutation)

def create_calorie_query(food_type):
    return '{{ getUnitCalories(foodType: "{}") }}'.format(food_type)


food_type_variable = "banana"  # can be any string
query_calories = create_calorie_query(food_type_variable)

result = schema.execute(query_calories)
if result.errors:
    print("Errors:", result.errors)
else:
    print(result.data['getUnitCalories'])
