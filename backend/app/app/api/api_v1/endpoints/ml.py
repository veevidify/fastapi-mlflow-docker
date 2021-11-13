from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from celery.result import AsyncResult
from sqlalchemy.orm import Session

import mlflow

from app import crud, models, schemas
from app.api import deps
from app.worker import celery_app

router = APIRouter()

# /train-model
@router.post("/train-model", response_model=schemas.ResponseMsg, status_code=201)
async def train_model(
    params: schemas.EnetParam,
    current_user: models.User = Depends(deps.get_current_active_superuser),
):
    """
        Order celery worker to run train model in the background
        return HTTP result immediately
        run task-status/{task_id} afterwards to get mlflow's run_id
    """

    handle: AsyncResult = celery_app.send_task("app.worker.train_enet_diabetes_model", args=[params.alpha, params.l1_ratio])
    return {"msg": "Training started.", "task_id": handle.task_id}

# /run/{run_id}
async def get_run_details(
    run_id: str,
    current_user: models.User = Depends(deps.get_current_active_superuser),
):
    pass

# /get-runs
async def query_all_runs(
    current_user: models.User = Depends(deps.get_current_active_superuser),
):
    pass
