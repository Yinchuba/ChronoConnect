from django.apps import AppConfig
from .sigPoints import generate_edge_data, modify_edge_data
import os

class MyappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'myapp'

    def ready(self):
        # Generate data files using sigPoints.py
        day1_data = generate_edge_data(10, 20, (1, 10))
        day2_data = modify_edge_data(day1_data, 0.2, (1, 10))
        
        # Save data files to myapp directory
        current_dir = os.path.dirname(os.path.abspath(__file__))
        with open(os.path.join(current_dir, 'DataofDay1.txt'), 'w') as file:
            file.write(day1_data)
        with open(os.path.join(current_dir, 'DataofDay2.txt'), 'w') as file:
            file.write(day2_data)
