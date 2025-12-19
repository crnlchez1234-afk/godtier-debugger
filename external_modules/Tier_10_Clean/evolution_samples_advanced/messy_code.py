from typing import Any



def process_order(order: Any) -> int:
    # COMPLEXITY ISSUE: Too many nested conditions
    if order is not None:
        if 'items' in order:
            if len(order['items']) > 0:
                total = 0
                for item in order['items']:
                    if 'price' in item:
                        if 'quantity' in item:
                            if item['quantity'] > 0:
                                if item['price'] > 0:
                                    total += item['price'] * item['quantity']
                                    if total > 1000:
                                        if 'discount' in order:
                                            if order['discount'] > 0:
                                                total = total * (1 - order['discount'])
                return total
    return 0

def validate_email(email: Any) -> int:
    # COMPLEXITY ISSUE: Multiple nested checks
    if email:
        if '@' in email:
            if '.' in email:
                parts = email.split('@')
                if len(parts) == 2:
                    if len(parts[0]) > 0:
                        if len(parts[1]) > 0:
                            domain_parts = parts[1].split('.')
                            if len(domain_parts) >= 2:
                                return True
    return False
