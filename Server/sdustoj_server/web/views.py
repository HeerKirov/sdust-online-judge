from django.shortcuts import render, redirect, reverse, get_object_or_404
from rest_api.permissions import GROUP_NAME_ROOT, GROUP_NAME_USER_ADMIN, GROUP_NAME_CLIENT
from rest_api.permissions import GROUP_NAME_PROBLEM_ADMIN, GROUP_NAME_CATEGORY_ADMIN
from rest_api.permissions import GROUP_NAME_JUDGE_ADMIN, GROUP_NAME_CLIENT_ADMIN

from rest_api.models import *
from django.contrib.auth.models import Group

from config import OJ_SETTINGS, OJ_STATUS_SCORE

MAX_INPUT_SIZE = OJ_SETTINGS['test_data_input_max_size']


# == Utils =============================================================================================================

def user_info(request):
    user = request.user
    if user.is_authenticated():
        group = set()
        for it in user.groups.all().values('name'):
            group.add(it['name'])
        info = {
            'is_authenticated': True,
            'user': user,
            'group': group
        }
    else:
        info = {
            'is_authenticated': False,
        }
    return info


def has_problem_access(info):
    group = info['group']
    return GROUP_NAME_ROOT in group or GROUP_NAME_PROBLEM_ADMIN in group or GROUP_NAME_CATEGORY_ADMIN in group


def has_submission_access(info):
    group = info['group']

    return has_problem_access(info) or GROUP_NAME_JUDGE_ADMIN in group or GROUP_NAME_CLIENT_ADMIN in group


def is_problem_admin(info):
    group = info['group']
    return GROUP_NAME_ROOT in group or GROUP_NAME_PROBLEM_ADMIN in group


def is_category_admin(info):
    return has_problem_access(info)


def is_client_admin(info):
    group = info['group']
    return GROUP_NAME_ROOT in group or GROUP_NAME_CLIENT_ADMIN in group


def is_user_admin(info):
    group = info['group']
    return GROUP_NAME_USER_ADMIN in group or GROUP_NAME_ROOT in group


def is_judge_admin(info):
    group = info['group']
    return GROUP_NAME_JUDGE_ADMIN in group or GROUP_NAME_ROOT in group


# == Views =============================================================================================================

def to_home(request):
    return redirect(reverse('homepage'))


def homepage(request):
    info = user_info(request)

    return render(request, 'homepage.html', {
        'user': info
    })


def personal_info(request):
    info = user_info(request)

    if not info['is_authenticated']:
        return redirect(reverse('login_page'))

    return render(request, 'personal/info.html', {
        'user': info
    })


def personal_edit(request):
    info = user_info(request)

    if not info['is_authenticated']:
        return redirect(reverse('login_page'))

    return render(request, 'personal/edit.html', {
        'user': info
    })


def personal_password(request):
    info = user_info(request)

    if not info['is_authenticated']:
        return redirect(reverse('login_page'))

    return render(request, 'personal/password.html', {
        'user': info
    })


def problem_home(request):
    info = user_info(request)

    if not info['is_authenticated']:
        return redirect(reverse('login_page'))

    if not has_problem_access(info):
        return redirect(reverse('homepage'))

    return render(request, 'problem/home.html', {
        'user': info
    })


def problem_meta(request):
    info = user_info(request)

    if not info['is_authenticated']:
        return redirect(reverse('login_page'))

    if not is_problem_admin(info):
        return redirect(reverse('homepage'))

    return render(request, 'problem/metaProblem/list0.html', {
        'user': info
    })


def problem_meta_create(request):
    info = user_info(request)

    if not info['is_authenticated']:
        return redirect(reverse('login_page'))

    if not is_problem_admin(info):
        return redirect(reverse('homepage'))

    return render(request, 'problem/metaProblem/create.html', {
        'user': info
    })


def problem_meta_instance(request, mid):
    info = user_info(request)

    if not info['is_authenticated']:
        return redirect(reverse('login_page'))

    if not is_problem_admin(info):
        return redirect(reverse('homepage'))

    meta_problem = get_object_or_404(MetaProblem.objects, id=int(mid))

    return render(request, 'problem/metaProblem/instance.html', {
        'user': info,
        'meta_problem': meta_problem
    })


def problem_meta_description(request, mid):
    info = user_info(request)

    if not info['is_authenticated']:
        return redirect(reverse('login_page'))

    if not is_problem_admin(info):
        return redirect(reverse('homepage'))

    meta_problem = get_object_or_404(MetaProblem.objects, id=int(mid))

    return render(request, 'problem/metaProblem/description/list0.html', {
        'user': info,
        'meta_problem': meta_problem
    })


def problem_meta_description_create(request, mid):
    info = user_info(request)

    if not info['is_authenticated']:
        return redirect(reverse('login_page'))

    if not is_problem_admin(info):
        return redirect(reverse('homepage'))

    meta_problem = get_object_or_404(MetaProblem.objects, id=int(mid))

    return render(request, 'problem/metaProblem/description/create.html', {
        'user': info,
        'meta_problem': meta_problem
    })


def problem_meta_description_instance(request, mid, did):
    info = user_info(request)

    if not info['is_authenticated']:
        return redirect(reverse('login_page'))

    if not is_problem_admin(info):
        return redirect(reverse('homepage'))

    meta_problem = get_object_or_404(MetaProblem.objects, id=int(mid))
    description = get_object_or_404(Description.objects, id=int(did))

    return render(request, 'problem/metaProblem/description/instance.html', {
        'user': info,
        'meta_problem': meta_problem,
        'description': description
    })


def problem_meta_sample(request, mid):
    info = user_info(request)

    if not info['is_authenticated']:
        return redirect(reverse('login_page'))

    if not is_problem_admin(info):
        return redirect(reverse('homepage'))

    meta_problem = get_object_or_404(MetaProblem.objects, id=int(mid))

    return render(request, 'problem/metaProblem/sample/list0.html', {
        'user': info,
        'meta_problem': meta_problem
    })


def problem_meta_sample_create(request, mid):
    info = user_info(request)

    if not info['is_authenticated']:
        return redirect(reverse('login_page'))

    if not is_problem_admin(info):
        return redirect(reverse('homepage'))

    meta_problem = get_object_or_404(MetaProblem.objects, id=int(mid))

    return render(request, 'problem/metaProblem/sample/create.html', {
        'user': info,
        'meta_problem': meta_problem
    })


def problem_meta_sample_instance(request, mid, sid):
    info = user_info(request)

    if not info['is_authenticated']:
        return redirect(reverse('login_page'))

    if not is_problem_admin(info):
        return redirect(reverse('homepage'))

    meta_problem = get_object_or_404(MetaProblem.objects, id=int(mid))
    sample = get_object_or_404(Sample.objects, id=int(sid))

    return render(request, 'problem/metaProblem/sample/instance.html', {
        'user': info,
        'meta_problem': meta_problem,
        'sample': sample
    })


def problem_meta_test(request, mid):
    info = user_info(request)

    if not info['is_authenticated']:
        return redirect(reverse('login_page'))

    if not is_problem_admin(info):
        return redirect(reverse('homepage'))

    meta_problem = get_object_or_404(MetaProblem.objects, id=int(mid))

    return render(request, 'problem/metaProblem/testData/list0.html', {
        'user': info,
        'meta_problem': meta_problem
    })


def problem_meta_test_create(request, mid):
    info = user_info(request)

    if not info['is_authenticated']:
        return redirect(reverse('login_page'))

    if not is_problem_admin(info):
        return redirect(reverse('homepage'))

    meta_problem = get_object_or_404(MetaProblem.objects, id=int(mid))

    return render(request, 'problem/metaProblem/testData/create.html', {
        'user': info,
        'meta_problem': meta_problem
    })


def problem_meta_test_instance(request, mid, tid):
    info = user_info(request)

    if not info['is_authenticated']:
        return redirect(reverse('login_page'))

    if not is_problem_admin(info):
        return redirect(reverse('homepage'))

    meta_problem = get_object_or_404(MetaProblem.objects, id=int(mid))
    test_data = get_object_or_404(TestData.objects, id=int(tid))

    return render(request, 'problem/metaProblem/testData/instance.html', {
        'user': info,
        'meta_problem': meta_problem,
        'test': test_data,
        'max_input': MAX_INPUT_SIZE
    })


def problem_meta_problem(request, mid):
    info = user_info(request)

    if not info['is_authenticated']:
        return redirect(reverse('login_page'))

    if not is_problem_admin(info):
        return redirect(reverse('homepage'))

    meta_problem = get_object_or_404(MetaProblem.objects, id=int(mid))

    return render(request, 'problem/metaProblem/problem/list0.html', {
        'user': info,
        'meta_problem': meta_problem
    })


def problem_meta_problem_create(request, mid):
    info = user_info(request)

    if not info['is_authenticated']:
        return redirect(reverse('login_page'))

    if not is_problem_admin(info):
        return redirect(reverse('homepage'))

    meta_problem = get_object_or_404(MetaProblem.objects, id=int(mid))

    return render(request, 'problem/metaProblem/problem/create.html', {
        'user': info,
        'meta_problem': meta_problem
    })


def problem_meta_problem_instance(request, mid, pid):
    info = user_info(request)

    if not info['is_authenticated']:
        return redirect(reverse('login_page'))

    if not is_problem_admin(info):
        return redirect(reverse('homepage'))

    meta_problem = get_object_or_404(MetaProblem.objects, id=int(mid))
    prob = get_object_or_404(Problem.objects, id=int(pid))

    return render(request, 'problem/metaProblem/problem/instance.html', {
        'user': info,
        'meta_problem': meta_problem,
        'problem': prob
    })


def problem_meta_problem_limits(request, mid, pid):
    info = user_info(request)

    if not info['is_authenticated']:
        return redirect(reverse('login_page'))

    if not is_problem_admin(info):
        return redirect(reverse('homepage'))

    meta_problem = get_object_or_404(MetaProblem.objects, id=int(mid))
    prob = get_object_or_404(Problem.objects, id=int(pid))

    return render(request, 'problem/metaProblem/problem/limit/list0.html', {
        'user': info,
        'meta_problem': meta_problem,
        'problem': prob
    })


def problem_meta_problem_limits_create(request, mid, pid):
    info = user_info(request)

    if not info['is_authenticated']:
        return redirect(reverse('login_page'))

    if not is_problem_admin(info):
        return redirect(reverse('homepage'))

    meta_problem = get_object_or_404(MetaProblem.objects, id=int(mid))
    prob = get_object_or_404(Problem.objects, id=int(pid))

    return render(request, 'problem/metaProblem/problem/limit/create.html', {
        'user': info,
        'meta_problem': meta_problem,
        'problem': prob
    })


def problem_meta_problem_limits_instance(request, mid, pid, lid):
    info = user_info(request)

    if not info['is_authenticated']:
        return redirect(reverse('login_page'))

    if not is_problem_admin(info):
        return redirect(reverse('homepage'))

    meta_problem = get_object_or_404(MetaProblem.objects, id=int(mid))
    prob = get_object_or_404(Problem.objects, id=int(pid))
    limit = get_object_or_404(Limit.objects, id=int(lid))

    return render(request, 'problem/metaProblem/problem/limit/instance.html', {
        'user': info,
        'meta_problem': meta_problem,
        'problem': prob,
        'limit': limit
    })


def problem_meta_problem_spj(request, mid, pid):
    info = user_info(request)

    if not info['is_authenticated']:
        return redirect(reverse('login_page'))

    if not is_problem_admin(info):
        return redirect(reverse('homepage'))

    meta_problem = get_object_or_404(MetaProblem.objects, id=int(mid))
    prob = get_object_or_404(Problem.objects, id=int(pid))

    return render(request, 'problem/metaProblem/problem/specialJudge/list0.html', {
        'user': info,
        'meta_problem': meta_problem,
        'problem': prob
    })


def problem_meta_problem_spj_create(request, mid, pid):
    info = user_info(request)

    if not info['is_authenticated']:
        return redirect(reverse('login_page'))

    if not is_problem_admin(info):
        return redirect(reverse('homepage'))

    meta_problem = get_object_or_404(MetaProblem.objects, id=int(mid))
    prob = get_object_or_404(Problem.objects, id=int(pid))

    return render(request, 'problem/metaProblem/problem/specialJudge/create.html', {
        'user': info,
        'meta_problem': meta_problem,
        'problem': prob
    })


def problem_meta_problem_spj_instance(request, mid, pid, sid):
    info = user_info(request)

    if not info['is_authenticated']:
        return redirect(reverse('login_page'))

    if not is_problem_admin(info):
        return redirect(reverse('homepage'))

    meta_problem = get_object_or_404(MetaProblem.objects, id=int(mid))
    prob = get_object_or_404(Problem.objects, id=int(pid))
    spj = get_object_or_404(SpecialJudge.objects, id=int(sid))

    return render(request, 'problem/metaProblem/problem/specialJudge/instance.html', {
        'user': info,
        'meta_problem': meta_problem,
        'problem': prob,
        'spj': spj
    })


def problem_meta_problem_iw(request, mid, pid):
    info = user_info(request)

    if not info['is_authenticated']:
        return redirect(reverse('login_page'))

    if not is_problem_admin(info):
        return redirect(reverse('homepage'))

    meta_problem = get_object_or_404(MetaProblem.objects, id=int(mid))
    prob = get_object_or_404(Problem.objects, id=int(pid))

    return render(request, 'problem/metaProblem/problem/invalidWord/list0.html', {
        'user': info,
        'meta_problem': meta_problem,
        'problem': prob
    })


def problem_meta_problem_iw_create(request, mid, pid):
    info = user_info(request)

    if not info['is_authenticated']:
        return redirect(reverse('login_page'))

    if not is_problem_admin(info):
        return redirect(reverse('homepage'))

    meta_problem = get_object_or_404(MetaProblem.objects, id=int(mid))
    prob = get_object_or_404(Problem.objects, id=int(pid))

    return render(request, 'problem/metaProblem/problem/invalidWord/create.html', {
        'user': info,
        'meta_problem': meta_problem,
        'problem': prob
    })


def problem_meta_problem_iw_instance(request, mid, pid, iw_id):
    info = user_info(request)

    if not info['is_authenticated']:
        return redirect(reverse('login_page'))

    if not is_problem_admin(info):
        return redirect(reverse('homepage'))

    meta_problem = get_object_or_404(MetaProblem.objects, id=int(mid))
    prob = get_object_or_404(Problem.objects, id=int(pid))
    iw = get_object_or_404(InvalidWord.objects, id=int(iw_id))

    return render(request, 'problem/metaProblem/problem/invalidWord/instance.html', {
        'user': info,
        'meta_problem': meta_problem,
        'problem': prob,
        'iw': iw
    })


def problem_meta_problem_test(request, mid, pid):
    info = user_info(request)

    if not info['is_authenticated']:
        return redirect(reverse('login_page'))

    if not is_problem_admin(info):
        return redirect(reverse('homepage'))

    meta_problem = get_object_or_404(MetaProblem.objects, id=int(mid))
    prob = get_object_or_404(Problem.objects, id=int(pid))

    return render(request, 'problem/metaProblem/problem/testDataRelation/list0.html', {
        'user': info,
        'meta_problem': meta_problem,
        'problem': prob
    })


def problem_meta_problem_test_create(request, mid, pid):
    info = user_info(request)

    if not info['is_authenticated']:
        return redirect(reverse('login_page'))

    if not is_problem_admin(info):
        return redirect(reverse('homepage'))

    meta_problem = get_object_or_404(MetaProblem.objects, id=int(mid))
    prob = get_object_or_404(Problem.objects, id=int(pid))

    return render(request, 'problem/metaProblem/problem/testDataRelation/create.html', {
        'user': info,
        'meta_problem': meta_problem,
        'problem': prob
    })


def problem_meta_problem_test_instance(request, mid, pid, tid):
    info = user_info(request)

    if not info['is_authenticated']:
        return redirect(reverse('login_page'))

    if not is_problem_admin(info):
        return redirect(reverse('homepage'))

    meta_problem = get_object_or_404(MetaProblem.objects, id=int(mid))
    prob = get_object_or_404(Problem.objects, id=int(pid))
    test = get_object_or_404(ProblemTestData.objects, id=int(tid))

    return render(request, 'problem/metaProblem/problem/testDataRelation/instance.html', {
        'user': info,
        'meta_problem': meta_problem,
        'problem': prob,
        'test': test
    })


def problem(request):
    info = user_info(request)

    if not info['is_authenticated']:
        return redirect(reverse('login_page'))

    if not is_category_admin(info):
        return redirect(reverse('homepage'))

    return render(request, 'problem/problem/list0.html', {
        'user': info
    })


def problem_create(request):
    info = user_info(request)

    if not info['is_authenticated']:
        return redirect(reverse('login_page'))

    if not is_problem_admin(info):
        return redirect(reverse('homepage'))

    envs = Environment.objects.filter(available=True, deleted=False)

    return render(request, 'problem/problem/create.html', {
        'user': info,
        'envs': envs
    })


def problem_instance(request, pid):
    info = user_info(request)

    if not info['is_authenticated']:
        return redirect(reverse('login_page'))

    if not is_category_admin(info):
        return redirect(reverse('homepage'))

    prob = get_object_or_404(Problem.objects, id=int(pid))

    return render(request, 'problem/problem/instance.html', {
        'user': info,
        'pid': pid,
        'problem': prob
    })


def problem_category(request):
    info = user_info(request)

    if not info['is_authenticated']:
        return redirect(reverse('login_page'))

    if not has_submission_access(info):
        return redirect(reverse('homepage'))

    return render(request, 'problem/category/list0.html', {
        'user': info
    })


def problem_category_create(request):
    info = user_info(request)

    if not info['is_authenticated']:
        return redirect(reverse('login_page'))

    if not has_submission_access(info):
        return redirect(reverse('homepage'))

    return render(request, 'problem/category/create.html', {
        'user': info
    })


def problem_category_instance(request, cid):
    info = user_info(request)

    if not info['is_authenticated']:
        return redirect(reverse('login_page'))

    if not is_category_admin(info):
        return redirect(reverse('homepage'))

    category = get_object_or_404(Category.objects, id=int(cid))

    return render(request, 'problem/category/instance.html', {
        'user': info,
        'cat': category
    })


def problem_category_dir(request, cid):
    info = user_info(request)

    if not info['is_authenticated']:
        return redirect(reverse('login_page'))

    if not is_category_admin(info):
        return redirect(reverse('homepage'))

    category = get_object_or_404(Category.objects, id=int(cid))

    return render(request, 'problem/category/directory/tree.html', {
        'user': info,
        'cat': category
    })


def problem_submissions(request):
    info = user_info(request)

    if not info['is_authenticated']:
        return redirect(reverse('login_page'))

    if not is_category_admin(info):
        return redirect(reverse('homepage'))

    return render(request, 'submission/list0.html', {
        'user': info
    })


def problem_submission_info(request, sid):
    info = user_info(request)

    if not info['is_authenticated']:
        return redirect(reverse('login_page'))

    if not is_category_admin(info):
        return redirect(reverse('homepage'))

    submission = get_object_or_404(Submission.objects, id=int(sid))

    return render(request, 'submission/instance.html', {
        'user': info,
        'submission': submission,
        'OJ_STATUS_SCORE': OJ_STATUS_SCORE
    })


def client_clients(request):
    info = user_info(request)

    if not info['is_authenticated']:
        return redirect(reverse('login_page'))

    if not is_client_admin(info):
        return redirect(reverse('homepage'))

    return render(request, 'client/client/list0.html', {
        'user': info,
    })


def client_create(request):
    info = user_info(request)

    if not info['is_authenticated']:
        return redirect(reverse('login_page'))

    if not is_client_admin(info):
        return redirect(reverse('homepage'))

    return render(request, 'client/client/create.html', {
        'user': info,
    })


def client_instance(request, cid):
    info = user_info(request)

    if not info['is_authenticated']:
        return redirect(reverse('login_page'))

    if not is_client_admin(info):
        return redirect(reverse('homepage'))

    client = get_object_or_404(Client.objects, id=int(cid))

    return render(request, 'client/client/instance.html', {
        'user': info,
        'client': client
    })


def client_categories(request, cid):
    info = user_info(request)

    if not info['is_authenticated']:
        return redirect(reverse('login_page'))

    if not is_client_admin(info):
        return redirect(reverse('homepage'))

    client = get_object_or_404(Client.objects, id=int(cid))

    return render(request, 'client/client/categoryRelation/list0.html', {
        'user': info,
        'client': client
    })


def client_categories_create(request, cid):
    info = user_info(request)

    if not info['is_authenticated']:
        return redirect(reverse('login_page'))

    if not is_client_admin(info):
        return redirect(reverse('homepage'))

    client = get_object_or_404(Client.objects, id=int(cid))

    return render(request, 'client/client/categoryRelation/create.html', {
        'user': info,
        'client': client
    })


def client_category_instance(request, cid, rid):
    info = user_info(request)

    if not info['is_authenticated']:
        return redirect(reverse('login_page'))

    if not is_client_admin(info):
        return redirect(reverse('homepage'))

    client = get_object_or_404(Client.objects, id=int(cid))
    relation = get_object_or_404(ClientCategory.objects, id=int(rid))

    return render(request, 'client/client/categoryRelation/instance.html', {
        'user': info,
        'client': client,
        'relation': relation
    })


def client_users(request):
    info = user_info(request)

    if not info['is_authenticated']:
        return redirect(reverse('login_page'))

    if not is_client_admin(info):
        return redirect(reverse('homepage'))

    return render(request, 'client/user/list0.html', {
        'user': info,
    })


def client_user_create(request):
    info = user_info(request)

    if not info['is_authenticated']:
        return redirect(reverse('login_page'))

    if not is_client_admin(info):
        return redirect(reverse('homepage'))

    return render(request, 'client/user/create.html', {
        'user': info,
    })


def client_user_instance(request, username):
    info = user_info(request)

    if not info['is_authenticated']:
        return redirect(reverse('login_page'))

    if not is_client_admin(info):
        return redirect(reverse('homepage'))

    client_user = get_object_or_404(User.objects.filter(groups__name=GROUP_NAME_CLIENT), username=username)

    return render(request, 'client/user/instance.html', {
        'user': info,
        'clientUser': client_user
    })


def users(request):
    info = user_info(request)

    if not info['is_authenticated']:
        return redirect(reverse('login_page'))

    if not is_user_admin(info):
        return redirect(reverse('homepage'))

    return render(request, 'user/list0.html', {
        'user': info
    })


def user_create(request):
    info = user_info(request)

    if not info['is_authenticated']:
        return redirect(reverse('login_page'))

    if not is_user_admin(info):
        return redirect(reverse('homepage'))

    groups = Group.objects.exclude(name=GROUP_NAME_CLIENT)

    return render(request, 'user/create.html', {
        'user': info,
        'groups': groups
    })


def user_instance(request, username):
    info = user_info(request)

    if not info['is_authenticated']:
        return redirect(reverse('login_page'))

    if not is_user_admin(info):
        return redirect(reverse('homepage'))

    groups = Group.objects.exclude(name=GROUP_NAME_CLIENT)
    u_info = get_object_or_404(User.objects.exclude(groups__name=GROUP_NAME_CLIENT), username=username)

    return render(request, 'user/instance.html', {
        'user': info,
        'groups': groups,
        'u_info': u_info
    })


def submit_problem(request, pid):
    info = user_info(request)

    if not info['is_authenticated']:
        return redirect(reverse('login_page'))

    if not has_problem_access(info):
        return redirect(reverse('homepage'))

    prob = get_object_or_404(Problem.objects.filter(available=True, deleted=False), id=int(pid))
    environments = Environment.objects.filter(available=True, deleted=False).order_by('id')

    return render(request, 'problem/problem/submit.html', {
        'user': info,
        'problem': prob,
        'envs': environments
    })


def environments(request):
    info = user_info(request)

    if not info['is_authenticated']:
        return redirect(reverse('login_page'))

    if not is_judge_admin(info):
        return redirect(reverse('homepage'))

    return render(request, 'judge/environment/list0.html', {
        'user': info
    })


def environment_create(request):
    info = user_info(request)

    if not info['is_authenticated']:
        return redirect(reverse('login_page'))

    if not is_judge_admin(info):
        return redirect(reverse('homepage'))

    return render(request, 'judge/environment/create.html', {
        'user': info
    })


def environment_instance(request, eid):
    info = user_info(request)

    if not info['is_authenticated']:
        return redirect(reverse('login_page'))

    if not is_judge_admin(info):
        return redirect(reverse('homepage'))

    env = get_object_or_404(Environment.objects.all(), id=int(eid))

    return render(request, 'judge/environment/instance.html', {
        'user': info,
        'env': env
    })


def judges(request):
    info = user_info(request)

    if not info['is_authenticated']:
        return redirect(reverse('login_page'))

    if not is_judge_admin(info):
        return redirect(reverse('homepage'))

    return render(request, 'judge/judge/list0.html', {
        'user': info
    })


def judge_create(request):
    info = user_info(request)

    if not info['is_authenticated']:
        return redirect(reverse('login_page'))

    if not is_judge_admin(info):
        return redirect(reverse('homepage'))

    return render(request, 'judge/judge/create.html', {
        'user': info
    })


def judge_instance(request, jid):
    info = user_info(request)

    if not info['is_authenticated']:
        return redirect(reverse('login_page'))

    if not is_judge_admin(info):
        return redirect(reverse('homepage'))

    judge = get_object_or_404(Judge.objects.all(), id=int(jid))

    return render(request, 'judge/judge/instance.html', {
        'user': info,
        'jid': jid,
        'judge': judge
    })


def login(request):
    if request.user.is_authenticated():
        return redirect(reverse('homepage'))
    return render(request, 'personal/login.html')
