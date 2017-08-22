from . import vj_hdu, vj_poj
from . import config


def request_problem_detail(oj, pid):
    return {
        'hdu': vj_hdu.request_problem_detail,
        'poj': vj_poj.request_problem_detail,
    }[oj](pid)
