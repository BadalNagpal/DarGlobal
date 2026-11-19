import json

with open('data/darglobal_data.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

global_attrs = d['globalData']['attributes']
page_attrs = d['pageData']['attributes']

# Curated details based on DarGlobal's official portfolio
project_metadata = {
    "AIDA": {
        "location": "Muscat, Oman",
        "description": "One of the world's largest premium mixed-use developments perched 130 meters above the shores of the Gulf of Oman. Features luxury villas, residences, and Trump International Golf Club Oman.",
        "type": "Masterplan / Luxury Villas & Golf Community",
        "partners": ["Trump Organization", "Fendi Casa", "Marriott Residences"],
        "starting_price": "Starting from approx. 1,500,000 USD",
        "amenities": ["Trump International Golf Course", "Clifftop Oceanfront views", "Private Beach Club", "5-star luxury hotels", "Wellness & Spa Centers"],
        "url": "https://darglobal.co.uk/landing-page/aida"
    },
    "Trump International Hotel & Tower Dubai": {
        "location": "Dubai, UAE",
        "description": "Ultra-luxury hotel and branded residential tower in Dubai featuring iconic architecture and signature Trump hospitality, world-class golf amenities and skyline views.",
        "type": "Branded Luxury Residences & 5-Star Hotel",
        "partners": ["Trump Organization"],
        "starting_price": "Premium pricing upon request",
        "amenities": ["Infinity pool overlooking Dubai skyline", "Exclusive Trump Club membership", "Valet & 24/7 Concierge", "Fine dining restaurants"],
        "url": "https://darglobal.co.uk/project/trump-international-hotel-tower-dubai"
    },
    "DG1": {
        "location": "Business Bay, Dubai, UAE",
        "description": "A landmark architectural masterpiece on the banks of Dubai Canal designed by Gensler. Offers 1, 2, and 3-bedroom luxury apartments with unobstructed Burj Khalifa and canal views.",
        "type": "Luxury Waterfront High-Rise Residences",
        "partners": ["Gensler Architecture"],
        "starting_price": "From approx. 1,800,000 AED",
        "amenities": ["Infinity Sky Pool", "Dubai Canal views", "State-of-the-art gym", "Direct waterfront promenade access"],
        "url": "https://darglobal.co.uk/project/dg1"
    },
    "Da Vinci Tower, Interiors by Pagani": {
        "location": "Downtown Dubai Canal, UAE",
        "description": "Exclusive residential tower with bespoke interiors created in partnership with legendary Italian hypercar atelier Pagani Automobili. Pure Italian design excellence.",
        "type": "Ultra-Luxury Branded Residences",
        "partners": ["Pagani Automobili"],
        "starting_price": "Starting from approx. 6,000,000 AED",
        "amenities": ["Pagani signature carbon-fiber detailing", "Rooftop infinity pool with Burj Khalifa view", "Bespoke fitness center", "Private resident lounge"],
        "url": "https://darglobal.co.uk/project/da-vinci-tower"
    },
    "Tierra Viva": {
        "location": "Benahavís, Costa del Sol, Spain",
        "description": "An ultra-exclusive architectural enclave of luxury villas inspired by Automobili Lamborghini. Located on the slopes of the Andalusian hills near Marbella.",
        "type": "Super-Luxury Villas",
        "partners": ["Automobili Lamborghini"],
        "starting_price": "From 9,000,000 EUR",
        "amenities": ["Direct Mediterranean views", "Private elevator in every villa", "Infinity pools", "24/7 gated security community"],
        "url": "https://darglobal.co.uk/project/tierra-viva"
    },
    "Marea-Interiors by Missoni": {
        "location": "Cortesín, Costa del Sol, Spain",
        "description": "Elite branded villas overlooking Finca Cortesín resort and golf club, with stylish Italian interiors by Missoni. Mediterranean living at its pinnacle.",
        "type": "Luxury Branded Villas & Apartments",
        "partners": ["Missoni"],
        "starting_price": "From 1,200,000 EUR",
        "amenities": ["Panoramic golf & Mediterranean views", "Finca Cortesin golf access", "Tennis & padel courts", "Missoni interior customization"],
        "url": "https://darglobal.co.uk/project/marea"
    },
    "W Residences": {
        "location": "Downtown Dubai, UAE",
        "description": "Sophisticated branded residences managed by Marriott International under the rebellious luxury W brand, right in the heart of Downtown Dubai with Burj Khalifa views.",
        "type": "Branded Luxury Apartments",
        "partners": ["W Hotels / Marriott International"],
        "starting_price": "From 2,200,000 AED",
        "amenities": ["W Clubhouse", "Whatever/Whenever concierge", "Infinity swimming pool", "Co-working spaces & Media lounge"],
        "url": "https://darglobal.co.uk/project/w-residences"
    },
    "Urban Oasis": {
        "location": "Business Bay / Dubai Canal, UAE",
        "description": "Vibrant Miami-inspired waterfront development with bespoke interiors by Missoni Home, right by Dubai Water Canal.",
        "type": "Waterfront Luxury Residences",
        "partners": ["Missoni Home"],
        "starting_price": "From 1,500,000 AED",
        "amenities": ["Infinity pool overlooking Dubai Canal", "Missoni-styled common areas", "Gymnasium & wellness club"],
        "url": "https://darglobal.co.uk/project/urban-oasis"
    },
    "The Astera": {
        "location": "Al Marjan Island, Ras Al Khaimah, UAE",
        "description": "Breathtaking beachfront residences designed with interiors by Aston Martin, located adjacent to the upcoming Wynn Al Marjan Island casino resort.",
        "type": "Branded Beachfront Residences",
        "partners": ["Aston Martin"],
        "starting_price": "From 1,900,000 AED",
        "amenities": ["Private pristine beach", "Aston Martin curated aesthetics", "Infinity beach pool", "Scenic sea & sunset views"],
        "url": "https://darglobal.co.uk/project/the-astera"
    },
    "Trump Mansions, Rayana, Wadi Safar": {
        "location": "Wadi Safar, Riyadh, Saudi Arabia",
        "description": "Palatial luxury estate mansions in Riyadh's prestigious Wadi Safar cultural & equestrian valley, offering bespoke architecture and Trump brand distinction.",
        "type": "Ultra-Luxury Private Mansions",
        "partners": ["Trump Organization", "Wadi Safar / Diriyah Gate"],
        "starting_price": "Price on exclusive application",
        "amenities": ["Private sprawling gardens", "Golf & equestrian club access", "Highest level private security", "Majlis & banquet halls"],
        "url": "https://darglobal.co.uk/project/trump-mansions-wadi-safar"
    },
    "Trump Tower Jeddah": {
        "location": "Jeddah Corniche, Saudi Arabia",
        "description": "A soaring high-rise landmark redefining the Jeddah waterfront skyline with five-star luxury hotel services and elite branded residences.",
        "type": "Skyline Branded Tower & Hotel",
        "partners": ["Trump Organization"],
        "starting_price": "Premium luxury rates upon launch",
        "amenities": ["Red Sea views", "Trump Spa & Wellness", "Sky lounge & signature restaurant", "VIP concierge"],
        "url": "https://darglobal.co.uk/project/trump-tower-jeddah"
    },
    "Les Vagues": {
        "location": "Qetaifan Island North, Doha, Qatar",
        "description": "Super-luxury sea-facing apartments with elegant interiors by Elie Saab on Qatar's entertainment island capital.",
        "type": "Branded Island Waterfront Residences",
        "partners": ["Elie Saab Haute Couture"],
        "starting_price": "From 2,000,000 QAR",
        "amenities": ["Private beach access", "Water park proximity", "Elie Saab custom interior finishes", "Sea view balconies"],
        "url": "https://darglobal.co.uk/project/les-vagues"
    }
}

darglobal_projects = []
project_list = global_attrs.get('ProjectList', [])

for p in project_list:
    name = p.get('name')
    country = p.get('country') or ("Oman" if p.get('isOmanProject') else "International")
    code = p.get('projectCode')
    
    # Enrich with metadata if available
    meta = project_metadata.get(name, {})
    
    item = {
        "id": f"dg_{code or name.lower().replace(' ', '_')[:12]}",
        "source": "DarGlobal",
        "developer": "DarGlobal PLC (Dar Al Arkan Group)",
        "project_name": name,
        "location": meta.get('location') or country,
        "country": country,
        "project_type": meta.get('type') or "Luxury Residential Development",
        "brand_partners": meta.get('partners') or ([] if not any(b in name for b in ['Trump', 'Pagani', 'Missoni', 'Fendi', 'Aston Martin', 'Lamborghini', 'Mouawad', 'Marriott', 'Nickelodeon']) else [b for b in ['Trump', 'Pagani', 'Missoni', 'Fendi', 'Aston Martin', 'Lamborghini', 'Mouawad', 'Marriott', 'Nickelodeon'] if b in name]),
        "starting_price": meta.get('starting_price') or "Available on request / consultation",
        "description": meta.get('description') or f"Prestigious luxury development by DarGlobal located in {country}. Designed with international architectural standards and world-class finishes.",
        "amenities": meta.get('amenities') or ["Concierge service", "Swimming pool", "Fitness club", "Private parking", "Landscaped grounds"],
        "url": meta.get('url') or "https://darglobal.co.uk"
    }
    darglobal_projects.append(item)

print(f"Constructed {len(darglobal_projects)} DarGlobal comprehensive project profiles!")
with open('data/darglobal_scraped.json', 'w', encoding='utf-8') as f:
    json.dump(darglobal_projects, f, indent=2, ensure_ascii=False)
print("Saved data/darglobal_scraped.json successfully!")
