#!/usr/bin/env python3
"""
Flask Web Application for VRT Calculator
"""

from flask import Flask, render_template, request, jsonify, flash, redirect, url_for
import requests
from datetime import datetime
import json
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'your-secret-key-change-this')

class VRTCalculatorWeb:
    def __init__(self):
        # Official VRT rates from Irish Revenue (Category A) - 2024
        # Format: (min_co2, max_co2): (rate_percent, minimum_amount_eur)
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
        
        # Fuel type multipliers (if any - keeping for compatibility)
        self.fuel_type_info = {
            'petrol': {'name': 'Petrol'},
            'diesel': {'name': 'Diesel'},
            'electric': {'name': 'Electric'},
            'hybrid': {'name': 'Hybrid'}
        }
    
    def get_current_exchange_rate(self):
        """Get current GBP to EUR exchange rate"""
        try:
            url = "https://api.exchangerate-api.com/v4/latest/GBP"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                return data['rates'].get('EUR', 1.17)
        except Exception:
            pass
        
        return 1.17  # Fallback rate
    
    def get_co2_rate_and_minimum(self, co2_emissions):
        """Get VRT percentage rate and minimum amount based on CO2 emissions"""
        for min_co2, max_co2, rate, minimum in self.co2_bands:
            if min_co2 <= co2_emissions <= max_co2:
                return rate, minimum
        # Default to highest rate if not found
        return 41, 820
    
    def estimate_transport_costs(self, vehicle_value, transport_method='ferry'):
        """Estimate transport and associated costs"""
        costs = {
            'transport': 300 if transport_method.lower() == 'ferry' else 150,
            'insurance': vehicle_value * 0.015,
            'customs_clearance': 50
        }
        costs['total'] = sum(costs.values())
        return costs
    
    def estimate_motor_tax(self, co2_emissions, fuel_type):
        """
        Estimate annual motor tax based on CO2 emissions
        Rates are approximate - actual rates depend on year of registration
        """
        if fuel_type.lower() == 'electric':
            return 120  # Electric vehicle rate
        
        # Motor tax bands (approximate rates for recent vehicles)
        if co2_emissions <= 80:
            return 120
        elif co2_emissions <= 100:
            return 170
        elif co2_emissions <= 110:
            return 190
        elif co2_emissions <= 120:
            return 200
        elif co2_emissions <= 130:
            return 270
        elif co2_emissions <= 140:
            return 330
        elif co2_emissions <= 155:
            return 481
        elif co2_emissions <= 170:
            return 677
        elif co2_emissions <= 190:
            return 920
        else:
            return 1200  # High emission vehicles
    
    def calculate_comprehensive_costs(self, uk_price_gbp, co2_emissions, fuel_type, 
                                    vehicle_age_years=0, transport_method='ferry', import_origin='uk'):
        """Calculate all costs associated with importing a vehicle"""
        
        # Get current exchange rate
        exchange_rate = self.get_current_exchange_rate()
        
        # Convert UK price to EUR
        vehicle_value_eur = uk_price_gbp * exchange_rate
        
        # Calculate transport costs
        transport_costs = self.estimate_transport_costs(vehicle_value_eur, transport_method)
        
        # Calculate OMV (Open Market Value)
        omv = vehicle_value_eur + transport_costs['total']
        
        # Calculate Customs Duty (10% of vehicle value for UK, 0% for Northern Ireland)
        customs_duty = vehicle_value_eur * 0.10 if import_origin.lower() == 'uk' else 0.0
        
        # Calculate VRT using official Irish Revenue rates
        co2_rate, vrt_minimum = self.get_co2_rate_and_minimum(co2_emissions)
        base_vrt = omv * (co2_rate / 100)
        
        # Apply age depreciation if applicable
        if vehicle_age_years > 0:
            depreciation_rate = min(vehicle_age_years * 0.02, 0.1)
            base_vrt = base_vrt * (1 - depreciation_rate)
        
        # Apply minimum VRT (whichever is greater: calculated VRT or minimum)
        final_vrt = max(base_vrt, vrt_minimum)
        
        # Calculate VAT (21% on vehicle value + customs duty + VRT)
        vat_base = vehicle_value_eur + customs_duty + final_vrt
        vat_amount = vat_base * 0.21
        
        # Calculate motor tax
        motor_tax = self.estimate_motor_tax(co2_emissions, fuel_type)
        
        # Calculate total import cost
        total_import_cost = (vehicle_value_eur + transport_costs['total'] + 
                           customs_duty + final_vrt + vat_amount + 102)
        
        return {
            'purchase_details': {
                'uk_price_gbp': uk_price_gbp,
                'exchange_rate': round(exchange_rate, 4),
                'vehicle_value_eur': round(vehicle_value_eur, 2),
                'import_origin': import_origin.upper()
            },
            'transport_costs': {k: round(v, 2) for k, v in transport_costs.items()},
            'omv': round(omv, 2),
            'customs_duty': round(customs_duty, 2),
            'customs_duty_applicable': import_origin.lower() == 'uk',
            'vrt_calculation': {
                'co2_emissions': co2_emissions,
                'co2_rate_percent': co2_rate,
                'base_vrt': round(base_vrt, 2),
                'minimum_vrt': vrt_minimum,
                'final_vrt': round(final_vrt, 2)
            },
            'vat_calculation': {
                'vat_base': round(vat_base, 2),
                'vat_rate_percent': 21,
                'vat_amount': round(vat_amount, 2)
            },
            'additional_costs': {
                'motor_tax_annual': motor_tax,
                'nct_test': 55 if vehicle_age_years >= 4 else 0,
                'registration_fee': 102
            },
            'total_import_cost': round(total_import_cost, 2),
            'calculation_date': datetime.now().isoformat()
        }

# Initialize calculator
calculator = VRTCalculatorWeb()

@app.route('/')
def index():
    """Main calculator page"""
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    """Handle VRT calculation"""
    try:
        # Get form data
        uk_price = float(request.form.get('uk_price', 0))
        co2_emissions = int(request.form.get('co2_emissions', 0))
        fuel_type = request.form.get('fuel_type', 'petrol')
        vehicle_age = int(request.form.get('vehicle_age', 0))
        transport_method = request.form.get('transport_method', 'ferry')
        import_origin = request.form.get('import_origin', 'uk')
        
        # Validate inputs
        if uk_price <= 0:
            flash('Please enter a valid UK price', 'error')
            return redirect(url_for('index'))
        
        if co2_emissions <= 0:
            flash('Please enter valid CO2 emissions', 'error')
            return redirect(url_for('index'))
        
        # Calculate costs
        result = calculator.calculate_comprehensive_costs(
            uk_price, co2_emissions, fuel_type, vehicle_age, transport_method, import_origin
        )
        
        return render_template('results.html', result=result)
        
    except ValueError as e:
        flash(f'Invalid input: {str(e)}', 'error')
        return redirect(url_for('index'))
    except Exception as e:
        flash(f'Calculation error: {str(e)}', 'error')
        return redirect(url_for('index'))

@app.route('/api/calculate', methods=['POST'])
def api_calculate():
    """API endpoint for VRT calculation"""
    try:
        data = request.get_json()
        
        uk_price = float(data.get('uk_price', 0))
        co2_emissions = int(data.get('co2_emissions', 0))
        fuel_type = data.get('fuel_type', 'petrol')
        vehicle_age = int(data.get('vehicle_age', 0))
        transport_method = data.get('transport_method', 'ferry')
        import_origin = data.get('import_origin', 'uk')
        
        if uk_price <= 0 or co2_emissions <= 0:
            return jsonify({'error': 'Invalid input values'}), 400
        
        result = calculator.calculate_comprehensive_costs(
            uk_price, co2_emissions, fuel_type, vehicle_age, transport_method, import_origin
        )
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/exchange-rate')
def get_exchange_rate():
    """API endpoint to get current exchange rate"""
    try:
        rate = calculator.get_current_exchange_rate()
        return jsonify({
            'gbp_to_eur': rate,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/about')
def about():
    """About page with disclaimer and information"""
    return render_template('about.html')

@app.route('/api/vrt-bands')
def get_vrt_bands():
    """API endpoint to get current VRT bands"""
    bands = []
    for (min_co2, max_co2), rate in calculator.co2_bands.items():
        bands.append({
            'min_co2': min_co2,
            'max_co2': max_co2 if max_co2 != float('inf') else 'unlimited',
            'rate_percent': rate
        })
    
    return jsonify({
        'co2_bands': bands,
        'minimum_vrt': calculator.minimum_vrt
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
