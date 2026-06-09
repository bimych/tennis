import json
import os
from typing import Any

STATE_DIR = "state"
STATE_FILE = os.path.join(STATE_DIR, "availability_state.json")


def ensure_state_dir():
    """Ensure state directory exists"""
    if not os.path.exists(STATE_DIR):
        os.makedirs(STATE_DIR)


def load_state(key: str) -> list:
    """Load previous state for a given key (e.g., 'coaching', 'courts')"""
    ensure_state_dir()
    if not os.path.exists(STATE_FILE):
        return []
    
    try:
        with open(STATE_FILE, "r") as f:
            data = json.load(f)
            return data.get(key, [])
    except (json.JSONDecodeError, IOError):
        return []


def save_state(key: str, current_state: list) -> None:
    """Save current state for a given key"""
    ensure_state_dir()
    
    # Load existing state for other keys
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, "r") as f:
                all_state = json.load(f)
        except (json.JSONDecodeError, IOError):
            all_state = {}
    else:
        all_state = {}
    
    # Update this key's state
    all_state[key] = current_state
    
    # Save back
    with open(STATE_FILE, "w") as f:
        json.dump(all_state, f, indent=2)


def has_changes(key: str, current_state: list) -> bool:
    """
    Check if current state differs from previous state.
    Returns True if there are changes.
    """
    previous_state = load_state(key)
    
    # Convert to sets of normalized strings for comparison
    # This makes comparison order-independent
    previous_set = set(str(item) for item in previous_state)
    current_set = set(str(item) for item in current_state)
    
    return previous_set != current_set


def get_changes_summary(key: str, current_state: list) -> dict:
    """
    Get a summary of what changed.
    Returns dict with 'new', 'removed', 'unchanged' items.
    """
    previous_state = load_state(key)
    
    previous_set = set(str(item) for item in previous_state)
    current_set = set(str(item) for item in current_state)
    
    new_items = current_set - previous_set
    removed_items = previous_set - current_set
    unchanged_items = current_set & previous_set
    
    return {
        "new": sorted(list(new_items)),
        "removed": sorted(list(removed_items)),
        "unchanged": sorted(list(unchanged_items)),
        "total": len(current_state)
    }
