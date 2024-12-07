from fastapi import APIRouter
from typing import Dict
import random
import metrics

router = APIRouter()

@router.get("/pairs", tags=["pairs"])
async def get_pairs() -> Dict:
    metrics.GET_PAIRS_COUNT.inc()  # Increment metric
    return {
        "USDRUB": round(random.random() * 100, 2),
        "EURRUB": round(random.random() * 100, 2)
    }
