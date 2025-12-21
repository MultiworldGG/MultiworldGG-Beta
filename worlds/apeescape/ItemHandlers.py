import random
import time
import worlds._bizhawk as bizhawk

from .RAMAddress import RAM
from typing import TYPE_CHECKING, Optional, Dict, Set, ClassVar, Any, Tuple, Union
if TYPE_CHECKING:
    from worlds._bizhawk.context import BizHawkClientContext, BizHawkClientCommandProcessor

class ApeEscapeMemoryInput:
    def __init__(self, bizhawk_client_context: "BizHawkClientContext"):
        self.bizhawk_client_context = bizhawk_client_context

        self.all_digital_buttons = list(RAM.BUTTON_BIT_MAP.keys())
        # Combined list of all possible inputs for the handler to choose from (includes Pseudo-Right Joystick)
        self.all_inputs = self.all_digital_buttons + [RAM.RIGHT_JOYSTICK_PSEUDO_INPUT]

    async def set_inputs(self, desired_inputs: dict):
        """
        Constructs and sends memory write requests to BizHawk to set controller inputs.
        This method sends writes ONLY for the inputs explicitly present in desired_inputs.
        If an input (digital or analog) is NOT in desired_inputs, it's assumed to be released,
        and its memory address will NOT be explicitly written by this client for that frame.
        This relies on the game's natural input polling to reset non-written inputs.

        Args:
            desired_inputs (dict): A dictionary where keys are input names (e.g., "P1 X", "P1 R_X")
                                   and values are True/False for digital buttons, or 0-255 for analog.
        """
        writes_list = []

        # --- 1. Construct Digital Button Bytes ---
        # Start with all bits set to 1 (all digital buttons unpressed in inverse logic)
        # This will be the base for the digital button memory write.
        new_digital_word = 0xFFFF

        for input_name, state in desired_inputs.items():
            if input_name in RAM.BUTTON_BIT_MAP:
                bit_pos = RAM.BUTTON_BIT_MAP[input_name]
                if state is True:  # If button is desired to be pressed
                    # Clear its corresponding bit (set to 0) in the 16-bit word
                    new_digital_word &= ~(1 << bit_pos)
                # If state is False, leave the bit as 1 (unpressed), which is default in new_digital_word.

        # Split the 16-bit word into two 8-bit integers
        byte_low_value = new_digital_word & 0xFF
        byte_high_value = (new_digital_word >> 8) & 0xFF

        # Add digital button writes to the list
        writes_list.append((RAM.BUTTON_BYTE_ADDR_LOW, [byte_low_value], "MainRAM"))
        writes_list.append((RAM.BUTTON_BYTE_ADDR_HIGH, [byte_high_value], "MainRAM"))

        # --- 2. Construct Analog Stick Bytes ---
        analog_axis_addresses = {
            "P1 R_Y": RAM.ANALOG_START_ADDR,
            "P1 R_X": RAM.ANALOG_START_ADDR + 1,
            "P1 L_Y": RAM.ANALOG_START_ADDR + 2,
            "P1 L_X": RAM.ANALOG_START_ADDR + 3,
        }

        # Iterate through desired_inputs and add writes only for present analog axes.
        for stick_axis, value_to_set in desired_inputs.items():
            if stick_axis in analog_axis_addresses:
                clamped_value = max(0, min(255, value_to_set))
                writes_list.append((analog_axis_addresses[stick_axis], [clamped_value], "MainRAM"))

        # --- 3. Send all constructed writes to BizHawk ---
        try:
            await bizhawk.write(self.bizhawk_client_context.bizhawk_ctx, writes_list)
        except Exception as e:
            print(f"ERROR: Failed to send input memory writes: {e}")
            raise

        # --- MonkeyMashHandler class ---

class MonkeyMashHandler:
    MAX_TRAP_DURATION = 20  # Maximum duration for the trap in seconds

    def __init__(self, bizhawk_client_context: Union["BizHawkClientContext", None]):
        self.bizhawk_client_context = bizhawk_client_context
        self.bizhawk_context = bizhawk_client_context.bizhawk_ctx if bizhawk_client_context else None

        self.is_active = False
        self.duration = 0
        self.remaining_time = 0
        self.last_update = 0

        self.pause = False

        self.input_controller = ApeEscapeMemoryInput(
            self.bizhawk_client_context) if self.bizhawk_client_context else None

        self.input_frequency = 1      # Time between NEW random inputs (e.g., generate new input every 1s)
        self.last_input_time = 0

        self.input_hold_time = 0.5      # How long the inputs will be pressed

        self.current_held_inputs = {}   # Stores inputs that are currently being pressed
        self.press_start_time = None    # Timestamp when the current brief press started
        self.sentMessage = True         # To track if the last activation sent a Bizhawk message on expiration

    def activate_monkey(self, duration_seconds: int):
        if not self.is_active:
            self.is_active = True
            self.duration = duration_seconds
            self.remaining_time = duration_seconds
            self.last_update = time.time()
            self.last_input_time = 0
            self.current_held_inputs = {}
            self.press_start_time = None
            print(f"Monkey Button Mash activated for {duration_seconds} seconds.")
        else:
            new_remaining_time = self.remaining_time + duration_seconds
            self.remaining_time = min(new_remaining_time, self.MAX_TRAP_DURATION)
            self.duration = self.remaining_time
            print(f"Monkey Button Mash extended by {duration_seconds} seconds. Total remaining: {self.remaining_time:.2f}s (capped at {self.MAX_TRAP_DURATION}s)")
        self.sentMessage = False
    async def send_monkey_inputs(self):
        if self.input_controller is None or self.bizhawk_client_context.bizhawk_ctx.connection_status != bizhawk.ConnectionStatus.CONNECTED:
            print("Error: BizHawk connection not ready for inputs. Cannot send inputs.")
            self.is_active = False
            self.current_held_inputs = {}
            self.press_start_time = None
            return

        current_time = time.time()

        if self.pause:
            self.current_held_inputs = {}
            self.press_start_time = None
            self.last_update = current_time
            return

        if self.is_active and self.remaining_time > 0:
            elapsed_time_since_last_update = current_time - self.last_update
            self.remaining_time -= elapsed_time_since_last_update
            self.last_update = current_time

            if self.remaining_time <= 0:
                self.remaining_time = 0

            # State 1: It's time to generate a NEW input sequence (press for hold_time)
            if current_time - self.last_input_time >= self.input_frequency:
                newly_generated_inputs = {}

                # Randomly select MULTIPLE inputs (digital buttons or the "Right Joystick" pseudo-input)
                num_inputs_to_change = random.randint(1, 3)
                inputs_to_change = random.sample(self.input_controller.all_inputs, num_inputs_to_change)

                for input_name in inputs_to_change:
                    if input_name == RAM.RIGHT_JOYSTICK_PSEUDO_INPUT:  # Handle the Right Joystick as one unit
                        # Randomly pick one axis to be 0xFF, the other to be random
                        axis_to_be_max = random.choice(["P1 R_Y", "P1 R_X"])
                        axis_to_be_random = "P1 R_Y" if axis_to_be_max == "P1 R_X" else "P1 R_X"

                        newly_generated_inputs[axis_to_be_max] = 0xFF
                        newly_generated_inputs[axis_to_be_random] = random.randint(0x00, 0xFF)
                        # Left Joystick values are not touched here.
                    else:
                        # For digital buttons, set to pressed (True)
                        newly_generated_inputs[input_name] = True

                self.current_held_inputs = newly_generated_inputs
                self.press_start_time = current_time
                self.last_input_time = current_time

                #print(f"[{self.remaining_time:.2f}s remaining] Initiating brief press of: {self.current_held_inputs}")

            # State 2: Check if a brief press is active and within its hold window
            if self.press_start_time is not None and (current_time - self.press_start_time < self.input_hold_time):
                try:
                    await self.input_controller.set_inputs(self.current_held_inputs)
                except bizhawk.NotConnectedError:
                    print("BizHawk connection lost during input hold. Deactivating monkey.")
                    self.is_active = False
                    self.current_held_inputs = {}
                    self.press_start_time = None
                    return
                except Exception as e:
                    print(f"Failed to hold inputs via memory write: {e}")
                    self.is_active = False
                    print("Monkey Button Mash deactivated due to input hold error.")
                    return
            else:
                # State 3: If no press is active, or hold time has expired, stop sending *active* inputs.
                if self.current_held_inputs or self.press_start_time is not None:
                    print(f"[{self.remaining_time:.2f}s remaining] Releasing inputs. Held: {self.current_held_inputs}")

                    self.current_held_inputs = {}  # Clear tracker for *briefly held* inputs
                    self.press_start_time = None  # Reset press start time

        if self.is_active and self.remaining_time <= 0:
            self.is_active = False
            self.remaining_time = 0
            self.current_held_inputs = {}
            self.press_start_time = None
            print("Monkey Button Mash finished.")

class RainbowCookieHandler:
    """
    Manages the state and effects of the Rainbow Cookie power-up.
    When active, makes Spike invincible and activates his golden form.
    """
    MAX_DURATION = 20  # Maximum duration for the Rainbow Cookie in seconds

    def __init__(self, bizhawk_client_context: Union["BizHawkClientContext", None]):
        self.bizhawk_client_context = bizhawk_client_context
        self.bizhawk_context = bizhawk_client_context.bizhawk_ctx if bizhawk_client_context else None

        self.is_active = False          # True if Rainbow Cookie effects are currently active
        self.duration = 0               # The initial or current duration set for the cookie
        self.remaining_time = 0         # How much time is left for the effects
        self.last_update = 0            # Timestamp of the last update, for calculating elapsed time
        self.pause = False              # Flag to pause the cookie's timer/effects
        self.sentMessage = True         # To track if the last activation sent a Bizhawk message on expiration
    async def activate_rainbow_cookie(self, duration_seconds: int):
        """
        Activates the Rainbow Cookie effects (invincibility and golden form).
        If already active, extends the duration up to MAX_DURATION.

        Args:
            duration_seconds (int): The number of seconds to activate/extend the cookie's effects.
        """
        if not self.is_active:
            # First activation
            self.is_active = True
            self.duration = duration_seconds
            self.remaining_time = duration_seconds
            self.last_update = time.time()
            print(f"Rainbow Cookie activated for {duration_seconds} seconds.")
            await self._apply_effects(True) # Apply effects immediately
        else:
            # Extend existing duration
            new_remaining_time = self.remaining_time + duration_seconds
            self.remaining_time = min(new_remaining_time, self.MAX_DURATION)
            self.duration = self.remaining_time # Update current duration if extended
            print(
                f"Rainbow Cookie extended by {duration_seconds} seconds. Total remaining: {self.remaining_time:.2f}s (capped at {self.MAX_DURATION}s)")
        self.sentMessage = False
    async def _apply_effects(self, enable: bool):
        """
        Internal method to apply or remove the Rainbow Cookie's effects
        by writing to BizHawk memory addresses.

        Args:
            enable (bool): If True, enables effects; if False, disables them.
        """
        if self.bizhawk_context is None or self.bizhawk_context.connection_status != bizhawk.ConnectionStatus.CONNECTED:
            print("Warning: BizHawk not connected. Cannot apply/remove Rainbow Cookie effects.")
            return

        writes_list = []
        invincible_value = RAM.INVINCIBLE_ON_VALUE if enable else RAM.INVINCIBLE_OFF_VALUE
        golden_value = RAM.GOLDEN_ON_VALUE if enable else RAM.GOLDEN_OFF_VALUE

        invincible_bytes = list(invincible_value.to_bytes(4, "little"))

        writes_list.append((RAM.SPIKE_INVINCIBILITY_ADDR, invincible_bytes, "MainRAM"))
        writes_list.append((RAM.SPIKE_GOLDEN_FORM_ADDR, [golden_value], "MainRAM"))

        try:
            await bizhawk.write(self.bizhawk_context, writes_list)
            print(f"Rainbow Cookie effects {'applied' if enable else 'removed'}.")
        except Exception as e:
            print(f"ERROR: Failed to {'apply' if enable else 'remove'} Rainbow Cookie effects: {e}")
            raise

    async def update_state_and_deactivate(self):
        """
        Updates the remaining time for the Rainbow Cookie.
        If the duration runs out, deactivates the effects.
        This method should be called periodically in the main loop of the client.
        It also re-applies the golden visual effect if it's lost and the cookie is active.
        """
        if not self.is_active:
            return

        if self.pause:
            # If paused, don't decrement remaining_time, but update last_update
            # to prevent a large time jump when unpaused.
            self.last_update = time.time()
            return

        current_time = time.time()
        elapsed_time_since_last_update = current_time - self.last_update
        self.remaining_time -= elapsed_time_since_last_update
        self.last_update = current_time

        # Check and re-apply golden visual effect if it's not active but the cookie is
        if self.bizhawk_context and self.bizhawk_context.connection_status == bizhawk.ConnectionStatus.CONNECTED:
            try:
                # Read the current value of the golden form address
                current_golden_value_bytes = await bizhawk.read(self.bizhawk_context, [(RAM.SPIKE_GOLDEN_FORM_ADDR, 1, "MainRAM")])
                current_golden_value = int.from_bytes(current_golden_value_bytes[0], byteorder="little")

                if current_golden_value is not None and current_golden_value != RAM.GOLDEN_ON_VALUE:
                    print("Rainbow Cookie active, but golden visual effect lost. Reapplying...")
                    await self._apply_effects(True)
            except Exception as e:
                print(f"ERROR: Failed to read golden form address for reapplication: {e}")
                # Log error but don't stop the loop for this non-critical re-application check

        if self.remaining_time <= 0:
            self.remaining_time = 0
            self.is_active = False
            print("Rainbow Cookie duration finished. Deactivating effects.")
            await self._apply_effects(False) # Remove effects

class StunTrapHandler:
    """
    Manages the state and effects of the Stun Trap.
    When active, makes Spike invincible and activates his golden form.
    """
    MAX_DURATION = 2

    def __init__(self, bizhawk_client_context: Union["BizHawkClientContext", None]):
        self.bizhawk_client_context = bizhawk_client_context
        self.bizhawk_context = bizhawk_client_context.bizhawk_ctx if bizhawk_client_context else None

        self.is_active = False          # True if Rainbow Cookie effects are currently active
        self.RoomType = "Special"
        self.duration = 0               # The initial or current duration set for the cookie
        self.remaining_time = 0         # How much time is left for the effects
        self.last_update = 0            # Timestamp of the last update, for calculating elapsed time
        self.pause = False              # Flag to pause the cookie's timer/effects
        self.lastspikestate = 0x00      # To store last SpikeState on activation
        self.sentMessage = True         # To track if the last activation sent a Bizhawk message on expiration
    async def activate_StunTrap(self, duration_seconds: int,lastspikestate,currentRoom):
        """
        Activates the Stun Trap effects.
        If already active, extends the duration up to MAX_DURATION.

        Args:
            duration_seconds (int): The number of seconds to activate/extend the cookie's effects.
        """
        # Only store a new lastspikestate if the trap is not activated
        # (Since if it's already active we already have the last spike state)
        if not self.is_active:
            self.lastspikestate = lastspikestate
        # First activation
        self.is_active = True

        read_list = []
        read_list += [(RAM.SpecialRoom_CameraMode, 1, "MainRAM"),(RAM.Boss_CameraMode, 1, "MainRAM"),(RAM.Inside_CameraMode, 1, "MainRAM")]
        CameraMode_reads = await bizhawk.read(self.bizhawk_context, read_list)
        isSpecialRoom = int.from_bytes(CameraMode_reads[0], byteorder="little") == 0x01
        isBossRoom = int.from_bytes(CameraMode_reads[1], byteorder="little") == 0x01
        isInside  = int.from_bytes(CameraMode_reads[2], byteorder="little") == 0x01
        if isSpecialRoom:
            self.RoomType = "Special"
        elif isBossRoom:
            self.RoomType = "Boss"
        elif isInside:
            self.RoomType = "Inside"
        else:
            self.RoomType = "Outside"

        self.duration = duration_seconds
        self.remaining_time = duration_seconds
        self.last_update = time.time()
        print(f"Stun Trap activated for {duration_seconds} seconds.")
        await self._apply_effects(True,currentRoom) # Apply effects immediately
        #else:
        # Activate it each time, do not extend it
        # Extend existing duration
        #new_remaining_time = self.remaining_time + duration_seconds
        #self.remaining_time = min(new_remaining_time, self.MAX_DURATION)
        #self.duration = self.remaining_time # Update current duration if extended
        #print(f"Stun Trap extended by {duration_seconds} seconds. Total remaining: {self.remaining_time:.2f}s (capped at {self.MAX_DURATION}s)")
        #self.sentMessage = False
    async def _apply_effects(self, enable: bool,currentRoom):
        """
        Internal method to apply or remove the Rainbow Cookie's effects
        by writing to BizHawk memory addresses.

        Args:
            enable (bool): If True, enables effects; if False, disables them.
        """
        if self.bizhawk_context is None or self.bizhawk_context.connection_status != bizhawk.ConnectionStatus.CONNECTED:
            print("Warning: BizHawk not connected. Cannot apply/remove Stun Trap effects.")
            return

        writes_list = []
        Spike_PosUpdatesAddress = RAM.Spike_PosUpdates
        Spike_PosUpdates_keys = list(Spike_PosUpdatesAddress.keys())
        Spike_PosUpdates_values = list(Spike_PosUpdatesAddress.values())

        #for x in range(len(Spike_PosUpdates_keys)):
        #    PosUpdates_values = list(Spike_PosUpdates_values[x])
        #    PosUpdates_bytes = PosUpdates_values[0]
        #    PosUpdates_onvalue = PosUpdates_values[1].to_bytes(PosUpdates_bytes, "little")
        #    PosUpdates_offvalue = PosUpdates_values[2].to_bytes(PosUpdates_bytes, "little")
        #    PosUpdates_address = (Spike_PosUpdates_keys[x])
        if enable:
            writes_list += [(RAM.Spike_CanMove, 0x01.to_bytes(1,"little"), "MainRAM")]
        else:
            writes_list += [(RAM.Spike_CanMove, 0x00.to_bytes(1,"little"), "MainRAM")]

        Spike_VelocityUpdatesAddress = RAM.Spike_VelocityUpdates
        Spike_VelocityUpdates_keys = list(Spike_VelocityUpdatesAddress.keys())
        Spike_VelocityUpdates_values = list(Spike_VelocityUpdatesAddress.values())

        #for x in range(len(Spike_VelocityUpdates_keys)):
        #    VelocityUpdates_values = list(Spike_VelocityUpdates_values[x])
        #    VelocityUpdates_bytes = VelocityUpdates_values[0]
        #    VelocityUpdates_onvalue = VelocityUpdates_values[1].to_bytes(VelocityUpdates_bytes, "little")
        #    VelocityUpdates_offvalue = VelocityUpdates_values[2].to_bytes(VelocityUpdates_bytes, "little")
        #    VelocityUpdates_address = (Spike_VelocityUpdates_keys[x])
        #    if enable:
        #        writes_list += [(VelocityUpdates_address, VelocityUpdates_offvalue, "MainRAM")]
        #    else:
        #        writes_list += [(VelocityUpdates_address, VelocityUpdates_onvalue, "MainRAM")]

        #LastState = self.lastspikestate

        #InvalidLastStates = [0x80, 0x81, 0x82, 0x83, 0x84,0x2F,0x30,0x58]
        # If enabling the Trap set it to 0x58, else set it to the last saved state
        #if enable:
        #    Spikestate2_value = 0x58
        #    CameraMode = 0x00
        #else:
        #    #If LastState is invalid,
        #    Spikestate2_value = 0x00 if LastState in InvalidLastStates else LastState
        #    CameraMode = 0x01
        #    self.lastspikestate = 0x00

        #SpecialRooms = [30,83, 84, 87, 88, 90, 91]
        #BossRooms = [item for item in RAM.bossListLocal.keys() if item not in SpecialRooms]

        #if self.RoomType == "Special":
        #    CameraModeAddress = RAM.SpecialRoom_CameraMode
        #elif self.RoomType == "Boss":
        #    CameraModeAddress = RAM.Boss_CameraMode
        #else:
        #    if self.RoomType == "Inside":
        #        CameraModeAddress = RAM.Inside_CameraMode
        #    else:
        #        CameraModeAddress = RAM.Outside_CameraMode

        #Spikestate2_bytes = list(Spikestate2_value.to_bytes(1, "little"))
        #CameraMode_bytes = list(CameraMode.to_bytes(1, "little"))

        #writes_list.append((RAM.spikeState2Address, Spikestate2_bytes, "MainRAM"))
        #writes_list.append((CameraModeAddress, CameraMode_bytes, "MainRAM"))

        try:
            await bizhawk.write(self.bizhawk_context, writes_list)
            print(f"Stun Trap effects {'applied' if enable else 'removed'}.")
        except Exception as e:
            print(f"ERROR: Failed to {'apply' if enable else 'remove'} Stun Trap effects: {e}")
            raise

    async def update_state_and_deactivate(self,currentRoom):
        """
        Updates the remaining time for the Rainbow Cookie.
        If the duration runs out, deactivates the effects.
        This method should be called periodically in the main loop of the client.
        It also re-applies the golden visual effect if it's lost and the cookie is active.
        """
        if not self.is_active:
            return

        if self.pause:
            # If paused, don't decrement remaining_time, but update last_update
            # to prevent a large time jump when unpaused.
            self.last_update = time.time()
            return

        current_time = time.time()
        elapsed_time_since_last_update = current_time - self.last_update
        self.remaining_time -= elapsed_time_since_last_update
        self.last_update = current_time

        if self.remaining_time <= 0:
            self.remaining_time = 0
            self.is_active = False
            print("Stun Trap duration finished. Deactivating effects.")
            await self._apply_effects(False,currentRoom) # Remove effects

class CameraRotateHandler:
    """
    Manages the state and effects of the Rainbow Cookie power-up.
    When active, makes Spike invincible and activates his golden form.
    """
    MAX_DURATION = 40  # Maximum duration for the Rainbow Cookie in seconds

    def __init__(self, bizhawk_client_context: Union["BizHawkClientContext", None]):
        self.bizhawk_client_context = bizhawk_client_context
        self.bizhawk_context = bizhawk_client_context.bizhawk_ctx if bizhawk_client_context else None
        self.chosen_side = "Left"       # Store which side the Camera Rotate is currently on
        self.RoomType = "Special"
        self.is_active = False          # True if effects are currently active
        self.duration = 0               # The initial or current duration set
        self.remaining_time = 0         # How much time is left for the effects
        self.last_update = 0            # Timestamp of the last update, for calculating elapsed time
        self.pause = False              # Flag to pause the timer/effects
        self.sentMessage = True         # To track if the last activation sent a Bizhawk message on expiration
    async def activate_camera_rotate(self, duration_seconds: int, currentRoom):
        """
        Activates the Rainbow Cookie effects (invincibility and golden form).
        If already active, extends the duration up to MAX_DURATION.

        Args:
            duration_seconds (int): The number of seconds to activate/extend the cookie's effects.
        """
        if not self.is_active:
            # First activation
            self.is_active = True
            self.duration = duration_seconds
            self.remaining_time = duration_seconds
            self.last_update = time.time()
            possibleSides = ["Left","Right"]
            self.chosen_side = possibleSides[random.randint(0,1)]
            print(f"Camera Rotate activated for {duration_seconds} seconds.")

        else:
            ## Extend existing duration
            new_remaining_time = self.remaining_time + duration_seconds
            self.remaining_time = min(new_remaining_time, self.MAX_DURATION)
            self.duration = self.remaining_time # Update current duration if extended
            print(f"Camera Rotate extended by {duration_seconds} seconds. Total remaining: {self.remaining_time:.2f}s (capped at {self.MAX_DURATION}s)")

        await self._apply_effects(True, currentRoom)  # Apply effects immediately
        self.sentMessage = False
    async def _apply_effects(self, enable: bool,currentRoom):
        """
        Internal method to apply or remove the Rainbow Cookie's effects
        by writing to BizHawk memory addresses.

        Args:
            enable (bool): If True, enables effects; if False, disables them.
        """
        if self.bizhawk_context is None or self.bizhawk_context.connection_status != bizhawk.ConnectionStatus.CONNECTED:
            print("Warning: BizHawk not connected. Cannot apply/remove Rainbow Cookie effects.")
            return
        read_list = []
        read_list += [(RAM.SpecialRoom_CameraMode, 1, "MainRAM"),(RAM.Boss_CameraMode, 1, "MainRAM"),(RAM.Inside_CameraMode, 1, "MainRAM")]
        CameraMode_reads = await bizhawk.read(self.bizhawk_context, read_list)
        isSpecialRoom = int.from_bytes(CameraMode_reads[0], byteorder="little") == 0x01
        isBossRoom = int.from_bytes(CameraMode_reads[1], byteorder="little") == 0x01
        isInside  = int.from_bytes(CameraMode_reads[2], byteorder="little") == 0x01
        if isSpecialRoom:
            self.RoomType = "Special"
        elif isBossRoom:
            self.RoomType = "Boss"
        elif isInside:
            self.RoomType = "Inside"
        else:
            self.RoomType = "Outside"
        writes_list = []
        #SpecialRooms = [83, 84, 87, 88, 90, 91]
        #BossRooms = [item for item in RAM.bossListLocal.keys() if item not in SpecialRooms]

        #InABossRoom = False

        CameraRotate_value = 0xFF if enable else 0x00
        CameraRotate_bytes = list(CameraRotate_value.to_bytes(1, "little"))

        LeftRotateAddress2 = ""
        LeftRotateAddress = ""
        RightRotateAddress = ""
        RightRotateAddress2 = ""

        if self.RoomType == "Special":
            LeftRotateAddress = RAM.SpecialRoom_CameraRotateLeft
            RightRotateAddress = RAM.SpecialRoom_CameraRotateRight
        elif self.RoomType == "Boss":
            LeftRotateAddress = RAM.Boss_CameraRotateLeft
            RightRotateAddress = RAM.Boss_CameraRotateRight
        else:
            if self.RoomType == "Inside":
                LeftRotateAddress = RAM.Inside_CameraRotateLeft
                RightRotateAddress = RAM.Inside_CameraRotateLeft
            else:
                LeftRotateAddress = RAM.Outside_CameraRotateLeft
                RightRotateAddress = RAM.Outside_CameraRotateRight

        if self.chosen_side == "Left":
            writes_list.append((LeftRotateAddress, CameraRotate_bytes, "MainRAM"))
        else:
            writes_list.append((RightRotateAddress, CameraRotate_bytes, "MainRAM"))

        try:
            await bizhawk.write(self.bizhawk_context, writes_list)
            print(f"Camera Rotate effects {'applied' if enable else 'removed'}.")
        except Exception as e:
            print(f"ERROR: Failed to {'apply' if enable else 'remove'} Camera Rotate effects: {e}")
            raise

    async def update_state_and_deactivate(self,currentRoom):
        """
        Updates the remaining time for the Camera Rotate.
        If the duration runs out, deactivates the effects.
        This method should be called periodically in the main loop of the client.
        It also re-applies the camera Rotate effect if it's lost and the cookie is active.
        """
        if not self.is_active:
            return

        if self.pause:
            # If paused, don't decrement remaining_time, but update last_update
            # to prevent a large time jump when unpaused.
            self.last_update = time.time()
            return

        current_time = time.time()
        elapsed_time_since_last_update = current_time - self.last_update
        self.remaining_time -= elapsed_time_since_last_update
        self.last_update = current_time

        # Check and re-apply Rotate effect if it's not active but the effect is
        if self.bizhawk_context and self.bizhawk_context.connection_status == bizhawk.ConnectionStatus.CONNECTED:
            try:
                #SpecialRooms = [83, 84, 87, 88, 90, 91]
                #BossRooms = [item for item in RAM.bossListLocal.keys() if item not in SpecialRooms]
                #InABossRoom = False
                read_list = []
                read_list += [(RAM.SpecialRoom_CameraMode, 1, "MainRAM"), (RAM.Boss_CameraMode, 1, "MainRAM"),(RAM.Inside_CameraMode, 1, "MainRAM")]
                CameraMode_reads = await bizhawk.read(self.bizhawk_context, read_list)
                isSpecialRoom = int.from_bytes(CameraMode_reads[0], byteorder="little") == 0x01
                isBossRoom = int.from_bytes(CameraMode_reads[1], byteorder="little") == 0x01
                isInside = int.from_bytes(CameraMode_reads[2], byteorder="little") == 0x01
                if isSpecialRoom:
                    self.RoomType = "Special"
                elif isBossRoom:
                    self.RoomType = "Boss"
                elif isInside:
                    self.RoomType = "Inside"
                else:
                    self.RoomType = "Outside"
                CameraRotate_value = 0xFF
                if self.RoomType == "Special":
                    LeftRotateAddress = RAM.SpecialRoom_CameraRotateLeft
                    RightRotateAddress = RAM.SpecialRoom_CameraRotateRight
                elif self.RoomType == "Boss":
                    LeftRotateAddress = RAM.Boss_CameraRotateLeft
                    RightRotateAddress = RAM.Boss_CameraRotateRight
                else:
                    if self.RoomType == "Inside":
                        LeftRotateAddress = RAM.Inside_CameraRotateLeft
                        RightRotateAddress = RAM.Inside_CameraRotateLeft
                    else:
                        LeftRotateAddress = RAM.Outside_CameraRotateLeft
                        RightRotateAddress = RAM.Outside_CameraRotateRight

                if self.chosen_side == "Left":
                    CameraRotateAddress = LeftRotateAddress
                else:
                    CameraRotateAddress = RightRotateAddress

                # Read the current value of the chosen CameraRotate address
                current_camera_rotate_bytes = await bizhawk.read(self.bizhawk_context, [(CameraRotateAddress, 1, "MainRAM")])
                current_camera_rotate = int.from_bytes(current_camera_rotate_bytes[0], byteorder="little")

                if current_camera_rotate is not None and current_camera_rotate != 0xFF:
                    print("Camera Rotate active, but rotate effect lost. Reapplying...")
                    await self._apply_effects(True,currentRoom)
            except Exception as e:
                print(f"ERROR: Failed to read rotate form address for reapplication: {e}")
                # Log error but don't stop the loop for this non-critical re-application check

        if self.remaining_time <= 0:
            self.remaining_time = 0
            self.is_active = False
            print("Camera Rotate duration finished. Deactivating effects.")
            await self._apply_effects(False,currentRoom) # Remove effects
