from django.core.management import BaseCommand
from django.core.cache import cache

from django.conf import settings

from django.forms.models import model_to_dict

from feinstaub.sensors.models import SensorLocation, Sensor

import os
import json
import datetime
from django.utils import timezone

from django.db import connection

from rest_framework import serializers


class SensorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sensor
        fields = "__all__"

class SensorLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = SensorLocation
        fields = "__all__"


class Command(BaseCommand):
    help = ""

    def add_arguments(self, parser):
        parser.add_argument('--interval', type=str)

    def handle(self, *args, **options):
        intervals = {'5m': '5 minutes', '1h': '1 hour', '24h': '24 hours'}
        paths = {'5m': '../../static/v2/data.json',
                 '1h': '../../static/v2/data.1h.json', '24h': '../../static/v2/data.24h.json'}
        cursor = connection.cursor()
        cursor.execute('''
            SELECT sd.sensor_id, sdv.value_type, AVG(CAST(sdv."value" AS FLOAT)) as "value", COUNT("value"), sd.location_id
                FROM sensors_sensordata sd
                    INNER JOIN sensors_sensordatavalue sdv
                        ON  sd.id = sdv.sensordata_id WHERE "timestamp" >= (NOW() - interval %s)
                GROUP BY sd.sensor_id, sdv.value_type, sd.location_id
        ''', [intervals[options['interval']]])

        data = {}
        while True:
            row = cursor.fetchone()
            if row == None:
                break

            if row[0] in data:
                data[row[0]]['sensordatavalues'].append(dict({
                    'samples': row[3],
                    'value': row[2],
                    'value_type': row[1]
                }))
            else:
                data[row[0]] = dict({
                    'location': SensorLocationSerializer(SensorLocation.objects.get(pk=row[4])).data,
                    'sensor': SensorSerializer(Sensor.objects.get(pk=row[0])).data,
                    'sensordatavalues': [{
                        'samples': row[3],
                        'value': row[2],
                        'value_type': row[1]
                    }]
                })

        with open(os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            paths[options['interval']]),
            'w'
        ) as f:
            json.dump(list(data.values()), f)
