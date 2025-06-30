"""
Tests for tide storage functionality
"""

from datetime import datetime, timedelta

import pytest

from server.storage.tide_storage import (
    CreateTideInput,
    FlowEntry,
    ListTidesFilter,
    TideStorage,
)


class TestTideStorage:
    """Test suite for TideStorage"""

    @pytest.mark.asyncio
    async def test_create_tide(self, tide_storage: TideStorage):
        """Test creating a new tide"""
        # Create a daily tide
        input_data = CreateTideInput(
            name="Morning Flow",
            flow_type="daily",
            description="Morning productivity session",
        )

        tide = await tide_storage.create_tide(input_data)

        assert tide.id.startswith("tide_")
        assert tide.name == "Morning Flow"
        assert tide.flow_type == "daily"
        assert tide.status == "active"
        assert tide.description == "Morning productivity session"
        assert tide.next_flow is not None
        assert len(tide.flow_history) == 0

        # Verify next_flow is approximately 1 day from now
        next_flow_time = datetime.fromisoformat(tide.next_flow)
        expected_time = datetime.now() + timedelta(days=1)
        time_diff = abs((next_flow_time - expected_time).total_seconds())
        assert time_diff < 60  # Within 1 minute tolerance

    @pytest.mark.asyncio
    async def test_create_tide_different_types(self, tide_storage: TideStorage):
        """Test creating tides with different flow types"""
        flow_types = {
            "daily": timedelta(days=1),
            "weekly": timedelta(weeks=1),
            "seasonal": timedelta(days=90),
            "project": None,  # No automatic next flow
        }

        for flow_type, expected_delta in flow_types.items():
            input_data = CreateTideInput(
                name=f"{flow_type.capitalize()} Tide", flow_type=flow_type
            )

            tide = await tide_storage.create_tide(input_data)

            assert tide.flow_type == flow_type

            if expected_delta:
                assert tide.next_flow is not None
                next_flow_time = datetime.fromisoformat(tide.next_flow)
                expected_time = datetime.now() + expected_delta
                time_diff = abs((next_flow_time - expected_time).total_seconds())
                assert time_diff < 60  # Within 1 minute tolerance
            else:
                assert tide.next_flow is None

    @pytest.mark.asyncio
    async def test_get_tide(self, tide_storage: TideStorage):
        """Test retrieving a tide by ID"""
        # Create a tide
        input_data = CreateTideInput(name="Test Tide", flow_type="daily")
        created_tide = await tide_storage.create_tide(input_data)

        # Retrieve it
        retrieved_tide = await tide_storage.get_tide(created_tide.id)

        assert retrieved_tide is not None
        assert retrieved_tide.id == created_tide.id
        assert retrieved_tide.name == created_tide.name
        assert retrieved_tide.flow_type == created_tide.flow_type

    @pytest.mark.asyncio
    async def test_get_nonexistent_tide(self, tide_storage: TideStorage):
        """Test retrieving a non-existent tide"""
        tide = await tide_storage.get_tide("nonexistent_id")
        assert tide is None

    @pytest.mark.asyncio
    async def test_list_tides(self, tide_storage: TideStorage):
        """Test listing all tides"""
        # Create multiple tides
        tide_names = ["Morning", "Afternoon", "Evening"]
        for name in tide_names:
            input_data = CreateTideInput(name=f"{name} Tide", flow_type="daily")
            await tide_storage.create_tide(input_data)

        # List all tides
        tides = await tide_storage.list_tides()

        assert len(tides) == 3
        # Verify they're sorted by created_at descending
        assert tides[0].name == "Evening Tide"
        assert tides[1].name == "Afternoon Tide"
        assert tides[2].name == "Morning Tide"

    @pytest.mark.asyncio
    async def test_list_tides_with_filters(self, tide_storage: TideStorage):
        """Test listing tides with filters"""
        # Create tides with different types
        await tide_storage.create_tide(
            CreateTideInput(name="Daily 1", flow_type="daily")
        )
        await tide_storage.create_tide(
            CreateTideInput(name="Weekly 1", flow_type="weekly")
        )
        await tide_storage.create_tide(
            CreateTideInput(name="Daily 2", flow_type="daily")
        )

        # Filter by flow type
        filter_data = ListTidesFilter(flow_type="daily")
        daily_tides = await tide_storage.list_tides(filter_data)

        assert len(daily_tides) == 2
        assert all(tide.flow_type == "daily" for tide in daily_tides)

    @pytest.mark.asyncio
    async def test_add_flow_to_tide(self, tide_storage: TideStorage):
        """Test adding a flow entry to a tide"""
        # Create a tide
        input_data = CreateTideInput(name="Test Tide", flow_type="daily")
        tide = await tide_storage.create_tide(input_data)

        # Add a flow entry
        flow_entry = FlowEntry(
            timestamp=datetime.now().isoformat(), intensity="moderate", duration=25
        )

        updated_tide = await tide_storage.add_flow_to_tide(tide.id, flow_entry)

        assert updated_tide is not None
        assert len(updated_tide.flow_history) == 1
        assert updated_tide.flow_history[0].intensity == "moderate"
        assert updated_tide.flow_history[0].duration == 25
        assert updated_tide.last_flow == flow_entry.timestamp

        # Verify next_flow is updated for daily tide
        next_flow_time = datetime.fromisoformat(updated_tide.next_flow)
        flow_time = datetime.fromisoformat(flow_entry.timestamp)
        expected_time = flow_time + timedelta(days=1)
        time_diff = abs((next_flow_time - expected_time).total_seconds())
        assert time_diff < 60  # Within 1 minute tolerance

    @pytest.mark.asyncio
    async def test_update_tide(self, tide_storage: TideStorage):
        """Test updating a tide"""
        # Create a tide
        input_data = CreateTideInput(name="Original Name", flow_type="daily")
        tide = await tide_storage.create_tide(input_data)

        # Update it
        updates = {"name": "Updated Name", "status": "paused"}

        updated_tide = await tide_storage.update_tide(tide.id, updates)

        assert updated_tide is not None
        assert updated_tide.name == "Updated Name"
        assert updated_tide.status == "paused"
        assert updated_tide.id == tide.id  # ID should not change
        assert updated_tide.flow_type == "daily"  # Unchanged fields remain
