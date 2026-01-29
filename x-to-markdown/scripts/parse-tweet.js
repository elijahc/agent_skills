#!/usr/bin/env node
/**
 * parse-tweet.js — Convert fxtwitter API JSON to clean markdown
 *
 * Usage:
 *   curl -s "https://api.fxtwitter.com/{user}/status/{id}" | node parse-tweet.js [output.md]
 *   node parse-tweet.js --url "https://x.com/user/status/123" [output.md]
 *
 * If no output path given, writes to stdout.
 */

const fs = require('fs');
const path = require('path');

async function fetchTweet(url) {
  const match = url.match(/(?:x\.com|twitter\.com)\/(\w+)\/status\/(\d+)/);
  if (!match) {
    console.error('Invalid X/Twitter URL');
    process.exit(1);
  }
  const [, user, id] = match;
  const apiUrl = `https://api.fxtwitter.com/${user}/status/${id}`;
  const res = await fetch(apiUrl);
  return res.json();
}

function buildEntityMap(entityMapArray) {
  const map = {};
  if (!entityMapArray) return map;
  for (const e of entityMapArray) {
    map[String(e.key)] = e.value;
  }
  return map;
}

function resolveMedia(entity, mediaEntities) {
  if (!entity?.data?.mediaItems?.length) return null;
  const mediaId = String(entity.data.mediaItems[0].mediaId);
  const matched = (mediaEntities || []).find(m => String(m.media_id) === mediaId);
  if (matched?.media_info?.original_img_url) {
    return `![image](${matched.media_info.original_img_url})`;
  }
  return `[Image: media_id ${mediaId}]`;
}

function applyInlineStyles(text, ranges) {
  if (!ranges || !ranges.length || !text) return text;

  // Sort ranges by offset descending so we can splice without shifting indices
  const sorted = [...ranges].sort((a, b) => b.offset - a.offset);
  let result = text;
  for (const range of sorted) {
    const { offset, length, style } = range;
    const before = result.slice(0, offset);
    const inner = result.slice(offset, offset + length);
    const after = result.slice(offset + length);
    if (style === 'Bold') {
      result = `${before}**${inner}**${after}`;
    } else if (style === 'Italic') {
      result = `${before}*${inner}*${after}`;
    }
  }
  return result;
}

function convertArticleToMarkdown(data) {
  const tweet = data.tweet;
  const article = tweet.article;
  const blocks = article.content.blocks;
  const entityMap = buildEntityMap(article.content.entityMap);
  const mediaEntities = article.media_entities || [];

  let md = `# ${article.title}\n\n`;
  md += `**Author:** ${tweet.author.name} (@${tweet.author.screen_name})\n`;
  md += `**Published:** ${article.created_at}\n`;
  md += `**Source:** ${tweet.url}\n`;

  const stats = [];
  if (tweet.likes) stats.push(`${tweet.likes.toLocaleString()} likes`);
  if (tweet.retweets) stats.push(`${tweet.retweets.toLocaleString()} retweets`);
  if (tweet.views) stats.push(`${tweet.views.toLocaleString()} views`);
  if (stats.length) md += `**Stats:** ${stats.join(' · ')}\n`;
  md += '\n---\n\n';

  for (const block of blocks) {
    const text = (block.text || '').trim();

    // Handle atomic blocks (embedded content)
    if (block.type === 'atomic' && block.entityRanges?.length > 0) {
      const entityKey = String(block.entityRanges[0].key);
      const entity = entityMap[entityKey];
      if (entity) {
        if (entity.type === 'MARKDOWN') {
          md += entity.data.markdown + '\n\n';
        } else if (entity.type === 'MEDIA') {
          const img = resolveMedia(entity, mediaEntities);
          if (img) md += img + '\n\n';
        } else if (entity.type === 'TWEET') {
          md += `> [Embedded Tweet](https://x.com/i/status/${entity.data.tweetId})\n\n`;
        }
      }
      continue;
    }

    if (!text) continue;

    const styled = applyInlineStyles(text, block.inlineStyleRanges);

    switch (block.type) {
      case 'header-one':
        md += `# ${styled}\n\n`;
        break;
      case 'header-two':
        md += `## ${styled}\n\n`;
        break;
      case 'header-three':
        md += `### ${styled}\n\n`;
        break;
      case 'unordered-list-item':
        md += `- ${styled}\n`;
        break;
      case 'ordered-list-item':
        md += `1. ${styled}\n`;
        break;
      default:
        md += `${styled}\n\n`;
    }
  }

  return md;
}

function convertTweetToMarkdown(data) {
  const tweet = data.tweet;
  const text = tweet.text || tweet.raw_text?.text || '';

  let md = `# Tweet by ${tweet.author.name}\n\n`;
  md += `**Author:** ${tweet.author.name} (@${tweet.author.screen_name})\n`;
  md += `**Published:** ${tweet.created_at}\n`;
  md += `**Source:** ${tweet.url}\n`;

  const stats = [];
  if (tweet.likes) stats.push(`${tweet.likes.toLocaleString()} likes`);
  if (tweet.retweets) stats.push(`${tweet.retweets.toLocaleString()} retweets`);
  if (tweet.views) stats.push(`${tweet.views.toLocaleString()} views`);
  if (stats.length) md += `**Stats:** ${stats.join(' · ')}\n`;
  md += '\n---\n\n';

  md += text + '\n';

  // Include media if present
  if (tweet.media?.all?.length) {
    md += '\n';
    for (const m of tweet.media.all) {
      if (m.type === 'photo' && m.url) {
        md += `![image](${m.url})\n\n`;
      } else if (m.type === 'video' && m.thumbnail_url) {
        md += `[Video thumbnail](${m.thumbnail_url})\n\n`;
      }
    }
  }

  return md;
}

function slugify(text) {
  return text
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-|-$/g, '')
    .slice(0, 80);
}

async function main() {
  const args = process.argv.slice(2);
  let data;
  let outputPath;

  const urlIdx = args.indexOf('--url');
  if (urlIdx !== -1) {
    const url = args[urlIdx + 1];
    data = await fetchTweet(url);
    outputPath = args.find((a, i) => i !== urlIdx && i !== urlIdx + 1 && !a.startsWith('--'));
  } else {
    // Read from stdin
    const input = fs.readFileSync('/dev/stdin', 'utf8');
    data = JSON.parse(input);
    outputPath = args.find(a => !a.startsWith('--'));
  }

  if (!data?.tweet) {
    console.error('No tweet data found');
    process.exit(1);
  }

  const md = data.tweet.article
    ? convertArticleToMarkdown(data)
    : convertTweetToMarkdown(data);

  if (outputPath) {
    const dir = path.dirname(outputPath);
    if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
    fs.writeFileSync(outputPath, md);
    console.log(outputPath);
  } else {
    process.stdout.write(md);
  }
}

main().catch(e => { console.error(e.message); process.exit(1); });
