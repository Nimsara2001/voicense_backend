# from db_config import get_db
# import pymongo
#
# db = get_db()
#
#
# def generate_module_id():
#     modules_collection = db['modules']
#     last_module = modules_collection.find_one(sort=[("module_id", pymongo.DESCENDING)])
#     if last_module:
#         module_id_parts = last_module["module_id"].split("VCSM")
#         if len(module_id_parts) > 1:
#             numerical_part = int(module_id_parts[1])
#             new_numerical_part = numerical_part + 1
#             new_numerical_part_str = f"{new_numerical_part:04d}"
#             new_module_id = f"VCSM{new_numerical_part_str}"
#             # print(new_module_id)
#     else:
#         new_module_id = "VCSM0001"
#     return new_module_id
#
#
# def generate_note_id():
#     notes_collection = db['notes']
#     last_note = notes_collection.find_one(sort=[("note_id", pymongo.DESCENDING)])
#
#     if last_note:
#         note_id_parts = last_note["note_id"].split("VCSN")
#         if len(note_id_parts) > 1:
#             numerical_part = int(note_id_parts[1])
#             new_numerical_part = numerical_part + 1
#             new_numerical_part_str = f"{new_numerical_part:04d}"
#             new_note_id = f"VCSN{new_numerical_part_str}"
#             # print(new_note_id)
#     else:
#         new_note_id = "VCSN0001"
#     return new_note_id
#
#
# def generate_user_id(user_type):
#     users_collection = db['User']
#     last_user = users_collection.find_one({"user_type": user_type}, sort=[("user_id", pymongo.DESCENDING)])
#
#     if last_user:
#         if user_type == 'lecturer':
#             user_id_parts = last_user["user_id"].split("VCSL")
#         else:
#             user_id_parts = last_user["user_id"].split("VCSS")
#
#         if len(user_id_parts) > 1:
#             numerical_part = int(user_id_parts[1])
#             new_numerical_part = numerical_part + 1
#             new_numerical_part_str = f"{new_numerical_part:04d}"
#             if user_type == 'lecturer':
#                 new_user_id = f"VCSL{new_numerical_part_str}"
#             else:
#                 new_user_id = f"VCSS{new_numerical_part_str}"
#     else:
#         if user_type == 'lecturer':
#             new_user_id = "VCSL0001"
#         else:
#             new_user_id = "VCSS0001"
#             # print("Id is "+new_user_id)
#     return new_user_id
