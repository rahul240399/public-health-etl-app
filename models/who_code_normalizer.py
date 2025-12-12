class WhoCodeNormalizer:
    """
    Standardizes WHO-specific API codes into readable domain terms.
    """
    
    # Mapping of WHO Codes to UI labels
    _SEX_CODE_MAP = {
        "MLE": "Male",
        "FMLE": "Female",
        "BTSX": "Both sexes"
    }

    @staticmethod
    def normalize_sex(api_code):
        """
        Converts a WHO sex code (e.g., 'MLE') to a readable string.
        Returns the original code if no mapping is found.
        """
        return WhoCodeNormalizer._SEX_CODE_MAP.get(api_code, api_code)