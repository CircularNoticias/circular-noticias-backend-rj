from datetime import datetime
from dateutil import parser
from dateutil.relativedelta import relativedelta

def summarize(text):
    if not text:
        return ''
    return text[:147].strip() + '...' if len(text) > 150 else text.strip()

def format_time(date_str):
    try:
        pub_date = parser.parse(date_str)
        now = datetime.utcnow()
        delta = relativedelta(now, pub_date)

        if delta.years > 0:
            return f"{delta.years}y"
        elif delta.months > 0:
            return f"{delta.months}mo"
        elif delta.days > 0:
            return f"{delta.days}d"
        elif delta.hours > 0:
            return f"{delta.hours}h"
        elif delta.minutes > 0:
            return f"{delta.minutes}min"
        else:
            return f"{delta.seconds}s"
    except:
        return ""
