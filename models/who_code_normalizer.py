class WhoCodeNormalizer:
    """
    Standardizes WHO-specific API codes into readable domain terms.
    """
    
    _SEX_CODE_MAP = {
        "MLE": "Male",
        "FMLE": "Female",
        "BTSX": "Both sexes"
    }

    @staticmethod
    def normalize_sex(api_code):
        """
        Converts a WHO sex code to a readable string.
        Edge Case Handling:
        - If input is None, returns None.
        - If input is not in map, returns original input (safe fallback).
        - Handles non-string types (e.g. int) by returning them as-is.
        """
        if api_code is None:
            return None
            
        return WhoCodeNormalizer._SEX_CODE_MAP.get(api_code, api_code)