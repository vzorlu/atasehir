import os
import django
import json

# Set the environment variable for Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from council.models import Way

def process_tags(tag_dict):
    # Ensure tag_dict is a dictionary and remove empty/whitespace values
    if not isinstance(tag_dict, dict):
        return {}
    return {
        k: v for k, v in tag_dict.items()
        if v is not None and len(str(v).strip()) > 0
    }

def import_ways_from_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    for item in data:
        tags = process_tags(item.get('tags', {}))
        if not tags.get('name'):
            continue
        Way.objects.create(
            nodes=item.get('nodes', []),
            destination=tags.get('destination', None),
            base_type=item.get('base_type', 'default_base_type'),  # Provide a default value if missing
            way_id=item.get('id'),
            highway=tags.get('highway', 'default_highway'),  # Use the retrieved highway value
            hist_ref=tags.get('hist_ref', None),
            loc_name=tags.get('loc_name', None),
            maxspeed=tags.get('maxspeed', None),
            name=tags['name'],  # Provide a default value if missing
            oneway=tags.get('oneway', 'no'),  # Provide a default value if missing
            ref=tags.get('ref', ''),  # Provide a default value if missing
            lanes=tags.get('lanes', None),
            nat_ref=tags.get('nat_ref', None),
            toll=tags.get('toll', None)
        )

import_ways_from_json('/Users/volkanzorlu/Downloads/22.json')
