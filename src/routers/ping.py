from fastapi import APIRouter
from sqlalchemy import text

from src.dependencies import DatabaseDep, SettingsDep
from src.schemas.health import HealthResponse, ServiceStatus

router = APIRouter()

@router.get("/ping", tags=["Health"])
async def ping():
    """Simple ping endpoint for basic connectivity tests."""
    return {"status": "ok", "message": "ping pong"}

@router.get("/health", 
            response_model=HealthResponse, 
            summary="HealthCheck",
            description="Check the health and status of the API service including database connectivity",
            response_description="Service Health Information",
            tags=["Health"]
            )
async def health_check(settings:SettingsDep, database:DatabaseDep) -> HealthResponse:
    """
    Comprehensive health check endpoint for monitoring and load balancer probes.

    This endpoint provides information about the service health, version,
    environment, and checks connectivity to dependent services like database.

    Returns:
        HealthResponse: Contains service status, version, environment, and service checks
    
    Example:
        Response:
        ```
        {
            "status": "ok",
            "version": "0.1.0",
            "environment": "development",
            "service_name": "rag-api",
            "services": {
                "database": {"status": "healthy", "message": "Connected successfully"}
            }
        }
        ```
    """
    services = {}
    overall_status = "OK"

    #Test the dataabse connectivity
    try:
        with database.get_session() as session:
            session.execute(text("SELECT 1"))
            services["database"] = ServiceStatus(status="healthy", message="Connected successfully")
    except Exception as e:
        services["database"] = ServiceStatus(status="unhealthy",
                    message=f"Connection Failed: {str(e)}")
        overall_status="degraded"

    return HealthResponse(
        status=overall_status,
        version=settings.app_version,
        environment=settings.environment,
        service_name=settings.service_name,
        services=services,
    )
