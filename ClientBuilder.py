from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Optional, Any, Dict, TYPE_CHECKING
import asyncio
import logging
import os
import weakref
from ClientState import ClientState

from frontend_protocol import resolve_frontend_class

logger = logging.getLogger("Client")

if TYPE_CHECKING:
    from CommonClient import CommonContext, InitContext
    from frontend_protocol import FrontendProtocol
    from multiprocessing import Queue

class ClientBuilder(ABC):
    _ctx: Optional[weakref.ReferenceType['InitContext']] = None
    _mgr: Optional[weakref.ReferenceType['ClientManager']] = None

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            if key == "ctx":
                self._ctx = weakref.ref(value)
            elif key == "mgr":
                self._mgr = weakref.ref(value)
            else:
                raise ValueError(f"Invalid keyword argument: {key}")
        self._is_running = False

    @property
    def ctx(self):
        if self._ctx:
            ctx = self._ctx()
            if ctx is None:
                raise RuntimeError("Context has been garbage collected")
            return ctx
        elif self._mgr:
            mgr = self._mgr()
            if mgr is None:
                raise RuntimeError("Manager has been garbage collected")
            return mgr
        else:
            raise RuntimeError("No context or manager available")
    
    @abstractmethod
    def build(self) -> Any:
        pass

    @abstractmethod
    def cleanup(self) -> None:
        pass

    @abstractmethod
    def can_transition_to(self, new_state: ClientState) -> bool:
        pass

class InitialClient(ClientBuilder):

    def __init__(self, ctx: InitContext):
        super().__init__(ctx=ctx)
        self._ui_task: Optional[asyncio.Task] = None
        self._kivy_ui: Optional[FrontendProtocol] = None

    async def build(self) -> Dict[str, Any]:
        self._is_running = True

        try:
            self._kivy_ui = resolve_frontend_class()(self.ctx)
            self._ui_task = asyncio.create_task(self._run_gui(splash_queue=self.ctx._splash_queue))

            return {
                "ui_task": self._ui_task
            }
        
        except Exception as e:
            self._is_running = False
            raise e
        
    async def _run_gui(self, splash_queue: "Queue" = None):
        pass

    async def _run_cli(self):
        pass
    
    async def cleanup(self) -> None:
        self._is_running = False
        await asyncio.sleep(0.1)
    
    def can_transition_to(self, new_state: ClientState) -> bool:
        return new_state == ClientState.GAME and self._is_running

class GameClient(ClientBuilder):
    def __init__(self, ctx: 'CommonContext', init_data: dict[str, Any] = None):
        super().__init__(ctx=ctx)
        self._init_data = init_data or {}
        # No need to store ui_task or kivy_ui - always available via global access

    async def build(self) -> Dict[str, Any]:
        """Build game client extending initial client"""
        self._is_running = True
        
        try:
            await self._setup_game_features()

            legacy_builder = LegacyKvuiClientBuilder(
                self.ctx,
                self._init_data.get("ui"),
            )
            legacy_result = await legacy_builder.build()

            # ExtrasBuilder is a sibling of the legacy path: it operates on
            # ctx.feature_registry.features regardless of which builder wired the per-game frontend.
            extras_builder = ExtrasBuilder(
                self.ctx,
                {"ui": self._init_data.get("ui")},
            )
            extras_result = await extras_builder.build()

            return {"legacy_kvui": legacy_result, "extras": extras_result}

        except Exception as e:
            self._is_running = False
            raise e
    
    async def _setup_game_features(self) -> None:
        """Initialize game-specific functionality"""
        # Override in subclasses for game-specific setup
        pass

    async def cleanup(self) -> None:
        """Clean up game client resources"""
        self._is_running = False
        await asyncio.sleep(0.1)
    
    def can_transition_to(self, new_state: ClientState) -> bool:
        """Check if can transition to new state"""
        return self._is_running and new_state == ClientState.LEGACY_KVUI


class LegacyKvuiClientBuilder(ClientBuilder):
    """Bridge legacy Kivy UI setup onto the already-running frontend.

    This builder coordinates the legacy UI phase. It keeps CommonClient
    from needing to know whether a world uses an explicit build_gui hook or
    the old make_gui()/build() compatibility shape. Both run when both are
    present: a context inheriting TrackerGameContext gets build_gui from the
    tracker while its own make_gui() subclass still owns the game tab.
    """

    def __init__(self, ctx: 'CommonContext', app: Optional['FrontendProtocol'] = None):
        super().__init__(ctx=ctx)
        self.app = app
        self.manager = None

    async def build(self) -> Dict[str, Any]:
        if os.environ.get("MWGG_FRONTEND", "gui") == "tui":
            return {}

        app = self.app or getattr(self.ctx, "ui", None)
        if app is None:
            return {}

        self._is_running = True
        result: Dict[str, Any] = {"builders": []}

        try:
            if self._build_explicit_gui(app):
                result["builders"].append("build_gui")
        except Exception:
            logger.exception("Post-takeover build_gui hook failed")

        try:
            manager_cls = self._legacy_manager_class(app)
            if manager_cls is None:
                return result

            build_legacy_kvui = getattr(app, "build_legacy_kvui", None)
            if build_legacy_kvui is not None:
                self.manager = build_legacy_kvui(self.ctx, manager_cls)
            else:
                build_for_live_app = getattr(manager_cls, "build_for_live_app", None)
                if build_for_live_app is not None:
                    self.manager = build_for_live_app(self.ctx, app)
                else:
                    self.manager = manager_cls(self.ctx)
                    self.manager.build()

            result["builders"].append("legacy_kvui")
            result["manager"] = self.manager
            return result
        except Exception:
            logger.exception("Post-takeover per-game UI setup failed")
            return result

    def _build_explicit_gui(self, app: 'FrontendProtocol') -> bool:
        build_gui = getattr(self.ctx, "build_gui", None)
        if build_gui is None:
            return False

        previous_state = getattr(self.ctx, "_state", None)
        self.ctx._state = ClientState.LEGACY_KVUI
        try:
            build_gui(app)
        finally:
            if previous_state is not None:
                self.ctx._state = previous_state
        return True

    def _legacy_manager_class(self, app: 'FrontendProtocol') -> Optional[type]:
        try:
            manager_cls = self.ctx.make_gui()
        except Exception:
            logger.exception("Failed to resolve legacy kvui manager")
            return None

        if not isinstance(manager_cls, type):
            return None

        frontend_cls = resolve_frontend_class()
        if manager_cls is frontend_cls or manager_cls is type(app):
            return None

        # upstream make_gui()/build() shape: a subclass of the live frontend class
        if issubclass(manager_cls, frontend_cls) or hasattr(manager_cls, "build_for_live_app"):
            return manager_cls

        try:
            from kvui import GameManager
        except Exception:
            return None

        if issubclass(manager_cls, GameManager):
            return manager_cls

        return None

    async def cleanup(self) -> None:
        self._is_running = False
        await asyncio.sleep(0.1)

    def can_transition_to(self, new_state: ClientState) -> bool:
        return self._is_running and new_state == ClientState.GAME


class ExtrasBuilder(ClientBuilder):
    """Activate opt-in overlay features registered on ``ctx.feature_registry``.

    Runs after the per-game UI is wired up. Iterates ``ctx.feature_registry.features``
    and calls each as ``feature(ctx, app)``. Per-feature failures are logged
    and skipped so one broken overlay can't poison the others. Frontend-
    agnostic: it does not care whether the per-game UI was wired up by
    LegacyKvuiClientBuilder, an explicit ``build_gui`` hook, or a future
    non-legacy frontend.
    """

    def __init__(self, ctx: 'CommonContext', init_data: Optional[Dict[str, Any]] = None):
        super().__init__(ctx=ctx)
        self._init_data = init_data or {}

    async def build(self) -> Dict[str, Any]:
        self._is_running = True
        app = self._init_data.get("ui") or getattr(self.ctx, "ui", None)
        registry = getattr(self.ctx, "feature_registry", None)
        features = registry.features if registry else []
        for feature in features:
            try:
                feature(self.ctx, app)
            except Exception:
                logger.exception(
                    f"Extras feature {getattr(feature, '__name__', feature)!r} failed"
                )
        return {"features_run": len(features)}

    async def cleanup(self) -> None:
        self._is_running = False
        await asyncio.sleep(0.1)

    def can_transition_to(self, new_state: ClientState) -> bool:
        return self._is_running


class FeatureRegistry():
    """Per-context registry of opt-in overlay features.

    Each feature is a callable ``feature(ctx, app)`` registered during a
    feature's Phase-1 attach (e.g. ``attach_tracker_overlay`` appending
    ``start_overlay_ui_refresh``). ExtrasBuilder iterates and invokes them
    in registration order after the per-game UI is wired.

    Lives at ``ctx.feature_registry``; ``ctx.client`` is off-limits because
    upstream world contexts assign their own game client there.
    """
    def __init__(self):
        self.features: list = []
    def add(self, feature) -> None:
        self.features.append(feature)
    def __str__(self) -> str:
        names = [getattr(f, "__name__", repr(f)) for f in self.features]
        return "FeatureRegistry with features: " + ", ".join(names)


class ClientDirector():

    def __init__(self) -> None:
        self._client_builder = None

    @property
    def client_builder(self) -> ClientBuilder:
        return self._client_builder

    @client_builder.setter
    def client_builder(self, client_builder: ClientBuilder) -> None:
        self._client_builder = client_builder

    def build_cli_client(self) -> None:
        self._client_builder.build()
    
    def build_gui_client(self) -> None:
        self._client_builder.build()

    def build_client(self) -> None:
        self._client_builder.produce_client_cli()
        self._client_builder.produce_client_gui()
        self._client_builder.produce_client_ctx()
        self._client_builder.produce_client_world_data()
        self._client_builder.produce_client_connector()

class ClientManager:
    """Manager that can work with existing InitContext or create new one"""
    
    def __init__(self, existing_context: Optional['InitContext'] = None):
        self._existing_context = existing_context
        self._current_producer: Optional[ClientBuilder] = None
        self._state = ClientState.INITIAL
        self._is_transitioning = False
        self._client_data: Dict[str, Any] = {}
        self._context_adapter: Optional['ContextAdapter'] = None
        
        if existing_context:
            self._context_adapter = ContextAdapter(existing_context, self)

class ContextAdapter:
    """Adapter to bridge existing InitContext with our client producers"""
    
    def __init__(self, existing_context: 'InitContext', manager: 'ClientManager'):
        self._existing_context = existing_context
        self._manager = weakref.ref(manager)
        self._inherited_tasks: Dict[str, asyncio.Task] = {}
    
    @property
    def manager(self) -> 'ClientManager':
        mgr = self._manager()
        if mgr is None:
            raise RuntimeError("Manager has been garbage collected")
        return mgr
    
    def inherit_existing_tasks(self) -> Dict[str, Any]:
        """Extract and inherit tasks from existing context"""
        inherited_data = {}
        
        # Try to extract common attributes from existing context
        if hasattr(self._existing_context, '_client_data'):
            inherited_data.update(self._existing_context._client_data)
        
        if hasattr(self._existing_context, 'get_running_tasks'):
            self._inherited_tasks = self._existing_context.get_running_tasks()
            inherited_data['inherited_tasks'] = self._inherited_tasks
        
        return inherited_data
    
    async def register_new_tasks(self, new_tasks: Dict[str, asyncio.Task]):
        """Register new tasks with existing context if it supports it"""
        if hasattr(self._existing_context, 'register_tasks'):
            await self._existing_context.register_tasks(new_tasks) 