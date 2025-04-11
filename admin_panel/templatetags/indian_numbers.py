from django import template

register = template.Library()

def indian_number_format(value):
    """Format number as per Indian numbering system."""
    value = str(value)
    
    if '.' in value:
        int_part, dec_part = value.split('.')
    else:
        int_part, dec_part = value, None

    # Reverse the integer part for easier processing
    int_part = int_part[::-1]

    # Group the first 3 digits, then every 2 digits
    grouped = [int_part[:3]] + [int_part[i:i+2] for i in range(3, len(int_part), 2)]
    
    # Join the groups with commas and reverse back
    formatted_value = ','.join(grouped)[::-1]

    # Append the decimal part if it exists
    if dec_part:
        formatted_value = formatted_value + '.' + dec_part

    return formatted_value

register.filter('indian_number_format', indian_number_format)
