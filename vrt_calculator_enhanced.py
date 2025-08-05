#!/usr/bin/env python3
"""
Enhanced VRT Calculator with API integration capabilities
Includes currency conversion and vehicle data lookup features
"""

import requests
import json
from datetime import datetime
from typing import Dict, Optional, Tuple
import os

class EnhancedVRTCalculator:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv('EXCHANGE_API_KEY')
        
        # VRT rates - ALWAYS VERIFY WITH CURRENT IRISH REVENUE RATES
        self.co2_bands = {
            (0, 120): 14,
            (121, 140): 16,
            (141, 155): 20,
            (156, 170): 24,
            (171, 190): 28,
            (191, 225): 32,
            (226, float('inf')): 36
        }
        
        self.minimum_vrt = {
            'petrol': 125,
            'diesel': 200,
            'electric': 0,
            'hybrid': 125
        }
    
    def get_current_exchange_rate(self) -> Optional[float]:
        """
        Get current GBP to EUR exchange rate from API
        You can use services like exchangerate-api.com, fixer.io, etc.
        """
        try:
            # Example using exchangerate-api.com (free tier available)
            url = "https://api.exchangerate-api.com/v4/latest/GBP"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                eur_rate = data['rates'].get('EUR')
                if eur_rate:
                    print(f"Current exchange rate: 1 GBP = {eur_rate:.4f} EUR")
                    return eur_rate
        except Exception as e:
            print(f"Could not fetch exchange rate: {e}")
        
        return None
    
    def lookup_vehicle_by_reg(self, registration: str) -> Optional[Dict]:
        """
        Lookup vehicle details by UK registration
        This would require integration with DVLA API or similar service
        """
        # Placeholder - would need actual API integration
        # DVLA provides some vehicle data APIs
        print(f"Vehicle lookup for {registration} - API integration needed")
        
        # Example of what this might return:
        example_data = {
            'registration': registration,
            'make': 'Example Make',
            'model': 'Example Model',
            'fuel_type': 'Petrol',
            'co2_emissions': 150,
            'year_of_manufacture': 2020,
            'engine_capacity': 2000
        }
        
        return None  # Return None until real API is integrated
    
    def estimate_transport_costs(self, vehicle_value: float, 
                               transport_method: str = 'ferry') -> Dict:
        """
        Estimate transport and associated costs
        """
        costs = {
            'transport': 0,
            'insurance': 0,
            'customs_clearance': 0,
            'total': 0
        }
        
        if transport_method.lower() == 'ferry':
            # Ferry costs typically £200-400 depending on route and vehicle size
            costs['transport'] = 300
        elif transport_method.lower() == 'drive':
            # Fuel, tolls, accommodation if needed
            costs['transport'] = 150
        
        # Transit insurance (typically 1-2% of vehicle value)
        costs['insurance'] = vehicle_value * 0.015
        
        # Customs clearance fees
        costs['customs_clearance'] = 50
        
        costs['total'] = sum(costs.values())
        
        return costs
    
    def calculate_comprehensive_costs(self, 
                                    uk_price_gbp: float,
                                    co2_emissions: int,
                                    fuel_type: str,
                                    vehicle_age_years: int = 0,
                                    transport_method: str = 'ferry') -> Dict:
        """
        Calculate all costs associated with importing a vehicle
        """
        # Get current exchange rate
        exchange_rate = self.get_current_exchange_rate()
        if not exchange_rate:
            exchange_rate = 1.17  # Fallback rate
            print("Using fallback exchange rate - verify current rate!")
        
        # Convert UK price to EUR
        vehicle_value_eur = uk_price_gbp * exchange_rate
        
        # Calculate transport costs
        transport_costs = self.estimate_transport_costs(vehicle_value_eur, transport_method)
        
        # Calculate OMV (Open Market Value)
        omv = vehicle_value_eur + transport_costs['total']
        
        # Calculate VRT
        co2_rate = self.get_co2_rate(co2_emissions)
        base_vrt = omv * (co2_rate / 100)
        
        # Apply age depreciation if applicable
        if vehicle_age_years > 0:
            depreciation_rate = min(vehicle_age_years * 0.02, 0.1)
            base_vrt = base_vrt * (1 - depreciation_rate)
        
        # Apply minimum VRT
        minimum = self.minimum_vrt.get(fuel_type.lower(), 125)
        final_vrt = max(base_vrt, minimum)
        
        # Calculate motor tax (simplified - actual rates vary by CO2 and year)
        motor_tax = self.estimate_motor_tax(co2_emissions, fuel_type)
        
        return {
            'purchase_details': {
                'uk_price_gbp': uk_price_gbp,
                'exchange_rate': exchange_rate,
                'vehicle_value_eur': round(vehicle_value_eur, 2)
            },
            'transport_costs': {k: round(v, 2) for k, v in transport_costs.items()},
            'omv': round(omv, 2),
            'vrt_calculation': {
                'co2_emissions': co2_emissions,
                'co2_rate_percent': co2_rate,
                'base_vrt': round(base_vrt, 2),
                'minimum_vrt': minimum,
                'final_vrt': round(final_vrt, 2)
            },
            'additional_costs': {
                'motor_tax_annual': motor_tax,
                'nct_test': 55 if vehicle_age_years >= 4 else 0,
                'registration_fee': 102
            },
            'total_import_cost': round(vehicle_value_eur + transport_costs['total'] + final_vrt + 102, 2),
            'calculation_date': datetime.now().isoformat()
        }
    
    def get_co2_rate(self, co2_emissions: int) -> int:
        """Get VRT percentage rate based on CO2 emissions"""
        for (min_co2, max_co2), rate in self.co2_bands.items():
            if min_co2 <= co2_emissions <= max_co2:
                return rate
        return 36
    
    def estimate_motor_tax(self, co2_emissions: int, fuel_type: str) -> int:
        """
        Estimate annual motor tax - simplified calculation
        Actual rates depend on CO2 emissions, fuel type, and year of registration
        """
        if fuel_type.lower() == 'electric':
            return 120  # Electric vehicle rate
        
        # Simplified CO2-based rates (verify current rates)
        if co2_emissions <= 120:
            return 200
        elif co2_emissions <= 140:
            return 270
        elif co2_emissions <= 155:
            return 330
        elif co2_emissions <= 170:
            return 481
        elif co2_emissions <= 190:
            return 677
        else:
            return 1200  # High emission vehicles

def main():
    calculator = EnhancedVRTCalculator()
    
    print("Enhanced VRT Calculator for UK to Ireland Car Imports")
    print("=" * 60)
    print("⚠️  WARNING: Always verify current rates with Irish Revenue!")
    print("⚠️  This calculator provides estimates only!")
    print()
    
    try:
        # Option to lookup by registration
        lookup_option = input("Do you want to lookup vehicle by UK registration? (y/n): ")
        
        if lookup_option.lower() == 'y':
            registration = input("Enter UK registration: ").upper()
            vehicle_data = calculator.lookup_vehicle_by_reg(registration)
            
            if vehicle_data:
                print("Vehicle found!")
                # Use looked up data
                co2_emissions = vehicle_data['co2_emissions']
                fuel_type = vehicle_data['fuel_type']
                vehicle_age = datetime.now().year - vehicle_data['year_of_manufacture']
            else:
                print("Vehicle lookup not available - please enter details manually")
                co2_emissions = int(input("Enter CO2 emissions (g/km): "))
                fuel_type = input("Enter fuel type (petrol/diesel/electric/hybrid): ")
                vehicle_age = int(input("Enter vehicle age in years: "))
        else:
            # Manual entry
            co2_emissions = int(input("Enter CO2 emissions (g/km): "))
            fuel_type = input("Enter fuel type (petrol/diesel/electric/hybrid): ")
            vehicle_age = int(input("Enter vehicle age in years: "))
        
        uk_price = float(input("Enter UK purchase price (GBP): £"))
        transport_method = input("Transport method (ferry/drive) [ferry]: ") or "ferry"
        
        # Calculate comprehensive costs
        result = calculator.calculate_comprehensive_costs(
            uk_price, co2_emissions, fuel_type, vehicle_age, transport_method
        )
        
        # Display detailed results
        print("\n" + "=" * 60)
        print("COMPREHENSIVE IMPORT COST CALCULATION")
        print("=" * 60)
        
        print(f"\n📋 PURCHASE DETAILS:")
        print(f"UK Price: £{result['purchase_details']['uk_price_gbp']:,.2f}")
        print(f"Exchange Rate: {result['purchase_details']['exchange_rate']:.4f}")
        print(f"Vehicle Value (EUR): €{result['purchase_details']['vehicle_value_eur']:,.2f}")
        
        print(f"\n🚚 TRANSPORT COSTS:")
        for cost_type, amount in result['transport_costs'].items():
            if cost_type != 'total':
                print(f"{cost_type.replace('_', ' ').title()}: €{amount:,.2f}")
        print(f"Total Transport: €{result['transport_costs']['total']:,.2f}")
        
        print(f"\n💰 VRT CALCULATION:")
        print(f"Open Market Value: €{result['omv']:,.2f}")
        print(f"CO2 Emissions: {result['vrt_calculation']['co2_emissions']}g/km")
        print(f"VRT Rate: {result['vrt_calculation']['co2_rate_percent']}%")
        print(f"VRT Amount: €{result['vrt_calculation']['final_vrt']:,.2f}")
        
        print(f"\n📄 ADDITIONAL COSTS:")
        for cost_type, amount in result['additional_costs'].items():
            print(f"{cost_type.replace('_', ' ').title()}: €{amount:,.2f}")
        
        print(f"\n🎯 TOTAL IMPORT COST: €{result['total_import_cost']:,.2f}")
        print("=" * 60)
        
        print(f"\n📝 ONGOING ANNUAL COSTS:")
        print(f"Motor Tax: €{result['additional_costs']['motor_tax_annual']:,.2f}")
        print(f"Insurance: €??? (get quotes from Irish insurers)")
        
        # Save detailed results
        save_file = input("\nSave detailed results to JSON file? (y/n): ")
        if save_file.lower() == 'y':
            filename = f"vrt_detailed_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(filename, 'w') as f:
                json.dump(result, f, indent=2)
            print(f"Results saved to {filename}")
    
    except ValueError as e:
        print(f"❌ Error: Invalid input - {e}")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
