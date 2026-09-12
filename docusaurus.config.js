const {themes: prismThemes} = require('prism-react-renderer');

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: 'Mystical Ninja Starring Goemon Recompiled',
  tagline: 'Mod development reference: native functions, variables, and C examples',
  favicon: 'img/favicon.svg',
  url: 'https://8ae.github.io',
  baseUrl: '/mnsg-documentation/',
  organizationName: '8AE',
  projectName: 'mnsg-documentation',
  trailingSlash: true,
  onBrokenLinks: 'throw',
  i18n: {defaultLocale: 'en', locales: ['en']},
  markdown: {format: 'md', hooks: {onBrokenMarkdownLinks: 'throw'}},
  presets: [['classic', {
    docs: {routeBasePath: '/', sidebarPath: require.resolve('./sidebars.js'), showLastUpdateAuthor: false, showLastUpdateTime: false},
    blog: false,
    theme: {customCss: require.resolve('./src/css/custom.css')},
  }]],
  themeConfig: {
    image: 'img/social-card.svg',
    colorMode: {defaultMode: 'light', respectPrefersColorScheme: true},
    navbar: {
      title: 'Mystical Ninja Starring Goemon Recompiled',
      items: [
        {to: '/reference', label: 'API reference', position: 'left'},
        {to: '/textures', label: 'Textures', position: 'left'},
        {to: '/getting-started', label: 'Getting started', position: 'left'},
        {href: 'https://github.com/klorfmorf/Goemon64Recomp', label: 'Game source', position: 'left'},
        {type: 'search', position: 'right'},
      ],
    },
    footer: {
      style: 'light',
      links: [
        {title: 'Reference', items: [{label: 'Functions', to: '/functions'}, {label: 'Variables', to: '/variables'}]},
        {title: 'Learn', items: [{label: 'Getting started', to: '/getting-started'}, {label: 'Native lifecycle', to: '/native-lifecycle'}]},
        {title: 'Game project', items: [{label: 'Goemon64Recomp on GitHub', href: 'https://github.com/klorfmorf/Goemon64Recomp'}]},
      ],
      copyright: 'Mystical Ninja Starring Goemon Recompiled · Mod development reference. Built with Docusaurus.',
    },
    prism: {theme: prismThemes.github, darkTheme: prismThemes.dracula, additionalLanguages: ['c','bash','toml']},
    tableOfContents: {minHeadingLevel: 2, maxHeadingLevel: 3},
  },
};

module.exports = config;
