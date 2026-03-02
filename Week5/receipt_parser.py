import re
import json


def parse_receipt(text):
    item_pattern = re.compile(
        r'(\d+)\.\s*\n'                 
        r'(.+?)\n'                      
        r'([\d,]+\s*x\s*[\d\s,]+)\n'    
        r'([\d\s,]+)\n',                
        re.DOTALL
    )

    items = []

    for match in item_pattern.finditer(text):
        items.append({
            "item_number": match.group(1),
            "product_name": " ".join(match.group(2).split()),
            "qty_unit": match.group(3),
            "final_price": match.group(4).strip()
        })

    total_pattern = re.search(r'ИТОГО:\s*\n([\d\s,]+)', text)
    receipt_total = total_pattern.group(1).strip() if total_pattern else None

    datetime_pattern = re.search(r'Время:\s*([\d\.]+\s+[\d:]+)', text)
    date_time = datetime_pattern.group(1) if datetime_pattern else None

    payment_pattern = re.search(r'(Банковская карта|Наличные)', text)
    payment_method = payment_pattern.group(1) if payment_pattern else "Unknown"

    return {
        "items": items,
        "receipt_total": receipt_total,
        "date_time": date_time,
        "payment_method": payment_method
    }


def main():
    with open("Week5/raw.txt", "r", encoding="utf-8") as f:
        text = f.read()

    parsed_data = parse_receipt(text)

    print(json.dumps(parsed_data, indent=4, ensure_ascii=False))


if __name__ == "__main__":
    main()