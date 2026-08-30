#!/usr/bin/env python3
"""Generate the transparent, blurred Solarized Osaka dark theme for Zed."""
import json

# --- Palette (dark), computed from solarized-osaka.nvim colors.lua HSL values ---
c = {
    "base04": "#001419", "base03": "#002c38", "base02": "#063540",
    "base01": "#576d74", "base00": "#637981", "base0": "#9eabac",
    "base1": "#adb7b7", "base2": "#ede7d3", "base3": "#fdf5e2", "base4": "#ffffff",
    "fg": "#839395",
    "yellow": "#b28500", "yellow300": "#ffbf00", "yellow500": "#b28500",
    "yellow700": "#664c00", "yellow900": "#332700",
    "orange": "#c94c16", "orange500": "#c94c16", "orange700": "#a13c10",
    "red": "#db302d", "red500": "#db302d", "red900": "#570f0e", "red950": "#380605",
    "magenta": "#d23681", "magenta500": "#d23681", "magenta900": "#541131",
    "violet": "#6d71c4", "violet500": "#6d71c4", "violet900": "#24275a",
    "blue": "#268bd3", "blue500": "#268bd3", "blue700": "#1a6397", "blue900": "#0f3856",
    "cyan": "#29a298", "cyan300": "#2aeddd", "cyan500": "#29a298",
    "cyan800": "#154e50", "cyan900": "#103a3c",
    "green": "#849900", "green500": "#849900", "green700": "#586600",
    "green900": "#2c3300",
}


def a(hex6, alpha):
    """Append an 8-bit alpha (0-255) to a #rrggbb color."""
    return f"{hex6}{alpha:02x}"


def make_style(transparent: bool):
    # Base backgrounds. In blur mode we make the primary surfaces translucent
    # so the OS blur/wallpaper shows through, while keeping panels/popups solid
    # enough to stay readable.
    bg = c["base04"]           # editor / window background
    bg_hl = c["base03"]        # highlighted background (statusline, popup)
    surface = c["base03"]
    elevated = c["base02"]

    if transparent:
        # Blur mode. The blurred wallpaper only shows through surfaces whose
        # alpha < ff. Recipe (same as jenslys/zed-catppuccin-blur):
        #  - Big content surfaces (editor, gutter, panel, toolbar, tab bar) are
        #    FULLY transparent (#00000000) so the blurred backdrop reads through.
        #  - The dark solarized tint lives on the ROOT `background` layer, which
        #    sits behind the transparent editor -> you get blur + tint + contrast.
        #  - Chrome that must stay legible (status/title bars, surfaces) uses a
        #    partial-alpha tint; popovers (elevated_surface) stay fully opaque.
        TINT_A = 0xd7     # ~84% — root/window tint over the blur
        CHROME_A = 0xd7   # ~84% — status/title bars
        SURFACE_A = 0xd0  # ~82% — surface panels
        clear = "#00000000"

        window_bg = a(c["base04"], TINT_A)     # the tint the editor shows through
        editor_bg = clear
        gutter_bg = clear
        panel_bg = clear
        toolbar_bg = clear
        tabbar_bg = clear
        tab_inactive_bg = clear
        tab_active_bg = a(c["base02"], 0xb0)
        surface_bg = a(c["base03"], SURFACE_A)
        status_bg = a(c["base03"], CHROME_A)
        title_bg = a(c["base03"], CHROME_A)
        elevated_bg = c["base02"]              # opaque: popovers stay readable
        element_bg = a(c["base02"], 0x80)
        active_line = a(c["base03"], 0x66)
    else:
        editor_bg = bg
        window_bg = bg
        panel_bg = bg
        surface_bg = surface
        elevated_bg = elevated
        status_bg = bg_hl
        title_bg = bg_hl
        toolbar_bg = bg
        tabbar_bg = bg_hl
        tab_active_bg = bg
        tab_inactive_bg = bg_hl
        gutter_bg = bg
        element_bg = c["base02"]
        active_line = a(c["base03"], 0xb3)

    style = {
        "background.appearance": "blurred" if transparent else "opaque",

        "border": c["base02"],
        "border.variant": c["base03"],
        "border.focused": c["blue700"],
        "border.selected": c["blue500"],
        "border.transparent": a(c["base02"], 0x00),
        "border.disabled": c["base03"],

        "elevated_surface.background": elevated_bg,
        "surface.background": surface_bg,
        "background": window_bg,

        "element.background": element_bg,
        "element.hover": a(c["base02"], 0x99),
        "element.active": a(c["blue900"], 0xcc),
        "element.selected": a(c["blue900"], 0xcc),
        "element.disabled": a(c["base03"], 0x80),

        "drop_target.background": a(c["blue500"], 0x40),

        "ghost_element.background": a(c["base02"], 0x00),
        "ghost_element.hover": a(c["base02"], 0x80),
        "ghost_element.active": a(c["blue900"], 0xaa),
        "ghost_element.selected": a(c["blue900"], 0xaa),
        "ghost_element.disabled": a(c["base03"], 0x80),

        "text": c["base0"],
        "text.muted": c["base00"],
        "text.placeholder": c["base01"],
        "text.disabled": c["base01"],
        "text.accent": c["blue500"],

        "icon": c["base0"],
        "icon.muted": c["base00"],
        "icon.disabled": c["base01"],
        "icon.placeholder": c["base00"],
        "icon.accent": c["blue500"],

        "status_bar.background": status_bg,
        "title_bar.background": title_bg,
        "title_bar.inactive_background": title_bg,
        "toolbar.background": toolbar_bg,
        "tab_bar.background": tabbar_bg,
        "tab.inactive_background": tab_inactive_bg,
        "tab.active_background": tab_active_bg,

        "search.match_background": a(c["yellow500"], 0x55),
        "search.active_match_background": a(c["orange500"], 0x66),

        "panel.background": panel_bg,
        "panel.focused_border": c["blue500"],
        "panel.indent_guide": a(c["base02"], 0x80),
        "panel.indent_guide_active": c["base01"],
        "panel.indent_guide_hover": c["base01"],
        "pane.focused_border": c["blue500"],
        "pane_group.border": c["base02"],

        "scrollbar.thumb.background": a(c["base1"], 0x33),
        "scrollbar.thumb.hover_background": a(c["base1"], 0x55),
        "scrollbar.thumb.border": a(c["base02"], 0x00),
        "scrollbar.track.background": a(c["base04"], 0x00),
        "scrollbar.track.border": a(c["base03"], 0x00),

        "editor.foreground": c["base0"],
        "editor.background": editor_bg,
        "editor.gutter.background": gutter_bg,
        "editor.subheader.background": surface_bg,
        "editor.active_line.background": active_line,
        "editor.highlighted_line.background": a(c["base03"], 0x99),
        "editor.line_number": c["yellow700"],
        "editor.active_line_number": c["orange500"],
        "editor.invisible": c["base01"],
        "editor.wrap_guide": a(c["base02"], 0x80),
        "editor.active_wrap_guide": c["base02"],
        "editor.indent_guide": a(c["base02"], 0x80),
        "editor.indent_guide_active": c["base01"],
        "editor.document_highlight.read_background": a(c["magenta900"], 0x88),
        "editor.document_highlight.write_background": a(c["magenta900"], 0xaa),
        "editor.document_highlight.bracket_background": a(c["red900"], 0x88),

        "terminal.background": editor_bg,
        "terminal.ansi.background": editor_bg,
        "terminal.foreground": c["fg"],
        "terminal.bright_foreground": c["base1"],
        "terminal.dim_foreground": c["base00"],
        "terminal.ansi.black": c["base04"],
        "terminal.ansi.red": c["red"],
        "terminal.ansi.green": c["green"],
        "terminal.ansi.yellow": c["yellow"],
        "terminal.ansi.blue": c["blue"],
        "terminal.ansi.magenta": c["magenta"],
        "terminal.ansi.cyan": c["cyan"],
        "terminal.ansi.white": c["base0"],
        "terminal.ansi.bright_black": c["base04"],
        "terminal.ansi.bright_red": c["red"],
        "terminal.ansi.bright_green": c["green"],
        "terminal.ansi.bright_yellow": c["yellow"],
        "terminal.ansi.bright_blue": c["blue"],
        "terminal.ansi.bright_magenta": c["magenta"],
        "terminal.ansi.bright_cyan": c["cyan"],
        "terminal.ansi.bright_white": c["fg"],

        "link_text.hover": c["blue500"],

        # Dedicated Git colors prevent the version control UI from inheriting
        # generic status colors whose semantics differ from upstream.
        "version_control.added": c["cyan500"],
        "version_control.deleted": c["red500"],
        "version_control.modified": c["yellow500"],
        "version_control.renamed": c["blue500"],
        "version_control.conflict": c["orange500"],
        "version_control.ignored": c["base01"],

        "conflict": c["orange500"],
        "conflict.background": c["red950"],
        "conflict.border": c["orange700"],

        "created": c["green500"],
        "created.background": c["green900"],
        "created.border": c["green700"],

        "deleted": c["red500"],
        "deleted.background": c["red950"],
        "deleted.border": c["red900"],

        "error": c["red500"],
        "error.background": c["red900"],
        "error.border": c["red900"],

        "hidden": c["base00"],
        "hidden.background": c["base03"],
        "hidden.border": c["base02"],

        "hint": c["cyan500"],
        "hint.background": c["cyan900"],
        "hint.border": c["cyan800"],

        "ignored": c["base01"],
        "ignored.background": c["base03"],
        "ignored.border": c["base02"],

        "info": c["blue500"],
        "info.background": c["blue900"],
        "info.border": c["blue700"],

        "modified": c["yellow500"],
        "modified.background": c["yellow900"],
        "modified.border": c["yellow700"],

        "predictive": c["base01"],
        "predictive.background": c["base03"],
        "predictive.border": c["base02"],

        "renamed": c["blue500"],
        "renamed.background": c["blue900"],
        "renamed.border": c["blue700"],

        "success": c["cyan500"],
        "success.background": c["cyan900"],
        "success.border": c["cyan800"],

        "unreachable": c["base00"],
        "unreachable.background": c["base03"],
        "unreachable.border": c["base02"],

        "warning": c["yellow500"],
        "warning.background": c["yellow900"],
        "warning.border": c["yellow700"],

        "players": [
            {"cursor": c["base0"], "background": c["base0"], "selection": a(c["base02"], 0xcc)},
            {"cursor": c["cyan500"], "background": c["cyan500"], "selection": a(c["cyan900"], 0xcc)},
            {"cursor": c["blue500"], "background": c["blue500"], "selection": a(c["blue900"], 0xcc)},
            {"cursor": c["green500"], "background": c["green500"], "selection": a(c["green900"], 0xcc)},
            {"cursor": c["magenta500"], "background": c["magenta500"], "selection": a(c["magenta900"], 0xcc)},
            {"cursor": c["orange500"], "background": c["orange500"], "selection": a(c["red950"], 0xcc)},
            {"cursor": c["violet500"], "background": c["violet500"], "selection": a(c["violet900"], 0xcc)},
            {"cursor": c["yellow500"], "background": c["yellow500"], "selection": a(c["yellow900"], 0xcc)},
        ],

        "accents": [
            c["blue500"], c["cyan500"], c["green500"], c["yellow500"],
            c["orange500"], c["red500"], c["magenta500"], c["violet500"],
        ],

        "syntax": syntax(),
    }
    return style


def s(color, weight=None, italic=False):
    d = {"color": color}
    if italic:
        d["font_style"] = "italic"
    if weight is not None:
        d["font_weight"] = weight
    return d


def syntax():
    return {
        # Comments
        "comment": s(c["base01"], italic=True),
        "comment.doc": s(c["base00"], italic=True),

        # Constants & literals -> cyan (Solarized: constants family)
        "constant": s(c["cyan500"]),
        "constant.builtin": s(c["orange500"]),
        "string": s(c["cyan500"]),
        "string.regex": s(c["cyan300"]),
        "string.escape": s(c["orange700"]),
        "string.special": s(c["orange500"]),
        "string.special.symbol": s(c["cyan500"]),
        "character": s(c["cyan500"]),
        "number": s(c["cyan500"]),
        "boolean": s(c["cyan500"]),

        # Identifiers / functions -> blue
        "variable": s(c["base0"]),
        "variable.special": s(c["orange500"]),
        "variable.builtin": s(c["orange500"]),
        "variable.parameter": s(c["orange500"]),
        "variable.member": s(c["cyan500"]),
        "property": s(c["blue500"]),
        "function": s(c["blue500"]),
        "function.builtin": s(c["orange500"]),
        "function.method": s(c["blue500"]),
        "function.special.definition": s(c["blue500"]),
        "constructor": s(c["orange500"]),

        # Keywords / statements / operators -> green
        "keyword": s(c["green500"], italic=True),
        "operator": s(c["green500"]),
        "label": s(c["green500"]),

        # Preprocessor / attributes -> red
        "preproc": s(c["red500"]),
        "attribute": s(c["red500"]),
        "embedded": s(c["base0"]),

        # Types / namespaces / enums -> yellow
        "type": s(c["yellow500"]),
        "type.builtin": s(c["yellow500"]),
        "type.super": s(c["yellow500"]),
        "namespace": s(c["yellow500"]),
        "enum": s(c["yellow500"]),

        # Punctuation / special -> orange
        "punctuation": s(c["base0"]),
        "punctuation.bracket": s(c["orange500"]),
        "punctuation.delimiter": s(c["green500"]),
        "punctuation.special": s(c["orange500"]),
        "punctuation.list_marker": s(c["blue500"]),
        "punctuation.markup": s(c["orange500"]),

        # CSS selectors
        "selector": s(c["blue500"]),
        "selector.pseudo": s(c["cyan500"]),

        # Tags (HTML/JSX) -> yellow, delimiters orange
        "tag": s(c["yellow500"]),
        "tag.delimiter": s(c["orange500"]),

        # Markup / markdown
        "title": s(c["orange500"], weight=700),
        "emphasis": s(c["base0"], italic=True),
        "emphasis.strong": s(c["base0"], weight=700),
        "link_text": s(c["blue500"], italic=True),
        "link_uri": s(c["cyan500"]),
        "text.literal": s(c["yellow500"]),

        # Misc
        "predictive": s(c["base01"], italic=True),
        "hint": s(c["cyan500"]),
        "primary": s(c["base0"]),
        "variant": s(c["blue500"]),
    }


family = {
    "$schema": "https://zed.dev/schema/themes/v0.2.0.json",
    "name": "Solarized Osaka",
    "author": "craftzdog (port by Thao Dang)",
    "themes": [
        {
            "name": "Solarized Osaka",
            "appearance": "dark",
            "style": make_style(transparent=True),
        },
    ],
}

import os
out = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   "themes", "solarized-osaka.json")
with open(out, "w") as f:
    json.dump(family, f, indent=2)
    f.write("\n")
print("wrote", os.path.relpath(out))
