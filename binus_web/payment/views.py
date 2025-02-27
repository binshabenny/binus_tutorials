from django.shortcuts import render, get_object_or_404
from home.models import BookSeat  # Assuming you have BookSeat model for bookings
import razorpay
from django.shortcuts import render
from django.conf import settings
import logging
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
logger = logging.getLogger(__name__)

razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))


# Initialize Razorpay client
#razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
@csrf_exempt
def razorpay_webhook(request):
    try:
        data = json.loads(request.body)
        event = data.get("event")

        if event == "payment.captured":
            payment_id = data["payload"]["payment"]["entity"]["id"]
            order_id = data["payload"]["payment"]["entity"]["order_id"]

            # Find the corresponding booking
            booking = BookSeat.objects.filter(order_id=order_id).first()
            if booking:
                booking.status = True
                booking.payment_id = payment_id
                booking.save()
                return JsonResponse({"status": "success"}, status=200)
        
        return JsonResponse({"status": "ignored"}, status=400)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)

def payment_page(request, order_id, fee):
    # Retrieve the booking based on the order_id
    booking = get_object_or_404(BookSeat, order_id=order_id)

    # Pass the required Razorpay data and booking details to the template
    context = {
        'order_id': order_id,
        'fee': int(fee) * 100,  # Convert fee to paisa (Razorpay accepts amounts in paisa)
        'RAZORPAY_KEY_ID': settings.RAZORPAY_KEY_ID,  # Fetch Razorpay Key ID from settings
        'booking': booking,  # Pass the booking object to access name and email
    }
    return render(request, 'payment.html',context)


def payment_success(request, order_id, fee):
    payment_id = request.GET.get('payment_id')

    try:
        booking = BookSeat.objects.get(order_id=order_id)
    except BookSeat.DoesNotExist:
        return render(request, 'payment_failed.html', {'message': 'Booking not found.'})

    try:
        # Fetch the payment details
        payment = razorpay_client.payment.fetch(payment_id)

        if payment['order_id'] == order_id and payment['status'] == 'captured':
            # Update booking status to 'paid'
            booking.status = True
            booking.payment_id = payment_id
            booking.save()
            return render(request, 'payment_success.html', {'message': 'Payment successful!'})
        else:
            return render(request, 'payment_failed.html', {'message': 'Payment verification failed.'})
    except razorpay.errors.BadRequestError as e:
        return render(request, 'payment_failed.html', {'message': f'Error capturing payment: {str(e)}'})


def payment_failed(request, order_id, fee):
    
    payment_id = request.GET.get('payment_id', 'N/A')
    

    logger.info(f'Payment failed for Order ID: {order_id}, Payment ID: {payment_id}')
    
    # Optionally retrieve the booking object to show details
    booking = BookSeat.objects.filter(order_id=order_id).first()
    
    context = {
        'order_id': order_id,
        'payment_id': payment_id,
        'fee': fee,
        'booking': booking,
        'message': 'Payment was not successful. Please try again or contact support.'
    } 
    
    return render(request, 'payment_failed.html', context)
   
