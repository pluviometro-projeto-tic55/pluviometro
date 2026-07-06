#!/usr/bin/env python
"""
Standalone script to run VAR model calibration
Usage: python calibrate_model.py <station_id>
"""

import sys
from src.model_calibration import print_calibration_report

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python calibrate_model.py <station_id>")
        sys.exit(1)
    
    station_id = int(sys.argv[1])
    print_calibration_report(station_id)
