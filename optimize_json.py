import json

def optimize_medical_json(input_file, output_file):
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            old_data = json.load(f)

        new_categories = {}
        new_services = []

        for item in old_data:
            # 1. Kateqoriya məlumatı və tarixləri
            cat = item.get('category', {})
            cat_id = cat.get('id')

            if cat_id and cat_id not in new_categories:
                cat_name = cat.get('name')
                for t in cat.get('translations', []):
                    if t.get('locale') == 'az':
                        cat_name = t.get('name', cat_name)
                        break

                new_categories[cat_id] = {
                    "id": cat_id,
                    "name": cat_name,
                    "image": cat.get('image'),
                    "status": cat.get('status'),
                    "created_at": cat.get('created_at'),
                    "updated_at": cat.get('updated_at')
                }

            # 2. Xidmət adı (yalnız Azərbaycan dilində)
            service_name = item.get('name')
            for t in item.get('translations', []):
                if t.get('locale') == 'az':
                    service_name = t.get('name', service_name)
                    break

            # 3. Bütün vacib sahələr
            optimized_service = {
                "id": item.get('id'),
                "cat_id": cat_id,
                "no": item.get('no'),
                "name": service_name,
                "note": item.get('note'),
                "note_detail": item.get('note_detail'),
                "xbt": item.get('xbt'),
                "xbt9": item.get('xbt9'),
                "xbt10": item.get('xbt10'),
                "price": item.get('price') if item.get('price') else "0",
                "status": item.get('status'),
                "order": item.get('order'),
                "created_at": item.get('created_at'),
                "updated_at": item.get('updated_at')
            }
            new_services.append(optimized_service)

        final_data = {
            "categories": new_categories,
            "services": new_services
        }

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(final_data, f, ensure_ascii=False, indent=2)

        print(f"Tarixlər daxil olmaqla optimizasiya uğurla tamamlandı: {output_file}")
        
    except Exception as e:
        print(f"Xəta baş verdi: {e}")

# Skripti işlət
optimize_medical_json('xidmetler-kohne.json', 'xidmetler-yeni.json')
