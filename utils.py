from datetime import datetime
from dateutil import parser

def summarize(text):
    if not text:
        return ''
    return text[:147].strip() + '...' if len(text) > 150 else text.strip()

def format_time(date_input):
    try:
        if isinstance(date_input, str):
            pub_date = parser.parse(date_input)
        elif hasattr(date_input, 'tm_year'):  # time.struct_time
            pub_date = datetime(*date_input[:6])
        else:
            return ""
        return pub_date.strftime("%d/%m/%Y")
    except:
        return ""
