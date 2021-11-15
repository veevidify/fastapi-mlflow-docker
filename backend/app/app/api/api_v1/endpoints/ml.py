import time
from typing import Optional, List

from fastapi import APIRouter, Depends, HTTPException, status
from celery.result import AsyncResult
from sqlalchemy.orm import Session

import mlflow
from mlflow.tracking import MlflowClient
from mlflow.entities import ViewType
from mlflow.utils.rest_utils import RestException, RESOURCE_DOES_NOT_EXIST

from app import crud, models, schemas
from app.api import deps
from app.worker import celery_app

router = APIRouter()

# == run workflow == #

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
    run_infos = mlflow_client.list_run_infos(
        "0",
        run_view_type=ViewType.ALL,
    )

    results = []
    for run_info in run_infos:
        results.append(schemas.RunInfo.parse_obj(run_info))

    return results

# /run/{run_id}
@router.get("/runs/{run_id}", response_model=schemas.Run)
async def get_run_details(
    run_id: str,
    current_user: models.User = Depends(deps.get_current_active_superuser),
    mlflow_client: MlflowClient = Depends(deps.get_mlflow_client),
):

    try:
        run = mlflow_client.get_run(run_id)

    except RestException as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Run does not exist.")

    except:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Unknown error.")

    result = schemas.Run.parse_obj(run)

    return result

# == end run workflow == #

# == model reg workflow == #

# /run/{run_id}/register-model
@router.post("/run/{run_id}/register-model", response_model=schemas.ModelVersion)
async def register_model_from_run(
    run_id: str,
    model_meta: schemas.ModelCreateMeta,
    current_user: models.User = Depends(deps.get_current_active_superuser),
    mlflow_client: MlflowClient = Depends(deps.get_mlflow_client),
):
    model_name = model_meta.name.replace(" ", "-")

    # check run exist
    try:
        run = mlflow_client.get_run(run_id)

    except RestException as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Run does not exist.")

    except:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Unknown error.")

    # register
    result = mlflow.register_model(
        f"runs:/{run_id}/model",
        model_name,
    )

    model_version = schemas.ModelVersion.parse_obj(result)
    return model_version

# /registered-models
# will have to paginate in the future?
@router.get('/registered-models', response_model=List[schemas.RegisteredModel])
async def list_registered_models(
    current_user: models.User = Depends(deps.get_current_active_superuser),
    mlflow_client: MlflowClient = Depends(deps.get_mlflow_client),
):

    models = mlflow_client.list_registered_models()
    results = []
    for model in models:
        results.append(schemas.RegisteredModel.parse_obj(model))

    return results

# wip:
# /model/{}/update
# rename, change description, transition model stage, refit

# /model/{}/archive
@router.get("/model/{model_name}/archive", status_code=204)
async def archive_registered_model(
    model_name: str,
    current_user: models.User = Depends(deps.get_current_active_superuser),
    mlflow_client: MlflowClient = Depends(deps.get_mlflow_client),
):
    # worth abstractions using deps?
    try:
        model = mlflow.pyfunc.load_model(model_uri=f"models:/{model_name}/None")

    except RestException as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"Model with name {model_name} does not exist.")

    except Exception as e:
        print(e)
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Unknown error.")


    mlflow_client.transition_model_version_stage(model_name, 1, "Archived")

# == end model reg workflow == #

# == predict workflow == #

# /model/{}/predict

# == end predict workflow == #
