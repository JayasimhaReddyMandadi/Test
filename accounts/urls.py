from django.urls import path
from .views import (
    RegisterView, LoginView,ProfileView,ChangeEmailView,ChangePasswordView,DeleteAccountView,
    add_income, add_expense,
    dashboard_data, recent_transactions, get_user_info, get_all_riders, get_rider_by_email, verify_rider_email,
    get_personal_info, update_personal_info,
    login_page, register_page, dashboard_selection_page, daily_expense_dashboard_page,phonepay_gold_dashboard,mutualfund_dashboard,add_fund_api,funds_list_api,delete_fund_api,portfolio_summary_api,
    market_data_api,update_fund_api,profile_page,
)

urlpatterns = [
    # API routes
    path('api/register/', RegisterView.as_view(), name='api-register'),
    path('api/login/', LoginView.as_view(), name='api-login'),
    path('api/user-info/', get_user_info, name='api-user-info'),
    path('api/riders/all/', get_all_riders, name='api-all-riders'),
    path('api/riders/by-email/', get_rider_by_email, name='api-rider-by-email'),
    path('api/riders/verify/', verify_rider_email, name='api-verify-rider-email'),
    path('api/personal-info/', get_personal_info, name='api-get-personal-info'),
    path('api/personal-info/update/', update_personal_info, name='api-update-personal-info'),
    path('api/profile/', ProfileView.as_view(), name='api-profile'),
    path('api/income/add/', add_income, name='api-add-income'),
    path('api/expense/add/', add_expense, name='api-add-expense'),
    path('api/dashboard/', dashboard_data, name='api-dashboard'),
    path('api/transactions/recent/', recent_transactions, name='api-recent-transactions'),
     path('api/funds/add/', add_fund_api, name='api-add-fund'),
    path('api/funds/', funds_list_api, name='api-funds-list'),
    path('api/funds/update/<int:fund_id>/', update_fund_api, name='api-update-fund'),
    path('api/funds/delete/', delete_fund_api, name='api-delete-fund'),
     path('api/portfolio/summary/', portfolio_summary_api, name='api-portfolio-summary'),
     path('api/market-data/', market_data_api, name='api-market-data'),
     path('api/profile/change-email/', ChangeEmailView.as_view(), name='api-change-email'),
     path('api/profile/change-password/', ChangePasswordView.as_view(), name='api-change-password'),
     path('api/profile/delete-account/', DeleteAccountView.as_view(), name='api-delete-account'),

    # UI routes
    path('', login_page, name='login-page'),
    path('register/', register_page, name='register-page'),
    path('profile/', profile_page, name='profile-page'),
    path('dashboard/', dashboard_selection_page, name='dashboard-selection'),
    path('daily-expense-dashboard/', daily_expense_dashboard_page, name='daily-expense-dashboard'),
    path('phonepay-gold-dashboard/', phonepay_gold_dashboard, name='phonepay-gold-dashboard'),
    path('mutual_fund_dashboard/', mutualfund_dashboard, name='mutual_fund_dashboard'),
]
