from __future__ import annotations

import asyncio
import re
# webserver imports
import urllib.parse
from collections.abc import Iterable

import Utils
from BaseClasses import CollectionState, Location
from CommonClient import logger, get_base_parser, gui_enabled, server_loop

apname = Utils.instance_name if Utils.instance_name else "Archipelago"
from MultiServer import mark_raw
from NetUtils import JSONMessagePart
#from Gui import CommandPromptTextInput
from .logic.logic import StardewLogic
from .stardew_rule.rule_explain import explain, ExplainMode, RuleExplanation

try:
    from worlds.tracker.TrackerClient import TrackerGameContext, TrackerCommandProcessor as ClientCommandProcessor, UT_VERSION  # noqa
    from worlds.tracker.TrackerCore import TrackerCore

    tracker_loaded = True
except ImportError as e:
    logger.error(e)
    from CommonClient import CommonContext, ClientCommandProcessor

    TrackerCore = object


    class TrackerGameContextMixin:
        """Expecting the TrackerGameContext to have these methods."""
        tracker_core: TrackerCore

        def make_gui(self, manager):
            ...

        def run_generator(self):
            ...


    class TrackerGameContext(CommonContext, TrackerGameContextMixin):
        pass


    tracker_loaded = False
    UT_VERSION = "Not found"


class StardewCommandProcessor(ClientCommandProcessor):
    ctx: StardewClientContext

    @mark_raw
    def _cmd_explain(self, location: str = ""):
        """Explain the logic behind a location."""
        logic = self.ctx.logic
        if logic is None:
            return

        try:
            rule = logic.region.can_reach_location(location)
            expl = explain(rule, self.ctx.current_state, expected=None, mode=ExplainMode.CLIENT)
        except KeyError:

            result, usable, response = Utils.get_intended_text(location, [loc.name for loc in self.ctx.all_locations])
            if usable:
                rule = logic.region.can_reach_location(result)
                expl = explain(rule, self.ctx.current_state, expected=None, mode=ExplainMode.CLIENT)
            else:
                self.ctx.ui.last_autofillable_command = "/explain"
                self.output(response)
                return

        self.ctx.previous_explanation = expl
        self.ctx.ui.print_json(parse_explanation(expl))

    @mark_raw
    def _cmd_explain_item(self, item: str = ""):
        """Explain the logic behind a game item."""
        logic = self.ctx.logic
        if logic is None:
            return

        result, usable, response = Utils.get_intended_text(item, logic.registry.item_rules.keys())
        if usable:
            rule = logic.has(result)
            expl = explain(rule, self.ctx.current_state, expected=None, mode=ExplainMode.CLIENT)
        else:
            self.ctx.ui.last_autofillable_command = "/explain_item"
            self.output(response)
            return

        self.ctx.previous_explanation = expl
        self.ctx.ui.print_json(parse_explanation(expl))

    @mark_raw
    def _cmd_explain_missing(self, location: str = ""):
        """Explain what is missing for a location to be in logic. It explains the logic behind a location, while skipping the rules that are already satisfied."""
        self.__explain("/explain_missing", location, expected=True)

    @mark_raw
    def _cmd_explain_how(self, location: str = ""):
        """Explain how a location is in logic. It explains the logic behind the location, while skipping the rules that are not satisfied."""
        self.__explain("/explain_how", location, expected=False)

    def __explain(self, command: str, location: str, expected: bool | None = None):
        logic = self.ctx.logic
        if logic is None:
            return

        try:
            rule = logic.region.can_reach_location(location)
            expl = explain(rule, self.ctx.current_state, expected=expected, mode=ExplainMode.CLIENT)
        except KeyError:

            result, usable, response = Utils.get_intended_text(location, [loc.name for loc in self.ctx.all_locations])
            if usable:
                rule = logic.region.can_reach_location(result)
                expl = explain(rule, self.ctx.current_state, expected=expected, mode=ExplainMode.CLIENT)
            else:
                self.ctx.ui.last_autofillable_command = command
                self.output(response)
                return

        self.ctx.previous_explanation = expl
        self.ctx.ui.print_json(parse_explanation(expl))

    @mark_raw
    def _cmd_more(self, index: str = ""):
        """Will tell you what's missing to consider a location in logic."""
        if self.ctx.previous_explanation is None:
            self.output("No previous explanation found.")
            return

        try:
            expl = self.ctx.previous_explanation.more(int(index))
        except (ValueError, IndexError):
            self.output("Which previous rule do you want to explained?")
            self.ctx.ui.last_autofillable_command = "/more"
            for i, rule in enumerate(self.ctx.previous_explanation.more_explanations):
                # TODO handle autofillable commands
                self.output(f"/more {i} -> {str(rule)})")
            return

        self.ctx.previous_explanation = expl
        self.ctx.ui.print_json(parse_explanation(expl))

    if not tracker_loaded:
        del _cmd_explain
        del _cmd_explain_missing


class StardewClientContext(TrackerGameContext):
    game = "Stardew Valley"
    command_processor = StardewCommandProcessor
    previous_explanation: RuleExplanation | None = None

    def __init__(self, server_address, password, ready_callback=None, error_callback=None):
        super().__init__(server_address, password)
        self.ready_callback = ready_callback
        self.error_callback = error_callback
        if self.ready_callback:
            from kivy.clock import Clock
            Clock.schedule_once(self.ready_callback, 0.1)
    # def make_gui(self):
    #     ui = super().make_gui()  # before the kivy imports so Gui gets loaded first

    #     class StardewManager(ui):
    #         base_title = f"Stardew Valley Tracker with UT {UT_VERSION} for AP version"  # core appends ap version so this works
    #         ctx: StardewClientContext

    #         def build(self):
    #             container = super().build()
    #             if not tracker_loaded:
    #                 logger.info("To enable the tracker page, install Universal Tracker.")

    #             # Until self.ctx.ui.last_autofillable_command allows for / commands, this is needed to remove the "!" before the /commands when using intended text autofill.
    #             def on_text_remove_hardcoded_exclamation_mark_garbage(textinput: CommandPromptTextInput, text: str) -> None:
    #                 if text.startswith("!/"):
    #                     textinput.text = text[1:]

    #             self.textinput.bind(text=on_text_remove_hardcoded_exclamation_mark_garbage)

    #             return container

    @property
    def logic(self) -> StardewLogic | None:
        if self.tracker_core.get_current_world() is None:
            logger.warning("Internal logic was not able to load, check your yamls and relaunch.")
            return None

        if self.game != "Stardew Valley":
            logger.warning(f"Please connect to a slot with explainable logic (not {self.game}).")
            return None

        return self.tracker_core.get_current_world().logic

    @property
    def current_state(self) -> CollectionState:
        return self.tracker_core.updateTracker().state

    @property
    def world(self) -> StardewValleyWorld:
        return self.tracker_core.get_current_world()

    @property
    def all_locations(self) -> Iterable[Location]:
        return self.tracker_core.multiworld.get_locations(self.tracker_core.player_id)


def parse_explanation(explanation: RuleExplanation) -> list[JSONMessagePart]:
    # Split the explanation in parts, by isolating all the delimiters, being \(, \), & , -> , | , \d+x , \[ , \] , \(\w+\), \n\s*
    result_regex = r"(\(|\)| & | -> | \| |\d+x | \[|\](?: ->)?\s*| \(\w+\)|\n\s*)"
    splits = re.split(result_regex, str(explanation).strip())

    messages = []
    for s in splits:
        if len(s) == 0:
            continue

        if s == "True":
            messages.append({"type": "color", "color": "green", "text": s})
        elif s == "False":
            messages.append({"type": "color", "color": "salmon", "text": s})
        elif s.startswith("Reach Location "):
            messages.append({"type": "text", "text": "Reach Location "})
            messages.append({"type": "location_name", "text": s[15:]})
        elif s.startswith("Reach Entrance "):
            messages.append({"type": "text", "text": "Reach Entrance "})
            messages.append({"type": "entrance_name", "text": s[15:]})
        elif s.startswith("Reach Region "):
            messages.append({"type": "text", "text": "Reach Region "})
            messages.append({"type": "color", "color": "yellow", "text": s[13:]})
        elif s.startswith("Received event "):
            messages.append({"type": "text", "text": "Received event "})
            messages.append({"type": "item_name", "text": s[15:]})
        elif s.startswith("Received "):
            messages.append({"type": "text", "text": "Received "})
            messages.append({"type": "item_name", "flags": 0b001, "text": s[9:]})
        elif s.startswith("Has "):
            if s[4].isdigit():
                messages.append({"type": "text", "text": "Has "})
                digit_end = re.search(r"\D", s[4:])
                digit = s[4:4 + digit_end.start()]
                messages.append({"type": "color", "color": "cyan", "text": digit})
                messages.append({"type": "text", "text": s[4 + digit_end.start():]})

            else:
                messages.append({"text": s, "type": "text"})
        else:
            messages.append({"text": s, "type": "text"})

    return messages


def get_updated_state(ctx: TrackerGameContext) -> CollectionState:
    return updateTracker(ctx).state


def launch(server_address: str = None, password: str = None, ready_callback=None, error_callback=None, slot_name: str = None):
    """
    Launch the client
    """
    import logging
    logging.getLogger("StardewClient")

    async def main():
        ctx = StardewClientContext(server_address, password, ready_callback, error_callback)
        if ctx._can_takeover_existing_gui():
            await ctx._takeover_existing_gui() 
        else:
            logger.critical("Client did not launch properly, exiting.")
            if error_callback:
                error_callback()
            return

        ctx.ui.base_title = apname + " | Stardew Valley"
        ctx.auth = slot_name
        ctx.server_task = asyncio.create_task(server_loop(ctx), name="server loop")
        await ctx.server_auth()

        if tracker_loaded:
            ctx.run_generator()
        else:
            logger.warning("Could not find Universal Tracker.")

        await ctx.exit_event.wait()
        await ctx.shutdown()

    import colorama

    # Check if we're already in an event loop (GUI mode) first
    try:
        loop = asyncio.get_running_loop()
        # We're in an existing event loop, create a task
        logger.info("Running in existing event loop (GUI mode)")
        
        task = asyncio.create_task(main(), name="StardewMain")
        return task
    except RuntimeError:
        logger.critical("This is not a standalone client. Please run the MultiWorld GUI to start the Stardew Valley client.")
        if error_callback:
            error_callback()


def main(server_address: str = None, password: str = None, ready_callback=None, error_callback=None, slot_name: str = None):
    """Main entry point for integration with MultiWorld system"""
    launch(server_address, password, ready_callback, error_callback, slot_name)
