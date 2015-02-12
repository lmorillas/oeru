import json

courses = json.load(open('courses.json'))

items = {'items': courses,
    "types": {
        "Item": {
            "pluralLabel": "courses",
            "label": "course"
        }}
        ,
     "properties":{
        "url": {"valueType": "url"},
        "weeks": {"valueType": "number"},
        "hpw": {"valueType": "number"}
    }
    }

open('courses_exhibit.js', 'w').write(json.dumps(items).replace('name', 'label').replace('"type"', '"type_c"'))
