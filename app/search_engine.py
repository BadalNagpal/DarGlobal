import json
import re
import os
from typing import List, Dict, Any

class RealEstateSearchEngine:
    def __init__(self, data_path: str = "data/combined_realestate_db.json"):
        if not os.path.exists(data_path):
            raise FileNotFoundError(f"Database not found at {data_path}")
        with open(data_path, "r", encoding="utf-8") as f:
            db = json.load(f)
        self.metadata = db.get("metadata", {})
        self.darglobal_projects = db.get("darglobal_projects", [])
        self.wasalt_properties = db.get("wasalt_properties", [])
        
    def search(self, query: str, limit: int = 5) -> Dict[str, Any]:
        """Performs multi-criteria keyword & semantic token search across both datasets."""
        tokens = [t.lower() for t in re.findall(r'\w+', str(query or '')) if len(t) > 2]
        if not tokens:
            return {"darglobal": self.darglobal_projects[:3], "wasalt": self.wasalt_properties[:3]}
        
        # Score DarGlobal
        dg_scored = []
        for p in self.darglobal_projects:
            score = 0
            name = str(p.get('project_name') or '')
            loc = str(p.get('location') or '')
            partners = [str(b).lower() for b in p.get('brand_partners') or []]
            desc = str(p.get('description') or '')
            ptype = str(p.get('project_type') or '')
            text = f"{name} {loc} {p.get('country', '')} {ptype} {' '.join(partners)} {desc}".lower()
            
            for token in tokens:
                if token in text:
                    score += 2
                if token in name.lower():
                    score += 5
                if token in loc.lower():
                    score += 4
                if token in partners:
                    score += 6
            if score > 0:
                dg_scored.append((score, p))
        dg_scored.sort(key=lambda x: x[0], reverse=True)
        top_dg = [item[1] for item in dg_scored[:limit]]
        
        # Score Wasalt
        wasalt_scored = []
        for p in self.wasalt_properties:
            score = 0
            loc = p.get('location') or {}
            city = str(loc.get('city') or '')
            district = str(loc.get('district') or '')
            title = str(p.get('title') or '')
            category = str(p.get('category') or '')
            ptype = str(p.get('property_type') or '')
            text = f"{title} {city} {district} {category} {ptype}".lower()
            
            for token in tokens:
                if token in text:
                    score += 2
                if token in city.lower():
                    score += 4
                if token in district.lower():
                    score += 4
                if token in ptype.lower():
                    score += 3
            if score > 0:
                wasalt_scored.append((score, p))
        wasalt_scored.sort(key=lambda x: x[0], reverse=True)
        top_wasalt = [item[1] for item in wasalt_scored[:limit]]
        
        return {
            "darglobal": top_dg,
            "wasalt": top_wasalt
        }
        
    def generate_expert_response(self, user_query: str, search_results: Dict[str, Any]) -> str:
        """High-fidelity real estate advisory response using scraped knowledge."""
        dg = search_results.get("darglobal", [])
        wasalt = search_results.get("wasalt", [])
        
        response_parts = []
        
        if dg:
            response_parts.append("### 🌟 DarGlobal Luxury Developments")
            for p in dg[:3]:
                partners = ", ".join(p.get("brand_partners", [])) if p.get("brand_partners") else "Exclusive DarGlobal Design"
                amenities = ", ".join(p.get("amenities", [])[:4])
                response_parts.append(
                    f"- **{p.get('project_name')}** ({p.get('location')})\n"
                    f"  - **Type**: {p.get('project_type')} | **Brand Partnership**: {partners}\n"
                    f"  - **Starting Price**: {p.get('starting_price')}\n"
                    f"  - **Highlights**: {p.get('description')}\n"
                    f"  - **Amenities**: {amenities}\n"
                    f"  - 🔗 [Explore Project]({p.get('url')})"
                )
                
        if wasalt:
            response_parts.append("\n### 🏢 Wasalt Market Properties (Saudi Arabia)")
            for p in wasalt[:3]:
                loc = p.get('location', {})
                specs = p.get('specs', {})
                price_val = p.get('price')
                price_str = f"{price_val:,} SAR" if isinstance(price_val, (int, float)) else f"{price_val} SAR"
                response_parts.append(
                    f"- **{p.get('title')}**\n"
                    f"  - **Location**: {loc.get('district') or 'Prime District'}, {loc.get('city')}\n"
                    f"  - **Price & Category**: {price_str} ({p.get('category')})\n"
                    f"  - **Specs**: {specs.get('bedrooms')} Beds • {specs.get('bathrooms')} Baths • {specs.get('area_sqm')} SQM\n"
                    f"  - 🔗 [View Listing on Wasalt]({p.get('url')})"
                )
                
        if not dg and not wasalt:
            response_parts.append(
                "I couldn't find specific matching listings for that exact query in our current dataset, "
                "but I can guide you through:\n"
                "- **DarGlobal Portfolios**: Landmark developments across Dubai (DG1, Da Vinci by Pagani, W Residences), Oman (AIDA by Trump & Fendi Casa), Spain (Tierra Viva by Lamborghini), and Riyadh (Trump Mansions, Wadi Safar).\n"
                "- **Wasalt Saudi Real Estate**: Top residential & commercial properties for sale and rent in Riyadh and Jeddah."
            )
            
        return "\n\n".join(response_parts)
