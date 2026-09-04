const fs = require('node:fs');
const path = require('node:path');
const group = (folder) => fs.readdirSync(path.join(__dirname, 'docs', folder))
  .filter(name => name.endsWith('.md') && name !== 'index.md')
  .sort()
  .map(name => folder + '/' + name.slice(0, -3));

module.exports = {
  reference: [
    'getting-started',
    'native-lifecycle',
    {type: 'category', label: 'Functions', link: {type: 'doc', id: 'functions/index'}, items: group('functions')},
    {type: 'category', label: 'Variables', link: {type: 'doc', id: 'variables/index'}, items: group('variables')},
  ],
};
