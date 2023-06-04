# tasks_producer.py
import random
from faker import Faker
from faker.providers import BaseProvider

# Create and initialise a faker generator and return data in US English
# Seeding to have the same results every time we execute the script
fakeTasks = Faker('en_US')
# Seed the Faker instance to have the same results every time we run the program
fakeTasks.seed_instance(0)

# Define a TaskProvider
class TaskProvider(BaseProvider):
    def SKUs():
        apparel = ["SWEATSHIRT", "TSHIRT", "HOODIE", "PFMTSHIRT"]
        manufacturer = ["CN_KD", "CN_US", "CN_WM", "LS_US","RC_US"]
        model = ["HWT","CLS","BAS","PRM"]
        size = ["S", "M", "L", "XL", "2XL","3XL"]
        colour = fakeTasks.color_name()
        SKU = [apparel[random.randint(0, len(apparel)-1)], manufacturer[random.randint(0, len(manufacturer)-1)],
                model[random.randint(0, len(model)-1)], size[random.randint(0, len(size)-1)], colour[random.randint(0, len(colour)-1)]]
        return SKU

# Assign the TaskProvider to the Faker instance
fakeTasks.add_provider(TaskProvider)

randomSKU = "_".join(fakeTasks.SKUs())

print(randomSKU)