import pickle
loaded_model = pickle.load(open('PySAC1', 'rb'))
result = loaded_model.score(Property_test, Response_test)
print(result)
