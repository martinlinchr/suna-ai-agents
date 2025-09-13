import os
import asyncio
from typing import Optional, Dict, Any, List
from core.utils.logger import logger
from daytona_sdk.common.errors import DaytonaError

# Your existing daytona_config (keep as is)
logger.info("Initializing Daytona sandbox configuration")

daytona_config = {
    "api_key": os.getenv("DAYTONA_API_KEY"),
    "jwt_token": os.getenv("DAYTONA_JWT_TOKEN"),
}

if not daytona_config["api_key"] and not daytona_config["jwt_token"]:
    logger.warning("No Daytona API key found in environment variables")

# Set other Daytona configuration
daytona_config["api_url"] = os.getenv("DAYTONA_API_URL", "https://app.daytona.io/api")
logger.debug(f"Daytona API URL set to: {daytona_config['api_url']}")

daytona_config["target"] = os.getenv("DAYTONA_TARGET", "us")
logger.debug(f"Daytona target set to: {daytona_config['target']}")

# Graceful Daytona initialization
def initialize_daytona() -> Optional[Any]:
    """Initialize Daytona with graceful fallback"""
    
    # Check if sandbox is explicitly disabled
    if os.getenv('DISABLE_SANDBOX', 'false').lower() == 'true':
        logger.info("Sandbox functionality disabled via DISABLE_SANDBOX environment variable")
        return None
    
    # Check if we have required credentials
    if not daytona_config.get("api_key") and not daytona_config.get("jwt_token"):
        logger.warning("No Daytona credentials found - sandbox functionality disabled")
        return None
    
    try:
        from daytona_sdk import AsyncDaytona
        daytona_instance = AsyncDaytona(daytona_config)
        logger.info("Daytona sandbox initialized successfully")
        return daytona_instance
    except DaytonaError as e:
        logger.warning(f"Daytona initialization failed - sandbox features disabled: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error initializing Daytona: {e}")
        return None

# Initialize daytona (replaces the original line that was causing the error)
daytona = initialize_daytona()

# Helper function to check if sandbox is available
def is_sandbox_available() -> bool:
    """Check if sandbox functionality is available"""
    return daytona is not None

# Modified sandbox functions with availability checks
async def get_or_start_sandbox(sandbox_id: str = None, **kwargs) -> Dict[str, Any]:
    """Get or start a sandbox with availability check"""
    if not is_sandbox_available():
        raise RuntimeError(
            "Sandbox functionality is disabled. "
            "Please configure DAYTONA_API_KEY or set DISABLE_SANDBOX=false"
        )
    
    try:
        # Your existing get_or_start_sandbox logic here
        # This is where your original implementation would go
        logger.info(f"Getting or starting sandbox: {sandbox_id}")
        # Replace with your actual implementation
        return {"status": "success", "sandbox_id": sandbox_id}
    except Exception as e:
        logger.error(f"Failed to get or start sandbox: {e}")
        raise

async def create_sandbox(config: Dict[str, Any]) -> Dict[str, Any]:
    """Create a new sandbox with availability check"""
    if not is_sandbox_available():
        raise RuntimeError(
            "Sandbox functionality is disabled. "
            "Please configure DAYTONA_API_KEY or set DISABLE_SANDBOX=false"
        )
    
    try:
        # Your existing create_sandbox logic here
        logger.info(f"Creating sandbox with config: {config}")
        # Replace with your actual implementation
        return {"status": "created", "config": config}
    except Exception as e:
        logger.error(f"Failed to create sandbox: {e}")
        raise

async def delete_sandbox(sandbox_id: str) -> Dict[str, Any]:
    """Delete a sandbox with availability check"""
    if not is_sandbox_available():
        raise RuntimeError(
            "Sandbox functionality is disabled. "
            "Please configure DAYTONA_API_KEY or set DISABLE_SANDBOX=false"
        )
    
    try:
        # Your existing delete_sandbox logic here
        logger.info(f"Deleting sandbox: {sandbox_id}")
        # Replace with your actual implementation
        return {"status": "deleted", "sandbox_id": sandbox_id}
    except Exception as e:
        logger.error(f"Failed to delete sandbox: {e}")
        raise

# Add any other sandbox-related functions you have, following the same pattern
async def list_sandboxes() -> List[Dict[str, Any]]:
    """List available sandboxes with availability check"""
    if not is_sandbox_available():
        logger.warning("Sandbox functionality disabled - returning empty list")
        return []
    
    try:
        # Your existing list_sandboxes logic here
        logger.info("Listing sandboxes")
        # Replace with your actual implementation
        return []
    except Exception as e:
        logger.error(f"Failed to list sandboxes: {e}")
        return []

# Export the daytona instance and helper functions
__all__ = [
    'daytona',
    'is_sandbox_available',
    'get_or_start_sandbox',
    'create_sandbox',
    'delete_sandbox',
    'list_sandboxes'
]
