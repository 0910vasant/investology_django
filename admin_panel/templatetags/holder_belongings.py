from django import template

register = template.Library()

@register.filter
def full_name(short_code):
    short_to_full = {
        # 'S': 'Self',
        # 'F': 'Family',
        "SE" : "Self",
        "SP" : "Spouse",
        "DC" : "Dependent Children",
        "DP" : "Dependent Parents",
        "DS" : "Dependent Siblings",
        "GD" : "Guardian",
        "F"  : "Family",
        # Add more mappings as needed
    }
   
    return short_to_full.get(short_code, short_code)  # Returns the short code if no match
