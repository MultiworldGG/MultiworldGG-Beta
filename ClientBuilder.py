from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Optional, Any, Dict, TYPE_CHECKING
import asyncio
import weakref
from ClientState import ClientState

import Gui

if TYPE_CHECKING:
    from CommonClient import CommonContext, InitContext
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
        self._kivy_ui: Optional[Gui.MultiMDApp] = None

    async def build(self) -> Dict[str, Any]:
        self._is_running = True
        
        try:
            self._kivy_ui = Gui.MultiMDApp(self.ctx)
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
            # Access ui, ui_task, and exit_event from global app reference when needed
            # MDApp.get_running_app().ctx.ui
            # MDApp.get_running_app().ctx.ui_task
            # MDApp.get_running_app().ctx.exit_event
            
            # Set up game-specific features
            await self._setup_game_features()
            
            return {}
            
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
        return False  # Game clients don't transition to other states
        #TODO: Figure out how to do this

class Client():
    def __init__(self):
        self.features = []
    def add(self, feature: str) -> None:
        self.features.append(feature)
    def __str__(self) -> str:
        return "Client with features: " + ", ".join(self.features)
    
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