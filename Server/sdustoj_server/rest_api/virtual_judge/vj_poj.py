import requests
import re
import html2text
from . import utils


SETTING = {
    'host': 'http://poj.org/',
    'login': 'login',
    'submit': 'submit',
    'submissions': 'status',
    'problem': 'problem'
}

# POJ中，double的语言的限制翻倍。
LANG_STANDARD = ['C', 'C++', 'GCC', 'G++', 'Pascal', 'Fortran']
LANG_DOUBLE = ['Java']


def get_url(url, *args):
    return SETTING['host'] + SETTING[url] % args


def get_problem(text):
    def get_regex(string, regex):
        reg_content = re.findall(regex, string)
        if reg_content is not None and len(reg_content) > 0:
            return reg_content[0]
        else:
            return None

    def to_md(string):
        if string is None:
            return None
        md = html2text.html2text(string).strip('\n')
        return md

    def html_correct(string):
        """
        修正原页面的字符串错误与html错误，防止md转换出问题。
        :param string: 
        :return: 
        """
        t = re.sub('\r([^\n])', '\r\n\\1', string)

        rep_link = """<a href="([\\s\\S]*?)"[^>]*>"""
        rep_link_g = """<a href='%s\\1'>""" % (SETTING['host'],)
        rep_img = """<img([^>]*)src="([\\s\\S]*?)">"""
        rep_img_g = """<img\\1src=%s\\2>""" % (SETTING['host'],)
        t = re.sub(rep_link, rep_link_g, t)
        t = re.sub(rep_img, rep_img_g, t)

        # 用于去除br的
        # pre = re.search('([\\s\\S]*<pre[^>]*>)([\\s\\S]*)(</pre>[\\s\\S]*)', t)
        # while pre is not None:
        #     prev_content, content, next_content = pre.groups()
        #     content = re.sub('<br>', '', content)
        #     t = prev_content + content + next_content
        #     pre = re.search('([.\n]*)<pre[^>]*>([.\n]*)</pre>([.\n]*)', next_content)

        return t

    text = html_correct(text)

    title = get_regex(text, '<div class="ptt" lang="en-US">([\\s\\S]*?)</div>')
    time_limit, memory_limit = get_regex(text, '<tr><td><b>Time Limit:</b> (\\d*)MS</td><td width="10px"></td>' +
                                         '<td><b>Memory Limit:</b> (\\d*)K</td></tr>')
    description = get_regex(
        text, '<p class="pst">Description</p><div class="ptx" lang="en-US">([\\s\\S\\n]*?)</div>')
    c_input = get_regex(
        text, '<p class="pst">Input</p><div class="ptx" lang="en-US">([\\s\\S\\n]*?)</div>')
    c_output = get_regex(
        text, '<p class="pst">Output</p><div class="ptx" lang="en-US">([\\s\\S\\n]*?)</div>')
    sample_input = get_regex(
        text, '<p class="pst">Sample Input</p>(<pre class="sio">[\\s\\S\\n]*?</pre>)')
    sample_output = get_regex(
        text, '<p class="pst">Sample Output</p>(<pre class="sio">[\\s\\S\\n]*?</pre>)')
    hint = get_regex(
        text, '<p class="pst">Hint</p><div class="ptx" lang="en-US">([\\s\\S]*?)</div>')
    source = get_regex(
        text, '<p class="pst">Source</p><div class="ptx" lang="en-US">([\\s\\S\\n]*?)</div>')
    return {
        'title': title,
        'time_limit': time_limit,
        'memory_limit': memory_limit,
        'description': to_md(description),
        'input': to_md(c_input),
        'output': to_md(c_output),
        'sample_input': to_md(sample_input),
        'sample_output': to_md(sample_output),
        'hint': to_md(hint),
        'source': to_md(source),
        'author': None
    }


def get_problem_instance(pid):
    def build_description(description, inputs, outputs):
        return '## Description\n%s\n## Input\n%s\n## Output\n%s' % (description, inputs, outputs)

    def build_sample(s_input, s_output):
        return "## Sample Input\n%s\n## Sample Output\n%s" % (s_input, s_output)

    def build_limit(standard):
        limits = {}
        for it in LANG_DOUBLE:
            limits[it] = str(int(standard) * 2)
        for it in LANG_STANDARD:
            limits[it] = standard
        return limits
    data = {'id': pid}
    res = requests.get(get_url('problem'), params=data)
    if res.status_code != 200:
        return None
    try:
        item = get_problem(res.text)
    except Exception:
        raise utils.VirtualException('Request Error.')
    return utils.VirtualProblem(
        oj='poj', pid=pid, title=item['title'],
        introduction="Poj Problem %s" % (pid,),
        description=build_description(item['description'], item['input'], item['output']),
        sample=build_sample(item['sample_input'], item['sample_output']),
        author=item['author'],
        source=item['source'],
        time=build_limit(item['time_limit']),
        memory=build_limit(item['memory_limit'])
    )


def request_problem_detail(pid):
    return get_problem_instance(pid)
