# VRT Calculator for UK to Ireland Car Imports

This project provides multiple ways to calculate Vehicle Registration Tax (VRT) for importing cars from the UK to Ireland:
- Command-line Python scripts
- **Flask web application with modern UI**

## ⚠️ Important Disclaimer

**This calculator provides estimates only!** Always verify current rates and regulations with:
- Irish Revenue (revenue.ie)
- Customs officials
- Professional import agents

VRT rates, CO2 bands, and minimum amounts change regularly.

## Files

### Command Line Tools
- `vrt_calculator.py` - Basic VRT calculator
- `vrt_calculator_enhanced.py` - Enhanced version with API integration capabilities

### Web Application
- `app.py` - Flask web application
- `run.py` - Production runner script
- `templates/` - HTML templates
- `static/` - CSS and JavaScript files
- `requirements.txt` - Python dependencies

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### 🌐 Web Application (Recommended)
```bash
# Run the Flask web app
python3 app.py

# Or use the production runner
python3 run.py

# Access at: http://localhost:5000
```

**Features:**
- Modern, responsive web interface
- **Import origin selection** (UK vs Northern Ireland)
- Real-time exchange rate fetching
- Interactive form validation
- Detailed cost breakdown with conditional customs duty
- Print-friendly results
- Mobile-friendly design
- API endpoints for integration

### Command Line Tools

#### Basic Calculator
```bash
python3 vrt_calculator.py
```

#### Enhanced Calculator
```bash
python3 vrt_calculator_enhanced.py
```

## What the Calculator Includes

### VRT Calculation
- CO2-based VRT rates (14% to 36%)
- Minimum VRT amounts by fuel type
- Age-related depreciation
- Open Market Value (OMV) calculation

### Additional Costs Estimated
- Transport costs (ferry/driving)
- Transit insurance
- Customs clearance fees
- Motor tax estimates
- Registration fees

### Current VRT Rates (Verify These!)
- 0-120g/km CO2: 14%
- 121-140g/km CO2: 16%
- 141-155g/km CO2: 20%
- 156-170g/km CO2: 24%
- 171-190g/km CO2: 28%
- 191-225g/km CO2: 32%
- 226g/km+ CO2: 36%

### Minimum VRT Amounts
- Petrol: €125
- Diesel: €200
- Electric: €0
- Hybrid: €125

## Features to Add

1. **Real-time exchange rates** - Integrate with currency API
2. **Vehicle lookup** - Connect to DVLA or similar API
3. **Updated rates** - Automatically fetch current VRT rates
4. **Motor tax calculator** - More accurate annual tax calculation
5. **Insurance estimates** - Integration with Irish insurance providers

## Example Calculation

For a 2020 petrol car with 150g/km CO2, purchased for £15,000:

### From United Kingdom:
```
UK Price: £15,000
Exchange Rate: 1.17
Vehicle Value: €17,550
Transport Costs: €350
OMV: €17,900

Customs Duty (10%): €1,755
VRT Rate: 20% (150g/km CO2)
VRT Amount: €3,580
VAT Base: €17,550 + €1,755 + €3,580 = €22,885
VAT (21%): €4,806
Registration Fee: €102

Total Import Cost: €28,143
```

### From Northern Ireland:
```
UK Price: £15,000
Exchange Rate: 1.17
Vehicle Value: €17,550
Transport Costs: €350
OMV: €17,900

Customs Duty: €0 (No duty - EU customs union)
VRT Rate: 20% (150g/km CO2)
VRT Amount: €3,580
VAT Base: €17,550 + €0 + €3,580 = €21,130
VAT (21%): €4,437
Registration Fee: €102

Total Import Cost: €26,369
```

**Savings from Northern Ireland: €1,774** (6.3% less)

**Cost Breakdown (UK Import):**
- Vehicle + Transport: €17,900 (63.6%)
- Customs Duty: €1,755 (6.2%)
- VRT: €3,580 (12.7%)
- VAT: €4,806 (17.1%)
- Registration: €102 (0.4%)

## Legal Requirements

When importing a car from UK to Ireland, you must:

1. **Declare the import** to Irish Customs
2. **Pay VRT** within specified timeframe
3. **Register the vehicle** with NCTS
4. **Get NCT test** (if vehicle is 4+ years old)
5. **Arrange Irish insurance**
6. **Pay motor tax**

## Useful Resources

- [Irish Revenue VRT Information](https://www.revenue.ie/en/importing-vehicles-duty-free-allowances/importing-a-vehicle/vehicle-registration-tax/index.aspx)
- [Citizens Information - Importing a Car](https://www.citizensinformation.ie/en/travel-and-recreation/motoring/buying-or-selling-a-vehicle/importing-a-vehicle-into-ireland/)
- [NCTS Vehicle Registration](https://www.ncts.ie/)

## Contributing

This is a basic framework. Contributions welcome for:
- API integrations
- Updated rate tables
- Better cost estimates
- UI improvements

## License

This script is provided as-is for educational purposes. No warranty provided.
