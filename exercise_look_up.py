import graphene
from graphene import ObjectType, String, Float, List, Schema

# ref: https://www.mayoclinic.org/healthy-lifestyle/weight-loss/in-depth/exercise/art-20050999
EXERCISE_LOOKUP_DB = {
    "running": {"calories_burned_per_minute": 606 / 60},  # 10.1 calories per minute
    "cycling": {"calories_burned_per_minute": 292 / 60},  # 4.87 calories per minute
    "swimming": {"calories_burned_per_minute": 423 / 60},  # 7.05 calories per minute
    "yoga": {"calories_burned_per_minute": 183 / 60},  # 3.05 calories per minute (moderate effort)
    "weightlifting": {"calories_burned_per_minute": 108 / 60},  # 1.8 calories per minute
    "aerobics_low_impact": {"calories_burned_per_minute": 365 / 60},  # 6.08 calories per minute
    "aerobics_water": {"calories_burned_per_minute": 402 / 60},  # 6.7 calories per minute
    "dancing_ballroom": {"calories_burned_per_minute": 219 / 60},  # 3.65 calories per minute
    "elliptical_trainer": {"calories_burned_per_minute": 365 / 60},  # 6.08 calories per minute
    "golfing": {"calories_burned_per_minute": 314 / 60},  # 5.23 calories per minute
    "hiking": {"calories_burned_per_minute": 438 / 60},  # 7.3 calories per minute
    "skiing_downhill": {"calories_burned_per_minute": 314 / 60},  # 5.23 calories per minute
    "walking": {"calories_burned_per_minute": 314 / 60} ,
    "jogging": {"calories_burned_per_minute": 450 / 60},  # 7.5 calories per minute
    "tennis": {"calories_burned_per_minute": 480 / 60},  # 8.0 calories per minute
    "basketball": {"calories_burned_per_minute": 584 / 60},  # 9.73 calories per minute
    "soccer": {"calories_burned_per_minute": 504 / 60},  # 8.4 calories per minute
    "zumba": {"calories_burned_per_minute": 350 / 60},  # 5.83 calories per minute
    "crossfit": {"calories_burned_per_minute": 500 / 60},  # 8.33 calories per minute
    "rock_climbing": {"calories_burned_per_minute": 550 / 60}
    # 5.23 calories per minute (3.5 mph)
}

# ExerciseItem Type
class ExerciseItem(ObjectType):
    exercise_type = String()
    calories_burned_per_minute = Float()

# Query Class
class ExerciseQuery(ObjectType):
    list_all_exercises = List(String)
    get_calories_burned = graphene.Field(Float, exercise_type=String())

    def resolve_list_all_exercises(root, info):
        return list(EXERCISE_LOOKUP_DB.keys())

    def resolve_get_calories_burned(root, info, exercise_type):
        exercise_data = EXERCISE_LOOKUP_DB.get(exercise_type)
        if exercise_data:
            return exercise_data['calories_burned_per_minute']
        return None

# Mutation Class
class CreateExerciseItem(graphene.Mutation):
    class Arguments:
        exercise_type = String(required=True)
        calories_burned_per_minute = Float(required=True)

    exercise_item = graphene.Field(ExerciseItem)

    def mutate(self, info, exercise_type, calories_burned_per_minute):
        EXERCISE_LOOKUP_DB[exercise_type] = {"calories_burned_per_minute": calories_burned_per_minute}
        return CreateExerciseItem(exercise_item=ExerciseItem(exercise_type=exercise_type, calories_burned_per_minute=calories_burned_per_minute))

# Mutation ObjectType
class ExerciseMutation(ObjectType):
    create_exercise_item = CreateExerciseItem.Field()

# Schema
exercise_schema = Schema(query=ExerciseQuery, mutation=ExerciseMutation)

# Executing Queries
# Query to List All Exercise Types
query_all_exercises = '{ listAllExercises }'
result = exercise_schema.execute(query_all_exercises)
if result.errors:
    print("Errors:", result.errors)
else:
    print("All exercise types:", result.data['listAllExercises'])

def create_exercise_calorie_query(exercise_type):
    return '{{ getCaloriesBurned(exerciseType: "{}") }}'.format(exercise_type)

# Example usage:
exercise_type_variable = "running"  # can be any string
query_exercise_calories = create_exercise_calorie_query(exercise_type_variable)


result = exercise_schema.execute(query_exercise_calories)
if result.errors:
    print("Errors:", result.errors)
else:
    print(result.data['getCaloriesBurned'])
