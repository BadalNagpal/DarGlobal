import json
import urllib.request
import re
import time

urls = {
    "Riyadh Sale": "https://wasalt.com/en/properties-for-sale-in-riyadh",
    "Jeddah Sale": "https://wasalt.com/en/properties-for-sale-in-jeddah",
    "Riyadh Rent": "https://wasalt.com/en/properties-for-rent-in-riyadh",
    "Jeddah Rent": "https://wasalt.com/en/properties-for-rent-in-jeddah"
}

all_wasalt_props = []

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9'
}

for category, u in urls.items():
    print(f"Fetching {category} from {u}...")
    try:
        req = urllib.request.Request(u, headers=headers)
        with urllib.request.urlopen(req, timeout=15) as res:
            html = res.read().decode('utf-8', errors='ignore')
            m = re.search(r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>', html)
            if m:
                d = json.loads(m.group(1))
                sr = d.get('props', {}).get('pageProps', {}).get('searchResult', {})
                raw_props = sr.get('properties', [])
                
                flat_props = []
                for item in raw_props:
                    if isinstance(item, dict):
                        flat_props.append(item)
                    elif isinstance(item, list):
                        for sub in item:
                            if isinstance(sub, dict):
                                flat_props.append(sub)

                print(f"  -> Extracted {len(flat_props)} listings in {category}")
                for p in flat_props:
                    prop_info = p.get('propertyInfo') or {}
                    attrs_list = p.get('attributes') or []
                    attr_map = {}
                    if isinstance(attrs_list, list):
                        for a in attrs_list:
                            if isinstance(a, dict) and 'key' in a:
                                attr_map[a['key']] = a.get('value')
                    
                    price = (
                        prop_info.get('salePrice') or 
                        prop_info.get('expectedRent') or 
                        prop_info.get('conversionPrice') or 
                        prop_info.get('price') or 
                        attr_map.get('price')
                    )
                    
                    title = prop_info.get('title') or prop_info.get('propertyName') or "Saudi Real Estate Property"
                    bedrooms = attr_map.get('noOfBedrooms') or prop_info.get('bedrooms')
                    bathrooms = attr_map.get('noOfBathrooms') or prop_info.get('bathrooms')
                    area_sqm = attr_map.get('builtUpArea') or attr_map.get('landArea') or p.get('floorSize')
                    
                    city = prop_info.get('city') or ("Riyadh" if "Riyadh" in category else "Jeddah")
                    district = prop_info.get('district') or prop_info.get('zone')
                    address = prop_info.get('address')
                    
                    slug = prop_info.get('slug') or p.get('slug')
                    prop_url = f"https://wasalt.com/en/{slug}" if slug else u
                    
                    cleaned = {
                        "id": f"wasalt_{p.get('id')}",
                        "source": "Wasalt",
                        "category": category,
                        "title": title,
                        "property_type": prop_info.get('propertySubType') or prop_info.get('propertyMainType') or "Residential",
                        "price": price,
                        "currency": "SAR",
                        "location": {
                            "city": city,
                            "district": district,
                            "full_address": address
                        },
                        "specs": {
                            "bedrooms": bedrooms,
                            "bathrooms": bathrooms,
                            "area_sqm": area_sqm,
                            "listing_type": "Rent" if "Rent" in category else "Sale"
                        },
                        "amenities": [a.get('enName') or a.get('name') for a in p.get('featureAmenities', []) if isinstance(a, dict)],
                        "url": prop_url
                    }
                    all_wasalt_props.append(cleaned)
    except Exception as e:
        print(f"  -> Error fetching {category}: {e}")
    time.sleep(1)

print(f"\nTotal Wasalt properties collected: {len(all_wasalt_props)}")
with open('data/wasalt_scraped.json', 'w', encoding='utf-8') as f:
    json.dump(all_wasalt_props, f, indent=2, ensure_ascii=False)
print("Saved data/wasalt_scraped.json successfully!")
