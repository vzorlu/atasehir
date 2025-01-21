# [2] resources.py
# (Way modeline göre Alan Sıralaması)

from import_export import resources
from .models import Way, Department

class WayResource(resources.ModelResource):
    class Meta:
        model = Way
        # [2.1] Import ve Export sırasında kullanılacak alanlar
        fields = (
            'id',        # Django internal PK
            'way_id',    # Bizim "Way" modelindeki
            'type',
            'nodes',
            'destination',
            'highway',
            'hist_ref',
            'loc_name',
            'maxspeed',
            'name',
            'oneway',
            'ref',
            'lanes',
            'nat_ref',
            'toll'
        )

class DepartmentResource(resources.ModelResource):
    class Meta:
        model = Department
