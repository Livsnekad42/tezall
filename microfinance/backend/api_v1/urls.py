from django.urls import path


from .views import (
    is_live,
    ProfileInfoAPI,
    RefreshEmailFromAPI,
    RefreshPasswordFromAPI,
    PawnTicketListFromAPI,
    PawnTicketOperationsFromAPI,
    PawnTicketPropertyListAPI,
    PawnTicketPropertiesAPI,
    PawnTicketDocumentsAPI,
    PawnTicketCurrentOverdraftAPI,
    CreditListFromAPI,
    CreditOperationsFromAPI,
    CreditDocumentsAPI,
    CreditCurrentOverdraftAPI,
    ProlongationPawnTicketAPIView,
    LoanPayBackAPIView,
    CheckStatusAPIView,
)


urlpatterns = [
    path('profile/', ProfileInfoAPI.as_view(), name="profile"),
    path('reEmail/', RefreshEmailFromAPI.as_view(), name="reEmail"),
    path('rePswd/', RefreshPasswordFromAPI.as_view(), name="rePswd"),
    path('pawnTicketList/', PawnTicketListFromAPI.as_view(), name="pawnTicketList"),
    path('pawnTicketOperations/', PawnTicketOperationsFromAPI.as_view(), name="pawnTicketOperations"),
    path('pawnTicketPropertyList/', PawnTicketPropertyListAPI.as_view(), name="pawnTicketPropertyList"),
    path('pawnTicketProperties/', PawnTicketPropertiesAPI.as_view(), name="pawnTicketProperties"),
    path('pawnTicketDocumentsAPI/', PawnTicketDocumentsAPI.as_view(), name="pawnTicketDocumentsAPI"),
    path('pawnTicketCurrentOverdraftAPI/', PawnTicketCurrentOverdraftAPI.as_view(),
         name="pawnTicketCurrentOverdraftAPI"),
    path('creditListFromAPI/', CreditListFromAPI.as_view(), name="creditListFromAPI"),
    path('creditOperationsFromAPI/', CreditOperationsFromAPI.as_view(), name="creditOperationsFromAPI"),
    path('creditCurrentOverdraftAPI/', CreditCurrentOverdraftAPI.as_view(), name="creditCurrentOverdraftAPI"),
    path('creditDocumentsAPI/', CreditDocumentsAPI.as_view(), name="creditDocumentsAPI"),
    path('prolongationPawnTicketAPIView/', ProlongationPawnTicketAPIView.as_view(),
         name="prolongationPawnTicketAPIView"),
    path('loanPayBackAPIView/', LoanPayBackAPIView.as_view(), name="loanPayBackAPIView"),
    path('checkStatusAPIView/', CheckStatusAPIView.as_view(), name="checkStatusAPIView"),
    path('is_live/', is_live, name="is_live"),
]
