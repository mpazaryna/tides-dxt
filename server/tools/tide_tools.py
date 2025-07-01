"""
Tidal workflow management tools
"""

import logging
import os
from datetime import datetime, timedelta
from typing import Any, Literal

from mcp import types
from pydantic import BaseModel, Field

# Use absolute import when running as a module, relative import otherwise
try:
    from storage.tide_storage import (
        CreateTideInput,
        FlowEntry,
        ListTidesFilter,
        TideStorage,
    )
except ImportError:
    from ..storage.tide_storage import (
        CreateTideInput,
        FlowEntry,
        ListTidesFilter,
        TideStorage,
    )

logger = logging.getLogger(__name__)

# Initialize storage (use mounted volume in Docker or local directory for development)

storage_path = os.getenv("TIDES_STORAGE_PATH", "./tides_data")
# Expand user home directory if present
if storage_path.startswith("~/"):
    storage_path = os.path.expanduser(storage_path)
elif "${HOME}" in storage_path:
    storage_path = storage_path.replace("${HOME}", os.path.expanduser("~"))

# If using default relative path, try to use a more appropriate location
if storage_path == "./tides_data":
    # Try to use user's home directory as fallback
    try:
        home_path = os.path.expanduser("~/Documents/tides_data")
        # Test if we can create the directory
        os.makedirs(home_path, exist_ok=True)
        storage_path = home_path
    except Exception:
        # If that fails, keep the original path
        pass

tide_storage = TideStorage(storage_path)


# Schema definitions
class CreateTideInputSchema(BaseModel):
    """Schema for creating a tide"""

    name: str = Field(description="Name of the tidal workflow")
    flow_type: Literal["daily", "weekly", "project", "seasonal"] = Field(
        description="Type of tidal flow"
    )
    description: str | None = Field(
        default=None, description="Description of the workflow"
    )


class CreateTideOutputSchema(BaseModel):
    """Schema for create tide output"""

    success: bool
    tide_id: str
    name: str
    flow_type: str
    created_at: str
    next_flow: str | None = None


class TideSummary(BaseModel):
    """Summary of a tide for listing"""

    id: str
    name: str
    flow_type: str
    status: Literal["active", "paused", "completed"]
    created_at: str
    last_flow: str | None = None
    next_flow: str | None = None


class ListTidesInputSchema(BaseModel):
    """Schema for listing tides"""

    flow_type: str | None = Field(default=None, description="Filter by flow type")
    active_only: bool | None = Field(default=None, description="Show only active tides")


class ListTidesOutputSchema(BaseModel):
    """Schema for list tides output"""

    tides: list[TideSummary]
    total: int


class FlowTideInputSchema(BaseModel):
    """Schema for flowing a tide"""

    tide_id: str = Field(description="ID of the tide to flow")
    intensity: Literal["gentle", "moderate", "strong"] | None = Field(
        default="moderate", description="Flow intensity"
    )
    duration: int | None = Field(default=25, description="Flow duration in minutes")


class FlowTideOutputSchema(BaseModel):
    """Schema for flow tide output"""

    success: bool
    tide_id: str
    flow_started: str
    estimated_completion: str
    flow_guidance: str
    next_actions: list[str]


class EndTideInputSchema(BaseModel):
    """Schema for ending a tide"""

    tide_id: str = Field(description="ID of the tide to end")
    status: Literal["completed", "paused"] = Field(
        default="completed", description="How to end the tide"
    )
    notes: str | None = Field(
        default=None, description="Optional notes about ending the tide"
    )


class EndTideOutputSchema(BaseModel):
    """Schema for end tide output"""

    success: bool
    tide_id: str
    final_status: str
    completion_time: str
    summary: str


# Tool definitions
tide_tools: list[types.Tool] = [
    types.Tool(
        name="create_tide",
        description="Create a new tidal workflow for rhythmic productivity",
        inputSchema=CreateTideInputSchema.model_json_schema(),
    ),
    types.Tool(
        name="list_tides",
        description="List all tidal workflows with their current status",
        inputSchema=ListTidesInputSchema.model_json_schema(),
    ),
    types.Tool(
        name="flow_tide",
        description="Start a flow session for a specific tidal workflow",
        inputSchema=FlowTideInputSchema.model_json_schema(),
    ),
    types.Tool(
        name="end_tide",
        description="End a tidal workflow by completing or pausing it",
        inputSchema=EndTideInputSchema.model_json_schema(),
    ),
]


# Tool handlers
async def create_tide_handler(args: dict) -> dict[str, Any]:
    """Handle tide creation"""
    validated_args = CreateTideInputSchema(**args)

    try:
        input_data = CreateTideInput(
            name=validated_args.name,
            flow_type=validated_args.flow_type,
            description=validated_args.description,
        )

        tide = await tide_storage.create_tide(input_data)

        logger.info(
            f"Creating tide: {validated_args.name} ({validated_args.flow_type})"
        )

        return CreateTideOutputSchema(
            success=True,
            tide_id=tide.id,
            name=tide.name,
            flow_type=tide.flow_type,
            created_at=tide.created_at,
            next_flow=tide.next_flow,
        ).model_dump()

    except Exception as error:
        logger.error(f"Failed to create tide: {error}")
        return CreateTideOutputSchema(
            success=False,
            tide_id="",
            name=validated_args.name,
            flow_type=validated_args.flow_type,
            created_at=datetime.now().isoformat(),
        ).model_dump()


async def list_tides_handler(args: dict) -> dict[str, Any]:
    """Handle listing tides"""
    validated_args = ListTidesInputSchema(**args)

    try:
        filter_data = ListTidesFilter(
            flow_type=validated_args.flow_type, active_only=validated_args.active_only
        )

        tides = await tide_storage.list_tides(filter_data)

        tide_summaries = [
            TideSummary(
                id=tide.id,
                name=tide.name,
                flow_type=tide.flow_type,
                status=tide.status,
                created_at=tide.created_at,
                last_flow=tide.last_flow,
                next_flow=tide.next_flow,
            )
            for tide in tides
        ]

        return ListTidesOutputSchema(
            tides=tide_summaries, total=len(tide_summaries)
        ).model_dump()

    except Exception as error:
        logger.error(f"Failed to list tides: {error}")
        return ListTidesOutputSchema(tides=[], total=0).model_dump()


async def flow_tide_handler(args: dict) -> dict[str, Any]:
    """Handle starting a flow session"""
    validated_args = FlowTideInputSchema(**args)

    try:
        # Verify tide exists
        tide = await tide_storage.get_tide(validated_args.tide_id)
        if not tide:
            return FlowTideOutputSchema(
                success=False,
                tide_id=validated_args.tide_id,
                flow_started="",
                estimated_completion="",
                flow_guidance="Tide not found",
                next_actions=[],
            ).model_dump()

        flow_started = datetime.now().isoformat()
        duration = validated_args.duration or 25  # Default to 25 if None
        estimated_completion = (
            datetime.now() + timedelta(minutes=duration)
        ).isoformat()

        # Add flow to tide history
        intensity = (
            validated_args.intensity or "moderate"
        )  # Default to moderate if None
        flow_entry = FlowEntry(
            timestamp=flow_started,
            intensity=intensity,
            duration=duration,
        )

        await tide_storage.add_flow_to_tide(validated_args.tide_id, flow_entry)

        # Generate guidance based on intensity
        guidance_map = {
            "gentle": "🌊 Begin with calm, steady focus. Let thoughts flow naturally without forcing. Take breaks as needed.",
            "moderate": "🌊 Maintain focused attention with deliberate action. Balance effort with ease. Stay present to the work.",
            "strong": "🌊 Dive deep with sustained concentration. Channel energy into meaningful progress. Push through resistance mindfully.",
        }

        flow_guidance = guidance_map[intensity]

        next_actions = [
            "🎯 Set clear intention for this flow session",
            "⏰ Start timer and begin focused work",
            "🧘 Take mindful breaks if needed",
            "📝 Capture insights and progress",
            "🌊 Honor the natural rhythm of the work",
        ]

        logger.info(
            f"Starting flow session for tide: {validated_args.tide_id} "
            f"({validated_args.intensity} intensity, {validated_args.duration}min)"
        )

        return FlowTideOutputSchema(
            success=True,
            tide_id=validated_args.tide_id,
            flow_started=flow_started,
            estimated_completion=estimated_completion,
            flow_guidance=flow_guidance,
            next_actions=next_actions,
        ).model_dump()

    except Exception as error:
        logger.error(f"Failed to start flow: {error}")
        return FlowTideOutputSchema(
            success=False,
            tide_id=validated_args.tide_id,
            flow_started="",
            estimated_completion="",
            flow_guidance="Failed to start flow session",
            next_actions=[],
        ).model_dump()


async def end_tide_handler(args: dict) -> dict[str, Any]:
    """Handle ending a tide"""
    validated_args = EndTideInputSchema(**args)

    try:
        # Verify tide exists
        tide = await tide_storage.get_tide(validated_args.tide_id)
        if not tide:
            return EndTideOutputSchema(
                success=False,
                tide_id=validated_args.tide_id,
                final_status="not_found",
                completion_time="",
                summary="Tide not found",
            ).model_dump()

        # Check if tide is already completed or paused
        if tide.status in ["completed", "paused"]:
            return EndTideOutputSchema(
                success=False,
                tide_id=validated_args.tide_id,
                final_status=tide.status,
                completion_time=tide.created_at,
                summary=f"Tide is already {tide.status}",
            ).model_dump()

        completion_time = datetime.now().isoformat()

        # Update tide status
        updates = {
            "status": validated_args.status,
            "last_flow": completion_time,
        }

        # Add completion notes if provided
        if validated_args.notes:
            if tide.flow_history:
                # Add notes to the last flow entry
                last_flow = tide.flow_history[-1]
                last_flow.notes = validated_args.notes
            else:
                # Create a completion flow entry
                completion_flow = FlowEntry(
                    timestamp=completion_time,
                    intensity="gentle",
                    duration=0,
                    notes=validated_args.notes,
                )
                await tide_storage.add_flow_to_tide(
                    validated_args.tide_id, completion_flow
                )

        await tide_storage.update_tide(validated_args.tide_id, updates)

        # Generate summary
        flow_count = len(tide.flow_history)
        summary_map = {
            "completed": f"🌊 Tide '{tide.name}' completed successfully with {flow_count} flow sessions. The natural rhythm has reached its conclusion.",
            "paused": f"🌊 Tide '{tide.name}' paused gracefully with {flow_count} flow sessions. The flow can resume when energy returns.",
        }

        summary = summary_map[validated_args.status]

        logger.info(
            f"Ended tide: {validated_args.tide_id} with status {validated_args.status}"
        )

        return EndTideOutputSchema(
            success=True,
            tide_id=validated_args.tide_id,
            final_status=validated_args.status,
            completion_time=completion_time,
            summary=summary,
        ).model_dump()

    except Exception as error:
        logger.error(f"Failed to end tide: {error}")
        return EndTideOutputSchema(
            success=False,
            tide_id=validated_args.tide_id,
            final_status="error",
            completion_time="",
            summary=f"Failed to end tide: {error}",
        ).model_dump()


# Handler mapping
tide_handlers = {
    "create_tide": create_tide_handler,
    "list_tides": list_tides_handler,
    "flow_tide": flow_tide_handler,
    "end_tide": end_tide_handler,
}
