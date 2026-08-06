"""Source contract for the restored classic hint surface in kvui.py.

AST-parses kvui.py without importing it (importing the GUI branch pulls in
mwgg_gui and kivy.core.window, which opens an SDL window): the GUI branch must
define the classic hint classes as real classes rather than aliases, bind the
supporting tables, re-export the ref-emitting parser as KivyJSONtoTextParser,
and the stray openpyxl import must stay gone.
"""
import ast
import os
import unittest

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
KVUI_PATH = os.path.join(REPO_ROOT, "kvui.py")

RESTORED_CLASSES = {
    "ToolTip", "HovererableLabel", "TooltipLabel", "MarkupDropdownTextItem",
    "MarkupDropdown", "AutocompleteHintInput", "HintLabel", "HintLayout",
    "ColumnSorter", "ColumnSortMixin", "HintLog", "ClassicHintScreen",
}
RESTORED_ASSIGNMENTS = {
    "remove_between_brackets", "status_icons", "status_names", "status_colors",
    "status_sort_weights",
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

    def test_gui_branch_defines_restored_classes(self) -> None:
        class_defs = {node.name for node in self.gui_branch if isinstance(node, ast.ClassDef)}
        missing = RESTORED_CLASSES - class_defs
        self.assertFalse(
            missing,
            f"classic hint classes missing (or demoted to aliases) in the GUI branch: {sorted(missing)}",
        )

    def test_gui_branch_binds_restored_assignments(self) -> None:
        bound = set()
        for node in self.gui_branch:
            if isinstance(node, ast.Assign):
                bound.update(t.id for t in node.targets if isinstance(t, ast.Name))
            elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
                bound.add(node.target.id)
        missing = RESTORED_ASSIGNMENTS - bound
        self.assertFalse(missing, f"classic hint tables missing from the GUI branch: {sorted(missing)}")

    def test_ref_parser_reexported_as_kivy_json_to_text_parser(self) -> None:
        for node in self.gui_branch:
            if isinstance(node, ast.ImportFrom) and node.module == "NetUtils":
                aliases = {alias.asname or alias.name: alias.name for alias in node.names}
                if aliases.get("KivyJSONtoTextParser") == "KivyRefJSONtoTextParser":
                    return
        self.fail(
            "GUI branch must re-export NetUtils.KivyRefJSONtoTextParser as KivyJSONtoTextParser"
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
