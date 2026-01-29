---
name: x-to-markdown
description: Extract and convert X/Twitter posts and articles to clean markdown files. Use when the user shares an x.com or twitter.com link and wants the content saved, exported, or converted to markdown. Handles tweets, threads, and long-form Twitter Articles. Can optionally upload the result to R2/S3 for sharing.
metadata: {"clawdbot":{"emoji":"🐦"}}
---

# X to Markdown

Convert X/Twitter posts and articles into clean, readable markdown documents.

## When to Use

- User shares an `x.com` or `twitter.com` URL and asks to export, save, read, or convert it
- User wants a markdown copy of a tweet, thread, or Twitter Article
- User wants to archive or share tweet content outside of X

## How It Works

X.com blocks direct scraping. This skill uses the **fxtwitter API** (`api.fxtwitter.com`) as a public proxy to fetch tweet data as structured JSON, then parses it into markdown.

### Step 1: Fetch the Tweet Data

Extract the tweet ID and author from the URL. Supported URL formats:
- `https://x.com/{user}/status/{id}`
- `https://x.com/{user}/status/{id}?s=...`
- `https://twitter.com/{user}/status/{id}`

Fetch via `web_fetch`:
```
https://api.fxtwitter.com/{user}/status/{id}
```

Request `maxChars: 100000` to avoid truncation on long articles.

### Step 2: Parse the JSON

The response is JSON with this structure:

```
{
  "tweet": {
    "url": "...",
    "text": "...",           // plain tweet text
    "author": { "name", "screen_name" },
    "created_at": "...",
    "likes": N,
    "retweets": N,
    "views": N,
    "article": { ... }      // only present for Twitter Articles
  }
}
```

#### For regular tweets/threads:
- Use `tweet.text` (or `tweet.raw_text.text`) for the content
- Include author, date, stats in the header

#### For Twitter Articles (long-form):
The article content is in `tweet.article.content.blocks[]` — an array of Draft.js content blocks.

Each block has:
- `type`: `"unstyled"`, `"header-two"`, `"header-three"`, `"unordered-list-item"`, `"ordered-list-item"`, `"atomic"`
- `text`: the block text
- `inlineStyleRanges`: bold/italic spans
- `entityRanges`: references to the `entityMap`
- `data.mentions`: @mentions with indices

The `entityMap` contains embedded content:
- `type: "MEDIA"` → embedded images (resolve `mediaId` against `tweet.article.media_entities[]` for `original_img_url`)
- `type: "MARKDOWN"` → embedded code blocks (use `data.markdown` directly)
- `type: "TWEET"` → embedded tweet references (link to `https://x.com/i/status/{tweetId}`)

### Step 3: Build the Markdown

**Header:**
```markdown
# {article.title or first line of tweet}

**Author:** {name} (@{screen_name})
**Published:** {created_at}
**Source:** {tweet.url}
**Stats:** {likes} likes · {retweets} retweets · {views} views

---
```

**Body — block type mapping:**

| Block type | Markdown |
|---|---|
| `unstyled` | Plain paragraph + blank line |
| `header-one` | `# text` |
| `header-two` | `## text` |
| `header-three` | `### text` |
| `unordered-list-item` | `- text` |
| `ordered-list-item` | `1. text` |
| `atomic` (with entity) | Resolve from entityMap (see above) |

**Inline styles:**
- `Bold` → `**text**`
- `Italic` → `*text*`

**Entity resolution for atomic blocks:**
1. Get entity key from `block.entityRanges[0].key`
2. Look up in `entityMap` by key
3. Based on `type`:
   - `MEDIA` → `![image](original_img_url)`
   - `MARKDOWN` → insert the markdown verbatim
   - `TWEET` → `> [Embedded Tweet](https://x.com/i/status/{tweetId})`

### Step 4: Save and Optionally Upload

Save to `<workspace>/exports/x-to-markdown/{slugified-title}.md`

If user wants a shareable link and the R2 upload skill is available:
```bash
<workspace>/scripts/r2 <filepath> --expires 7d
```

## Example Usage

**User:** "Can you export this as markdown? https://x.com/someone/status/123456"

**Agent:**
1. Fetch `https://api.fxtwitter.com/someone/status/123456` via `web_fetch`
2. Parse the JSON response
3. Convert blocks to markdown
4. Save to `exports/x-to-markdown/`
5. Optionally upload to R2 and share the link

## Notes

- fxtwitter is a public API — no auth needed, but may have rate limits
- Images are linked to `pbs.twimg.com` URLs which may expire over time
- For archival, consider downloading images locally
- Skip empty/whitespace-only blocks during conversion
- The `entityMap` keys are strings — always convert to string when looking up
