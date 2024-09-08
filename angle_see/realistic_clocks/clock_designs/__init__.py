from .classic import draw_classic_clock
from .modern import draw_modern_clock
from .minimalist import draw_minimalist_clock
from .vintage import draw_vintage_clock
from .numbered import draw_numbered_clock
from .roman import draw_roman_clock

AVAILABLE_DESIGNS = ["classic", "modern", "minimalist", "vintage", "numbered", "roman"]

def get_clock_design(design):
    designs = {
        "classic": draw_classic_clock,
        "modern": draw_modern_clock,
        "minimalist": draw_minimalist_clock,
        "vintage": draw_vintage_clock,
        "numbered": draw_numbered_clock,
        "roman": draw_roman_clock
    }
    return designs.get(design, draw_classic_clock)
