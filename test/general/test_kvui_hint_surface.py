"""Source contract for the legacy hint surface in kvui.py.

AST-parses kvui.py without importing it (importing the GUI branch pulls in
mwgg_gui and kivy.core.window, which opens an SDL window): the classic hint
classes moved to mwgg_gui, so the GUI branch must bind the old kvui names --
as reimport aliases or small real classes -- star-import the legacyhint
module, re-export the ref-emitting parser as KivyJSONtoTextParser, and the
stray openpyxl import must stay gone.
"""
import ast
import os
import unittest

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
KVUI_PATH = os.path.join(REPO_ROOT, "kvui.py")

# Old kvui names still imported by world wheels and worlds/tracker; bound via
# class def, assignment, or import alias. HintLog/HintLabel/HintLayout/
# MarkupDropdown, the status_* tables and remove_between_brackets arrive
# through the legacyhint star import (checked separately).
LEGACY_NAMES = {
    "MarkupToolTip", "ToolTip", "TooltipLabel", "HovererableLabel",
    "ColumnSorter", "ColumnSortMixin", "ColumnFilter", "ColumnFilterMixin",
    "ColumnFilterMulti", "ColumnFilterItemClassification", "ExtraColumn",
    "ClassicHintScreen",
}


class TestKvuiHintSurface(unittest.TestCase):
    tree: ast.Module
    gui_branch: list

    @classmethod
    def setUpClass(cls) -> None:
        with open(KVUI_PATH, encoding="utf-8") as f:
            cls.tree = ast.parse(f.read(), filename=KVUI_PATH)
        # Module shape: imports, then one top-level `if MWGG_FRONTEND == tui`
        # whose orelse is the GUI branch.
        top_if = next(node for node in cls.tree.body if isinstance(node, ast.If))
        cls.gui_branch = top_if.orelse

    def test_gui_branch_binds_legacy_names(self) -> None:
        bound = set()
        for node in self.gui_branch:
            if isinstance(node, ast.ClassDef):
                bound.add(node.name)
            elif isinstance(node, ast.Assign):
                bound.update(t.id for t in node.targets if isinstance(t, ast.Name))
            elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
                bound.add(node.target.id)
            elif isinstance(node, ast.ImportFrom):
                bound.update(alias.asname or alias.name for alias in node.names)
        missing = LEGACY_NAMES - bound
        self.assertFalse(
            missing,
            f"legacy hint names missing from the GUI branch: {sorted(missing)}",
        )

    def test_gui_branch_star_imports_legacyhint(self) -> None:
        for node in self.gui_branch:
            if (isinstance(node, ast.ImportFrom)
                    and node.module == "mwgg_gui.hint.legacyhint"
                    and any(alias.name == "*" for alias in node.names)):
                return
        self.fail(
            "GUI branch must `from mwgg_gui.hint.legacyhint import *` "
            "(supplies HintLog/HintLabel/HintLayout/MarkupDropdown)"
        )

    def test_ref_parser_reexported_as_kivy_json_to_text_parser(self) -> None:
        for node in self.gui_branch:
            if isinstance(node, ast.ImportFrom) and node.module == "NetUtils":
                aliases = {alias.asname or alias.name: alias.name for alias in node.names}
                if aliases.get("KivyJSONtoTextParser") == "KivyMarkupJSONtoTextParser":
                    return
        self.fail(
            "GUI branch must re-export NetUtils.KivyMarkupJSONtoTextParser as KivyJSONtoTextParser"
        )

    def test_openpyxl_never_imported(self) -> None:
        for node in ast.walk(self.tree):
            if isinstance(node, ast.Import):
                modules = [alias.name for alias in node.names]
            elif isinstance(node, ast.ImportFrom):
                modules = [node.module or ""]
            else:
                continue
            for module in modules:
                self.assertNotEqual(
                    module.split(".")[0], "openpyxl",
                    f"stray openpyxl import at kvui.py:{node.lineno}",
                )


if __name__ == "__main__":
    unittest.main()
