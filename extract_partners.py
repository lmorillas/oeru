import mwclient
import mwparserfromhell
import json


from geopy import geocoders
gc = geocoders.GoogleV3()


class University(object):
    def __init__(self, country, url='', name = '', founding = False):
        self.country = country
        self.name = name
        self.type = founding
        self.url = url

def link(l):
    if '[[' in l:
        l = l.replace(']]', '').replace('[[', '')
        data = l.split('|')
        if len(data)>1:
            return [d.strip() for d in data]
        else:
            print l
            return [l.strip(), l.strip()]
    else:
        l = l.replace('[', '').replace(']', '')
        return [d.strip() for d in l.split(' ', 1)]


def jdefault(o):
    return o.__dict__

def geocode(partner):
    geodata = gc.geocode('{}, {}'.format(partner.name, partner.country))
    if geodata:
        partner.latlon = '{},{}'.format(geodata.latitude, geodata.longitude)

def parse_page(page_name):
    page = we.Pages[page_name]
    content = mwparserfromhell.parse(page.text())
    templates = content.filter_templates()
    # flag templates
    templates = [t for t in templates if t.name == 'FlagC']
    partners = []
    for t in templates:
        partner = {}
    partners = [University(t.params[0], *link(t.params[1])) for t in templates]
    return partners

def convert_to_item(partner):
    data = 'country name url latlon'.split()
    datadict = 'country label url latlon'.split()
    content = [getattr(partner, d, '').encode('utf-8') for d in data]
    return dict(zip(datadict, content))

def founding_partner(partner):
    partner['type_partner'] = 'Founding'

def normal_partner(partner):
    partner['type_partner'] = 'Normal'



if __name__ == '__main__':
    we = mwclient.Site('wikieducator.org', path='/')

    founding_partners = parse_page('Template:OERu_founding_anchor_partners')
    map(geocode, founding_partners)

    partners = parse_page('Template:OERu_anchor_partners')
    map(geocode, partners)

    itemfpartners = [convert_to_item(p) for p in founding_partners]
    map(founding_partner, itemfpartners)

    itemnpartners = [convert_to_item(p) for p in partners]
    map(normal_partner, itemnpartners)

    itemfpartners.extend(itemnpartners)

    items = {'items': itemfpartners,
            "types": {"Item": {"label": "partner", "pluralLabel": "partners"}}
        }

    json.dump(items, open('partners2.json', 'w'))
