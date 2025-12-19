from typing import Any



def process_data(data: Any) -> Any:
    # Complexity score: 15 (too high)
    if data is None:
        return None

    result = []
    for item in data:
        if item > 0:
            if item % 2 == 0:
                if item < 100:
                    result.append(item * 2)
                else:
                    result.append(item)
            else:
                if item < 50:
                    result.append(item + 1)
                else:
                    result.append(item)
        else:
            result.append(0)

    return result
