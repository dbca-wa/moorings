const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const test = require('node:test');
const vm = require('node:vm');

const frontend = path.resolve(__dirname, '..');

for (const asset of ['moment.min.js', 'moment-en-au.js']) {
  test(`${asset} exposes the current Moment browser API`, () => {
    const context = {};
    vm.runInNewContext(
      fs.readFileSync(path.join(frontend, '../static/common/js', asset), 'utf8'),
      context,
    );
    const moment = context.moment;

    for (const app of ['mooring', 'admissions', 'availability2', 'exploreparks']) {
      const lock = JSON.parse(
        fs.readFileSync(path.join(frontend, app, 'package-lock.json'), 'utf8'),
      );
      assert.equal(moment.version, lock.packages['node_modules/moment'].version);
    }
    assert.equal(moment.version, '2.31.0');
    assert.equal(moment.locale(), 'en');
    assert.equal(moment('2026-10-06', 'YYYY-MM-DD', true).format('L'), '10/06/2026');
    assert.equal(moment('2024-02-29', 'YYYY-MM-DD', true).isValid(), true);
    assert.equal(moment('2026-02-29', 'YYYY-MM-DD', true).isValid(), false);
    assert.equal(
      moment('2026-10-06T15:30:00+08:00').valueOf(),
      Date.parse('2026-10-06T15:30:00+08:00'),
    );
    moment.now = () => Date.parse('2026-10-06T15:30:00+08:00');
    const expiry = moment('2026-10-06T15:35:00+08:00');
    assert.equal(Math.floor((expiry - moment.now()) / 1000), 300);

    if (asset === 'moment-en-au.js') {
      assert.ok(moment.locales().includes('en-au'));
      assert.ok(moment.locales().includes('fr'));
      assert.equal(
        moment('2026-10-06', 'YYYY-MM-DD', true).locale('en-au').format('L'),
        '06/10/2026',
      );
      assert.equal(moment.locale(), 'en');
    } else {
      assert.deepEqual(Array.from(moment.locales()), ['en']);
    }
  });
}
