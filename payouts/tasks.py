import logging
import time
import uuid

from celery import shared_task

from .models import Payouts

logger = logging.getLogger(__name__)

@shared_task
def process_payout(payout_id: uuid.UUID) -> None:
    logger.info(f"Start serving payout ID: {payout_id}")
    
    try:
        payout = Payouts.objects.get(id=payout_id)
        
        time.sleep(5) 
        
        if payout.amount > 0:
            payout.status = 'processed'
        else:
            payout.status = 'failed'
            
        payout.save()
        logger.info(f"Payout {payout_id} succeed")
        
    except Payouts.DoesNotExist:
        logger.error(f"Payout {payout_id} was not found")
