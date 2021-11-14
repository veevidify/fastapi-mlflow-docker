from typing import Optional, List

from fastapi import APIRouter, Depends, HTTPException
from celery.result import AsyncResult
from sqlalchemy.orm import Session

import mlflow
from mlflow.tracking import MlflowClient
from mlflow.entities import ViewType

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

# /get-runs
@router.get("/runs", response_model=List[schemas.RunInfo])
async def query_all_runs(
    current_user: models.User = Depends(deps.get_current_active_superuser),
    mlflow_client: MlflowClient = Depends(deps.get_mlflow_client),
):
    runs = mlflow_client.list_run_infos(
        "0",
        run_view_type=ViewType.ALL,
        order_by=["metric.click_rate DESC"]
    )

    results = []
    for run in runs:
        results.append(schemas.RunInfo.parse_obj(run))

    return results

# /run/{run_id}
@router.get("/runs/{run_id}", response_model=schemas.Run)
async def get_run_details(
    run_id: str,
    current_user: models.User = Depends(deps.get_current_active_superuser),
    mlflow_client: MlflowClient = Depends(deps.get_mlflow_client),
):

    run = mlflow_client.get_run(run_id)
    result = schemas.Run.parse_obj(run)

    return result
