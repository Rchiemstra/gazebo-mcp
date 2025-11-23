"""
Modern Gazebo adapter using ros_gz_interfaces.

Stub implementation for Gazebo Modern (Fortress/Harmonic).
Full implementation to be completed in Phase 2.
"""

from typing import Dict, List, Optional, Any

from ..gazebo_interface import (
    GazeboInterface,
    EntityPose,
    EntityTwist,
    WorldInfo
)
from ...utils.logger import get_logger


class ModernGazeboAdapter(GazeboInterface):
    """
    Adapter for Gazebo Modern (Fortress/Harmonic via ros_gz).

    STUB IMPLEMENTATION - To be completed in Phase 2.

    Modern Gazebo differences:
    - Package: ros_gz_interfaces (not gazebo_msgs)
    - Service paths: /world/{world_name}/* (not /gazebo/*)
    - Field names: .sdf (not .xml), .pose (not .initial_pose)
    - World parameter required (supports multiple worlds)
    """

    def __init__(self, node, default_world: str = "default", timeout: float = 5.0):
        """
        Initialize Modern Gazebo adapter.

        Args:
            node: ROS2 node
            default_world: Default world name
            timeout: Service call timeout
        """
        self.node = node
        self.default_world = default_world
        self.timeout = timeout
        self.logger = get_logger("modern_adapter")

        self.logger.info(f"Initialized Modern Gazebo adapter (stub) for world '{default_world}'")

    def get_backend_name(self) -> str:
        """Return backend identifier."""
        return "modern"

    async def spawn_entity(
        self,
        name: str,
        sdf: str,
        pose: EntityPose,
        world: str = "default"
    ) -> bool:
        """Spawn entity - NOT YET IMPLEMENTED."""
        raise NotImplementedError(
            "Modern Gazebo adapter not yet implemented. "
            "Use GAZEBO_BACKEND=classic during Phase 1. "
            "Full implementation coming in Phase 2."
        )

    async def delete_entity(
        self,
        name: str,
        world: str = "default"
    ) -> bool:
        """Delete entity - NOT YET IMPLEMENTED."""
        raise NotImplementedError("Modern adapter not yet implemented")

    async def get_entity_state(
        self,
        name: str,
        world: str = "default"
    ) -> Dict[str, Any]:
        """Get entity state - NOT YET IMPLEMENTED."""
        raise NotImplementedError("Modern adapter not yet implemented")

    async def set_entity_state(
        self,
        name: str,
        pose: EntityPose,
        twist: Optional[EntityTwist] = None,
        world: str = "default"
    ) -> bool:
        """Set entity state - NOT YET IMPLEMENTED."""
        raise NotImplementedError("Modern adapter not yet implemented")

    async def list_entities(
        self,
        world: str = "default"
    ) -> List[str]:
        """List entities - NOT YET IMPLEMENTED."""
        raise NotImplementedError("Modern adapter not yet implemented")

    async def get_world_properties(
        self,
        world: str = "default"
    ) -> WorldInfo:
        """Get world properties - NOT YET IMPLEMENTED."""
        raise NotImplementedError("Modern adapter not yet implemented")

    async def pause_simulation(self, world: str = "default") -> bool:
        """Pause simulation - NOT YET IMPLEMENTED."""
        raise NotImplementedError("Modern adapter not yet implemented")

    async def unpause_simulation(self, world: str = "default") -> bool:
        """Unpause simulation - NOT YET IMPLEMENTED."""
        raise NotImplementedError("Modern adapter not yet implemented")

    async def reset_simulation(self, world: str = "default") -> bool:
        """Reset simulation - NOT YET IMPLEMENTED."""
        raise NotImplementedError("Modern adapter not yet implemented")

    async def reset_world(self, world: str = "default") -> bool:
        """Reset world - NOT YET IMPLEMENTED."""
        raise NotImplementedError("Modern adapter not yet implemented")
