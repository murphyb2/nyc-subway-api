# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

# class RemoteComplexLookup(models.Model):
#     id = models.AutoField()
#     remote = models.CharField(max_length=5, blank=True, null=True)
#     booth = models.CharField(max_length=10, blank=True, null=True)
#     complex_id = models.CharField(max_length=5, blank=True, null=True)
#     station = models.CharField(max_length=50, blank=True, null=True)
#     line_name = models.CharField(max_length=20, blank=True, null=True)
#     division = models.CharField(max_length=5, blank=True, null=True)

#     class Meta:
#         managed = False
#         db_table = 'remote_complex_lookup'


class Station(models.Model):
    ogc_fid = models.IntegerField(blank=True, null=True)
    station_id = models.IntegerField(blank=True, null=True)
    complex_id = models.CharField(max_length=5, blank=True, null=True)
    gtfs_stop_id = models.CharField(max_length=5, blank=True, null=True)
    division = models.CharField(max_length=5, blank=True, null=True)
    line = models.CharField(max_length=40, blank=True, null=True)
    stop_name = models.CharField(max_length=255, blank=True, null=True)
    borough = models.CharField(max_length=2, blank=True, null=True)
    daytime_routes = models.CharField(max_length=20, blank=True, null=True)
    structure = models.CharField(max_length=20, blank=True, null=True)
    gtfs_latitude = models.DecimalField(max_digits=12, decimal_places=10, blank=True, null=True)
    gtfs_longitude = models.DecimalField(max_digits=12, decimal_places=10, blank=True, null=True)
    north_direction_label = models.CharField(max_length=255, blank=True, null=True)
    south_direction_label = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'stations'

class DailyCounts2019(models.Model):
    stop_name = models.CharField(max_length=255, blank=True, null=True)
    daytime_routes = models.CharField(max_length=20, blank=True, null=True)
    division = models.CharField(max_length=5, blank=True, null=True)
    line = models.CharField(max_length=40, blank=True, null=True)
    borough = models.CharField(max_length=2, blank=True, null=True)
    structure = models.CharField(max_length=20, blank=True, null=True)
    gtfs_latitude = models.DecimalField(max_digits=12, decimal_places=10, blank=True, null=True)
    gtfs_longitude = models.DecimalField(max_digits=12, decimal_places=10, blank=True, null=True)
    complex_id = models.TextField(blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    entries = models.DecimalField(max_digits=12, decimal_places=0, blank=True, null=True)
    exits = models.DecimalField(max_digits=12, decimal_places=0, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'daily_counts_2019'


class DailyCounts2020(models.Model):
    stop_name = models.CharField(max_length=255, blank=True, null=True)
    daytime_routes = models.CharField(max_length=20, blank=True, null=True)
    division = models.CharField(max_length=5, blank=True, null=True)
    line = models.CharField(max_length=40, blank=True, null=True)
    borough = models.CharField(max_length=2, blank=True, null=True)
    structure = models.CharField(max_length=20, blank=True, null=True)
    gtfs_latitude = models.DecimalField(max_digits=12, decimal_places=10, blank=True, null=True)
    gtfs_longitude = models.DecimalField(max_digits=12, decimal_places=10, blank=True, null=True)
    complex_id = models.TextField(primary_key=True)
    date = models.DateField(blank=True, null=True)
    entries = models.DecimalField(max_digits=12, decimal_places=0, blank=True, null=True)
    exits = models.DecimalField(max_digits=12, decimal_places=0, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'daily_counts_2020'


class DailyCounts2021(models.Model):
    stop_name = models.CharField(max_length=255, blank=True, null=True)
    daytime_routes = models.CharField(max_length=20, blank=True, null=True)
    division = models.CharField(max_length=5, blank=True, null=True)
    line = models.CharField(max_length=40, blank=True, null=True)
    borough = models.CharField(max_length=2, blank=True, null=True)
    structure = models.CharField(max_length=20, blank=True, null=True)
    gtfs_latitude = models.DecimalField(max_digits=12, decimal_places=10, blank=True, null=True)
    gtfs_longitude = models.DecimalField(max_digits=12, decimal_places=10, blank=True, null=True)
    complex_id = models.TextField(blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    entries = models.DecimalField(max_digits=12, decimal_places=0, blank=True, null=True)
    exits = models.DecimalField(max_digits=12, decimal_places=0, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'daily_counts_2021'

# class YearlyCounts(models.Model):
#     id = models.IntegerField(primary_key=True)
#     stop_name = models.CharField(max_length=255, blank=True, null=True)
#     longitude = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
#     latitude = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
#     total_year_entries = models.IntegerField(blank=True, null=True)
#     total_year_esits = models.IntegerField(blank=True, null=True)


# class DailySubunit(models.Model):
#     unit_id = models.CharField(max_length=-1, blank=True, null=True)
#     remoteunit = models.CharField(max_length=-1, blank=True, null=True)
#     date = models.DateField(blank=True, null=True)
#     entries = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
#     exits = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)

#     class Meta:
#         managed = False
#         db_table = 'daily_subunit'

# class TurnstileObservations(models.Model):
#     id = models.CharField(unique=True, max_length=-1)
#     unit_id = models.CharField(max_length=-1)
#     controlarea = models.CharField(max_length=-1)
#     remoteunit = models.CharField(max_length=-1)
#     subunit_channel_position = models.CharField(max_length=-1)
#     station = models.CharField(max_length=-1)
#     linenames = models.CharField(max_length=-1)
#     division = models.CharField(max_length=-1)
#     observed_at = models.DateTimeField()
#     description = models.CharField(max_length=-1)
#     entries = models.BigIntegerField()
#     exits = models.BigIntegerField()
#     net_entries = models.BigIntegerField(blank=True, null=True)
#     net_exits = models.BigIntegerField(blank=True, null=True)
#     filename = models.CharField(max_length=-1)

#     class Meta:
#         managed = False
#         db_table = 'turnstile_observations'
