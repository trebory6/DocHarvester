Metrics
This page describes how to set up metrics for Vikunja using Grafana and Prometheus.
Enable the prometheus exporter in Vikunja#
To be able to scrape the metrics, you need to enable the prometheus exporter in Vikunja. Check out the docs about the options you have for this.
Scraping Vikunja’s Metrics using Prometheus#
Here is a sample Prometheus configuration to scrape the metrics:
scrape\_configs:
- job\_name: 'vikunja'
scrape\_interval: 5s
metrics\_path: '/api/v1/metrics'
static\_configs:
- targets:
- your-vikunja-host-url:3456
Setting up Grafana#
In Grafana, import this dashboard using the dashboard ID 21928
.
