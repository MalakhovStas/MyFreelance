# import pickle
#
# with open('craft.recipes.csv', 'r') as f:
#     file = pickle.load(f)
#     # data = pickle.loads(file)
#     print(file)

with open('craft.recipes.csv', 'r', encoding='ascii') as file:
    data = file.read()
    print(data)
