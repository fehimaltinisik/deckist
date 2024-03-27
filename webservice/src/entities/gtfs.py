from tortoise import fields
from tortoise.models import Model
from tortoise import Tortoise
from tortoise import run_async


class Route(Model):
    """
        route_id,
        agency_id,
        route_short_name,
        route_long_name,
        route_desc,
        route_type,
        route_url,
        route_color,
        route_text_color
    """
    route_id = fields.IntField(pk=True)
    agency_id = fields.IntField()
    route_short_name = fields.CharField(max_length=255)
    route_long_name = fields.CharField(max_length=255)
    route_type = fields.IntField()
    route_desc = fields.CharField(max_length=255)
    route_code = fields.CharField(max_length=255, null=True)
    # Hints
    trips: fields.ReverseRelation['Route']

    class Meta:
        table = 'route'


class Shape(Model):
    shape_id = fields.IntField(index=True)
    shape_pt_lat = fields.FloatField()
    shape_pt_lon = fields.FloatField()
    shape_pt_sequence = fields.IntField()
    shape_dist_traveled = fields.FloatField()

    class Meta:
        table = 'shape'


class Trip(Model):
    trip_id = fields.IntField(pk=True)
    trip_short_name = fields.CharField(max_length=63, null=True)
    trip_headsign = fields.CharField(max_length=255)
    service_id = fields.IntField()
    direction_id = fields.SmallIntField(null=True)
    wheelchair_accessible = fields.SmallIntField(null=True)
    bikes_allowed = fields.SmallIntField(null=True)
    shape_id = fields.IntField(null=True)
    route: fields.ForeignKeyRelation['Route'] = fields.ForeignKeyField(
        model_name='models.Route',
        related_name='trips',
        null=True
    )
    stops: fields.ManyToManyRelation['Stop'] = fields.ManyToManyField(
        model_name='models.Stop',
        through='stop_time'
    )
    # Hints
    stop_times: fields.ReverseRelation['StopTime']

    class Meta:
        table = 'trip'


class Stop(Model):
    stop_id = fields.IntField(pk=True)
    stop_code = fields.CharField(max_length=32)
    stop_name = fields.CharField(max_length=255)
    stop_desc = fields.CharField(max_length=255)
    stop_url = fields.CharField(max_length=255, null=True)
    location_type = fields.SmallIntField()
    wheelchair_boarding = fields.SmallIntField(null=True)
    stop_lat = fields.FloatField()
    stop_lon = fields.FloatField()

    class Meta:
        table = 'stop'


class StopTime(Model):
    trip: fields.ForeignKeyRelation['Trip'] = fields.ForeignKeyField(
        model_name='models.Trip',
        related_name='stop_times',
        source_field='trip_id'
    )
    stop: fields.ForeignKeyRelation['Stop'] = fields.ForeignKeyField(
        model_name='models.Stop',
        related_name='stop_times',
        source_field='stop_id'
    )
    stop_sequence = fields.SmallIntField()
    arrival_time = fields.DatetimeField(null=True)
    departure_time = fields.DatetimeField(null=True)
    timepoint = fields.SmallIntField(null=True)

    class Meta:
        table = 'stop_time'
        indexes = (('trip_id', 'stop_id'),)


Tortoise.init_models(['src.entities.gtfs'], 'models')
