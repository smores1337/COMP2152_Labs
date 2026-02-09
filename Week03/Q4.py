monday_class = {"Alice", "Bob", "Charlie", "Diana"}
wednesday_class = {"Bob", "Diana", "Eve", "Frank"}
monday_class.add("Grace")
print(f"Monday class: {monday_class}")
print(f"Wednesday class: {wednesday_class}")
print(f"Both classes: {monday_class & wednesday_class}")
print(f"Attended either classes: {monday_class | wednesday_class}")
print(f"Only monday: {monday_class - wednesday_class}")
print(f"Only one class: {monday_class ^ wednesday_class}")
all_students = monday_class | wednesday_class
print(f"Is monday subset of all studnets: {monday_class <= all_students}")