import graphene
from graphene import ObjectType, String, Float, List, Schema, Int

# Exercise Database
EXERCISE_LOOKUP_DB = {
    1: {"exercise_type": "running", "calories_burned_per_minute": 10},
    2: {"exercise_type": "cycling", "calories_burned_per_minute": 8},
    3: {"exercise_type": "swimming", "calories_burned_per_minute": 9},
}

# ExerciseItem Type
class ExerciseItem(ObjectType):
    exercise_index = Int()
    exercise_type = String()
    calories_burned_per_minute = Float()

# Exercise Query Class
class ExerciseQuery(ObjectType):
    get_exercise_item = graphene.Field(ExerciseItem, exercise_index=Int())
    list_all_exercises = List(ExerciseItem)

    def resolve_get_exercise_item(root, info, exercise_index):
        exercise_data = EXERCISE_LOOKUP_DB.get(exercise_index)
        if exercise_data:
            return ExerciseItem(exercise_index=exercise_index, **exercise_data)
        return None

    def resolve_list_all_exercises(root, info):
        return [ExerciseItem(exercise_index=index, **data) for index, data in EXERCISE_LOOKUP_DB.items()]

# Exercise Mutation Class
class CreateExerciseItem(graphene.Mutation):
    class Arguments:
        exercise_type = String(required=True)
        calories_burned_per_minute = Float(required=True)

    exercise_item = graphene.Field(ExerciseItem)

    def mutate(self, info, exercise_type, calories_burned_per_minute):
        new_index = max(EXERCISE_LOOKUP_DB.keys()) + 1
        EXERCISE_LOOKUP_DB[new_index] = {"exercise_type": exercise_type, "calories_burned_per_minute": calories_burned_per_minute}
        return CreateExerciseItem(exercise_item=ExerciseItem(exercise_index=new_index, exercise_type=exercise_type, calories_burned_per_minute=calories_burned_per_minute))

# Exercise Mutation ObjectType
class ExerciseMutation(ObjectType):
    create_exercise_item = CreateExerciseItem.Field()

# Exercise Schema
exercise_schema = Schema(query=ExerciseQuery, mutation=ExerciseMutation)

# Executing a Query to Get a Specific Exercise Item
exercise_query_string = '''
{
    getExerciseItem(exerciseIndex: 1) {
        exerciseType
        caloriesBurnedPerMinute
    }
}
'''
result = exercise_schema.execute(exercise_query_string)
if result.errors:
    print("Errors:", result.errors)
else:
    print("Exercise item details:", result.data['getExerciseItem'])

# Executing a Mutation to Add a New Exercise Item
exercise_mutation_string = '''
mutation {
    createExerciseItem(exerciseType: "yoga", caloriesBurnedPerMinute: 5) {
        exerciseItem {
            exerciseType
            caloriesBurnedPerMinute
        }
    }
}
'''
result = exercise_schema.execute(exercise_mutation_string)
if result.errors:
    print("Errors:", result.errors)
else:
    print("Added exercise item:", result.data['createExerciseItem']['exerciseItem'])

# Executing a Query to List All Exercise Items
exercise_query_all_string = '''
{
    listAllExercises {
        exerciseIndex
        exerciseType
        caloriesBurnedPerMinute
    }
}
'''
result = exercise_schema.execute(exercise_query_all_string)
if result.errors:
    print("Errors:", result.errors)
else:
    print("All exercise items:")
    for item in result.data['listAllExercises']:
        print(f"Index {item['exerciseIndex']}: {item['exerciseType'].title()}, {item['caloriesBurnedPerMinute']} calories/min")

