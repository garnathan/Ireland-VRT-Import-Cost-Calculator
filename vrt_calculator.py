#!/usr/bin/env python3
"""
VRT (Vehicle Registration Tax) Calculator for importing cars from UK to Ireland
Note: This is a basic framework - always verify current rates with Irish Revenue
"""

import requests
import json
from datetime import datetime
from typing import Dict, Optional, Tuple

class VRTCalculator:
    def __init__(self):
        # Official VRT rates from Irish Revenue (Category A) - 2024
        # Format: (min_co2, max_co2, rate_percent, minimum_amount_eur)
        self.co2_bands = [
            (0, 50, 7, 140),
            (51, 80, 9, 180),
            (81, 85, 9.75, 195),
            (86, 90, 10.5, 210),
            (91, 95, 11.25, 225),
            (96, 100, 12, 240),
            (101, 105, 12.75, 255),
            (106, 110, 13.5, 270),
            (111, 115, 15.25, 305),
            (116, 120, 16, 320),
            (121, 125, 16.75, 335),
            (126, 130, 17.5, 350),
            (131, 135, 19.25, 385),
            (136, 140, 20, 400),
            (141, 145, 21.5, 430),
            (146, 150, 25, 500),
            (151, 155, 27.5, 550),
            (156, 170, 30, 600),
            (171, 190, 35, 700),
            (191, float('inf'), 41, 820)
        ]
    
    def get_omv_from_uk_price(self, uk_price_gbp: float, exchange_rate: float = None) -> float:
        """
        Calculate Open Market Value (OMV) from UK purchase price
        OMV = UK price converted to EUR + estimated transport/insurance costs
        """
        if exchange_rate is None:
            # You could integrate with a currency API here
            exchange_rate = 1.17  # Example rate - GET CURRENT RATE
        
        # Convert to EUR
        price_eur = uk_price_gbp * exchange_rate
        
        # Add estimated transport and insurance (typically 3-5% of value)
        transport_insurance = price_eur * 0.04  # 4% estimate
        
        omv = price_eur + transport_insurance
        return round(omv, 2)
    
    def get_co2_rate_and_minimum(self, co2_emissions: int) -> Tuple[float, int]:
        """Get VRT percentage rate and minimum amount based on CO2 emissions"""
        for min_co2, max_co2, rate, minimum in self.co2_bands:
            if min_co2 <= co2_emissions <= max_co2:
                return rate, minimum
        return 41, 820  # Default to highest rate
    
    def calculate_vrt(self, 
                     omv: float, 
                     co2_emissions: int, 
                     fuel_type: str,
                     vehicle_age_years: int = 0,
                     vehicle_value_eur: float = 0) -> Dict:
        """
        Calculate VRT and all import costs including Customs Duty and VAT
        """
        # Get CO2 rate and minimum
        co2_rate, vrt_minimum = self.get_co2_rate_and_minimum(co2_emissions)
        
        # Calculate base VRT
        base_vrt = omv * (co2_rate / 100)
        
        # Apply age-related depreciation (if applicable)
        if vehicle_age_years > 0:
            # Depreciation rates vary - this is simplified
            depreciation_rate = min(vehicle_age_years * 0.02, 0.1)  # Max 10%
            base_vrt = base_vrt * (1 - depreciation_rate)
        
        # Apply minimum VRT (whichever is greater)
        final_vrt = max(base_vrt, vrt_minimum)
        
        # Calculate Customs Duty (10% of vehicle value)
        customs_duty = vehicle_value_eur * 0.10
        
        # Calculate VAT (21% on vehicle value + customs duty + VRT)
        vat_base = vehicle_value_eur + customs_duty + final_vrt
        vat_amount = vat_base * 0.21
        
        return {
            'omv': omv,
            'co2_emissions': co2_emissions,
            'co2_rate_percent': co2_rate,
            'fuel_type': fuel_type,
            'vehicle_age_years': vehicle_age_years,
            'base_vrt': round(base_vrt, 2),
            'minimum_vrt': vrt_minimum,
            'final_vrt': round(final_vrt, 2),
            'customs_duty': round(customs_duty, 2),
            'vat_base': round(vat_base, 2),
            'vat_amount': round(vat_amount, 2),
            'total_import_cost': round(vehicle_value_eur + customs_duty + final_vrt + vat_amount + 102, 2),
            'calculation_date': datetime.now().isoformat()
        }
    
    def lookup_vehicle_specs(self, registration: str) -> Optional[Dict]:
        """
        Placeholder for vehicle lookup by registration
        You could integrate with DVLA API or similar service
        """
        # This would need to integrate with a vehicle data API
        # For now, return None - user must provide specs manually
        print(f"Vehicle lookup for {registration} not implemented")
        print("Please provide CO2 emissions and fuel type manually")
        return None

def main():
    calculator = VRTCalculator()
    
    print("VRT Calculator for UK to Ireland Car Imports")
    print("=" * 50)
    print("WARNING: Always verify current rates with Irish Revenue!")
    print()
    
    try:
        # Get vehicle details
        uk_price = float(input("Enter UK purchase price (GBP): £"))
        co2_emissions = int(input("Enter CO2 emissions (g/km): "))
        fuel_type = input("Enter fuel type (petrol/diesel/electric/hybrid): ")
        vehicle_age = int(input("Enter vehicle age in years (0 for new): "))
        
        # Optional: Get current exchange rate
        exchange_rate_input = input("Enter GBP to EUR exchange rate (press Enter for default): ")
        exchange_rate = float(exchange_rate_input) if exchange_rate_input else None
        
        # Calculate OMV
        omv = calculator.get_omv_from_uk_price(uk_price, exchange_rate)
        
        # Get vehicle value in EUR for customs duty calculation
        if exchange_rate_input:
            vehicle_value_eur = uk_price * float(exchange_rate_input)
        else:
            vehicle_value_eur = uk_price * 1.17  # Default rate
        
        # Calculate VRT and all import costs
        result = calculator.calculate_vrt(omv, co2_emissions, fuel_type, vehicle_age, vehicle_value_eur)
        
        # Display results
        print("\n" + "=" * 60)
        print("COMPREHENSIVE IMPORT COST CALCULATION")
        print("=" * 60)
        print(f"Open Market Value (OMV): €{result['omv']:,.2f}")
        print(f"CO2 Emissions: {result['co2_emissions']}g/km")
        print(f"VRT Rate: {result['co2_rate_percent']}%")
        print(f"Fuel Type: {result['fuel_type']}")
        print(f"Vehicle Age: {result['vehicle_age_years']} years")
        print()
        print("COST BREAKDOWN:")
        print(f"Base VRT: €{result['base_vrt']:,.2f}")
        print(f"Minimum VRT: €{result['minimum_vrt']:,.2f}")
        print(f"FINAL VRT: €{result['final_vrt']:,.2f}")
        print()
        print(f"Customs Duty (10%): €{result['customs_duty']:,.2f}")
        print(f"VAT Base: €{result['vat_base']:,.2f}")
        print(f"VAT Amount (21%): €{result['vat_amount']:,.2f}")
        print()
        print(f"🎯 TOTAL IMPORT COST: €{result['total_import_cost']:,.2f}")
        print("=" * 60)
        
        # Additional costs reminder
        print("\nADDITIONAL COSTS TO CONSIDER:")
        print("- Motor tax (varies by CO2 emissions)")
        print("- NCT test (if required)")
        print("- Irish insurance")
        print("- Vehicle modifications (if required)")
        print()
        print("IMPORTANT NOTES:")
        print("- Customs Duty: 10% of vehicle purchase price")
        print("- VAT: 21% on vehicle + customs duty + VRT")
        print("- VRT: Based on CO2 emissions and OMV")
        print("- All rates subject to change - verify with Irish Revenue")
        
        # Save results to file
        save_file = input("\nSave results to file? (y/n): ")
        if save_file.lower() == 'y':
            filename = f"vrt_calculation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(filename, 'w') as f:
                json.dump(result, f, indent=2)
            print(f"Results saved to {filename}")
    
    except ValueError as e:
        print(f"Error: Invalid input - {e}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
