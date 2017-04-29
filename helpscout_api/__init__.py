from datetime import datetime

format_dt = lambda dt: datetime.strftime(dt, "%Y-%m-%dT%H:%M:%SZ")
parse_dt = lambda dt: datetime.strptime(dt, "%Y-%m-%dT%H:%M:%SZ")
format_d = lambda dt: datetime.strftime(dt, "%Y-%m-%d")
