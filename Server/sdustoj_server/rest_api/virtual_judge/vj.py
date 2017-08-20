from . import vj_hdu
from . import config


def request_problem_detail(oj, pid):
    return {
        'hdu': vj_hdu.request_problem_detail
    }[oj](pid)
