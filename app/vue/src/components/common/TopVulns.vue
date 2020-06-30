<template>
  <d-card class="card-small">

    <!-- Card Header -->
    <d-card-header class="border-bottom">
      <h6 class="m-0">{{ title }}</h6>
      <div class="block-handle"></div>
    </d-card-header>

    <d-card-body class="p-0">

      <!-- Top Referrals List Group -->
      <d-list-group flush class="list-group-small">
        <d-list-group-item v-for="(item, idx) in referralData" :key="idx" class="d-flex px-3">
          <span class="text-semibold text-fiord-blue">{{ item.title }}</span>
          <span class="ml-auto text-right text-semibold text-reagent-gray">{{ item.value }}</span>
        </d-list-group-item>
      </d-list-group>

    </d-card-body>

    <d-card-footer class="border-top">
      <d-row>

        <!-- Time Frame -->
        <d-col>
          <d-select size="sm" value="last-week" style="max-width: 130px;">
            <option value="last-week">Last Week</option>
            <option value="today">Today</option>
            <option value="last-month">Last Month</option>
            <option value="last-year">Last Year</option>
          </d-select>
        </d-col>

        <!-- View Full Report -->
        <d-col class="text-right view-report">
          <a href="#">View full report &rarr;</a>
        </d-col>

      </d-row>
    </d-card-footer>

  </d-card>
</template>

<script>
const defaultTopReferrals = [{
  title: 'apache2',
  value: '291',
}, {
  title: 'open-ssl',
  value: '201',
}, {
  title: 'photoshop',
  value: '100',
}, {
  title: 'redis',
  value: '89',
}, {
  title: 'mysqld',
  value: '28',
}, {
  title: 'nginx',
  value: '18',
}, {
  title: 'spotify',
  value: '3',
}, {
  title: 'chrome',
  value: '1',
},
];

export default {
  name: 'ao-top-referrals',
  props: {
    /**
       * The component's title.
       */
    title: {
      type: String,
      default: 'Top Vulnerable Packages',
    },
    /**
       * The referral datasets.
       */
    referralData: {
      type: Array,
      default() {
        return defaultTopReferrals;
      },
    },
  },
};
</script>
