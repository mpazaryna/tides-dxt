"""
Tests for tide tools functionality
"""
import pytest
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock

from server.tools.tide_tools import (
    create_tide_handler,
    list_tides_handler,
    flow_tide_handler,
    CreateTideInputSchema,
    ListTidesInputSchema,
    FlowTideInputSchema
)
from server.storage.tide_storage import TideData


class TestTideTools:
    """Test suite for tide tool handlers"""
    
    @pytest.mark.asyncio
    async def test_create_tide_handler_success(self):
        """Test successful tide creation"""
        args = {
            "name": "Test Tide",
            "flow_type": "daily",
            "description": "A test tide"
        }
        
        mock_tide = TideData(
            id="tide_123",
            name="Test Tide",
            flow_type="daily",
            status="active",
            created_at=datetime.now().isoformat(),
            next_flow=(datetime.now() + timedelta(days=1)).isoformat(),
            description="A test tide",
            flow_history=[]
        )
        
        with patch('server.tools.tide_tools.tide_storage.create_tide', return_value=mock_tide):
            result = await create_tide_handler(args)
        
        assert result["success"] is True
        assert result["tide_id"] == "tide_123"
        assert result["name"] == "Test Tide"
        assert result["flow_type"] == "daily"
        assert result["next_flow"] is not None
    
    @pytest.mark.asyncio
    async def test_create_tide_handler_error(self):
        """Test tide creation error handling"""
        args = {
            "name": "Test Tide",
            "flow_type": "daily"
        }
        
        with patch('server.tools.tide_tools.tide_storage.create_tide', side_effect=Exception("Storage error")):
            result = await create_tide_handler(args)
        
        assert result["success"] is False
        assert result["tide_id"] == ""
        assert result["name"] == "Test Tide"
    
    @pytest.mark.asyncio
    async def test_list_tides_handler_success(self):
        """Test successful tide listing"""
        args = {
            "flow_type": "daily",
            "active_only": True
        }
        
        mock_tides = [
            TideData(
                id="tide_1",
                name="Morning Tide",
                flow_type="daily",
                status="active",
                created_at=datetime.now().isoformat(),
                flow_history=[]
            ),
            TideData(
                id="tide_2",
                name="Evening Tide",
                flow_type="daily",
                status="active",
                created_at=datetime.now().isoformat(),
                flow_history=[]
            )
        ]
        
        with patch('server.tools.tide_tools.tide_storage.list_tides', return_value=mock_tides):
            result = await list_tides_handler(args)
        
        assert len(result["tides"]) == 2
        assert result["total"] == 2
        assert result["tides"][0]["name"] == "Morning Tide"
        assert result["tides"][1]["name"] == "Evening Tide"
    
    @pytest.mark.asyncio
    async def test_list_tides_handler_empty(self):
        """Test listing tides when none exist"""
        args = {}
        
        with patch('server.tools.tide_tools.tide_storage.list_tides', return_value=[]):
            result = await list_tides_handler(args)
        
        assert len(result["tides"]) == 0
        assert result["total"] == 0
    
    @pytest.mark.asyncio
    async def test_flow_tide_handler_success(self):
        """Test successful flow session start"""
        args = {
            "tide_id": "tide_123",
            "intensity": "moderate",
            "duration": 25
        }
        
        mock_tide = TideData(
            id="tide_123",
            name="Test Tide",
            flow_type="daily",
            status="active",
            created_at=datetime.now().isoformat(),
            flow_history=[]
        )
        
        with patch('server.tools.tide_tools.tide_storage.get_tide', return_value=mock_tide):
            with patch('server.tools.tide_tools.tide_storage.add_flow_to_tide', return_value=mock_tide):
                result = await flow_tide_handler(args)
        
        assert result["success"] is True
        assert result["tide_id"] == "tide_123"
        assert result["flow_started"] is not None
        assert result["estimated_completion"] is not None
        assert "moderate" in result["flow_guidance"].lower()
        assert len(result["next_actions"]) > 0
    
    @pytest.mark.asyncio
    async def test_flow_tide_handler_not_found(self):
        """Test flow session with non-existent tide"""
        args = {
            "tide_id": "nonexistent",
            "intensity": "moderate",
            "duration": 25
        }
        
        with patch('server.tools.tide_tools.tide_storage.get_tide', return_value=None):
            result = await flow_tide_handler(args)
        
        assert result["success"] is False
        assert result["flow_guidance"] == "Tide not found"
        assert len(result["next_actions"]) == 0
    
    @pytest.mark.asyncio
    async def test_flow_tide_handler_different_intensities(self):
        """Test flow session with different intensities"""
        intensities = ["gentle", "moderate", "strong"]
        
        mock_tide = TideData(
            id="tide_123",
            name="Test Tide",
            flow_type="daily",
            status="active",
            created_at=datetime.now().isoformat(),
            flow_history=[]
        )
        
        for intensity in intensities:
            args = {
                "tide_id": "tide_123",
                "intensity": intensity,
                "duration": 25
            }
            
            with patch('server.tools.tide_tools.tide_storage.get_tide', return_value=mock_tide):
                with patch('server.tools.tide_tools.tide_storage.add_flow_to_tide', return_value=mock_tide):
                    result = await flow_tide_handler(args)
            
            assert result["success"] is True
            assert intensity in result["flow_guidance"].lower() or "🌊" in result["flow_guidance"]
    
    def test_schema_validation(self):
        """Test input schema validation"""
        # Valid inputs
        CreateTideInputSchema(name="Test", flow_type="daily")
        CreateTideInputSchema(name="Test", flow_type="weekly", description="A weekly tide")
        
        # Invalid flow type
        with pytest.raises(ValueError):
            CreateTideInputSchema(name="Test", flow_type="invalid")
        
        # Missing required fields
        with pytest.raises(ValueError):
            CreateTideInputSchema(flow_type="daily")
        
        # Test optional fields
        list_schema = ListTidesInputSchema()
        assert list_schema.flow_type is None
        assert list_schema.active_only is None
        
        # Test flow schema defaults
        flow_schema = FlowTideInputSchema(tide_id="test_id")
        assert flow_schema.intensity == "moderate"
        assert flow_schema.duration == 25