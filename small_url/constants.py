import re
import string

ATTEMPTS_TO_CREATE_SHORT = 30
GENERATED_SHORT_LENGTH = 6
MAX_SHORT_LENGTH = 16
ORIGINAL_LINK_LENGTH = 4321
SYMBOLS = string.ascii_letters + string.digits
PATTERN = rf'^[{re.escape(SYMBOLS)}]+$'
READDRESING_FUNCTION = 'readdressing'
