# Site Design Reference

This page is the style guide for the Heartlands Codex. Keep entries concise, consistent, and easy to scan.

## Headers
* `#` for page title
* `##` for primary sections
* `###` for subsections

## Lists
Use bullet lists for quick facts and scannable sections.

## Collapsible Sections
Use collapsible blocks for long lore or spoilers.

<details>
<summary>Click to expand history</summary>

The Kadian Empire was founded in...

</details>

## Linking
Use relative links so pages work locally and on GitHub Pages.

**Race:** [Kadian](../Heartlands/Races/Kadian.md)

## Galleries
Use the gallery pattern for pages with multiple images. The gallery supports a large main image with a thumbnail strip.

Example:

```html
<div class="hl-gallery" data-gallery>
  <div class="hl-gallery-main swiper">
    <div class="swiper-wrapper">
      <div class="swiper-slide"><img src="/images/example-1.png" alt="Example 1" /></div>
      <div class="swiper-slide"><img src="/images/example-2.png" alt="Example 2" /></div>
    </div>
    <div class="swiper-button-prev"></div>
    <div class="swiper-button-next"></div>
  </div>
  <div class="hl-gallery-thumbs swiper">
    <div class="swiper-wrapper">
      <div class="swiper-slide"><img src="/images/example-1.png" alt="Example 1 thumbnail" /></div>
      <div class="swiper-slide"><img src="/images/example-2.png" alt="Example 2 thumbnail" /></div>
    </div>
  </div>
</div>
```

Notes:
* Keep images relative to the current page.
* Use the same image list for the main carousel and thumbnails.

## Infoboxes
Use infoboxes for key stats and profiles so pages read consistently.

```html
<div class="hl-infobox">
  <div class="hl-infobox-title">Item Stats</div>
  <table>
    <tr><th>Weight</th><td>0.0</td></tr>
    <tr><th>Value</th><td>0.0</td></tr>
  </table>
</div>
```

## Page Templates
Use these templates when creating new pages. Copy one and fill it out:
* [NPC Template](../Templates/NPC.md)
* [Location Template](../Templates/Location.md)
* [Item Template](../Templates/Item.md)
* [Quest Template](../Templates/Quest.md)
* [Faction Template](../Templates/Faction.md)
* [Race Template](../Templates/Race.md)

## Tags
Tags help group related pages. Add tags in a front matter block at the very top of a page:

```yaml
---
tags: [example, lore, faction]
---
```

See the [Tags Index](../Tags/index.md) for available tags.

## Regenerating Indexes And Tags
If you add or remove pages, run the helper script to rebuild indexes, tags, and the home page “Latest Additions”.

```bash
python3 docs/tools/regenerate_indexes_and_tags.py
```

## Quick Jump
Use quick jump buttons for longer pages so readers can jump to sections.

Example:

```md
## Quick Jump
* [Summary](#summary)
* [Appearance](#appearance)
* [History](#history)
```

## Links and Paths
Use pretty URLs and relative links without `.md` where possible. Examples:

- Good: `../Skills/ShortBlade/`
- Good: `../Gameplay/ShieldTypes/#buckler-shields`
- Avoid: `../Skills/ShortBlade.md`
