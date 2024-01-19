def get_window_icon():
    data="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"
    return data