test_dict = {'a':1,'b':2}
# for i in test_dict:
#     print(i)
# for i in range(len(test_dict)):
#     print(i)
# print(len(test_dict))
# print(i for i in test_dict)

for i,g in enumerate(test_dict):
    print('i:',i,'g',g)

test_dict2 = [
    {
      "user_id": "alice",
      "name": "Alice Tan",
      "age": 45,
      "gender": "Female",
      "ailment": "Diabetes",
      "culture_and_religion": "Buddhist",
      "assigned_doctor_ids": [],
      "logs":[]
}
]

for i,a in enumerate(test_dict2):
    print(i)
    print(a)

class testClass:
    def __init__(self,a):
        self.a = a
        
g =testClass(3)
print(type(g))