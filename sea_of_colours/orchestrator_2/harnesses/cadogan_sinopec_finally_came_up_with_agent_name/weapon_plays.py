"""weapon_plays — YOUR agent's weapon moves. This is the only file you edit.

Everything else was installed once by ``forge_install.py``. To add a weapon or
a move, add a ``WeaponPlay`` below. Nothing else in the harness needs touching:
the menu group, the wire move, the replay tag, the doctrine and the rationale
are all derived from what you write here.

Each move is four decisions:

  WHEN           always | redsign_mine | redsign_theirs | other
                 The board condition. ``redsign_mine`` = a pure WE found is
                 live (we are defending it). ``redsign_theirs`` = a rival
                 found it (we are attacking it).

  HOUR           super_early (H1) | early (H1-2) | mid | late | last_night
                 Position in the move list IS the hour, so this is a hard
                 constraint. An 8h EMP cloud past H2 has no night left to use;
                 a chaff has to land on the hour they were going to act.

  COMBINES_WITH  smash_grab | blind_grab | probe | chain | standalone
                 Which existing play this borrows geometry from, so the option
                 has real coordinates rather than invented ones.

  WHY            One sentence: what firing this BUYS. Yours, in your words.
                 The full rationale the model reads is composed from this plus
                 the weapon's mechanics plus the alternative it beats — that
                 last part depends on what else is on tonight's menu, which is
                 why the machinery adds it rather than you.

Name the move whatever you like. It is public: it shows up in the game log as
the night resolves, in the lab's frozen-turn journals and in the season cards.
Be as silly as you like about the TONE and never about the CONTENT — calling a
cautious vision move ``NUKE`` tells the model that option is aggressive, and
that is a bug you will spend an hour not finding.

Check yourself any time with:

    python skills/soc-agent-forge/scripts/check_wiring.py <your_label>
"""

from __future__ import annotations

from typing import Tuple

from .weapon_forge import EconomyPolicy, WeaponPlay


# ── how the weapons get PAID FOR ──────────────────────────────────────────
# Pete fires all three weapons. buy_asap arms from day 1,
# seek_blue_always diverts a harvester to blue when the rack is empty,
# and hold_at caps each weapon at 1 (one of each = 600 blue = the cap).
ECONOMY = EconomyPolicy(
    buy_asap=False,
    never_buy_what_you_cannot_fire=True,
    hold_at={"emp": 0, "chaff": 1, "snap": 1},
    seek_blue_always=False,
)


PLAYS: Tuple[WeaponPlay, ...] = (
    # ── SNAP: trap a contested pure at H1 ─────────────────────────────
    # A pure we can see that a rival probe also watches is the one cell
    # whose occupation is predictable. Snap it, refuse their landing,
    # then our paired smash-grab lands on the cold pure at H2.
    WeaponPlay(
        play_id="PISTOL_TRAP",
        weapon="snap",
        when="always",
        hour="super_early",
        targets="contested_pure",
        min_targets=1,
        combines_with="smash_grab",
        why=("a pure we can see that a rival probe also watches is the "
             "one cell on the board whose occupation is predictable — "
             "they will smash-and-grab it at hour one; snapping it "
             "refuses that landing and damages the hull, then our "
             "smash-grab lands on the cold pure at hour two"),
    ),

    # ── SNAP: blind the finder when we cannot see the pure ────────────
    # When a rival lit a pure we have no vision on, the eye that found
    # it is the only target we can name. Kill it at H1 to refuse their
    # drop for lack of live vision.
    WeaponPlay(
        play_id="PISTOL_BLIND",
        weapon="snap",
        when="redsign_theirs",
        hour="super_early",
        targets="finder_probe",
        min_targets=1,
        combines_with="blind_grab",
        why=("when a rival has lit a pure we cannot see, the eye that "
             "found it is the only target we can name; snapping it at "
             "hour one refuses their drop for lack of live vision, "
             "then a paired blind-grab combs the smear they can no "
             "longer reach"),
    ),

    # ── CHAFF: cancel their hour-one drop on a rival redsign ──────────
    # A rival that just lit a pure drops on it at H1. Cancelling that
    # one hour kills their smash-and-grab and leaves the pure sitting
    # there for our follow-on grab.
    WeaponPlay(
        play_id="PISTOL_JAM",
        weapon="chaff",
        when="redsign_theirs",
        hour="super_early",
        combines_with="blind_grab",
        why=("a rival that has just lit a pure will drop on it at hour "
             "one; cancelling that hour kills their smash-and-grab and "
             "leaves the pure sitting there for our follow-on grab"),
    ),
)
