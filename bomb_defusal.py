"""Core data structures for the board game 《拆炸弹》.

This module intentionally focuses only on game initialization. It does not
include a game loop, turn rules, or AI behavior yet.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
import random
from typing import Optional


class Role(str, Enum):
    """Player identity."""

    RED = "Red"
    BLACK = "Black"


class CardType(str, Enum):
    """Card types used by the game."""

    WIRE = "Wire"
    BOMB = "Bomb"
    SAFE = "Safe"


@dataclass(frozen=True)
class AnnouncedInfo:
    """Information a player announces about their hand."""

    wire_count: int = 0
    bomb_count: int = 0


@dataclass
class Player:
    """A player in 《拆炸弹》."""

    id: int
    role: Role
    hand: list[CardType] = field(default_factory=list)
    announced_info: AnnouncedInfo = field(default_factory=AnnouncedInfo)


@dataclass
class Game:
    """Current game state.

    The state currently stores the player list and the undealt deck remainder.
    During initialization the deck remainder is empty because every card is
    dealt evenly to players.
    """

    player_count: int
    players: list[Player]
    deck: list[CardType] = field(default_factory=list)


def _build_roles(player_count: int) -> list[Role]:
    """Create the role list before shuffling.

    Even player counts split Red and Black evenly. Odd player counts give Red
    exactly one more player than Black.
    """

    red_count = (player_count + 1) // 2
    black_count = player_count // 2
    return [Role.RED] * red_count + [Role.BLACK] * black_count


def _build_deck(player_count: int) -> list[CardType]:
    """Create the full deck before shuffling."""

    total_cards = player_count * 5
    wire_count = player_count
    bomb_count = 1
    safe_count = total_cards - wire_count - bomb_count
    return (
        [CardType.WIRE] * wire_count
        + [CardType.BOMB] * bomb_count
        + [CardType.SAFE] * safe_count
    )


def _announce_hand(hand: list[CardType]) -> AnnouncedInfo:
    """Calculate the default announced information from a player's hand."""

    return AnnouncedInfo(
        wire_count=hand.count(CardType.WIRE),
        bomb_count=hand.count(CardType.BOMB),
    )


def init_game(player_count: int, seed: Optional[int] = None) -> Game:
    """Initialize a new 《拆炸弹》 game.

    Args:
        player_count: Number of players. Must be between 4 and 8 inclusive.
        seed: Optional random seed. Supplying this is useful for tests or
            reproducible examples.

    Returns:
        A fully initialized ``Game`` where each player has a role and five
        cards.

    Raises:
        ValueError: If ``player_count`` is outside the supported range.
    """

    if not 4 <= player_count <= 8:
        raise ValueError("player_count must be between 4 and 8 inclusive")

    rng = random.Random(seed)

    roles = _build_roles(player_count)
    rng.shuffle(roles)

    deck = _build_deck(player_count)
    rng.shuffle(deck)

    players: list[Player] = []
    for index in range(player_count):
        start = index * 5
        end = start + 5
        hand = deck[start:end]
        players.append(
            Player(
                id=index + 1,
                role=roles[index],
                hand=hand,
                announced_info=_announce_hand(hand),
            )
        )

    return Game(player_count=player_count, players=players, deck=[])
