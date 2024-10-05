from datetime import datetime, timedelta
from django.db import IntegrityError
from django.db.models import Sum
from django.utils.timezone import make_aware
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiResponse
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ExpenseTrackerAPI import settings
from api.models import Category, Expense
from api.serializers import CategorySerializer, ExpenseSerializer, SummarySerializer
from api.permissions import IsOwner
from api.validators import validate_date_range


# Create your views here.
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    @extend_schema(
        request=CategorySerializer,
        examples=[
            OpenApiExample(
                'Example Category Creation Request',
                value={
                    'name': 'Groceries'
                },
                request_only=True,
            ),
        ],
        responses={
            200: OpenApiResponse(
                response=CategorySerializer,
                examples=[
                    OpenApiExample(
                        'Example Category Creation Response',
                        value={
                            'id': 1,
                            'name': 'Groceries'
                        },
                    ),
                ]
            )
        }
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(
        responses={
            200: OpenApiResponse(
                description='A list of categories',
                response=OpenApiTypes.OBJECT,
                examples=[
                    OpenApiExample(
                        'Example Category List Response',
                        value=[
                            {'id': 1, 'name': 'Groceries'},
                            {'id': 2, 'name': 'Leisure'}
                        ],
                    ),
                ]
            )
        }
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


# Create your views here.
class ExpenseViewSet(viewsets.ModelViewSet):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated, IsOwner]


    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            # Pass the author to the save method
            serializer.save(owner=request.user)
        except IntegrityError:
            raise ValidationError({"detail": "Expense with this text already exists for the current user."})

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=False, url_path='summary')
    def summary(self, request):
        # Default end date to the global END_DATE from settings
        end_date = settings.END_DATE
        start_date = None

        # Get the 'range' query parameter
        date_range = request.query_params.get('range')

        # Determine the date range
        if date_range == 'week':
            start_date = end_date - timedelta(days=7)
        elif date_range == 'month':
            start_date = end_date - timedelta(days=30)
        elif date_range == '3_months':
            start_date = end_date - timedelta(days=90)
        elif date_range == 'custom':
            # Get custom start and end dates from query parameters
            start_date = request.query_params.get('start_date')
            end_date = request.query_params.get('end_date')
            if not start_date or not end_date:
                return Response({"error": "Custom range requires 'start_date' and 'end_date' parameters."}, status=400)
            try:
                start_date = datetime.strptime(start_date, '%Y-%m-%d')
                end_date = datetime.strptime(end_date, '%Y-%m-%d')
            except ValueError:
                return Response({"error": "Invalid date format. Use YYYY-MM-DD."}, status=400)

        # Default: Use a fixed start date from settings if no range is provided
        if not start_date:
            start_date = settings.START_DATE

        # Convert start_date and end_date to timezone-aware
        start_date = make_aware(start_date) if not start_date.tzinfo else start_date
        end_date = make_aware(end_date) if not end_date.tzinfo else end_date

        # Validate the date range
        try:
            validate_date_range(start_date, end_date)
        except ValidationError as e:
            return Response({"error": str(e)}, status=400)

        # Calculate expenses within the specified date range
        expenses = Expense.objects.filter(owner=request.user, created__gte=start_date, created__lte=end_date).aggregate(
            total_expenses=Sum('amount'))
        total_expenses = int(expenses['total_expenses']) if expenses['total_expenses'] else 0

        # Construct the data dictionary for the serializer
        data = {
            "total_expenses": total_expenses
        }

        serializer = SummarySerializer(data)
        return Response(serializer.data)