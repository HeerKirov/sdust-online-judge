from rest_framework_nested.routers import NestedSimpleRouter
from rest_framework.routers import DefaultRouter

from .views import MetaProblemViewSets, ProblemViewSets, CategoryViewSets, SubmissionViewSets
from .views import EnvironmentViewSets, UserViewSets
from .views import ClientViewSets


admin_router = DefaultRouter()
# == Meta Problem ======================================================================================================
admin_router.register(
    r'meta-problems', MetaProblemViewSets.MetaAdminViewSet, base_name='admin-meta-problems'
)
admin_meta_router = NestedSimpleRouter(admin_router, r'meta-problems', lookup='meta_problem')
# -- Components --------------------------------------------------------------------------------------------------------
admin_meta_router.register(
    r'descriptions', MetaProblemViewSets.Description.List.DescriptionAdminViewSet, base_name='admin-meta-descriptions'
)
admin_meta_router.register(
    r'descriptions',
    MetaProblemViewSets.Description.Instance.DescriptionAdminViewSet, base_name='admin-meta-descriptions'
)
admin_meta_router.register(
    r'samples', MetaProblemViewSets.Sample.List.SampleAdminViewSet, base_name='admin-meta-samples'
)
admin_meta_router.register(
    r'samples', MetaProblemViewSets.Sample.Instance.SampleAdminViewSet, base_name='admin-meta-samples'
)
admin_meta_router.register(
    r'test-data', MetaProblemViewSets.TestData.List.TestDataAdminViewSet, base_name='admin-meta-tests'
)
admin_meta_router.register(
    r'test-data', MetaProblemViewSets.TestData.Instance.TestDataAdminViewSet, base_name='admin-meta-tests'
)
admin_meta_router.register(
    r'problems', MetaProblemViewSets.Problem.List.ProblemAdminViewSet, base_name='admin-meta-problems-info'
)
admin_meta_router.register(
    r'problems', MetaProblemViewSets.Problem.Instance.ProblemAdminViewSet, base_name='admin-meta-problems-info'
)
meta_problem_router = NestedSimpleRouter(admin_meta_router, r'problems', lookup='problem')
meta_problem_router.register(
    r'description', MetaProblemViewSets.Problem.Description.DescriptionViewSet,
    base_name='admin-meta-problem-description'
)
meta_problem_router.register(
    r'sample', MetaProblemViewSets.Problem.Sample.SampleViewSet, base_name='admin-meta-problem-sample'
)
meta_problem_router.register(
    r'limits', MetaProblemViewSets.Problem.Limit.List.LimitAdminViewSet, base_name='admin-meta-problem-limits'
)
meta_problem_router.register(
    r'limits', MetaProblemViewSets.Problem.Limit.Instance.LimitAdminViewSet, base_name='admin-meta-problem-limits'
)
meta_problem_router.register(
    r'invalid-words', MetaProblemViewSets.Problem.InvalidWord.InvalidWordViewSet,
    base_name='admin-meta-problem-invalid-words'
)
meta_problem_router.register(
    r'test-data', MetaProblemViewSets.Problem.TestDataRelation.List.TestDataRelationAdminViewSet,
    base_name='admin-meta-problem-test-data'
)
meta_problem_router.register(
    r'test-data', MetaProblemViewSets.Problem.TestDataRelation.Instance.TestDataRelationAdminViewSet,
    base_name='admin-meta-problem-test-data'
)
meta_problem_router.register(
    r'special-judge', MetaProblemViewSets.Problem.SpecialJudge.List.SpecialJudgeAdminViewSet,
    base_name='admin-meta-problem-special-judge'
)
meta_problem_router.register(
    r'special-judge', MetaProblemViewSets.Problem.SpecialJudge.Instance.SpecialJudgeAdminViewSet,
    base_name='admin-meta-problem-special-judge'
)
# == Problem ===========================================================================================================
admin_router.register(
    r'problems', ProblemViewSets.List.ProblemAdminViewSet, base_name='admin-problems'
)
admin_router.register(
    r'problems', ProblemViewSets.Instance.ProblemAdminViewSet, base_name='admin-problems'
)
admin_router.register(
    r'problems-admin', ProblemViewSets.Admin.List.ProblemAdminViewSet, base_name='admin-problems-admin'
)
admin_router.register(
    r'problems-admin', ProblemViewSets.Admin.Instance.ProblemAdminViewSet, base_name='admin-problems-admin'
)
admin_router.register(
    r'virtual-problems', ProblemViewSets.Admin.List.VirtualProblemAdminViewSet, base_name='admin-virtual-problems'
)
admin_router.register(
    r'virtual-problems', ProblemViewSets.Admin.Instance.VirtualProblemAdminViewSet, base_name='admin-virtual-problems'
)
# == Environment =======================================================================================================
admin_router.register(
    r'environments', EnvironmentViewSets.EnvironmentAdminViewSet, base_name='admin-environments'
)
admin_router.register(
    r'judges', EnvironmentViewSets.JudgeAdminViewSet, base_name='admin-judges'
)
# == Submission ========================================================================================================
admin_router.register(
    r'submissions', SubmissionViewSets.List.SubmissionAdminViewSet, base_name='admin-submissions'
)
admin_router.register(
    r'submissions', SubmissionViewSets.Instance.SubmissionAdminViewSet, base_name='admin-submissions'
)
submission_router = NestedSimpleRouter(admin_router, r'submissions', lookup='submission')
# -- Components --------------------------------------------------------------------------------------------------------
submission_router.register(
    r'compile-info', SubmissionViewSets.CompileInfo.CompileInfoAdminViewSet, base_name='compile-info'
)
submission_router.register(
    r'status', SubmissionViewSets.TestDataStatus.TestDataStatusAdminViewSet, base_name='status'
)
submission_router.register(
    r'code', SubmissionViewSets.SubmissionCode.SubmissionCodeAdminViewSet, base_name='code'
)
# == Category ==========================================================================================================
admin_router.register(
    r'categories', CategoryViewSets.CategoryAdminViewSet, base_name='admin-categories'
)
admin_cat_router = NestedSimpleRouter(admin_router, r'categories', lookup='category')
# -- Components --------------------------------------------------------------------------------------------------------
admin_cat_router.register(
    r'problem-relations', CategoryViewSets.ProblemAdminViewSet, base_name='admin-category-problems'
)
# == Clients ===========================================================================================================
admin_router.register(
    r'client-users', ClientViewSets.UserAdminViewSet, base_name='admin-client-users'
)
admin_router.register(
    r'clients', ClientViewSets.ClientAdminViewSet, base_name='admin-clients'
)
client_router = NestedSimpleRouter(admin_router, r'clients', lookup='client')
# -- Components --------------------------------------------------------------------------------------------------------
client_router.register(
    r'category-relations', ClientViewSets.ClientCategoryViewSet, base_name='admin-clients-categories'
)
# == User ==============================================================================================================
admin_router.register(
    r'users', UserViewSets.UserAdminViewSet, base_name='admin-users'
)


router = DefaultRouter()

# == Submission ========================================================================================================
router.register(
    r'submissions', SubmissionViewSets.List.SubmissionViewSet, base_name='api-submissions'
)
router.register(
    r'submissions', SubmissionViewSets.Instance.SubmissionViewSet, base_name='api-submissions'
)
# == Problem ===========================================================================================================
router.register(
    r'problems', ProblemViewSets.List.ProblemViewSet, base_name='api-problems'
)
router.register(
    r'problems', ProblemViewSets.Instance.ProblemViewSet, base_name='api-problems'
)
# == Category ==========================================================================================================
router.register(
    r'categories', CategoryViewSets.CategoryViewSet, base_name='api-categories'
)
cat_router = NestedSimpleRouter(router, r'categories', lookup='category')
cat_router.register(r'problem-relations', CategoryViewSets.ProblemViewSet, base_name='problem-relations')
# == Environment =======================================================================================================
router.register(
    r'environments', EnvironmentViewSets.EnvironmentViewSet, base_name='api-environments'
)
# == User ==============================================================================================================
router.register(
    r'login', UserViewSets.LoginViewSet, base_name='login'
)
router.register(
    r'logout', UserViewSets.LogoutViewSet, base_name='logout'
)
router.register(
    r'user-info', UserViewSets.UserInfoViewSet, base_name='user-info'
)
router.register(
    r'user-password', UserViewSets.UserPasswordViewSet, base_name='user-password'
)

admin_url_patterns = []
admin_url_patterns += admin_router.urls
admin_url_patterns += admin_meta_router.urls + meta_problem_router.urls
admin_url_patterns += submission_router.urls
admin_url_patterns += admin_cat_router.urls
admin_url_patterns += client_router.urls

url_patterns = router.urls
url_patterns += cat_router.urls
