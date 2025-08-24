from typing import List, Dict, Any
import copy

def deep_freeze(obj):
    """Convert a dictionary/list into a tuple representation for hashing."""
    if isinstance(obj, dict):
        return tuple((k, deep_freeze(v)) for k, v in sorted(obj.items()))
    elif isinstance(obj, list):
        return tuple(deep_freeze(x) for x in obj)
    elif isinstance(obj, (bool, int, float, str)) or obj is None:
        return obj
    raise TypeError(f"Object of type {type(obj)} is not JSON serializable")

def deduplicate_lists(obj):
    """Deduplicate lists in place in a dictionary structure."""
    if isinstance(obj, dict):
        for k, v in obj.items():
            obj[k] = deduplicate_lists(v)
        return obj
    elif isinstance(obj, list):
        # Convert each item to a frozen form for deduplication
        seen = set()
        deduped = []
        for item in obj:
            item_frozen = deep_freeze(item)
            if item_frozen not in seen:
                seen.add(item_frozen)
                deduped.append(deduplicate_lists(item))
        return deduped
    else:
        return obj

def merge_jsons(json_list: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Fusionne récursivement plusieurs dictionnaires JSON.
    - Les valeurs scalaires sont remplacées par la dernière rencontrée.
    - Les listes sont fusionnées par union (sans doublons).
    - Les dicts sont fusionnés récursivement.
    """
    result: Dict[str, Any] = {}
    
    def custom_merge(dst: Dict[str, Any], src: Dict[str, Any]):
        src = deduplicate_lists(copy.deepcopy(src))  # On travaille sur une copie dédupliquée
        for key, src_value in src.items():
            if key not in dst:
                dst[key] = copy.deepcopy(src_value)
                continue
                
            dst_value = dst[key]
            if isinstance(src_value, dict) and isinstance(dst_value, dict):
                # Fusion récursive des dictionnaires
                custom_merge(dst_value, src_value)
            elif isinstance(src_value, list) and isinstance(dst_value, list):
                # Pour les listes, utiliser un ensemble avec deep_freeze pour la déduplication
                seen = {deep_freeze(v) for v in dst_value}
                dst_list = list(dst_value)
                for v in src_value:
                    if deep_freeze(v) not in seen:
                        seen.add(deep_freeze(v))
                        dst_list.append(copy.deepcopy(v))
                dst[key] = dst_list
            else:
                # Pour les autres types, remplacer par une copie de la nouvelle valeur
                dst[key] = copy.deepcopy(src_value)

    for j in json_list:
        custom_merge(result, j)
    return result
