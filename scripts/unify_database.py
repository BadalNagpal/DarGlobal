import json

with open('data/darglobal_scraped.json', 'r', encoding='utf-8') as f:
    dg_data = json.load(f)

with open('data/wasalt_scraped.json', 'r', encoding='utf-8') as f:
    wasalt_data = json.load(f)

print(f"Loaded {len(dg_data)} DarGlobal projects and {len(wasalt_data)} Wasalt properties.")

combined_db = {
    "metadata": {
        "version": "1.0",
        "total_properties": len(dg_data) + len(wasalt_data),
        "darglobal_count": len(dg_data),
        "wasalt_count": len(wasalt_data),
        "sources": ["DarGlobal (darglobal.co.uk)", "Wasalt (wasalt.com)"]
    },
    "darglobal_projects": dg_data,
    "wasalt_properties": wasalt_data
}

with open('data/combined_realestate_db.json', 'w', encoding='utf-8') as f:
    json.dump(combined_db, f, indent=2, ensure_ascii=False)

print("Unified real estate database saved to data/combined_realestate_db.json successfully!")
