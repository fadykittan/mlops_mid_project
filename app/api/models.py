from dataclasses import dataclass
from typing import Optional

@dataclass
class CustomerData:
    TotalCharges: float
    Contract: str
    PhoneService: str
    tenure: float

    def validate(self) -> tuple[bool, Optional[str]]:
        """Validate the input data"""
        if self.Contract not in ['Month-to-month', 'One year', 'Two year']:
            return False, "Contract must be one of: Month-to-month, One year, Two year"
        if self.PhoneService not in ['Yes', 'No']:
            return False, "PhoneService must be either 'Yes' or 'No'"
        if self.TotalCharges < 0:
            return False, "TotalCharges cannot be negative"
        if self.tenure < 0:
            return False, "tenure cannot be negative"
        return True, None 