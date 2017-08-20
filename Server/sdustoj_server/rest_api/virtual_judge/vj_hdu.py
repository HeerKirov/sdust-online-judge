import requests
import re
import html2text
from . import utils

SETTING = {
    'host': 'http://acm.hdu.edu.cn/',
    'login': 'userloginex.php?action=login',
    'list': 'listproblem.php',
    'instance': 'showproblem.php'
}

LANG_JAVA = ['Java', 'C#']
LANG_OTHER = ['C', 'C++', 'GCC', 'G++', 'Pascal']


def get_url(url, *args):
    return SETTING['host'] + SETTING[url] % args


def get_problem_item(html):
    def get_regex(text, regex):
        reg_content = re.findall(regex, text)
        if reg_content is not None and len(reg_content) > 0:
            return reg_content[0]
        else:
            return None

    def change_link(host, text):
        rep_link = """<a href='([\\s\\S]*?)'[\\s\\S]*?>"""
        rep_link_g = """<a href='%s\\1'>""" % (host,)
        rep_img = """<img(.*?)src=([\\s\\S]*?)>"""
        rep_img_g = """<img\\1src=%s\\2>""" % (host,)
        text = re.sub(rep_link, rep_link_g, text)
        text = re.sub(rep_img, rep_img_g, text)
        return text

    def to_md(text):
        if text is None:
            return None
        md = html2text.html2text(text)
        return md.strip('\n')
    html = change_link(SETTING['host'], html)
    title = get_regex(html, """<h1 style='\\S+'>([\\S\\s]+)</h1>""")
    time_limit = get_regex(html, """Time Limit: (\\d+)/(\\d+) MS \\(Java/Others\\)""")
    memory_limit = get_regex(html, """Memory Limit: (\\d+)/(\\d+) K \\(Java/Others\\)""")
    c_description = get_regex(html, """<div class=panel_title align=left>Problem Description</div>\\s*""" +
                              """<div class=panel_content>([\\s\\S\\n]*?)</div>\\s*""" +
                              """<div class=panel_bottom>&nbsp;</div><br>\\s*""")
    c_input = get_regex(html, """<div class=panel_title align=left>Input</div>\\s*""" +
                              """<div class=panel_content>([\\s\\S\\n]*?)</div>\\s*""" +
                              """<div class=panel_bottom>&nbsp;</div><br>\\s*""")
    c_output = get_regex(html, """<div class=panel_title align=left>Output</div>\\s*""" +
                               """<div class=panel_content>([\\s\\S\\n]*?)</div>\\s*""" +
                               """<div class=panel_bottom>&nbsp;</div><br>\\s*""")
    c_sample_input = get_regex(html, """<div class=panel_title align=left>Sample Input</div>\\s*""" +
                                     """<div class=panel_content>([\\s\\S\\n]*?)</div>\\s*""" +
                                     """<div class=panel_bottom>&nbsp;</div><br>\\s*""")
    c_sample_output = get_regex(html, """<div class=panel_title align=left>Sample Output</div>\\s*""" +
                                      """<div class=panel_content>([\\s\\S\\n]*?)</div>\\s*""" +
                                      """<div class=panel_bottom>&nbsp;</div><br>\\s*""")
    c_author = get_regex(html, """<div class=panel_title align=left>Author</div>\\s*""" +
                               """<div class=panel_content>([\\s\\S\\n]*?)</div>\\s*""" +
                               """<div class=panel_bottom>&nbsp;</div><br>\\s*""")
    c_source = get_regex(html, """<div class=panel_title align=left>Source</div>\\s*""" +
                               """<div class=panel_content>([\\s\\S\\n]*?)</div>\\s*""" +
                               """<div class=panel_bottom>&nbsp;</div><br>\\s*""")
    return {
        'title': title,
        'time_limit': {
            'java': time_limit[0],
            'other': time_limit[1]
        },
        'memory_limit': {
            'java': memory_limit[0],
            'other': memory_limit[1]
        },
        'description': to_md(c_description),
        'input': to_md(c_input),
        'output': to_md(c_output),
        'sample_input': to_md(c_sample_input),
        'sample_output': to_md(c_sample_output),
        'author': to_md(c_author),
        'source': to_md(c_source)
    }


def get_problem_instance(pid):
    def build_description(description, inputs, outputs):
        return '## Description\n%s\n## Input\n%s\n## Output\n%s' % (description, inputs, outputs)

    def build_sample(s_input, s_output):
        return "## Sample Input\n%s\n## Sample Output\n%s" % (s_input, s_output)

    def build_limit(java, other):
        limits = {}
        for it in LANG_JAVA:
            limits[it] = java
        for it in LANG_OTHER:
            limits[it] = other
        return limits
    res = requests.get(get_url('instance'), params={'pid': pid})
    if res.status_code != 200:
        raise utils.VirtualException('Network Error at HDU: %s' % (res.status_code,))
    html = res.text
    try:
        item = get_problem_item(html)
    except Exception:
        raise utils.VirtualException('Regex Error.')
    return utils.VirtualProblem(
        oj='hdu', pid=pid, title=item['title'],
        introduction="Hdu problem %s" % (pid,),
        description=build_description(item['description'], item['input'], item['output']),
        sample=build_sample(item['sample_input'], item['sample_output']),
        author=item['author'],
        source=item['source'],
        time=build_limit(item['time_limit']['java'], item['time_limit']['other']),
        memory=build_limit(item['memory_limit']['java'], item['memory_limit']['other'])
    )


def request_problem_detail(pid):
    return get_problem_instance(pid)
