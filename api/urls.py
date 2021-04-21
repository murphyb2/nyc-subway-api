from django.urls import path
from .views import index, stations, AggregateView, WeeklyUpdateView, Monthly2021View, Monthly2020View, Monthly2019View, Yearly2021View, Yearly2020View, Yearly2019View
from rest_framework.routers import DefaultRouter

app_name = 'api'

router = DefaultRouter(trailing_slash=False)
urlpatterns = [
	path('', index, name="base"),
	path('stations', stations, name="stations"),
    path('year/2021', Yearly2021View.as_view()),
    path('year/2020', Yearly2020View.as_view()),
    path('year/2019', Yearly2019View.as_view()),
    path('month/2021', Monthly2021View.as_view()),
    path('month/2020', Monthly2020View.as_view()),
    path('month/2019', Monthly2019View.as_view()),
    path('totals', AggregateView.as_view()),
    path('update', WeeklyUpdateView.as_view()),
]
urlpatterns += router.urls
