"""MCNP Cross Section Manager (Skill 29) - Manage xsdir and libraries"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))
from utils.zaid_database import ZAIDDatabase

class MCNPCrossSectionManager:
    def __init__(self):
        self.db = ZAIDDatabase()
    
    def parse_xsdir(self, xsdir_path: str):
        """Parse xsdir file to find available libraries"""
        self.db.parse_xsdir(xsdir_path)
    
    def check_availability(self, zaid_string: str) -> bool:
        """Check if ZAID is available"""
        from utils.zaid_database import ZAID
        zaid = ZAID.from_string(zaid_string)
        return self.db.is_zaid_available(zaid)
    
    def get_library_info(self, library_id: str) -> str:
        """Get description of library"""
        return self.db.get_library_description(library_id)
    
    def list_available_libraries(self) -> dict:
        """List all available libraries"""
        return self.db.LIBRARY_IDS
    
    def suggest_temperature_library(self, isotope: str, temp_kelvin: float) -> str:
        """Suggest library based on temperature"""
        # Simplified - match to closest standard temperature
        if temp_kelvin < 400:
            return '80c'  # ~293K
        elif temp_kelvin < 700:
            return '81c'  # ~600K
        elif temp_kelvin < 1000:
            return '82c'  # ~900K
        else:
            return '83c'  # ~1200K
