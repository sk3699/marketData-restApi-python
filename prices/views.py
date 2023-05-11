import calendar
import traceback
from django.db import IntegrityError
from json import JSONDecodeError
from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from .serializers import MarketDataSerializer
from prices.models import MarketData
from rest_framework import status
from rest_framework.decorators import api_view
import numpy as np
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta

'''This class holds the viewsets which will handle the API requests'''
class PricesAndMarketAPIView:

    # function handling the API requests
    @api_view(['GET', 'POST', 'DELETE'])
    def markets(request):
        if request.method == 'GET':
            try:
                markets = MarketData.objects.all()
                serialized_data = MarketDataSerializer(markets, many=True)
                # print(f'Serialized Data in GET: {serialized_data.data}')
                return JsonResponse({'Markets': serialized_data.data}, status=status.HTTP_200_OK)
            except ValueError as e:
                return JsonResponse({'Error': str(e)}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
            except Exception as e:
                return JsonResponse({'Error Parsing Data': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        elif request.method == 'POST':
            try:
                markets = JSONParser().parse(request)
                serialized_data = MarketDataSerializer(data=markets, many=True)
                if serialized_data.is_valid(raise_exception=True):
                    print(f'Serialized Data in POST: {serialized_data.data}')
                    calculate_PV(serialized_data)
                    updated_serialized_data = MarketDataSerializer(data=serialized_data.data, many=True)
                    if updated_serialized_data.is_valid(raise_exception=True):
                        updated_serialized_data.save()
                        return JsonResponse({'New Markets': updated_serialized_data.data},
                                            status=status.HTTP_201_CREATED)
                else:
                    return JsonResponse(serialized_data.errors, status=status.HTTP_400_BAD_REQUEST)
            except JSONDecodeError as e:
                return JsonResponse({'Error': 'While parsing the JSON request... ' + str(e)},
                                    status=status.HTTP_400_BAD_REQUEST)
            except IntegrityError as e:
                return JsonResponse({'Error': str(e) + ' ### ' + traceback.format_exception_only(type(e), e)[-1]},
                                    status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return JsonResponse({'Error': str(e) + ' ### ' + traceback.format_exception_only(type(e), e)[-1]},
                                    status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
            try:
                MarketData.objects.all().delete()
                return JsonResponse({'Success': 'Deleted All the DB entries.'}, status=status.HTTP_204_NO_CONTENT)
            except Exception as e:
                return JsonResponse({'Error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    # @api_view(['GET', 'PUT', 'DELETE'])
    # def single_market(request, id):
    #     try:
    #         market = MarketData.objects.get(id=id)
    #     except MarketData.DoesNotExist:
    #         JsonResponse(status=status.HTTP_404_NOT_FOUND)
    #     if request.method == 'GET':
    #         serialized_data = MarketDataSerializer(market)
    #         return JsonResponse(serialized_data.data, status=status.HTTP_200_OK)
    #     elif request.method == 'PUT':
    #
    #     elif request.method == 'DELETE':


# returns the no of days difference between future date and expiry date
def no_of_days(year, month, formatted_date) -> int:
    last_day = calendar.monthrange(year, month)[1]
    last_date = date(year, month, last_day)
    while last_date.weekday() in (calendar.SATURDAY, calendar.SUNDAY):
        last_date -= timedelta(days=1)
    return (formatted_date.date() - last_date).days


# calculates PV for the new markets data received
def calculate_PV(serialized_data) -> JsonResponse:
    for data in serialized_data.data:
        try:
            month = data['delivery_month']
            formatted_date = datetime.strptime(month, '%b%y')
            # print(f'Expire Month for Call: {formatted_date}')
            if data['option'] == 'BRN':
                expiry_date = formatted_date - relativedelta(months=2)
                days = no_of_days(expiry_date.year, expiry_date.month, formatted_date)
                data['PV'] = data['price'] * np.exp(-0.01 * (days / 365))

            elif data['option'] == 'HH':
                expiry_date = formatted_date - relativedelta(months=1)
                days = no_of_days(expiry_date.year, expiry_date.month, formatted_date)
                data['PV'] = data['price'] * np.exp(-0.01 * (days / 365))

            else:
                return JsonResponse({'Invalid Req:': serialized_data.data},
                                    status=status.HTTP_400_BAD_REQUEST)
        except ValueError as e:
            return JsonResponse({'Error': str(e)},
                                status=status.HTTP_400_BAD_REQUEST)
