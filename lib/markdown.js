const MarkdownIt = require("markdown-it");
const md = new MarkdownIt({ html: true, linkify: true, typographer: true });

// Enlaces externos: se abren en pestaña nueva y de forma segura
const defecto = md.renderer.rules.link_open || ((t, i, o, e, s) => s.renderToken(t, i, o));
md.renderer.rules.link_open = (tokens, idx, opts, env, self) => {
  const href = tokens[idx].attrGet("href") || "";
  if (/^https?:\/\//.test(href)) {
    tokens[idx].attrSet("target", "_blank");
    tokens[idx].attrSet("rel", "noopener");
  }
  return defecto(tokens, idx, opts, env, self);
};
module.exports = md;
