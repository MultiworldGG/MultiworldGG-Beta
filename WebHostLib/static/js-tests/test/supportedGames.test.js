// Behavioral tests for the favorites front-end.
//
// The product file (WebHostLib/static/assets/supportedGames.js) wraps ALL favorites
// logic inside a single `window.addEventListener('load', () => {...})` callback. Nothing
// is exported. So instead of refactoring it, each test:
//   1. installs a minimal HTML fixture into the jsdom document,
//   2. (optionally) seeds localStorage,
//   3. evaluates the UNMODIFIED product source in the jsdom realm so its load listener
//      registers, then dispatches a real `load` Event to run the initializer,
//   4. drives real DOM events (click .star-icon, set #game-search.value + dispatch input)
//      and asserts observable state (DOM + localStorage) -- never source text.
//
// Each assertion fails if the corresponding runtime behavior regresses.

import { describe, it, expect, beforeEach } from "vitest";
import { readFileSync } from "node:fs";
import { join } from "node:path";

// Resolve from this file's directory (import.meta.dirname is a native path, so it works
// regardless of whether jsdom rewrites import.meta.url to an http origin).
const SOURCE = readFileSync(
  join(import.meta.dirname, "..", "..", "assets", "supportedGames.js"),
  "utf8",
);

const STORAGE_KEY = "mwgg_favorite_games";

// Two games whose data-game sorts in the OPPOSITE order to their display name,
// so the "sorted by data-display-name" assertion is meaningful:
//   data-game "Zelda"          -> display "The Legend of Zelda"  (sorts LAST)
//   data-game "ALinkToThePast" -> display "A Link to the Past"   (sorts FIRST)
function gameDetails(dataGame, displayName, nsfw = false) {
  return `
    <details data-game="${dataGame}" data-display-name="${displayName}"${nsfw ? ' data-nsfw="true"' : ""}>
      <summary class="h2">
        ${displayName}
        <span class="star-icon" data-game="${dataGame}" title="Add to favorites">&#9733;</span>
      </summary>
      <div class="world_version">Version: 1.0</div>
    </details>`;
}

// Minimal fixture mirroring supportedGames.html. The load handler has NO null-guards on
// #game-search / #expand-all / #collapse-all / #toggle-nsfw, so all of them must exist or
// dispatching 'load' throws before any handler is wired. The two <details> are DIRECT
// children of #games (updateMainListVisibility only touches `#games > details`).
function fixture() {
  return `
    <div id="games" class="markdown">
      <div class="js-only">
        <input id="game-search" placeholder="Search by title..." />
        <button id="expand-all">Expand All</button>
        <button id="collapse-all">Collapse All</button>
        <p><a href="#" id="toggle-nsfw">Show NSFW games</a></p>
      </div>
      <div id="favorites-section" class="js-only" style="display: none;">
        <h2>Favorite Games</h2>
        <div id="favorites-list"></div>
        <hr class="favorites-divider">
      </div>
      ${gameDetails("Zelda", "The Legend of Zelda")}
      ${gameDetails("ALinkToThePast", "A Link to the Past")}
    </div>`;
}

// Install fixture + (optional) seed, then run the real script and fire 'load'.
function boot({ seed } = {}) {
  document.body.innerHTML = fixture();
  if (seed !== undefined) {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(seed));
  }
  // Run the unmodified product source in the jsdom realm. Using window.eval keeps the
  // file's bare references to localStorage/document/window/Event/MouseEvent bound to the
  // jsdom globals, and registers its `window.addEventListener('load', ...)`.
  window.eval(SOURCE);
  // Fire the load event the script is waiting on -> runs loadFavorites/storeOriginalElements/
  // initializeStarIcons/updateFavoritesSection/updateMainListVisibility and wires handlers.
  window.dispatchEvent(new window.Event("load"));
}

const $ = (sel) => document.querySelector(sel);
const $$ = (sel) => Array.from(document.querySelectorAll(sel));

// A star icon in the MAIN list (inside #games > details, not inside #favorites-list).
function mainStar(dataGame) {
  return $(`#games > details[data-game="${dataGame}"] .star-icon`);
}

function setSearch(value) {
  const input = $("#game-search");
  input.value = value;
  input.dispatchEvent(new window.Event("input"));
}

beforeEach(() => {
  localStorage.clear();
  document.body.innerHTML = "";
});

describe("supportedGames favorites", () => {
  // Contract 1: toggleFavorite persists to localStorage as a JSON array; loadFavorites reads back.
  describe("contract 1: localStorage persistence", () => {
    it("writes the favorited set to localStorage as a JSON array on favorite", () => {
      boot();
      expect(localStorage.getItem(STORAGE_KEY)).toBeNull();

      mainStar("Zelda").click();

      expect(localStorage.getItem(STORAGE_KEY)).toBe(JSON.stringify(["Zelda"]));
      expect(JSON.parse(localStorage.getItem(STORAGE_KEY))).toEqual(["Zelda"]);
    });

    it("removes the entry from the persisted array when unfavorited", () => {
      boot();
      mainStar("Zelda").click();
      mainStar("Zelda").click();

      expect(JSON.parse(localStorage.getItem(STORAGE_KEY))).toEqual([]);
    });

    it("loadFavorites reads a pre-seeded array back on load (no click)", () => {
      boot({ seed: ["Zelda"] });

      // Read-back is observable: the favorites section renders the seeded favorite,
      // and the main star reflects the favorited state -- with zero user interaction.
      expect($("#favorites-section").style.display).toBe("block");
      expect($$("#favorites-list .favorite-game-item")).toHaveLength(1);
      expect(mainStar("Zelda").classList.contains("favorited")).toBe(true);
    });
  });

  // Contract 2: clicking a .star-icon toggles .favorited and flips the title text.
  describe("contract 2: star icon class + title flip", () => {
    it("adds .favorited and sets the Remove title on first click", () => {
      boot();
      const star = mainStar("Zelda");
      expect(star.classList.contains("favorited")).toBe(false);
      expect(star.title).toBe("Add to favorites");

      star.click();

      expect(star.classList.contains("favorited")).toBe(true);
      expect(star.title).toBe("Remove from favorites");
    });

    it("removes .favorited and restores the Add title on second click", () => {
      boot();
      const star = mainStar("Zelda");
      star.click();
      star.click();

      expect(star.classList.contains("favorited")).toBe(false);
      expect(star.title).toBe("Add to favorites");
    });
  });

  // Contract 3: updateFavoritesSection shows/hides #favorites-section by set size and
  // clones favorited entries into #favorites-list, sorted by data-display-name.
  describe("contract 3: favorites section visibility + sorted clones", () => {
    it("keeps the section hidden when there are no favorites", () => {
      boot();
      expect($("#favorites-section").style.display).toBe("none");
      expect($$("#favorites-list .favorite-game-item")).toHaveLength(0);
    });

    it("shows the section once a favorite exists and hides it again when emptied", () => {
      boot();
      const star = mainStar("Zelda");

      star.click();
      expect($("#favorites-section").style.display).toBe("block");

      star.click();
      expect($("#favorites-section").style.display).toBe("none");
    });

    it("clones favorited entries into #favorites-list sorted by data-display-name", () => {
      boot();
      // Favorite Zelda (display 'The Legend of Zelda') first, then ALinkToThePast
      // (display 'A Link to the Past'). Insertion order != display-name order.
      mainStar("Zelda").click();
      mainStar("ALinkToThePast").click();

      const clones = $$("#favorites-list .favorite-game-item");
      expect(clones).toHaveLength(2);

      // Sorted by display name: "A Link to the Past" before "The Legend of Zelda".
      const order = clones.map((c) => c.getAttribute("data-display-name"));
      expect(order).toEqual(["A Link to the Past", "The Legend of Zelda"]);
    });
  });

  // Contract 4: updateMainListVisibility hides favorited games from the main #games list.
  describe("contract 4: main list hides favorited games", () => {
    it("hides the favorited details and leaves others visible", () => {
      boot();
      mainStar("Zelda").click();

      const favorited = $('#games > details[data-game="Zelda"]');
      const other = $('#games > details[data-game="ALinkToThePast"]');

      expect(favorited.style.display).toBe("none");
      // Non-favorited details are explicitly reset to display:null -> "" in jsdom.
      expect(other.style.display).toBe("");
    });

    it("restores the details to the main list when unfavorited", () => {
      boot();
      const star = mainStar("Zelda");
      star.click();
      star.click();

      expect($('#games > details[data-game="Zelda"]').style.display).toBe("");
    });
  });

  // Contract 5: the search input filters BOTH the main list and .favorite-game-item entries
  // by data-game / data-display-name.
  describe("contract 5: search filters main list and favorites", () => {
    it("filters main-list details by data-game / data-display-name substring", () => {
      boot();
      setSearch("link"); // matches display "A Link to the Past", not "The Legend of Zelda"

      expect($('#games > details[data-game="ALinkToThePast"]').style.display).toBe("");
      expect($('#games > details[data-game="Zelda"]').style.display).toBe("none");
    });

    it("filters .favorite-game-item entries by the same search term", () => {
      boot();
      // Favorite both so two clones exist in #favorites-list.
      mainStar("Zelda").click();
      mainStar("ALinkToThePast").click();

      setSearch("zelda"); // matches "The Legend of Zelda" only

      const clones = $$("#favorites-list .favorite-game-item");
      const zeldaClone = clones.find((c) => c.getAttribute("data-game") === "Zelda");
      const alttpClone = clones.find((c) => c.getAttribute("data-game") === "ALinkToThePast");

      expect(zeldaClone.style.display).toBe("");
      expect(alttpClone.style.display).toBe("none");
    });

    it("restores everything when the search term is cleared", () => {
      boot();
      mainStar("ALinkToThePast").click(); // favorite -> hidden from main, clone in favorites

      setSearch("zelda");
      setSearch(""); // empty -> restore

      // Clone restored to visible.
      const clone = $('#favorites-list .favorite-game-item[data-game="ALinkToThePast"]');
      expect(clone.style.display).toBe("");
      // Main list: the favorited game stays hidden (updateMainListVisibility re-applied),
      // the un-favorited one is visible.
      expect($('#games > details[data-game="ALinkToThePast"]').style.display).toBe("none");
      expect($('#games > details[data-game="Zelda"]').style.display).toBe("");
    });
  });

  // Contract 6: adding a favorite clears #game-search and re-dispatches an input event.
  describe("contract 6: favoriting clears the search box and re-dispatches input", () => {
    it("clears #game-search.value when a new favorite is added", () => {
      boot();
      const input = $("#game-search");
      input.value = "something";

      mainStar("Zelda").click(); // ADD -> should clear the search box

      expect(input.value).toBe("");
    });

    it("re-dispatches an 'input' event on add (observed via the input handler running)", () => {
      boot();
      const input = $("#game-search");
      let inputEvents = 0;
      input.addEventListener("input", () => {
        inputEvents += 1;
      });

      input.value = "zelda";
      mainStar("ALinkToThePast").click(); // ADD -> clears value and dispatches 'input'

      expect(inputEvents).toBeGreaterThanOrEqual(1);
      // The dispatched input ran against the cleared value, so the main list is fully
      // restored (empty search term path), not filtered by the stale "zelda" text.
      expect($('#games > details[data-game="Zelda"]').style.display).toBe("");
    });

    it("does NOT clear the search box when REMOVING a favorite", () => {
      boot({ seed: ["Zelda"] });
      const input = $("#game-search");
      input.value = "keep-me";

      // Zelda is favorited (and hidden from the main list); click its clone's star to remove.
      const cloneStar = $('#favorites-list .favorite-game-item[data-game="Zelda"] .star-icon');
      cloneStar.click(); // REMOVE -> wasFavorited true -> search box untouched

      expect(input.value).toBe("keep-me");
    });
  });
});
