export default function () {
  return [{
    title: 'Overview',
    to: {
      name: 'overview',
    },
    htmlBefore: '<i class="material-icons">analytics</i>',
    htmlAfter: '',
  },  {
    title: 'Most Vulnerable',
    htmlBefore: '<i class="material-icons">code</i>',
    to: {
      name: 'most-vulnerable',
    },
  }, {
    title: 'Servers',
    htmlBefore: '<i class="material-icons">vertical_split</i>',
    to: {
      name: 'servers',
    },
  }, {
    title: 'Hosts',
    htmlBefore: '<i class="material-icons">desktop_windows</i>',
    to: {
      name: 'hosts',
    },
  }, {
    title: 'Add pack',
    htmlBefore: '<i class="material-icons">view_module</i>',
    to: {
      name: 'add-pack',
    },
  },{
    title: 'Admin Panel',
    htmlBefore: '<i class="material-icons">admin_panel_settings</i>',
    to: {
      name: 'admin',
    },
  }];
}
