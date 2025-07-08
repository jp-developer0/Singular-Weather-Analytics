#!/usr/bin/env python3
"""
Environment verification script for Render deployment
"""

import sys
import subprocess

def check_python_version():
    """Check Python version"""
    print(f"✅ Python version: {sys.version}")
    print(f"✅ Python executable: {sys.executable}")
    
def check_imports():
    """Test critical imports"""
    try:
        import pandas as pd
        print(f"✅ Pandas {pd.__version__} imported successfully")
        
        import numpy as np
        print(f"✅ Numpy {np.__version__} imported successfully")
        
        import matplotlib
        print(f"✅ Matplotlib {matplotlib.__version__} imported successfully")
        
        import fastapi
        print(f"✅ FastAPI {fastapi.__version__} imported successfully")
        
        import uvicorn
        print(f"✅ Uvicorn imported successfully")
        
        import gunicorn
        print(f"✅ Gunicorn imported successfully")
        
        # Test pandas basic functionality
        df = pd.DataFrame({'test': [1, 2, 3]})
        print(f"✅ Pandas DataFrame creation works: {len(df)} rows")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def check_app_import():
    """Test app import"""
    try:
        import app
        print("✅ FastAPI app imported successfully")
        return True
    except Exception as e:
        print(f"❌ App import failed: {e}")
        return False

def main():
    print("🔍 Environment Check for Singular Weather Analytics")
    print("=" * 50)
    
    check_python_version()
    print()
    
    if check_imports():
        print("\n✅ All core dependencies working correctly")
    else:
        print("\n❌ Some dependencies failed to import")
        sys.exit(1)
    
    print()
    if check_app_import():
        print("✅ Application ready for deployment")
    else:
        print("❌ Application has import issues")
        sys.exit(1)
    
    print("\n🚀 Environment verification complete - ready for Render!")

if __name__ == "__main__":
    main() 